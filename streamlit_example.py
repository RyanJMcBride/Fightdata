import streamlit as st

header = st.beta_container()
left_column, right_column = st.beta_columns(2)

with header:
    st.title("I love Erin Mcklenzie")
with left_column:
    st.title("testing")
with right_column:
    st.title("test2")
