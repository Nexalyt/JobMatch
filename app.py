import streamlit as st
import random
import matplotlib.pyplot as plt

# Initialize or retrieve flip results
if 'flip_results' not in st.session_state:
    st.session_state.flip_results = {"Cara": 0, "Cruz": 0}

# Function to flip the coin
def flip_coin(prob_cara=0.5):
    return 'Cara' if random.random() < prob_cara else 'Cruz'

# App title and instructions
st.title('Coin Flip Simulator')
st.header('Flip a Coin with Adjustable Bias')
st.write('Set the bias and flip the coin to see the cumulative results.')

# Bias slider
prob_cara = st.slider('Adjust the probability of landing on "Cara"', 0.0, 1.0, 0.5)

# Flip button
if st.button('Flip the Coin'):
    result = flip_coin(prob_cara)
    st.session_state.flip_results[result] += 1
    st.success(f'You flipped: {result}')
    st.write(f'Current Counts: Cara = {st.session_state.flip_results["Cara"]}, Cruz = {st.session_state.flip_results["Cruz"]}')

# Plot the cumulative results
if sum(st.session_state.flip_results.values()) > 0:
    st.write("Cumulative Flip Results:")
    fig, ax = plt.subplots()
    ax.bar(st.session_state.flip_results.keys(), st.session_state.flip_results.values())
    ax.set_xlabel('Side')
    ax.set_ylabel('Number of Flips')
    ax.set_title('Cumulative Coin Flip Results')
    st.pyplot(fig)
    total_flips = sum(st.session_state.flip_results.values())
    if total_flips > 0:
        cara_percentage = (st.session_state.flip_results["Cara"] / total_flips) * 100
        cruz_percentage = (st.session_state.flip_results["Cruz"] / total_flips) * 100
        st.write(f'Percentage of Cara: {cara_percentage:.2f}%')
        st.write(f'Percentage of Cruz: {cruz_percentage:.2f}%')