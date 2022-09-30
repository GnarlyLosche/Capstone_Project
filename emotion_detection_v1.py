from mimetypes import init
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

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