# -*- coding: utf-8 -*-
"""heart_disease_deep_learning

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1x8nodMuAVi7l-BLJ-zs7pUYO2MjCx4co
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(context="talk")

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from tensorflow import nn, optimizers
from keras.models import Sequential
from keras.layers import Flatten, Dense, Dropout
from keras.callbacks import EarlyStopping

"""# Import Dataset"""

df = pd.read_csv("/content/heart.csv")

df.head()

"""# Preprocessing"""

minmax = MinMaxScaler()

df_num = pd.DataFrame(minmax.fit_transform(df[["age", "trestbps", "chol", "thalach", "oldpeak"]]))

df_num.columns = ["age", "trestbps", "chol", "thalac", "oldpeak"]

df_col = df.loc[:, ["sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal", "target"]]

df_new = pd.concat([df_num, df_col], axis="columns")

label = pd.get_dummies(df_new["target"])

df_new = pd.concat([df_new, label], axis="columns")
df_new.drop("target", axis="columns", inplace=True)

df_new = df_new.rename({0:"tidak_terkena", 1:"terkena"}, axis="columns")

"""# Datasets Splitting"""

X = df_new.loc[:, "age":"thal"]
y = df_new.loc[:, "tidak_terkena":"terkena"]

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42, test_size=0.2)
X_train.shape, X_test.shape, y_train.shape, y_test.shape

"""# Arsitektur Model"""

model = Sequential([
                    Dense(64, activation="relu", input_shape=(13,)),
                    Dense(256, activation="relu"),
                    Dropout(0.2),
                    Dense(128, activation="relu"),
                    Dense(2, activation="softmax")
])

"""# Model Compile"""

model.compile(optimizer=optimizers.Adam(learning_rate=0.0003), loss="categorical_crossentropy", metrics=["accuracy"])

"""# Training"""

es = EarlyStopping(monitor="val_accuracy", mode="max", patience=30, restore_best_weights=True)

hist = model.fit(X_train, y_train, batch_size=32, epochs=500, verbose=1, callbacks=[es], validation_data=(X_test, y_test))

model.evaluate(X_train, y_train, verbose=1)

model.evaluate(X_test, y_test, verbose=1)

plt.figure(figsize=(9, 5), constrained_layout=True)
plt.title("Grafik Akurasi dengan Deep Learning")
plt.plot(hist.history["val_accuracy"], color="r", label="Test Data")
plt.plot(hist.history["accuracy"], color="g", label="Train Data")
plt.xlabel("Epochs")
plt.ylabel("Hasil Akurasi")
plt.legend()
plt.show()

