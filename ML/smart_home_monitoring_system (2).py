# =============================================================
# SRTA 3353 — Machine Learning for IoT | Project 2
# Student 4  : Data Processing and Intelligence Engineer
# System     : Smart Home Hazard Detection
# Pipeline   : Dataset Loading → Preprocessing → Train/Test Split
#              → SMOTE →  → 5-Fold CV
#              → Evaluation → Baseline → Save → Live Prediction
#              → Dashboard Output
#
# Dataset    : dataset/*_raw.csv  (8 class files + 2 real files)
# Features   : temperature, humidity, motion, gas,
#               is_night, motion_duration_sec
# Target     : alert_class  (0=Normal, 1=Low, 2=Medium, 3=High)
# =============================================================


# ==============================================================
# SECTION 0: IMPORTS & SETUP
# ==============================================================

import warnings
warnings.filterwarnings('ignore')

import os
import glob
import json
import joblib
from datetime import datetime
from collections import Counter
from tqdm import tqdm

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

from sklearn.model_selection import (
    train_test_split, StratifiedKFold, cross_validate
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, label_binarize
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    confusion_matrix, classification_report,
    accuracy_score, precision_score, recall_score, f1_score,
    ConfusionMatrixDisplay,
    roc_auc_score, roc_curve, auc
)

try:
    from imblearn.over_sampling import SMOTE
    from imblearn.pipeline import Pipeline as ImbPipeline
except ImportError:
    import subprocess, sys
    print("Installing imbalanced-learn...")
    subprocess.check_call([sys.executable, '-m', 'pip',
                           'install', '-q', 'imbalanced-learn'])
    from imblearn.over_sampling import SMOTE
    from imblearn.pipeline import Pipeline as ImbPipeline

sns.set_style('whitegrid')
plt.rcParams['figure.facecolor'] = 'white'

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# ── Global constants ────────────────────────────────────────────
FEATURES     = ['temperature', 'humidity', 'motion', 'gas',
                 'is_night', 'motion_duration_sec']
TARGET       = 'alert_class'
numeric_cols = ['temperature', 'humidity', 'gas', 'motion_duration_sec']
binary_cols  = ['motion', 'is_night']

# 4-class label map
CLASS_NAMES  = {
    0: 'Normal',
    1: 'Low Alert',
    2: 'Medium Alert',
    3: 'High Alert'
}
CLASS_COLORS = {
    0: '#2ecc71',   # green
    1: '#f1c40f',   # yellow
    2: '#e67e22',   # orange
    3: '#e74c3c',   # red
}

# Actuator output per class
ACTUATOR_MAP = {
    0: {'led': 'GREEN',  'buzzer': 'OFF'},
    1: {'led': 'YELLOW', 'buzzer': 'BEEP'},
    2: {'led': 'ORANGE', 'buzzer': 'RAPID_BEEP'},
    3: {'led': 'RED',    'buzzer': 'ALARM'},
}

print("Libraries imported successfully.")


# ==============================================================
# SECTION 1: DATASET LOADING
# Reads all *_raw.csv files from the dataset/ folder.
# RAW files are used because they contain the 'alert_class'
# target label. Processed files are label-free (features only)
# and are used only for live deployment — NOT for training.
# ==============================================================


def load_dataset():
    files = sorted(glob.glob("dataset/*_processed.csv"))


    # ── Step 1: Scan columns of every file before loading ──────
    # Tells you immediately which file is missing alert_class
    # instead of crashing mid-concat.
    print(f"Found {len(files)} file(s). Scanning columns...\n")

    valid_files   = []
    skipped_files = []

    for f in files:
        cols = pd.read_csv(f, nrows=0).columns.tolist()
        name = os.path.basename(f)
        if 'alert_class' in cols:
            valid_files.append(f)
            print(f"  PASS  {name:45s}  cols={len(cols)}")
        else:
            skipped_files.append(f)
            print(f"  SKIP  {name:45s}  "
                  f"no alert_class | found: {cols}")

    print(f"\nLoading {len(valid_files)} valid file(s), "
          f"skipping {len(skipped_files)}.\n")

    if not valid_files:
        raise RuntimeError(
            "None of the files in dataset/ contain an "
            "'alert_class' column.\n"
            "Make sure you are using the *_raw.csv files, "
            "not the *_processed.csv files."
        )

    # ── Step 2: Load valid files with progress bar ─────────────
    dfs        = []
    total_rows = 0

    with tqdm(total=len(valid_files),
              desc="Loading",
              unit="file",
              bar_format="{l_bar}{bar:30}{r_bar}") as pbar:

        for f in valid_files:
            filename = os.path.basename(f)
            pbar.set_postfix_str(filename, refresh=True)

            tmp        = pd.read_csv(f)
            total_rows += len(tmp)
            tmp["source_file"] = filename
            dfs.append(tmp)

            pbar.set_postfix_str(
                f"{filename}  ({len(tmp):,} rows, "
                f"cumulative: {total_rows:,})",
                refresh=True
            )
            pbar.update(1)

    df = pd.concat(dfs, ignore_index=True)
    print(f"\nDone.  Combined shape : "
          f"{df.shape[0]:,} rows x {df.shape[1]} columns")
    print(f"alert_class values    : "
          f"{sorted(df['alert_class'].unique())}")
    return df, "local_csv"


print("\n" + "=" * 60)
print("SECTION 1: DATASET LOADING")
print("=" * 60)
print("\nLoading RAW files only — they contain alert_class labels.")
print("(*_processed.csv files are excluded — no labels present)\n")

df_raw, data_source = load_dataset()

print(f"\nData source : {data_source}")
print(f"Shape       : {df_raw.shape}")
print(f"Columns     : {df_raw.columns.tolist()}")
print(f"\nalert_class distribution:")
print(df_raw[TARGET].value_counts().sort_index()
        .rename(index=CLASS_NAMES).to_string())
print(f"\nSample rows:")
print(df_raw.head().to_string())


# ==============================================================
# SECTION 2: FEATURE SELECTION
# Drop non-sensor columns (created_at, alarm, reason,
# source_file) and keep only the 6 hardware sensor features
# plus the target label alert_class.
# ==============================================================

print("\n" + "=" * 60)
print("SECTION 2: FEATURE SELECTION")
print("=" * 60)
print("""
Sensor / derived feature mapping:
  temperature         → DHT11/DHT22 (continuous °C)
  humidity            → DHT11/DHT22 (continuous %)
  motion              → PIR sensor HC-SR501 (binary 0/1)
  gas                 → MQ-series gas sensor (continuous ADC)
  is_night            → Derived from timestamp (binary 0/1)
  motion_duration_sec → Derived from PIR trigger (continuous sec)

Dropped columns (not available as live sensor inputs):
  created_at, alarm, reason, source_file
""")

df_selected = df_raw[FEATURES + [TARGET]].copy()

# Coerce types
df_selected['is_night'] = df_selected['is_night'].astype(int)
df_selected[TARGET]     = df_selected[TARGET].astype(int)

print(f"Selected shape : {df_selected.shape}")
print(df_selected.head().to_string())


# ==============================================================
# SECTION 3: DATA PREPROCESSING
# 3.1 Missing value handling (median / mode imputation)
# 3.2 Outlier capping (IQR method, continuous cols only)
# 3.3 Feature scaling (StandardScaler, continuous cols only)
# ==============================================================

print("\n" + "=" * 60)
print("SECTION 3: DATA PREPROCESSING")
print("=" * 60)

# ── 3.1 Missing Value Handling ─────────────────────────────────
print("\n[3.1] Missing Value Handling")
print("Missing values BEFORE imputation:")
print(df_selected.isnull().sum().to_string())

for col in numeric_cols:
    n_miss = df_selected[col].isnull().sum()
    if n_miss > 0:
        med = df_selected[col].median()
        df_selected[col].fillna(med, inplace=True)
        print(f"  Imputed {n_miss} in '{col}' with median = {med:.2f}")

for col in binary_cols:
    n_miss = df_selected[col].isnull().sum()
    if n_miss > 0:
        mod = df_selected[col].mode()[0]
        df_selected[col].fillna(mod, inplace=True)
        print(f"  Imputed {n_miss} in '{col}' with mode = {mod}")

print("\nMissing values AFTER imputation:")
print(df_selected.isnull().sum().to_string())

# ── 3.2 Outlier Capping (IQR) ──────────────────────────────────
print("\n[3.2] Outlier Capping (IQR, continuous features only)")
outlier_bounds = {}
for col in numeric_cols:
    Q1, Q3 = df_selected[col].quantile(0.25), df_selected[col].quantile(0.75)
    IQR    = Q3 - Q1
    lo, hi = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    outlier_bounds[col] = (lo, hi)
    n_cap = ((df_selected[col] < lo) | (df_selected[col] > hi)).sum()
    df_selected[col] = df_selected[col].clip(lower=lo, upper=hi)
    print(f"  {col:24s}: {n_cap:4d} capped to [{lo:.2f}, {hi:.2f}]")

# ── 3.3 Feature Scaling (StandardScaler) ───────────────────────
print("\n[3.3] Feature Scaling (StandardScaler, continuous cols only)")
print("      Binary cols (motion, is_night) left as 0/1 — no scaling needed.")
scaler = StandardScaler()
df_selected[numeric_cols] = scaler.fit_transform(df_selected[numeric_cols])
joblib.dump(scaler, 'scaler.pkl')
print("  Scaler fitted and saved to 'scaler.pkl'")
print("\n  Scaled feature statistics:")
print(df_selected[numeric_cols].describe().round(3).to_string())


# ==============================================================
# SECTION 4: TARGET VERIFICATION
# alert_class is already a clean 4-class integer (0,1,2,3) from
# the raw CSV files — no encoding step needed.
# Just verify values and display the class distribution.
# ==============================================================

print("\n" + "=" * 60)
print("SECTION 4: TARGET VERIFICATION")
print("=" * 60)

print(f"\nUnique values in '{TARGET}': {sorted(df_selected[TARGET].unique())}")
print(f"Expected               : [0, 1, 2, 3]\n")

# Use alert_class directly as label
df_selected['label'] = df_selected[TARGET]

print("Class distribution:")
dist = df_selected['label'].value_counts().sort_index()
for cls, count in dist.items():
    pct = count / len(df_selected) * 100
    print(f"  {cls} — {CLASS_NAMES[cls]:12s}: {count:6,}  ({pct:.1f}%)")


# ==============================================================
# SECTION 5: EXPLORATORY DATA ANALYSIS
# ==============================================================

print("\n" + "=" * 60)
print("SECTION 5: EXPLORATORY DATA ANALYSIS")
print("=" * 60)

print(f"\n[5.1] Shape  : {df_selected.shape}")
print(f"\n[5.2] Info:")
df_selected.info()

print(f"\n[5.3] Missing values:")
print(df_selected.isnull().sum().to_string())

print(f"\n[5.4] Feature statistics:")
print(df_selected[FEATURES].describe().round(3).to_string())

# ── Class distribution bar ─────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 4))
x_labels = [f"{k}\n{v}" for k, v in CLASS_NAMES.items()]
counts   = [dist.get(k, 0) for k in CLASS_NAMES]
bars     = ax.bar(x_labels, counts,
                  color=[CLASS_COLORS[k] for k in CLASS_NAMES],
                  edgecolor='black')
for bar, cnt in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 30, f'{cnt:,}',
            ha='center', fontsize=10, fontweight='bold')
ax.set_title('Class Distribution — alert_class (0–3)',
             fontweight='bold')
ax.set_ylabel('Count')
plt.tight_layout()
plt.savefig('class_distribution.png', dpi=150, bbox_inches='tight')
plt.show()
print("\n[5.5] Saved: class_distribution.png")

# ── Correlation heatmap ────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 6))
corr = df_selected[FEATURES + ['label']].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
            center=0, square=True, linewidths=0.5, ax=ax)
ax.set_title('Feature Correlation Heatmap', fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()
print("[5.6] Saved: correlation_heatmap.png")

# ── Histograms per class ───────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(15, 9))
for ax, feat in zip(axes.flatten(), FEATURES):
    for cls, name in CLASS_NAMES.items():
        subset = df_selected[df_selected['label'] == cls][feat]
        ax.hist(subset, bins=25, alpha=0.55,
                color=CLASS_COLORS[cls], label=name, edgecolor='none')
    ax.set_title(f'{feat}', fontweight='bold')
    ax.set_xlabel(feat)
    ax.set_ylabel('Frequency')
    ax.legend(fontsize=7)
plt.suptitle('Feature Distributions per Class', fontsize=13,
             fontweight='bold')
plt.tight_layout()
plt.savefig('histograms.png', dpi=150, bbox_inches='tight')
plt.show()
print("[5.7] Saved: histograms.png")

# ── Boxplots per class ─────────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(15, 9))
class_labels_str = df_selected['label'].map(
    {k: f"{k}\n{v}" for k, v in CLASS_NAMES.items()})
palette = [CLASS_COLORS[k] for k in sorted(CLASS_NAMES)]
for ax, feat in zip(axes.flatten(), FEATURES):
    sns.boxplot(x=class_labels_str, y=df_selected[feat],
                ax=ax, palette=palette,
                hue=class_labels_str, legend=False)
    ax.set_title(f'{feat} by Class', fontweight='bold')
    ax.set_xlabel('')
plt.suptitle('Feature Boxplots per Class', fontsize=13,
             fontweight='bold')
plt.tight_layout()
plt.savefig('boxplots.png', dpi=150, bbox_inches='tight')
plt.show()
print("[5.8] Saved: boxplots.png")


# ==============================================================
# SECTION 6: TRAIN-TEST SPLIT (80/20, stratified)
# ==============================================================

print("\n" + "=" * 60)
print("SECTION 6: TRAIN-TEST SPLIT  (80 / 20, stratified)")
print("=" * 60)

X = df_selected[FEATURES]
y = df_selected['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20,
    random_state=RANDOM_STATE, stratify=y
)

print(f"\nTraining samples : {X_train.shape[0]:,}  "
      f"({X_train.shape[1]} features)")
print(f"Testing samples  : {X_test.shape[0]:,}")
print(f"\nTraining class balance:")
for k, v in y_train.value_counts().sort_index().items():
    print(f"  Class {k} {CLASS_NAMES[k]:12s}: {v:,}")
print(f"\nTesting class balance:")
for k, v in y_test.value_counts().sort_index().items():
    print(f"  Class {k} {CLASS_NAMES[k]:12s}: {v:,}")


# ==============================================================
# SECTION 7: RANDOM FOREST — IMBALANCE-AWARE TRAINING
#
# SMOTE generates synthetic minority-class samples inside the
# training set ONLY. Combined with class_weight='balanced',
# this ensures the tree learns meaningful boundaries even when
# class counts differ.
# ImbPipeline wraps SMOTE + tree so CV applies SMOTE per fold
# (no synthetic-sample leakage between folds).
# ==============================================================

print("\n" + "=" * 60)
print("SECTION 7:  — IMBALANCE-AWARE TRAINING")
print("=" * 60)

print("\nClass distribution BEFORE SMOTE:")
print(Counter(y_train))

smote = SMOTE(random_state=RANDOM_STATE)
_, y_smote_preview = smote.fit_resample(X_train, y_train)
print("\nClass distribution AFTER SMOTE (training set only):")
print(Counter(y_smote_preview))
print("\n(Test set untouched — real distribution preserved.)")

imb_pipeline = ImbPipeline([
    ('smote', SMOTE(random_state=RANDOM_STATE)),
    ('rf',    RandomForestClassifier(
        n_estimators = 150,
        max_depth    = 10,
        class_weight = 'balanced',
        random_state = RANDOM_STATE
    ))
])

imb_pipeline.fit(X_train, y_train)
model = imb_pipeline.named_steps['rf']   # ← key name changed: 'tree' → 'rf'

print(f"Number of trees : {model.n_estimators}")
print(f"Max depth       : {model.max_depth}")

class_name_list = [CLASS_NAMES[i] for i in range(4)]

# Feature importances
importances = (pd.Series(model.feature_importances_, index=FEATURES)
                 .sort_values(ascending=False))
print("\nRanked feature importances:")
print(importances.round(4).to_string())
 
fig, ax = plt.subplots(figsize=(7, 4))
importances.sort_values().plot(
    kind='barh', color='#9b59b6', edgecolor='black', ax=ax)
ax.set_title('Feature Importance — Decision Tree', fontweight='bold')
ax.set_xlabel('Importance Score')
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved: feature_importance.png")
# ==============================================================
# SECTION 8: 5-FOLD CROSS VALIDATION
# Uses full imb_pipeline so SMOTE runs inside each fold.
# Macro-averaged metrics are reported alongside accuracy since
# macro averaging weighs each class equally regardless of size.
# ==============================================================

print("\n" + "=" * 60)
print("SECTION 8: 5-FOLD CROSS VALIDATION")
print("=" * 60)

skf = StratifiedKFold(n_splits=5, shuffle=True,
                      random_state=RANDOM_STATE)

cv_results = cross_validate(
    imb_pipeline, X_train, y_train, cv=skf,
    scoring={
        'accuracy' : 'accuracy',
        'precision': 'precision_macro',
        'recall'   : 'recall_macro',
        'f1'       : 'f1_macro'
    }
)

print()
for i in range(5):
    print(f"Fold {i+1} -> "
          f"Acc: {cv_results['test_accuracy'][i]:.4f} | "
          f"Prec(macro): {cv_results['test_precision'][i]:.4f} | "
          f"Rec(macro): {cv_results['test_recall'][i]:.4f} | "
          f"F1(macro): {cv_results['test_f1'][i]:.4f}")

print(f"\nMean Accuracy         : "
      f"{cv_results['test_accuracy'].mean():.4f} "
      f"± {cv_results['test_accuracy'].std():.4f}")
print(f"Mean Precision(macro) : "
      f"{cv_results['test_precision'].mean():.4f} "
      f"± {cv_results['test_precision'].std():.4f}")
print(f"Mean Recall(macro)    : "
      f"{cv_results['test_recall'].mean():.4f} "
      f"± {cv_results['test_recall'].std():.4f}")
print(f"Mean F1(macro)        : "
      f"{cv_results['test_f1'].mean():.4f} "
      f"± {cv_results['test_f1'].std():.4f}")


# ==============================================================
# SECTION 9: VALIDATION METRICS (TEST SET)
# Confusion matrix, full classification report (per-class),
# and One-vs-Rest ROC curves for all 4 classes.
# ==============================================================

print("\n" + "=" * 60)
print("SECTION 9: VALIDATION METRICS")
print("=" * 60)

y_pred  = model.predict(X_test)
y_proba = model.predict_proba(X_test)     # shape: (n, 4)

# ── Confusion Matrix ───────────────────────────────────────────
cm = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:")
print(cm)

fig, ax = plt.subplots(figsize=(6, 5))
ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=class_name_list
).plot(ax=ax, cmap='Blues', colorbar=False)
ax.set_title('Confusion Matrix (4-class)', fontweight='bold')
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved: confusion_matrix.png")

# ── Classification Report ──────────────────────────────────────
print("\nClassification Report (per-class):\n")
print(classification_report(
    y_test, y_pred,
    target_names=class_name_list,
    digits=4
))

dt_acc  = accuracy_score(y_test, y_pred)
dt_prec = precision_score(y_test, y_pred, average='macro')
dt_rec  = recall_score(y_test, y_pred, average='macro')
dt_f1   = f1_score(y_test, y_pred, average='macro')

print(f"Accuracy          : {dt_acc:.4f}")
print(f"Precision (macro) : {dt_prec:.4f}")
print(f"Recall    (macro) : {dt_rec:.4f}")
print(f"F1        (macro) : {dt_f1:.4f}")

# ── One-vs-Rest ROC Curves (one per class) ─────────────────────
# Binarize labels for OvR: each class vs all others
n_classes  = 4
classes    = list(range(n_classes))
y_test_bin = label_binarize(y_test, classes=classes)  # (n, 4)

roc_auc_ovr = roc_auc_score(
    y_test, y_proba, multi_class='ovr', average='macro'
)
print(f"\nROC-AUC (macro OvR) : {roc_auc_ovr:.4f}")

fig, ax = plt.subplots(figsize=(7, 6))
for i in classes:
    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_proba[:, i])
    roc_i = auc(fpr, tpr)
    ax.plot(fpr, tpr, linewidth=2,
            color=CLASS_COLORS[i],
            label=f"Class {i} {CLASS_NAMES[i]} (AUC={roc_i:.3f})")

ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random')
ax.set_xlabel('False Positive Rate')
ax.set_ylabel('True Positive Rate')
ax.set_title('ROC Curves — One-vs-Rest (4 classes)', fontweight='bold')
ax.legend(loc='lower right', fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('roc_curve.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved: roc_curve.png")


# ==============================================================
# SECTION 10: BASELINE MODEL (DummyClassifier)
# ==============================================================

print("\n" + "=" * 60)
print("SECTION 10: BASELINE MODEL (DummyClassifier)")
print("=" * 60)

baseline = DummyClassifier(strategy='most_frequent',
                            random_state=RANDOM_STATE)
baseline.fit(X_train, y_train)
y_pred_base = baseline.predict(X_test)

b_acc  = accuracy_score(y_test, y_pred_base)
b_prec = precision_score(y_test, y_pred_base,
                          average='macro', zero_division=0)
b_rec  = recall_score(y_test, y_pred_base,
                       average='macro', zero_division=0)
b_f1   = f1_score(y_test, y_pred_base,
                   average='macro', zero_division=0)

print(f"\nBaseline Accuracy         : {b_acc:.4f}")
print(f"Baseline Precision (macro): {b_prec:.4f}")
print(f"Baseline Recall    (macro): {b_rec:.4f}")
print(f"Baseline F1        (macro): {b_f1:.4f}")


# ==============================================================
# SECTION 11: RANDOM FOREST vs BASELINE COMPARISON
# ==============================================================

print("\n" + "=" * 60)
print("SECTION 11:  vs BASELINE COMPARISON")
print("=" * 60)

comparison_df = pd.DataFrame({
    'Metric'       : ['Accuracy', 'Precision\n(macro)',
                      'Recall\n(macro)', 'F1\n(macro)'],
    'Baseline'     : [b_acc,  b_prec,  b_rec,  b_f1 ],
    'Random Forest': [dt_acc, dt_prec, dt_rec, dt_f1],
})
comparison_df['Improvement'] = (
    comparison_df['Random Forest'] - comparison_df['Baseline']
)

print()
print(comparison_df.set_index('Metric').round(4).to_string())


# ==============================================================
# SECTION 12: MODEL SAVING
# decision_tree_model.pkl → Student 3 (firmware deployment)
# scaler.pkl              → Student 3 (live preprocessing)
# ==============================================================

print("=" * 60)
print("SECTION 12: MODEL SAVING")
print("=" * 60)

joblib.dump(model,  'random_forest_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
print("\nSaved: random_forest_model.pkl  → Student 3 (firmware)")
print("Saved: scaler.pkl               → Student 3 (live scaling)")


