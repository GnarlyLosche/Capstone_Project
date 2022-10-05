import streamlit as st
import numpy as np

st.set_page_config(layout="wide")

def state_opt_in(input):
    if input == 'Yes':
        return False
    else:
        return True

st.title("Call Info")

sales_stages = np.array(['1. Prospecting', '2. Qualifying', '3. Exploration Call', '4. Demo/Pitch', '5. Negotiation', '6. Deal Signing/Account Close', '7. Customer Success Handoff'])

stage = st.select_slider(
    'At what stage in the sales pipeline did this call occur?',
    options=sales_stages)

prospects = st.slider(
    'How many stakeholders were on the call? Don\'t include salespeople.',
    min_value=1,
    max_value=10)

outcome = st.radio(
    'What was the outcome of the call?',
    ('Moved to Next Stage', 'Disqualified Lead', 'No Change (Objections Not Overcome)', 'Closed Sale', 'Lost Sale'))

st.write('## Here\'s How You Compare')

# Block will have 2 columns, first column much wider than 2nd
# 1. line plot of the frequencies of successful calls by stage
# 2. dataframe showing the most successful type of salesperson for each stage

# 3. Histogram of the % of successful calls by # of prospects on call
# 4. Write below - "Most successful calls only have {largest bucket on histogram} prospects on the call"
# 5. If they had same, less or more 
#       Less "you only had X stakeholders on the call, perhaps there's an internal stakeholder you need to win over" 
#       More "You had X stakeholders on the call, it can be hard to control a conversation with that much input, can you focus on the decision maker?"
#       same "Looks like you set up the call well!"

# 6. Write below- If they had a successful call say "Good Job! Only X% of {stage} calls are successful", if not successful, "Don't worry, only x% of {stage} calls are successful"

# 7. Most {stage} calls are successful when both the prospect and salepeople appear {emotion at stage when successful}, unfortunately, often people come across as {max emotion at stage}

st.write("#### If you're ready to try out the model and don't care about industry benchmarking, head to Emotion Detection")

st.title("Sales Call Information - Industry Benchmarking")

st.header('Optional: Share information to see benchmarking data')

opt_in = st.radio(
    'Can we use information to improve our metrics? This information will be kept private and only used for generating our benchmarks.',
    ('Yes', 'No'))

if opt_in == 'Yes':
    st.write(f'You selected: {opt_in}, \n Thank You!')
else:
    st.write(f'You selected: {opt_in},\n Please choose yes if you would like to view all of our benchmarking data. You will still get stats on your call\'s performance')

st.header("Sales Info")

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

disable = state_opt_in(opt_in)

# Add a function inputing their data in a dataframe to return benchmarks
# If I add the function to the on click callback, it will run the function to add their info
click = st.button('Click Here to Add your Call Details', help='If you opted out of sharing your call information, you can\'t add your call info', disabled=False)

# Add an 'if click:' statement to generate a 3 column section with dataframe(s) showing:
# 1. success rates for their industy vs the top 5 industries (success is Moved to next stage or closed sale)
# 2. success rates for each type of sales team member
# 3. text saying The {industry} sector is the {inverted ranking} hardest to sell into. Most sales in {industry} are lost during the {max(sales_stages)} stage

# 2nd block will have 2 columns, first column much wider than 2nd
# 1. line plot of the frequencies of successful calls at that stage for their industry
# 2. dataframe showing the most successful type of salesperson for each stage for their industry

# Recommendations Section
# st.write() saying "It looks like a {salesperson} led this call, at the {stage} stage, the {max(salesperson type at that stage)} tends to be the most successful"
# st.write() saying "You had at least {len(team) + prospects + 1} (for prospect and lead) people on the call, most successful calls only have {# of sales people +1 for most successful calls} salespeople
