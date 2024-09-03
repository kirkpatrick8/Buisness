import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Function to validate email
def validate_email(email):
    return email.endswith('@aecom.com')

# Function to send email
def send_email(receiver_email, csv_file):
    sender_email = "your_email@example.com"  # Replace with your email
    password = "your_password"  # Replace with your email password

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "Your Siphons Template CSV"

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(csv_file, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{csv_file}"')
    message.attach(part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(message)

# Streamlit app
st.title('Siphons Template Filler')

# Template selection (for future expansion)
template = st.selectbox('Select Template', ['Siphons Template'])

# Create a dictionary to store role assignments
roles = {
    'AECOM Technical Head': '',
    'Hydraulics Specialist - Major Conveyance': '',
    'Role 2 Technical Director Civil': '',
    'Role 3 Framework Manager': '',
    'Role 4 Principal Engineer / PM Wastewater Infra': '',
    # Add more roles as needed
}

# Role assignment
st.subheader('Role Assignment')
for role in roles:
    roles[role] = st.text_input(f'Assign name to {role}')

# Fee input
st.subheader('Fee Input')
fees = {}
for role in roles:
    fees[role] = st.number_input(f'Fee for {role} (£/hr)', min_value=0.0, step=0.1)

# Job and hours assignment
st.subheader('Job and Hours Assignment')
jobs = ['General project management', 'Project execution plan', 'Project delivery programme']  # Add more jobs as needed
job_assignments = {}

for job in jobs:
    st.write(f'Assign hours for: {job}')
    job_assignments[job] = {}
    for role in roles:
        job_assignments[job][role] = st.number_input(f'Hours for {role}', min_value=0, step=1)

if st.button('Generate CSV'):
    # Create DataFrame
    data = []
    for job in jobs:
        for role in roles:
            if job_assignments[job][role] > 0:
                data.append({
                    'Job': job,
                    'Role': role,
                    'Name': roles[role],
                    'Fee (£/hr)': fees[role],
                    'Hours': job_assignments[job][role],
                    'Total Cost': fees[role] * job_assignments[job][role]
                })
    
    df = pd.DataFrame(data)
    
    # Save DataFrame to CSV
    csv_file = 'siphons_template_output.csv'
    df.to_csv(csv_file, index=False)
    
    # Option to download or email
    option = st.radio("Choose an option", ('Download', 'Email'))
    
    if option == 'Download':
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='siphons_template_output.csv',
            mime='text/csv',
        )
    else:
        email = st.text_input('Enter your email (@aecom.com)')
        if st.button('Send Email'):
            if validate_email(email):
                try:
                    send_email(email, csv_file)
                    st.success('Email sent successfully!')
                except Exception as e:
                    st.error(f'An error occurred: {str(e)}')
            else:
                st.error('Invalid email. Please use an @aecom.com email address.')
