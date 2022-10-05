import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageOps
import tensorflow
import keras
import cv2
import numpy as np
from keras.utils import img_to_array

st.set_page_config(layout="wide")

st.set_option('deprecation.showfileUploaderEncoding', False)
@st.cache(allow_output_mutation=True)


def load_model():
    model = tensorflow.keras.models.load_model('/Users/charlielosche/Documents/Flatiron/Flatiron_Repos/Capstone_Project/Data/emotion_detector_models/charlie_model/v2_final_model.h5')
    return model

model = load_model()

class_labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def face_detector(img):
    """function to detect faces from screenshot"""
    scaled = img.resize((1500,1000))
    new_img = np.array(scaled.convert('RGB'))
    img = cv2.cvtColor(new_img, 1)
    gray = cv2.cvtColor(new_img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, scaleFactor=1.15,
	minNeighbors=5, minSize=(30, 30),
	flags=cv2.CASCADE_SCALE_IMAGE)
    if np.array_equal(faces,()):
        return (0,0,0,0), np.zeros((48,48), np.uint8), img
    
    allfaces = []   
    rects = []
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation = cv2.INTER_AREA)
        allfaces.append(roi_gray)
        rects.append((x,w,y,h))
    return rects, allfaces, img

def most_frequent(sentiment):
    return max(set(sentiment), key = sentiment.count)

def import_and_predict(image_data, model):
    """Function to predict the emotion class from the uploaded image"""
    img = Image.open(image_data)
    rects, faces, image = face_detector(img)

    sentiment = []
    i = 0
    for face in faces:
        roi = face.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)

        # make a prediction on the ROI, then lookup the class
        preds = model.predict(roi)[0]
        label = class_labels[preds.argmax()]   
        sentiment.append(label)

        #Overlay our detected emotion on our pic
        label_position = (rects[i][0] + int((rects[i][1]/2)), abs(rects[i][2] - 10))
        i = i + 1
        cv2.putText(image, label, label_position , cv2.FONT_HERSHEY_COMPLEX,1, (0,255,0), 2)
    primary_emotion = most_frequent(sentiment)    
    #Show the image with emotion labels
    st.image(image, caption=f'Overall, attendees appear {primary_emotion}', width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

starter_image = Image.open('/Users/charlielosche/Documents/Flatiron/Flatiron_Repos/Capstone_Project/Images/Zoom_Call.jpg')

st.title("Emotion Detection for Sales Call Performance")

st.header("Input your photo and see the predicted emotions")

st.write("People often think they are controlling their emotions better than they may actually be, this model provides an objective view of the likely way others interpret your facial expressions on a call")

uploaded_file = st.file_uploader("Upload an video meeting screenshot",
type=['png', 'jpg', 'jpeg', 'JPG'],
help='Upload a jpeg image taken during a sales video call with both your face and a prospect\'s face visible.')

st.write('## Here is your Image')

if uploaded_file is None:
    st.image(starter_image, caption='Example Image from Unsplash')
else:
    st.image(uploaded_file, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

st.write('## Click the button to see predictions')

col1, col2, col3, col4, col5 = st.columns(5)

with col3:
   emotions = st.button('Detect Emotions')

if emotions:
    import_and_predict(uploaded_file, model)
else:
    st.write('Please upload your own image file')