import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from streamlit_sortables import sort_items

# Set page config
st.set_page_config(page_title="Project Tools", layout="wide")

# Sidebar for tool selection
tool = st.sidebar.radio("Select Tool", ["Activity Scheduling", "Siphons Template Filler"])

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

if tool == "Activity Scheduling":
    # Activity Scheduling Tool
    st.title("Dynamic Project Activity Schedule")

    # Initialize session state
    if 'team' not in st.session_state:
        st.session_state.team = []
    if 'jobs' not in st.session_state:
        st.session_state.jobs = []
    if 'assignments' not in st.session_state:
        st.session_state.assignments = {}

    # Sidebar for adding team members and jobs
    with st.sidebar:
        st.header("Team and Activities Management")
        
        # Add team member
        new_role = st.text_input("Enter new role")
        if st.button("Add Team Member"):
            if new_role and new_role not in [member['role'] for member in st.session_state.team]:
                st.session_state.team.append({'role': new_role, 'id': len(st.session_state.team)})
        
        # Add job
        new_job = st.text_input("Enter new activity")
        if st.button("Add Activity"):
            if new_job and new_job not in st.session_state.jobs:
                st.session_state.jobs.append(new_job)
                st.session_state.assignments[new_job] = {}

        # Display and allow editing of team members
        st.subheader("Current Team")
        for i, member in enumerate(st.session_state.team):
            cols = st.columns([3, 1])
            cols[0].write(member['role'])
            if cols[1].button("Remove", key=f"remove_member_{i}"):
                st.session_state.team.pop(i)
                st.rerun()

        # Display and allow editing of jobs
        st.subheader("Current Activities")
        for i, job in enumerate(st.session_state.jobs):
            cols = st.columns([3, 1])
            cols[0].write(job)
            if cols[1].button("Remove", key=f"remove_job_{i}"):
                st.session_state.jobs.pop(i)
                del st.session_state.assignments[job]
                st.rerun()

    # Main content
    st.header("Assign Hours")

    # Create assignments for each job
    for job in st.session_state.jobs:
        st.subheader(f"Activity: {job}")
        
        # Use sortable list to add team members to the job
        available_team = [member['role'] for member in st.session_state.team 
                          if member['role'] not in st.session_state.assignments[job]]
        assigned_team = list(st.session_state.assignments[job].keys())
        
        columns = st.columns(2)
        with columns[0]:
            st.write("Available Team Members")
            selected = sort_items(available_team, key=f"available_{job}")
        with columns[1]:
            st.write("Assigned Team Members")
            assigned = sort_items(assigned_team, key=f"assigned_{job}")
        
        # Update assignments based on drag and drop
        for role in assigned:
            if role not in st.session_state.assignments[job]:
                st.session_state.assignments[job][role] = 0
        for role in list(st.session_state.assignments[job].keys()):
            if role not in assigned:
                del st.session_state.assignments[job][role]
        
        # Input hours for assigned team members
        for role in st.session_state.assignments[job]:
            st.session_state.assignments[job][role] = st.number_input(
                f"Hours for {role}",
                min_value=0,
                value=st.session_state.assignments[job][role],
                key=f"{job}_{role}"
            )

    # Generate and download CSV
    if st.button('Generate CSV'):
        data = []
        for job in st.session_state.jobs:
            job_data = {'Activity': job}
            job_data.update(st.session_state.assignments[job])
            data.append(job_data)
        
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="activity_schedule.csv",
            mime="text/csv",
        )

    # Display current assignments
    st.header("Current Assignments")
    st.json(st.session_state.assignments)

elif tool == "Siphons Template Filler":
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
            job_assignments[job][role] = st.number_input(f'Hours for {role} in {job}', min_value=0, step=1, key=f"{job}_{role}")

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
