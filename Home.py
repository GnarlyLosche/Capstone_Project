import streamlit as st
from PIL import Image, ImageOps

st.set_page_config(layout="wide")

starter_image = Image.open('./Images/Zoom_Call.jpg')
preds_image = Image.open('./Images/Zoom_Call_Preds.png')

st.title("Emotion Detection for Sales Call Performance")

st.header("Train Your Sales Team Effectively With AI Emotion Detection")
st.write("#### Benchmark your sales performance with just a few details and a screenshot taken at an important moment. Get insight into how your facial emotions likely appear to the prospect, and *what their likely emotion is at that point as well.*")

col1, col2 = st.columns(2)

with col1:
   st.header("Initial Screenshot")
   st.image(starter_image, caption='Example Image from Unsplash')

with col2:
   st.header("Predictions")
   st.image(preds_image, caption='Overall, attendees appear happy')

st.write('### For benchmarking, head to Call details. Otherwise, check out Emotion Detection')