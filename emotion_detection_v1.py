from mimetypes import init
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageOps
import tensorflow
import keras
import cv2
import numpy as np
from keras.utils import img_to_array


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

def opt_in_func(yes_no):
    if yes_no == 'Yes':
        st.write('You selected:', yes_no, '\n Thank You!'),
    else:
        st.write('You selected:', yes_no, '\n Please choose yes if you would like to view all of our benchmarking data. You will still get stats on your call\'s performance')

starter_image = Image.open('./Images/Zoom_Call.jpg')

def init_image(img):
    if uploaded_file is not None:
        st.image(uploaded_file, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
    else:
        st.image(starter_image, caption='Example Image from Unsplash')


st.title("Emotion Detection for Sales Call Performance")

st.header("Train Your Sales Team Effectively With AI Emotion Detection")
st.markdown("Benchmark your sales performance with just a few details on your sales call and a screenshot taken at an important moment. Get insight into how your facial emotions likely appear to the prospect, and *what their likely emotion is at that point as well.*")

#Add an image here showing input image, output predictions, and benchmarking


opt_in = st.radio(
    'Can we use your image and call information to improve our metrics? This information will be kept private and only used for generating our benchmarks',
    ('Yes', 'No'))

st.write(opt_in_func(opt_in))

st.write("## Sales Call Information")

st.write("### Sales Info")

role = st.radio(
    'What is your role on the sales team?',
    ('Sales Development Rep', 'Sales Specialist/Consultant', 'Account Executive', 'Customer Success Rep', 'Sales Manager', 'Other'))

team = st.multiselect(
    'If any, what other types of team members were on the call?',
    ['Sales Development Rep', 'Sales Specialist/Consultant', 'Account Executive', 'Customer Success Rep', 'Sales Manager'])

industry = st.selectbox(
    'What industry is your business primarily selling into?',
    ('Automotive', 'Banking', 'Education', 'Finance', 'Government', 'Healthcare',
     'Information (processing, commmunication, storage, etc.)', 'Insurance',
      'Logistics', 'Manufacturing','Marketing', 'Media', 'Mining', 'Oil and Gas',
       'Professional Services', 'Real Estate', 'Renewable Energy', 'Scientific Services', 'Technology/Software Development', 'Other'))

industry_other = st.text_input('If other, what industry do you primarily sell into', 'E.g. Clothing')

sale_type = st.radio(
    'Do you sell a good or service?',
    ('Good', 'Service'))

product = st.text_input('In 1 or 2 words, what do you sell?', 'E.g. HVAC, Insurance, SaaS Platform, Consulting, Etc.')

# Add a function/yes/no input asking if all information is accurate (print out overview of their responses), If they click yes, respond "great, let's move on" if no, ask to go back and update

st.write("### Call Info")

sales_stages = np.array(['1. Prospecting', '2. Qualifying', '3. Exploration Call', '4. Demo/Pitch', '5. Negotiation', '6. Deal Signing/Account Close', '7. Customer Success Handoff'])

stage = st.select_slider(
    'At what stage in the sales pipeline did this call occur?',
    options=sales_stages)

outcome = st.radio(
    'What was the outcome of the call?',
    ('Moved to Next Stage', 'Disqualified Lead', 'No Change (Objections Not Overcome)', 'Closed Sale', 'Lost Sale'))

st.write('## Here\'s How You Compare')

# Add Section Covering Stats on similar calls - emotions on faces when sale outcome was the same, when the outcome was better (moved to next stage, closed, etc.)
# Also breakdown of the outcomes by role, normalized outcomes across stages, etc.

uploaded_file = st.file_uploader("Upload an image from your computer",
type=['png', 'jpg', 'jpeg', 'JPG'],
help='Upload a jpeg image taken during a sales video call with both your face and a prospect\'s face visible.')

st.write('## Here is your Image')

init_image(uploaded_file)

st.write('## Here is your Image with Predictions')

if uploaded_file is None:
    st.write('Please upload your own image file')
else:
    import_and_predict(uploaded_file, model)