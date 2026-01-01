
import keras
import pandas as pd

data_file=pd.read_csv("TrainingModel/data.csv")
data_file = data_file.sample(frac=1).reset_index(drop=True)
total_recognitions=2

data=data_file.drop(data_file.columns[0],axis=1).to_numpy()
label=data_file.iloc[:, 0].to_numpy()

model=keras.Sequential([
    keras.layers.Flatten(input_shape=(40,1)),
    keras.layers.Dense(128,activation="relu"),
    keras.layers.Dense(total_recognitions,activation="softmax")
])

model.compile(optimizer="adam",loss="sparse_categorical_crossentropy",metrics=["accuracy"])
model.fit(data,label,epochs=5)
tdata_file=pd.read_csv("TrainingModel/tdata.csv")
tdata_file = tdata_file.sample(frac=1).reset_index(drop=True)

tdata=tdata_file.drop(data_file.columns[0],axis=1).to_numpy()
tlabel=tdata_file.iloc[:, 0].to_numpy()

tloss, tacc = model.evaluate(tdata, tlabel)
print(f"Test Loss: {tloss}, Test Accuracy: {tacc}")

# 2. SAVE in H5 format (Native to Legacy Keras)
# Change the extension from .keras to .h5
model.save("TrainingModel/gesturedetector.h5") 

print("Model saved successfully in H5 format.")