from micromlgen import port
import joblib, os
m = joblib.load('ML/random_forest_model_40_trees.pkl')
open('src/model.h','w').write(port(m))
print(f'size: {os.path.getsize("src/model.h")/1024:.1f} KB')