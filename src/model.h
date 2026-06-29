


    // !!! This file is generated using emlearn !!!

    #include <stdint.h>
    

static inline int32_t model_tree_0(const int16_t *features, int32_t features_length) {
          if (features[2] < 0) {
              if (features[0] < 0) {
                  if (features[4] < 0) {
                      if (features[1] < 1) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          return 2;
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          if (features[1] < 1) {
                              return 1;
                          } else {
                              return 2;
                          }
                      }
                  }
              } else {
                  if (features[0] < 1) {
                      if (features[4] < 0) {
                          if (features[1] < 0) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      }
                  } else {
                      return 3;
                  }
              }
          } else {
              if (features[4] < 0) {
                  if (features[5] < 1) {
                      if (features[5] < 0) {
                          if (features[5] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      }
                  } else {
                      if (features[0] < 1) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 2;
                          }
                      } else {
                          return 3;
                      }
                  }
              } else {
                  if (features[1] < 0) {
                      if (features[0] < 1) {
                          if (features[5] < 1) {
                              return 1;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 2;
                          }
                      }
                  } else {
                      if (features[5] < 1) {
                          return 1;
                      } else {
                          if (features[0] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  }
              }
          }
        }
        

static inline int32_t model_tree_1(const int16_t *features, int32_t features_length) {
          if (features[5] < 1) {
              if (features[2] < 0) {
                  if (features[0] < 0) {
                      if (features[0] < 0) {
                          if (features[4] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          return 2;
                      }
                  }
              } else {
                  if (features[1] < 0) {
                      if (features[0] < 0) {
                          if (features[4] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[5] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      }
                  } else {
                      return 1;
                  }
              }
          } else {
              if (features[0] < 1) {
                  if (features[4] < 0) {
                      if (features[1] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      if (features[0] < 0) {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  }
              } else {
                  return 3;
              }
          }
        }
        

static inline int32_t model_tree_2(const int16_t *features, int32_t features_length) {
          if (features[4] < 0) {
              if (features[5] < 0) {
                  if (features[1] < 1) {
                      if (features[0] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      return 2;
                  }
              } else {
                  if (features[5] < 1) {
                      if (features[0] < 0) {
                          if (features[5] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 2;
                          }
                      } else {
                          return 1;
                      }
                  }
              }
          } else {
              if (features[0] < 0) {
                  if (features[1] < 1) {
                      if (features[0] < 0) {
                          if (features[2] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      return 2;
                  }
              } else {
                  if (features[5] < 0) {
                      if (features[1] < 0) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      } else {
                          return 2;
                      }
                  } else {
                      if (features[1] < -1) {
                          if (features[1] < -1) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      }
                  }
              }
          }
        }
        

static inline int32_t model_tree_3(const int16_t *features, int32_t features_length) {
          if (features[5] < 1) {
              if (features[0] < 0) {
                  if (features[2] < 0) {
                      if (features[4] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      }
                  } else {
                      if (features[4] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          return 1;
                      }
                  }
              } else {
                  if (features[4] < 0) {
                      if (features[0] < 1) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 3;
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          return 2;
                      }
                  }
              }
          } else {
              if (features[4] < 0) {
                  if (features[0] < 0) {
                      if (features[1] < 0) {
                          if (features[0] < -1) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 2;
                          } else {
                              return 2;
                          }
                      }
                  }
              } else {
                  if (features[1] < -1) {
                      if (features[0] < 0) {
                          if (features[0] < 0) {
                              return 2;
                          } else {
                              return 3;
                          }
                      } else {
                          return 2;
                      }
                  } else {
                      if (features[0] < 1) {
                          if (features[0] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          return 3;
                      }
                  }
              }
          }
        }
        

static inline int32_t model_tree_4(const int16_t *features, int32_t features_length) {
          if (features[0] < 0) {
              if (features[4] < 0) {
                  if (features[0] < 0) {
                      if (features[1] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          if (features[2] < 0) {
                              return 2;
                          } else {
                              return 1;
                          }
                      }
                  } else {
                      return 1;
                  }
              } else {
                  if (features[0] < 0) {
                      if (features[0] < 0) {
                          if (features[0] < 0) {
                              return 3;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[1] < 1) {
                              return 0;
                          } else {
                              return 2;
                          }
                      }
                  } else {
                      return 1;
                  }
              }
          } else {
              if (features[1] < 0) {
                  if (features[5] < 0) {
                      if (features[0] < 1) {
                          if (features[4] < 0) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 3;
                      }
                  } else {
                      if (features[0] < 1) {
                          if (features[4] < 0) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 3;
                      }
                  }
              } else {
                  if (features[0] < 2) {
                      return 2;
                  } else {
                      return 3;
                  }
              }
          }
        }
        

static inline int32_t model_tree_5(const int16_t *features, int32_t features_length) {
          if (features[1] < 1) {
              if (features[5] < 1) {
                  if (features[1] < 0) {
                      if (features[0] < 0) {
                          if (features[4] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[1] < -1) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      return 1;
                  }
              } else {
                  if (features[0] < 1) {
                      if (features[0] < 0) {
                          if (features[0] < 0) {
                              return 3;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 2;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      return 3;
                  }
              }
          } else {
              return 2;
          }
        }
        

static inline int32_t model_tree_6(const int16_t *features, int32_t features_length) {
          if (features[4] < 0) {
              if (features[1] < 1) {
                  if (features[0] < 0) {
                      if (features[5] < 1) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[1] < -1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[0] < 1) {
                              return 1;
                          } else {
                              return 3;
                          }
                      }
                  }
              } else {
                  return 2;
              }
          } else {
              if (features[0] < 0) {
                  if (features[2] < 0) {
                      if (features[0] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      if (features[5] < 1) {
                          return 1;
                      } else {
                          if (features[1] < -1) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  }
              } else {
                  if (features[0] < 1) {
                      if (features[5] < 0) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      }
                  } else {
                      return 3;
                  }
              }
          }
        }
        

static inline int32_t model_tree_7(const int16_t *features, int32_t features_length) {
          if (features[0] < 0) {
              if (features[4] < 0) {
                  if (features[1] < 0) {
                      if (features[0] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      if (features[2] < 0) {
                          if (features[1] < 1) {
                              return 1;
                          } else {
                              return 2;
                          }
                      } else {
                          return 1;
                      }
                  }
              } else {
                  if (features[1] < 1) {
                      if (features[5] < 1) {
                          if (features[0] < 0) {
                              return 1;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[0] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      return 2;
                  }
              }
          } else {
              if (features[0] < 1) {
                  if (features[1] < 0) {
                      if (features[2] < 0) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      }
                  } else {
                      if (features[5] < 0) {
                          if (features[4] < 0) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 2;
                      }
                  }
              } else {
                  return 3;
              }
          }
        }
        

static inline int32_t model_tree_8(const int16_t *features, int32_t features_length) {
          if (features[4] < 0) {
              if (features[1] < 1) {
                  if (features[5] < 0) {
                      if (features[1] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 3;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      if (features[5] < 1) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[0] < 1) {
                              return 0;
                          } else {
                              return 3;
                          }
                      }
                  }
              } else {
                  return 2;
              }
          } else {
              if (features[0] < 0) {
                  if (features[5] < 1) {
                      if (features[2] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      if (features[0] < 0) {
                          if (features[0] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[0] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  }
              } else {
                  if (features[2] < 0) {
                      if (features[1] < 0) {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          return 2;
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 2;
                          } else {
                              return 3;
                          }
                      }
                  }
              }
          }
        }
        

static inline int32_t model_tree_9(const int16_t *features, int32_t features_length) {
          if (features[5] < 1) {
              if (features[5] < 0) {
                  if (features[1] < 1) {
                      if (features[0] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      return 2;
                  }
              } else {
                  if (features[4] < 0) {
                      if (features[0] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      return 1;
                  }
              }
          } else {
              if (features[0] < 1) {
                  if (features[4] < 0) {
                      if (features[0] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          return 2;
                      }
                  } else {
                      if (features[0] < 0) {
                          if (features[1] < -1) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 2;
                          } else {
                              return 3;
                          }
                      }
                  }
              } else {
                  return 3;
              }
          }
        }
        

static inline int32_t model_tree_10(const int16_t *features, int32_t features_length) {
          if (features[0] < 0) {
              if (features[0] < 0) {
                  if (features[1] < 1) {
                      if (features[5] < 1) {
                          if (features[5] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      return 2;
                  }
              } else {
                  return 1;
              }
          } else {
              if (features[5] < 0) {
                  if (features[0] < 1) {
                      if (features[1] < 0) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 2;
                      }
                  } else {
                      return 3;
                  }
              } else {
                  if (features[1] < 0) {
                      if (features[1] < 0) {
                          if (features[4] < 0) {
                              return 2;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[4] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 2;
                          }
                      }
                  }
              }
          }
        }
        

static inline int32_t model_tree_11(const int16_t *features, int32_t features_length) {
          if (features[1] < 1) {
              if (features[0] < 0) {
                  if (features[1] < 0) {
                      if (features[4] < 0) {
                          if (features[5] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          if (features[2] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      }
                  } else {
                      return 1;
                  }
              } else {
                  if (features[1] < 0) {
                      if (features[4] < 0) {
                          if (features[1] < -1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[5] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      if (features[0] < 1) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 3;
                      }
                  }
              }
          } else {
              return 2;
          }
        }
        

static inline int32_t model_tree_12(const int16_t *features, int32_t features_length) {
          if (features[0] < 0) {
              if (features[0] < 0) {
                  if (features[2] < 0) {
                      if (features[4] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 2;
                          }
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[4] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[4] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      }
                  }
              } else {
                  return 1;
              }
          } else {
              if (features[2] < 0) {
                  if (features[0] < 1) {
                      if (features[1] < 1) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 2;
                      }
                  } else {
                      return 3;
                  }
              } else {
                  if (features[0] < 1) {
                      if (features[1] < 0) {
                          if (features[4] < 0) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      }
                  } else {
                      return 3;
                  }
              }
          }
        }
        

static inline int32_t model_tree_13(const int16_t *features, int32_t features_length) {
          if (features[1] < 1) {
              if (features[0] < 0) {
                  if (features[0] < 0) {
                      if (features[2] < 0) {
                          if (features[4] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          if (features[5] < 1) {
                              return 1;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      return 1;
                  }
              } else {
                  if (features[2] < 0) {
                      if (features[1] < 0) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[4] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      if (features[0] < 1) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 3;
                      }
                  }
              }
          } else {
              return 2;
          }
        }
        

static inline int32_t model_tree_14(const int16_t *features, int32_t features_length) {
          if (features[1] < 1) {
              if (features[5] < 1) {
                  if (features[5] < 0) {
                      if (features[4] < 0) {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 1;
                          }
                      }
                  } else {
                      if (features[5] < 0) {
                          if (features[5] < 0) {
                              return 1;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[4] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      }
                  }
              } else {
                  if (features[0] < 1) {
                      if (features[4] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[0] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      return 3;
                  }
              }
          } else {
              return 2;
          }
        }
        

static inline int32_t model_tree_15(const int16_t *features, int32_t features_length) {
          if (features[0] < 0) {
              if (features[2] < 0) {
                  if (features[1] < 0) {
                      if (features[4] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      }
                  } else {
                      if (features[4] < 0) {
                          if (features[0] < 0) {
                              return 2;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[1] < 1) {
                              return 1;
                          } else {
                              return 2;
                          }
                      }
                  }
              } else {
                  if (features[1] < 0) {
                      if (features[1] < 0) {
                          if (features[0] < 0) {
                              return 1;
                          } else {
                              return 0;
                          }
                      } else {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      }
                  } else {
                      return 1;
                  }
              }
          } else {
              if (features[1] < 1) {
                  if (features[1] < -1) {
                      if (features[0] < 1) {
                          if (features[5] < 0) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 3;
                      }
                  } else {
                      if (features[2] < 0) {
                          if (features[4] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[4] < 0) {
                              return 2;
                          } else {
                              return 3;
                          }
                      }
                  }
              } else {
                  return 2;
              }
          }
        }
        

static inline int32_t model_tree_16(const int16_t *features, int32_t features_length) {
          if (features[4] < 0) {
              if (features[5] < 0) {
                  if (features[1] < 1) {
                      if (features[1] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 3;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      return 2;
                  }
              } else {
                  if (features[5] < 1) {
                      if (features[0] < 0) {
                          if (features[5] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 2;
                          }
                      } else {
                          return 1;
                      }
                  }
              }
          } else {
              if (features[0] < 0) {
                  if (features[1] < 1) {
                      if (features[0] < 0) {
                          if (features[2] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      return 2;
                  }
              } else {
                  if (features[5] < 0) {
                      if (features[0] < 1) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 3;
                      }
                  } else {
                      if (features[1] < -1) {
                          return 3;
                      } else {
                          if (features[1] < -1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      }
                  }
              }
          }
        }
        

static inline int32_t model_tree_17(const int16_t *features, int32_t features_length) {
          if (features[0] < 0) {
              if (features[0] < 0) {
                  if (features[4] < 0) {
                      if (features[1] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          if (features[0] < 0) {
                              return 2;
                          } else {
                              return 1;
                          }
                      }
                  } else {
                      if (features[2] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 2;
                          }
                      } else {
                          if (features[0] < 0) {
                              return 1;
                          } else {
                              return 1;
                          }
                      }
                  }
              } else {
                  return 1;
              }
          } else {
              if (features[0] < 1) {
                  if (features[0] < 1) {
                      if (features[2] < 0) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      }
                  } else {
                      if (features[5] < 0) {
                          if (features[1] < 0) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      }
                  }
              } else {
                  return 3;
              }
          }
        }
        

static inline int32_t model_tree_18(const int16_t *features, int32_t features_length) {
          if (features[4] < 0) {
              if (features[2] < 0) {
                  if (features[0] < 0) {
                      if (features[1] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          if (features[1] < 1) {
                              return 1;
                          } else {
                              return 2;
                          }
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[0] < 2) {
                              return 2;
                          } else {
                              return 3;
                          }
                      }
                  }
              } else {
                  if (features[1] < 0) {
                      if (features[1] < 0) {
                          if (features[5] < 1) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          if (features[5] < 1) {
                              return 0;
                          } else {
                              return 0;
                          }
                      }
                  } else {
                      return 1;
                  }
              }
          } else {
              if (features[5] < 1) {
                  if (features[2] < 0) {
                      if (features[1] < 1) {
                          if (features[0] < 0) {
                              return 1;
                          } else {
                              return 3;
                          }
                      } else {
                          return 2;
                      }
                  } else {
                      return 1;
                  }
              } else {
                  if (features[1] < 0) {
                      if (features[0] < 1) {
                          if (features[1] < -1) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          return 3;
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[0] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 2;
                          } else {
                              return 3;
                          }
                      }
                  }
              }
          }
        }
        

static inline int32_t model_tree_19(const int16_t *features, int32_t features_length) {
          if (features[0] < 0) {
              if (features[0] < 0) {
                  if (features[5] < 1) {
                      if (features[2] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 2;
                          }
                      } else {
                          if (features[5] < 0) {
                              return 1;
                          } else {
                              return 1;
                          }
                      }
                  } else {
                      if (features[0] < 0) {
                          if (features[0] < -1) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 2;
                          }
                      }
                  }
              } else {
                  return 1;
              }
          } else {
              if (features[1] < 1) {
                  if (features[0] < 1) {
                      if (features[1] < 0) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      }
                  } else {
                      return 3;
                  }
              } else {
                  return 2;
              }
          }
        }
        

static inline int32_t model_tree_20(const int16_t *features, int32_t features_length) {
          if (features[1] < 1) {
              if (features[1] < 0) {
                  if (features[4] < 0) {
                      if (features[5] < 0) {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 0;
                          }
                      } else {
                          if (features[5] < 1) {
                              return 0;
                          } else {
                              return 0;
                          }
                      }
                  } else {
                      if (features[5] < 1) {
                          if (features[0] < 0) {
                              return 1;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[1] < -1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      }
                  }
              } else {
                  return 1;
              }
          } else {
              return 2;
          }
        }
        

static inline int32_t model_tree_21(const int16_t *features, int32_t features_length) {
          if (features[4] < 0) {
              if (features[1] < 1) {
                  if (features[0] < 0) {
                      if (features[5] < 1) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[0] < -1) {
                              return 0;
                          } else {
                              return 0;
                          }
                      }
                  } else {
                      if (features[0] < 0) {
                          return 1;
                      } else {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      }
                  }
              } else {
                  return 2;
              }
          } else {
              if (features[1] < 1) {
                  if (features[0] < 0) {
                      if (features[5] < 1) {
                          if (features[2] < 0) {
                              return 1;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      if (features[2] < 0) {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 2;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  }
              } else {
                  return 2;
              }
          }
        }
        

static inline int32_t model_tree_22(const int16_t *features, int32_t features_length) {
          if (features[0] < 0) {
              if (features[5] < 1) {
                  if (features[5] < 0) {
                      if (features[4] < 0) {
                          if (features[1] < 1) {
                              return 1;
                          } else {
                              return 2;
                          }
                      } else {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      }
                  } else {
                      if (features[0] < 0) {
                          if (features[4] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          return 1;
                      }
                  }
              } else {
                  if (features[0] < 0) {
                      if (features[1] < 0) {
                          if (features[0] < 0) {
                              return 3;
                          } else {
                              return 2;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      return 1;
                  }
              }
          } else {
              if (features[0] < 1) {
                  if (features[2] < 0) {
                      if (features[0] < 1) {
                          if (features[4] < 0) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          if (features[4] < 0) {
                              return 2;
                          } else {
                              return 2;
                          }
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[4] < 0) {
                              return 2;
                          } else {
                              return 3;
                          }
                      } else {
                          return 3;
                      }
                  }
              } else {
                  return 3;
              }
          }
        }
        

static inline int32_t model_tree_23(const int16_t *features, int32_t features_length) {
          if (features[1] < 1) {
              if (features[1] < 0) {
                  if (features[2] < 0) {
                      if (features[1] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      }
                  } else {
                      if (features[4] < 0) {
                          if (features[5] < 1) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          if (features[0] < 0) {
                              return 1;
                          } else {
                              return 3;
                          }
                      }
                  }
              } else {
                  return 1;
              }
          } else {
              return 2;
          }
        }
        

static inline int32_t model_tree_24(const int16_t *features, int32_t features_length) {
          if (features[1] < 1) {
              if (features[5] < 1) {
                  if (features[1] < 0) {
                      if (features[0] < 0) {
                          if (features[5] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[4] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      return 1;
                  }
              } else {
                  if (features[4] < 0) {
                      if (features[1] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 2;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      if (features[0] < 1) {
                          if (features[0] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          return 3;
                      }
                  }
              }
          } else {
              return 2;
          }
        }
        

static inline int32_t model_tree_25(const int16_t *features, int32_t features_length) {
          if (features[0] < 0) {
              if (features[1] < 1) {
                  if (features[1] < 0) {
                      if (features[5] < 1) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[4] < 0) {
                              return 0;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      return 1;
                  }
              } else {
                  return 2;
              }
          } else {
              if (features[1] < 1) {
                  if (features[2] < 0) {
                      if (features[0] < 1) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 3;
                      }
                  } else {
                      if (features[0] < 1) {
                          if (features[4] < 0) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 3;
                      }
                  }
              } else {
                  return 2;
              }
          }
        }
        

static inline int32_t model_tree_26(const int16_t *features, int32_t features_length) {
          if (features[5] < 1) {
              if (features[1] < 1) {
                  if (features[1] < 0) {
                      if (features[4] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 1;
                          } else {
                              return 0;
                          }
                      }
                  } else {
                      return 1;
                  }
              } else {
                  return 2;
              }
          } else {
              if (features[0] < 1) {
                  if (features[4] < 0) {
                      if (features[0] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          return 2;
                      }
                  } else {
                      if (features[0] < 0) {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  }
              } else {
                  return 3;
              }
          }
        }
        

static inline int32_t model_tree_27(const int16_t *features, int32_t features_length) {
          if (features[4] < 0) {
              if (features[0] < 0) {
                  if (features[2] < 0) {
                      if (features[0] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 2;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          return 1;
                      }
                  }
              } else {
                  if (features[0] < 1) {
                      if (features[1] < 0) {
                          if (features[2] < 0) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 2;
                      }
                  } else {
                      return 3;
                  }
              }
          } else {
              if (features[5] < 1) {
                  if (features[2] < 0) {
                      if (features[0] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      return 1;
                  }
              } else {
                  if (features[1] < -1) {
                      if (features[1] < -1) {
                          if (features[0] < 0) {
                              return 3;
                          } else {
                              return 2;
                          }
                      } else {
                          if (features[1] < -1) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      if (features[1] < -1) {
                          if (features[0] < -1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[0] < 1) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  }
              }
          }
        }
        

static inline int32_t model_tree_28(const int16_t *features, int32_t features_length) {
          if (features[1] < 1) {
              if (features[1] < 0) {
                  if (features[5] < 1) {
                      if (features[0] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      if (features[0] < 1) {
                          if (features[4] < 0) {
                              return 0;
                          } else {
                              return 3;
                          }
                      } else {
                          return 3;
                      }
                  }
              } else {
                  return 1;
              }
          } else {
              return 2;
          }
        }
        

static inline int32_t model_tree_29(const int16_t *features, int32_t features_length) {
          if (features[4] < 0) {
              if (features[1] < 1) {
                  if (features[5] < 0) {
                      if (features[0] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          return 1;
                      }
                  }
              } else {
                  return 2;
              }
          } else {
              if (features[1] < 1) {
                  if (features[5] < 1) {
                      if (features[1] < 0) {
                          if (features[5] < 0) {
                              return 3;
                          } else {
                              return 1;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[0] < 1) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          return 3;
                      }
                  }
              } else {
                  return 2;
              }
          }
        }
        

static inline int32_t model_tree_30(const int16_t *features, int32_t features_length) {
          if (features[4] < 0) {
              if (features[2] < 0) {
                  if (features[1] < 1) {
                      if (features[1] < 0) {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 0;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      return 2;
                  }
              } else {
                  if (features[5] < 1) {
                      if (features[0] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      if (features[0] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      }
                  }
              }
          } else {
              if (features[5] < 1) {
                  if (features[0] < 0) {
                      if (features[2] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      if (features[0] < 1) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 3;
                      }
                  }
              } else {
                  if (features[1] < 0) {
                      if (features[1] < 0) {
                          if (features[1] < -1) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 2;
                          } else {
                              return 2;
                          }
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  }
              }
          }
        }
        

static inline int32_t model_tree_31(const int16_t *features, int32_t features_length) {
          if (features[5] < 1) {
              if (features[1] < 1) {
                  if (features[4] < 0) {
                      if (features[1] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 3;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[5] < 0) {
                              return 3;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[0] < -1) {
                              return 1;
                          } else {
                              return 1;
                          }
                      }
                  }
              } else {
                  return 2;
              }
          } else {
              if (features[0] < 1) {
                  if (features[4] < 0) {
                      if (features[0] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          return 2;
                      }
                  } else {
                      if (features[0] < 0) {
                          if (features[1] < -1) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[0] < 0) {
                              return 2;
                          } else {
                              return 3;
                          }
                      }
                  }
              } else {
                  return 3;
              }
          }
        }
        

static inline int32_t model_tree_32(const int16_t *features, int32_t features_length) {
          if (features[2] < 0) {
              if (features[0] < 0) {
                  if (features[0] < 0) {
                      if (features[4] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 2;
                          }
                      } else {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      }
                  } else {
                      return 1;
                  }
              } else {
                  if (features[4] < 0) {
                      if (features[1] < 1) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      } else {
                          return 2;
                      }
                  } else {
                      if (features[1] < 1) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      } else {
                          return 2;
                      }
                  }
              }
          } else {
              if (features[0] < 0) {
                  if (features[4] < 0) {
                      if (features[5] < 1) {
                          if (features[5] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      }
                  } else {
                      if (features[0] < 0) {
                          if (features[0] < 0) {
                              return 1;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 1;
                          }
                      }
                  }
              } else {
                  if (features[0] < 1) {
                      if (features[1] < -1) {
                          return 3;
                      } else {
                          if (features[4] < 0) {
                              return 2;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      return 3;
                  }
              }
          }
        }
        

static inline int32_t model_tree_33(const int16_t *features, int32_t features_length) {
          if (features[1] < 1) {
              if (features[4] < 0) {
                  if (features[0] < 0) {
                      if (features[2] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[5] < 1) {
                              return 0;
                          } else {
                              return 0;
                          }
                      }
                  } else {
                      if (features[0] < 0) {
                          return 1;
                      } else {
                          if (features[1] < -1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      }
                  }
              } else {
                  if (features[1] < 0) {
                      if (features[0] < 0) {
                          if (features[5] < 1) {
                              return 1;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[2] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      return 1;
                  }
              }
          } else {
              return 2;
          }
        }
        

static inline int32_t model_tree_34(const int16_t *features, int32_t features_length) {
          if (features[4] < 0) {
              if (features[1] < 1) {
                  if (features[1] < 0) {
                      if (features[2] < 0) {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 0;
                          }
                      } else {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 2;
                          }
                      }
                  } else {
                      return 1;
                  }
              } else {
                  return 2;
              }
          } else {
              if (features[0] < 0) {
                  if (features[5] < 1) {
                      if (features[5] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      if (features[0] < 0) {
                          if (features[0] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  }
              } else {
                  if (features[5] < 0) {
                      if (features[0] < 1) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 3;
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[0] < 1) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 2;
                          } else {
                              return 3;
                          }
                      }
                  }
              }
          }
        }
        

static inline int32_t model_tree_35(const int16_t *features, int32_t features_length) {
          if (features[2] < 0) {
              if (features[0] < 0) {
                  if (features[4] < 0) {
                      if (features[1] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          if (features[1] < 1) {
                              return 1;
                          } else {
                              return 2;
                          }
                      }
                  } else {
                      if (features[0] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 2;
                          }
                      } else {
                          return 1;
                      }
                  }
              } else {
                  if (features[4] < 0) {
                      if (features[0] < 1) {
                          if (features[1] < 0) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 3;
                      }
                  } else {
                      if (features[0] < 1) {
                          if (features[1] < 0) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 3;
                      }
                  }
              }
          } else {
              if (features[4] < 0) {
                  if (features[5] < 1) {
                      if (features[0] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[0] < 1) {
                              return 0;
                          } else {
                              return 3;
                          }
                      } else {
                          return 1;
                      }
                  }
              } else {
                  if (features[5] < 1) {
                      return 1;
                  } else {
                      if (features[1] < -1) {
                          if (features[0] < -1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  }
              }
          }
        }
        

static inline int32_t model_tree_36(const int16_t *features, int32_t features_length) {
          if (features[1] < 1) {
              if (features[5] < 1) {
                  if (features[2] < 0) {
                      if (features[1] < 0) {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 0;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      if (features[5] < 0) {
                          if (features[4] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 1;
                          } else {
                              return 1;
                          }
                      }
                  }
              } else {
                  if (features[4] < 0) {
                      if (features[1] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 2;
                          }
                      } else {
                          return 1;
                      }
                  } else {
                      if (features[0] < 1) {
                          if (features[0] < 0) {
                              return 3;
                          } else {
                              return 2;
                          }
                      } else {
                          return 3;
                      }
                  }
              }
          } else {
              return 2;
          }
        }
        

static inline int32_t model_tree_37(const int16_t *features, int32_t features_length) {
          if (features[1] < 1) {
              if (features[1] < 0) {
                  if (features[0] < 0) {
                      if (features[4] < 0) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[2] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      }
                  } else {
                      if (features[0] < 1) {
                          if (features[5] < 0) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 3;
                      }
                  }
              } else {
                  return 1;
              }
          } else {
              return 2;
          }
        }
        

static inline int32_t model_tree_38(const int16_t *features, int32_t features_length) {
          if (features[4] < 0) {
              if (features[0] < 0) {
                  if (features[5] < 0) {
                      if (features[1] < 1) {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          return 2;
                      }
                  } else {
                      if (features[5] < 1) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          if (features[5] < 1) {
                              return 0;
                          } else {
                              return 0;
                          }
                      }
                  }
              } else {
                  if (features[1] < 0) {
                      if (features[0] < 1) {
                          if (features[5] < 0) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 3;
                      }
                  } else {
                      return 2;
                  }
              }
          } else {
              if (features[0] < 0) {
                  if (features[5] < 1) {
                      if (features[1] < 1) {
                          if (features[2] < 0) {
                              return 1;
                          } else {
                              return 1;
                          }
                      } else {
                          return 2;
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[0] < 0) {
                              return 3;
                          } else {
                              return 2;
                          }
                      } else {
                          return 3;
                      }
                  }
              } else {
                  if (features[1] < 0) {
                      if (features[5] < 0) {
                          if (features[0] < 1) {
                              return 2;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      }
                  } else {
                      return 2;
                  }
              }
          }
        }
        

static inline int32_t model_tree_39(const int16_t *features, int32_t features_length) {
          if (features[4] < 0) {
              if (features[0] < 0) {
                  if (features[1] < 0) {
                      if (features[2] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          if (features[0] < 0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      }
                  } else {
                      if (features[1] < 1) {
                          return 1;
                      } else {
                          return 2;
                      }
                  }
              } else {
                  if (features[0] < 1) {
                      if (features[1] < 0) {
                          if (features[2] < 0) {
                              return 2;
                          } else {
                              return 2;
                          }
                      } else {
                          return 2;
                      }
                  } else {
                      return 3;
                  }
              }
          } else {
              if (features[2] < 0) {
                  if (features[0] < 0) {
                      if (features[1] < 0) {
                          if (features[1] < 0) {
                              return 0;
                          } else {
                              return 0;
                          }
                      } else {
                          if (features[1] < 1) {
                              return 1;
                          } else {
                              return 2;
                          }
                      }
                  } else {
                      if (features[1] < 0) {
                          if (features[1] < 0) {
                              return 3;
                          } else {
                              return 3;
                          }
                      } else {
                          if (features[1] < 0) {
                              return 2;
                          } else {
                              return 2;
                          }
                      }
                  }
              } else {
                  if (features[5] < 1) {
                      return 1;
                  } else {
                      if (features[0] < 1) {
                          if (features[0] < 1) {
                              return 3;
                          } else {
                              return 2;
                          }
                      } else {
                          return 3;
                      }
                  }
              }
          }
        }
        

int32_t model_predict(const int16_t *features, int32_t features_length) {

        int32_t votes[4] = {0,};
        int32_t _class = -1;

        _class = model_tree_0(features, features_length); votes[_class] += 1;
    _class = model_tree_1(features, features_length); votes[_class] += 1;
    _class = model_tree_2(features, features_length); votes[_class] += 1;
    _class = model_tree_3(features, features_length); votes[_class] += 1;
    _class = model_tree_4(features, features_length); votes[_class] += 1;
    _class = model_tree_5(features, features_length); votes[_class] += 1;
    _class = model_tree_6(features, features_length); votes[_class] += 1;
    _class = model_tree_7(features, features_length); votes[_class] += 1;
    _class = model_tree_8(features, features_length); votes[_class] += 1;
    _class = model_tree_9(features, features_length); votes[_class] += 1;
    _class = model_tree_10(features, features_length); votes[_class] += 1;
    _class = model_tree_11(features, features_length); votes[_class] += 1;
    _class = model_tree_12(features, features_length); votes[_class] += 1;
    _class = model_tree_13(features, features_length); votes[_class] += 1;
    _class = model_tree_14(features, features_length); votes[_class] += 1;
    _class = model_tree_15(features, features_length); votes[_class] += 1;
    _class = model_tree_16(features, features_length); votes[_class] += 1;
    _class = model_tree_17(features, features_length); votes[_class] += 1;
    _class = model_tree_18(features, features_length); votes[_class] += 1;
    _class = model_tree_19(features, features_length); votes[_class] += 1;
    _class = model_tree_20(features, features_length); votes[_class] += 1;
    _class = model_tree_21(features, features_length); votes[_class] += 1;
    _class = model_tree_22(features, features_length); votes[_class] += 1;
    _class = model_tree_23(features, features_length); votes[_class] += 1;
    _class = model_tree_24(features, features_length); votes[_class] += 1;
    _class = model_tree_25(features, features_length); votes[_class] += 1;
    _class = model_tree_26(features, features_length); votes[_class] += 1;
    _class = model_tree_27(features, features_length); votes[_class] += 1;
    _class = model_tree_28(features, features_length); votes[_class] += 1;
    _class = model_tree_29(features, features_length); votes[_class] += 1;
    _class = model_tree_30(features, features_length); votes[_class] += 1;
    _class = model_tree_31(features, features_length); votes[_class] += 1;
    _class = model_tree_32(features, features_length); votes[_class] += 1;
    _class = model_tree_33(features, features_length); votes[_class] += 1;
    _class = model_tree_34(features, features_length); votes[_class] += 1;
    _class = model_tree_35(features, features_length); votes[_class] += 1;
    _class = model_tree_36(features, features_length); votes[_class] += 1;
    _class = model_tree_37(features, features_length); votes[_class] += 1;
    _class = model_tree_38(features, features_length); votes[_class] += 1;
    _class = model_tree_39(features, features_length); votes[_class] += 1;
    
        int32_t most_voted_class = -1;
        int32_t most_voted_votes = 0;
        for (int32_t i=0; i<4; i++) {

            if (votes[i] > most_voted_votes) {
                most_voted_class = i;
                most_voted_votes = votes[i];
            }
        }
        return most_voted_class;
    }
    

int model_predict_proba(const int16_t *features, int32_t features_length, float *out, int out_length) {

        int32_t _class = -1;

        for (int i=0; i<out_length; i++) {
            out[i] = 0.0f;
        }

        _class = model_tree_0(features, features_length); out[_class] += 1.0f;
    _class = model_tree_1(features, features_length); out[_class] += 1.0f;
    _class = model_tree_2(features, features_length); out[_class] += 1.0f;
    _class = model_tree_3(features, features_length); out[_class] += 1.0f;
    _class = model_tree_4(features, features_length); out[_class] += 1.0f;
    _class = model_tree_5(features, features_length); out[_class] += 1.0f;
    _class = model_tree_6(features, features_length); out[_class] += 1.0f;
    _class = model_tree_7(features, features_length); out[_class] += 1.0f;
    _class = model_tree_8(features, features_length); out[_class] += 1.0f;
    _class = model_tree_9(features, features_length); out[_class] += 1.0f;
    _class = model_tree_10(features, features_length); out[_class] += 1.0f;
    _class = model_tree_11(features, features_length); out[_class] += 1.0f;
    _class = model_tree_12(features, features_length); out[_class] += 1.0f;
    _class = model_tree_13(features, features_length); out[_class] += 1.0f;
    _class = model_tree_14(features, features_length); out[_class] += 1.0f;
    _class = model_tree_15(features, features_length); out[_class] += 1.0f;
    _class = model_tree_16(features, features_length); out[_class] += 1.0f;
    _class = model_tree_17(features, features_length); out[_class] += 1.0f;
    _class = model_tree_18(features, features_length); out[_class] += 1.0f;
    _class = model_tree_19(features, features_length); out[_class] += 1.0f;
    _class = model_tree_20(features, features_length); out[_class] += 1.0f;
    _class = model_tree_21(features, features_length); out[_class] += 1.0f;
    _class = model_tree_22(features, features_length); out[_class] += 1.0f;
    _class = model_tree_23(features, features_length); out[_class] += 1.0f;
    _class = model_tree_24(features, features_length); out[_class] += 1.0f;
    _class = model_tree_25(features, features_length); out[_class] += 1.0f;
    _class = model_tree_26(features, features_length); out[_class] += 1.0f;
    _class = model_tree_27(features, features_length); out[_class] += 1.0f;
    _class = model_tree_28(features, features_length); out[_class] += 1.0f;
    _class = model_tree_29(features, features_length); out[_class] += 1.0f;
    _class = model_tree_30(features, features_length); out[_class] += 1.0f;
    _class = model_tree_31(features, features_length); out[_class] += 1.0f;
    _class = model_tree_32(features, features_length); out[_class] += 1.0f;
    _class = model_tree_33(features, features_length); out[_class] += 1.0f;
    _class = model_tree_34(features, features_length); out[_class] += 1.0f;
    _class = model_tree_35(features, features_length); out[_class] += 1.0f;
    _class = model_tree_36(features, features_length); out[_class] += 1.0f;
    _class = model_tree_37(features, features_length); out[_class] += 1.0f;
    _class = model_tree_38(features, features_length); out[_class] += 1.0f;
    _class = model_tree_39(features, features_length); out[_class] += 1.0f;
    
        // compute mean
        for (int i=0; i<out_length; i++) {
            out[i] = out[i] / 40;
        }
        return 0;
    }
    