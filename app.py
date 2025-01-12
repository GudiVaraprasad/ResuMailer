import streamlit as st
import json

from utils.prompt import construct_prompt
from utils.extract import extract_resume
from utils.extract import extract_jobdesc
from utils.api import generate_response

# Streamlit Layout
st.set_page_config(page_title="Cold Email Generator", layout="wide")
st.markdown(
    """
    <h1 style="text-align: center;">Cold Email Generator</h1>
    """,
    unsafe_allow_html=True
)

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
        <h4 style="text-align: center;">Cold Email Settings</h4>
        """,
        unsafe_allow_html=True
    )
    # receiver_email = st.text_input("Recruiter Email")
    # role_type = st.selectbox("Job Role Type", ["Custom", "Data Analysis", "Data Engineer", "Data Science", "SDE"], key="role_select")
    
    # custom_role = ""
    # if role_type == "Custom":
    #     custom_role = st.text_input("Enter Custom Role", key="custom_role_key")
    
    receiver_name = st.text_input("Recruiter Name")
    job_role = st.text_input("Job Role Name")
    job_desc = st.text_input("Job URL")
    uploaded_resume = st.file_uploader("Upload Resume (PDF, DOCX, TXT)", type=['pdf', 'docx', 'txt'])
    
    cold_email_button = st.button("Generate Cold Email")

    if cold_email_button:
        if not receiver_name or not job_desc or not uploaded_resume:
            st.error("Please fill all required fields.")
        else:
            resume_text = extract_resume(uploaded_resume)
            job_description = extract_jobdesc(job_desc)
            with open("sender_details.json", "r") as f:
                sender_details = json.load(f)

            prompt = construct_prompt(resume_text, job_description, sender_details, receiver_name, job_role)
            with st.spinner("Generating..."):
                cold_email = generate_response(prompt)
                st.session_state.cold_email = cold_email

                with open("coldemail.txt", "w") as file:
                    file.write(cold_email)

                st.success("Cold email generated!")

if 'cold_email' not in st.session_state:
    st.session_state.cold_email = ""

with col2:
    st.markdown(
        """
        <h4 style="text-align: center;">Generated Email</h4>
        """,
        unsafe_allow_html=True
    )
    
    # Display the email if it exists in session state
    if st.session_state.cold_email:
        st.markdown(st.session_state.cold_email)