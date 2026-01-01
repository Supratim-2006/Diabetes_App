import streamlit as st

st.markdown(
    "<h1 style='text-align: center;'>About the Project</h1>",
    unsafe_allow_html=True
)
st.markdown(
    """
    <div>
        <h5>This is an Machine-Learning Project give as a task by IEEE seniors of NIT DGP in the Epoch program.<br>
        Diabetes is a chronic metabolic disorder characterized by elevated blood glucose levels. Early and accurate detection of diabetes is crucial for effective management and prevention of complications. This project focuses on developing a machine learning model to predict the likelihood of an individual having diabetes based on various health indicators.Its predicts that a person is Diabetic or not by evaluating features including age,bmi,glucose level,Insulin etc. I have used XGBboost to train my model as it gave the highest accuracy in prediction from my dataset (Pima Indians Diabates Database), from kaggle.I used Standard Scalar to scale my data.<br>I also implemented hand gesture for locking and unlocking the website(there are fews errors in the gestures as I have made some mistakes while data collection).I used keras and tensorflow to train my model.<br>
        I implemented the whole logic in a Streamlit application which includes downloading the pdf of the data taken,show graphs of the variation of mean data with user given datas </h5>
    <div>
    <div>
    <h1 style='text-align: center;'>About Me</h1><br>
    <h5>
    I am Supratim Kukri,first year undergraduate at NIT DGP(ECE), AI-ML enthusiastic.This is my first Project.
    </h5><br>
    <h5>
    
    </h5>
    <div>
    """,unsafe_allow_html=True
)
url="https://www.linkedin.com/in/supratim-kukri-33871a29a/"
st.markdown("Linked-In Profile- %s" % url)


