import streamlit as st
import pandas as pd
import io

# Initialize session state
if 'roles' not in st.session_state:
    st.session_state.roles = {
        'AECOM Technical Head': {'name': '', 'fee': 0.0},
        'Hydraulics Specialist - Major Conveyance': {'name': '', 'fee': 0.0},
        'Role 2 Technical Director Civil': {'name': '', 'fee': 0.0},
        'Role 3 Framework Manager': {'name': '', 'fee': 0.0},
        'Role 4 Principal Engineer / PM Wastewater Infra': {'name': '', 'fee': 0.0},
    }

if 'tasks' not in st.session_state:
    st.session_state.tasks = {
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
            }
        }
    }

# Streamlit app
st.title('Dynamic Siphons Template Filler')

# Role management
st.header("Role Management")
new_role = st.text_input("Add new role")
if st.button("Add Role"):
    if new_role and new_role not in st.session_state.roles:
        st.session_state.roles[new_role] = {'name': '', 'fee': 0.0}
        st.success(f"Added role: {new_role}")

role_to_delete = st.selectbox("Select role to delete", options=list(st.session_state.roles.keys()))
if st.button("Delete Role"):
    del st.session_state.roles[role_to_delete]
    st.success(f"Deleted role: {role_to_delete}")

# Role assignment and fee input
st.header('Role Assignment and Fee Input')
for role in st.session_state.roles:
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.roles[role]['name'] = st.text_input(f'Assign name to {role}', key=f"name_{role}")
    with col2:
        st.session_state.roles[role]['fee'] = st.number_input(f'Fee for {role} (£/hr)', min_value=0.0, step=0.1, key=f"fee_{role}")

# Task management
st.header("Task Management")
new_main_task = st.text_input("Add new main task")
if st.button("Add Main Task"):
    if new_main_task and new_main_task not in st.session_state.tasks:
        st.session_state.tasks[new_main_task] = {
            'description': '',
            'sub_tasks': {}
        }
        st.success(f"Added main task: {new_main_task}")

main_task_to_delete = st.selectbox("Select main task to delete", options=list(st.session_state.tasks.keys()))
if st.button("Delete Main Task"):
    del st.session_state.tasks[main_task_to_delete]
    st.success(f"Deleted main task: {main_task_to_delete}")

# Sub-task management
st.subheader("Sub-task Management")
main_task_for_subtask = st.selectbox("Select main task for sub-task", options=list(st.session_state.tasks.keys()))
new_sub_task = st.text_input("Add new sub-task")
if st.button("Add Sub-task"):
    if new_sub_task and new_sub_task not in st.session_state.tasks[main_task_for_subtask]['sub_tasks']:
        st.session_state.tasks[main_task_for_subtask]['sub_tasks'][new_sub_task] = {
            'description': '',
            'deliverable': '',
            'hours': {role: 0 for role in st.session_state.roles}
        }
        st.success(f"Added sub-task: {new_sub_task} to {main_task_for_subtask}")

sub_task_to_delete = st.selectbox("Select sub-task to delete", options=list(st.session_state.tasks[main_task_for_subtask]['sub_tasks'].keys()))
if st.button("Delete Sub-task"):
    del st.session_state.tasks[main_task_for_subtask]['sub_tasks'][sub_task_to_delete]
    st.success(f"Deleted sub-task: {sub_task_to_delete} from {main_task_for_subtask}")

# Task and hours assignment
st.header('Task and Hours Assignment')
for main_task, main_details in st.session_state.tasks.items():
    st.subheader(main_task)
    main_details['description'] = st.text_area(f"Description for {main_task}", value=main_details['description'])
    for sub_task, details in main_details['sub_tasks'].items():
        st.write(f"### {sub_task}")
        details['description'] = st.text_area(f"Description for {sub_task}", value=details['description'])
        details['deliverable'] = st.text_input(f"Deliverable for {sub_task}", value=details['deliverable'])
        for role in st.session_state.roles:
            details['hours'][role] = st.number_input(f'Hours for {role}', min_value=0, step=1, key=f"{main_task}_{sub_task}_{role}")

if st.button('Generate CSV'):
    # Prepare data for CSV
    data = []
    total_hours = {role: 0 for role in st.session_state.roles}
    total_cost = {role: 0 for role in st.session_state.roles}
    
    for main_task, main_details in st.session_state.tasks.items():
        for sub_task, details in main_details['sub_tasks'].items():
            row = {
                'Task': main_task,
                'Sub-task': sub_task,
                'Description': details['description'],
                'Deliverable': details['deliverable'],
            }
            for role in st.session_state.roles:
                hours = details['hours'].get(role, 0)
                fee = st.session_state.roles[role]['fee']
                row[f'{role} Hours'] = hours
                row[f'{role} Cost'] = hours * fee
                total_hours[role] += hours
                total_cost[role] += hours * fee
            data.append(row)
    
    # Add total row
    total_row = {'Task': 'Total', 'Sub-task': '', 'Description': '', 'Deliverable': ''}
    for role in st.session_state.roles:
        total_row[f'{role} Hours'] = total_hours[role]
        total_row[f'{role} Cost'] = total_cost[role]
    data.append(total_row)
    
    df = pd.DataFrame(data)
    
    # Reorder columns to match the example
    columns = ['Task', 'Sub-task', 'Description', 'Deliverable']
    for role in st.session_state.roles:
        columns.extend([f'{role} Hours', f'{role} Cost'])
    df = df[columns]
    
    # Generate CSV
    csv = df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="siphons_template_output.csv",
        mime="text/csv",
    )

# Display current assignments
st.header('Current Assignments')
for main_task, main_details in st.session_state.tasks.items():
    st.subheader(main_task)
    st.write(f"Description: {main_details['description']}")
    for sub_task, details in main_details['sub_tasks'].items():
        st.write(f"### {sub_task}")
        st.write(f"Description: {details['description']}")
        st.write(f"Deliverable: {details['deliverable']}")
        for role, hours in details['hours'].items():
            if hours > 0:
                st.write(f"{role}: {hours} hours")
        st.write("---")
