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

# Create a dictionary to store role assignments and fees
roles = {
    'AECOM Technical Head': {'name': '', 'fee': 0.0},
    'Hydraulics Specialist - Major Conveyance': {'name': '', 'fee': 0.0},
    'Role 2 Technical Director Civil': {'name': '', 'fee': 0.0},
    'Role 3 Framework Manager': {'name': '', 'fee': 0.0},
    'Role 4 Principal Engineer / PM Wastewater Infra': {'name': '', 'fee': 0.0},
    'Role 4 Principal Engineer / Hydraulic Designer': {'name': '', 'fee': 0.0},
    'Role 5 Senior Engineer': {'name': '', 'fee': 0.0},
    'Role 6 Engineer': {'name': '', 'fee': 0.0},
    'Role 7 Graduate Engineer': {'name': '', 'fee': 0.0},
    'P6 Programmer equivalent to Role 5 Senior': {'name': '', 'fee': 0.0},
    'Role 10 Principal Designer': {'name': '', 'fee': 0.0},
}

# Role assignment and fee input
st.subheader('Role Assignment and Fee Input')
for role in roles:
    col1, col2 = st.columns(2)
    with col1:
        roles[role]['name'] = st.text_input(f'Assign name to {role}')
    with col2:
        roles[role]['fee'] = st.number_input(f'Fee for {role} (£/hr)', min_value=0.0, step=0.1)

# Job and hours assignment
st.subheader('Job and Hours Assignment')
jobs = {
    'General Project Management Duties': {
        'description': 'General aspects of multidisciplinary project management',
        'sub_tasks': {
            'General project management': {
                'description': 'General aspects of multidisciplinary project management, as required, including: general administration; management of the project in line with NIW Capital Works Procedures; management of the project in accordance with all legislative requirements; appointment, management and administration of subconsultants and other subcontracted resources; management of risk, value, time, quality, change, cost, safety and environmental aspects in compliance with NIW processes and procedures; general liaison and consultation with NIW on project related matters etc., as required.',
                'deliverable': 'Various - none defined per se',
                'hours': {}
            },
            'Project execution plan': {
                'description': 'Provide and regularly update a Project Execution Plan.',
                'deliverable': 'Project execution plan 24 hours for production plus 16 for update',
                'hours': {}
            },
            'Project delivery programme': {
                'description': 'Provide and regularly update a Project Delivery Programme showing: Key Activities and sub-activities as appropriate; Key constraints, e.g. planning, environmental, regulatory, legislative etc.; Key Dates, e.g. NIW KPI deadlines, Governance Gateways (A1, A2, A3 Approvals); Progress etc., as required.',
                'deliverable': '16 hours to create plus 4 hours per month to maintain over a 18 month period. 4 hours monthly PM review, 1 hour sub team updates over 6 months. Updates to be completed by P6 programmer',
                'hours': {}
            },
            'Stakeholder management plan': {
                'description': 'Provide and regularly update a Stakeholder Management Plan in agreement with NIW. Plan to include: Identification of key internal (NIW) and external stakeholders; Prioritisation of key stakeholders in line with project risks (e.g. statutory assents and consents, lands, site possessions. opposition, damage to PM / contractor / NIW reputation etc.); Establishment of contact details for key stakeholders; Plans for communicating with key stakeholders, as required.',
                'deliverable': 'Drafted by SD & JS, approved by SM and created by EM',
                'hours': {}
            },
            'Project risk register': {
                'description': 'Prepare and regularly update a Project Risk Register in accordance with NIW risk management procedures, as required.',
                'deliverable': 'Project risk register',
                'hours': {}
            },
            'Financial projections & reporting': {
                'description': 'Provide monthly financial information and data on the project for input to the Employer\'s "CPMR" financial management system as required, including monitoring and updating accrued and projected project budget profiles, broken down into accruals for development contracts, construction contracts (Civil & MEICA combined), NIE costs, land acquisition costs, wayleave costs, Transport NI costs and consultant fees, as required.',
                'deliverable': 'Monthly financial dashboard completion',
                'hours': {}
            },
            'Change management': {
                'description': 'Allowance for review and discussion with NIW Cost Management Team',
                'deliverable': 'Engagement with Cost Managers',
                'hours': {}
            },
            'Progress meetings': {
                'description': 'Prepare agendas, organise and attend progress meetings and record and circulate minutes, as required.',
                'deliverable': 'Meeting agendas and minutes',
                'hours': {}
            }
        }
    },
    'Principal Designer': {
        'description': 'Principal Designer duties',
        'sub_tasks': {
            'Principal Designer': {
                'description': 'Carry out all requisite Principal Designer duties, as required.',
                'deliverable': 'Various - none defined per se',
                'hours': {}
            },
            'Designers Risk Register': {
                'description': 'Prepare and maintain Designers Risk Register',
                'deliverable': 'Designers Risk Register',
                'hours': {}
            }
        }
    }
}

for main_task, main_details in jobs.items():
    st.write(f'## {main_task}')
    st.write(f'Description: {main_details["description"]}')
    for sub_task, details in main_details['sub_tasks'].items():
        st.write(f'### {sub_task}')
        st.write(f'Description: {details["description"]}')
        st.write(f'Deliverable: {details["deliverable"]}')
        for role in roles:
            details['hours'][role] = st.number_input(f'Hours for {role}', min_value=0, step=1, key=f"{main_task}_{sub_task}_{role}")

if st.button('Generate CSV'):
    # Create DataFrame
    data = []
    for main_task, main_details in jobs.items():
        for sub_task, details in main_details['sub_tasks'].items():
            for role in roles:
                if details['hours'][role] > 0:
                    data.append({
                        'Main Task': main_task,
                        'Sub Task': sub_task,
                        'Description': details['description'],
                        'Deliverable': details['deliverable'],
                        'Role': role,
                        'Name': roles[role]['name'],
                        'Fee (£/hr)': roles[role]['fee'],
                        'Hours': details['hours'][role],
                        'Total Cost': roles[role]['fee'] * details['hours'][role]
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

# Display current assignments
st.subheader('Current Assignments')
for main_task, main_details in jobs.items():
    st.write(f"## {main_task}")
    st.write(f"Description: {main_details['description']}")
    for sub_task, details in main_details['sub_tasks'].items():
        st.write(f"### {sub_task}")
        st.write(f"Description: {details['description']}")
        st.write(f"Deliverable: {details['deliverable']}")
        for role, hours in details['hours'].items():
            if hours > 0:
                st.write(f"{role}: {hours} hours")
        st.write("---")
