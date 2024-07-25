import streamlit as st
import requests

st.title("Automated Essay Scoring")

essay_text = st.text_area("Enter your essay:", height=300)
if st.button("Get Score"):
    if essay_text.strip():
        try:
            response = requests.post("http://localhost:8000/predict", json={"full_text": essay_text})
            response.raise_for_status()
            score = response.json().get("score")
            st.success(f"Predicted Score: {score}")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to get a score: {e}")
    else:
        st.warning("Please enter an essay.")


