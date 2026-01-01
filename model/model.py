import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
import pickle

df=pd.read_csv('model/diabetes.csv')



X=df.drop('Outcome',axis=1)
y=df['Outcome']

scaler=StandardScaler()
X_scaled=scaler.fit_transform(X)
X_scaled

X_train,X_test,y_train,y_test=train_test_split(X_scaled,y,test_size=0.2,random_state=10,stratify=y)



# XGBoost Classifier


xgb = XGBClassifier(
    n_estimators=80,
    learning_rate=0.1,
    max_depth=3,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric='logloss'
)

xgb.fit(X_train,y_train)
xgb_score=xgb.score(X_test,y_test)

with open('model/diabetes_model.pkl','wb') as f:
    pickle.dump(xgb,f)

f.close()

with open('model/scaler.pkl','wb') as f:
    pickle.dump(scaler,f)

f.close()


#predicting a single instance
import numpy as np

single_instance=np.array([[6,148,72,35,0,33.6,0.627,50]])
single_instance_scaled=scaler.fit_transform(single_instance)
prediction=xgb.predict(single_instance_scaled)
print(f"Prediction for single instance: {prediction}")


if(prediction[0]==1):
    print("The person is non diabetic.")
else:
    print("The person is not diabetic.")