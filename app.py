import pandas as pd
import scipy.stats
import streamlit as st
import time

# Set the state for the session
if 'experiment_no' not in st.session_state: 
    st.session_state['experiment_no'] = 0
    
if 'df_experiment_results' not in st.session_state: 
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteration', 'mean'])

# Set the header
st.header('Tossing a Coin')

# Creates a line chart 
chart = st.line_chart([[0.5]])

# Fuction to test the coin flip and add probability to the chart
def toss_coin(n): 
    
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    
    mean = None
    outcome_no = 0 
    outcome_1_count = 0
    
    for r in trial_outcomes: 
        outcome_no += 1
        if r == 1: 
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)
    
    return mean

# Creates a slider for user to pick the number of trials
number_of_trials = st.slider('Number of Trials', 1, 1000, 10)

# Makes buttons on the same line 
col1, col2 = st.columns(2)
with col1: 
    start_button = st.button('Run')
    reset_button = st.button('Reset')

# Start the trials and save each run result
if start_button: 
    
    st.write(f'Running the experiment of {number_of_trials} trials.')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'], 
        pd.DataFrame(data=[[st.session_state['experiment_no'], number_of_trials, mean]],
                     columns=['no', 'iteration', 'mean'])
        ],
        axis=0)
    st.session_state['df_experiment_results'] = st.session_state['df_experiment_results'].reset_index(drop=True)
    
# Reset the chart
if reset_button: 
   st.session_state['experiment_no'] = 0
   st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteration', 'mean'])
    
st.write(st.session_state['df_experiment_results'])

