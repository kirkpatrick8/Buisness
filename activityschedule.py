import streamlit as st
import pandas as pd
from streamlit_dragndrop import st_dragndrop

# Initialize session state
if 'templates' not in st.session_state:
    st.session_state.templates = {
        'Siphons Template': {
            'roles': {
                'AECOM Technical Head': {'name': '', 'fee': 0.0},
                'Hydraulics Specialist - Major Conveyance': {'name': '', 'fee': 0.0},
                'Role 2 Technical Director Civil': {'name': '', 'fee': 0.0},
                'Role 3 Framework Manager': {'name': '', 'fee': 0.0},
                'Role 4 Principal Engineer / PM Wastewater Infra': {'name': '', 'fee': 0.0},
            },
            'tasks': {
                'General Project Management Duties': {
                    'description': 'General aspects of multidisciplinary project management',
                    'sub_tasks': {
                        'General project management': {
                            'description': 'General aspects of multidisciplinary project management, as required.',
                            'deliverable': 'Various - none defined per se',
                            'hours': {}
                        },
                        'Project execution plan': {
                            'description': 'Provide and regularly update a Project Execution Plan.',
                            'deliverable': 'Project execution plan',
                            'hours': {}
                        },
                    }
                }
            }
        },
        'Custom Template': {
            'roles': {},
            'tasks': {}
        }
    }

if 'current_template' not in st.session_state:
    st.session_state.current_template = 'Siphons Template'

# Streamlit app
st.title('Advanced Siphons Template Filler')

# Sidebar for template selection and management
with st.sidebar:
    st.header("Template Management")
    st.session_state.current_template = st.selectbox("Select Template", options=list(st.session_state.templates.keys()))
    
    new_template = st.text_input("Add new template")
    if st.button("Add Template"):
        if new_template and new_template not in st.session_state.templates:
            st.session_state.templates[new_template] = {'roles': {}, 'tasks': {}}
            st.success(f"Added template: {new_template}")
    
    if st.button("Delete Current Template"):
        if st.session_state.current_template != 'Siphons Template':
            del st.session_state.templates[st.session_state.current_template]
            st.session_state.current_template = 'Siphons Template'
            st.success(f"Deleted template: {st.session_state.current_template}")
        else:
            st.error("Cannot delete the default Siphons Template")

# Main dashboard
st.header("Dashboard")
tab1, tab2, tab3 = st.tabs(["Roles", "Tasks", "Assignment"])

with tab1:
    st.subheader("Role Management")
    
    # Drag and drop for roles
    roles = list(st.session_state.templates[st.session_state.current_template]['roles'].keys())
    updated_roles = st_dragndrop(roles, key="roles")
    
    if updated_roles != roles:
        st.session_state.templates[st.session_state.current_template]['roles'] = {role: st.session_state.templates[st.session_state.current_template]['roles'][role] for role in updated_roles}
    
    new_role = st.text_input("Add new role")
    if st.button("Add Role"):
        if new_role and new_role not in st.session_state.templates[st.session_state.current_template]['roles']:
            st.session_state.templates[st.session_state.current_template]['roles'][new_role] = {'name': '', 'fee': 0.0}
            st.success(f"Added role: {new_role}")
    
    role_to_delete = st.selectbox("Select role to delete", options=list(st.session_state.templates[st.session_state.current_template]['roles'].keys()))
    if st.button("Delete Role"):
        del st.session_state.templates[st.session_state.current_template]['roles'][role_to_delete]
        st.success(f"Deleted role: {role_to_delete}")

with tab2:
    st.subheader("Task Management")
    
    # Drag and drop for main tasks
    main_tasks = list(st.session_state.templates[st.session_state.current_template]['tasks'].keys())
    updated_main_tasks = st_dragndrop(main_tasks, key="main_tasks")
    
    if updated_main_tasks != main_tasks:
        st.session_state.templates[st.session_state.current_template]['tasks'] = {task: st.session_state.templates[st.session_state.current_template]['tasks'][task] for task in updated_main_tasks}
    
    new_main_task = st.text_input("Add new main task")
    if st.button("Add Main Task"):
        if new_main_task and new_main_task not in st.session_state.templates[st.session_state.current_template]['tasks']:
            st.session_state.templates[st.session_state.current_template]['tasks'][new_main_task] = {
                'description': '',
                'sub_tasks': {}
            }
            st.success(f"Added main task: {new_main_task}")
    
    main_task_to_delete = st.selectbox("Select main task to delete", options=list(st.session_state.templates[st.session_state.current_template]['tasks'].keys()))
    if st.button("Delete Main Task"):
        del st.session_state.templates[st.session_state.current_template]['tasks'][main_task_to_delete]
        st.success(f"Deleted main task: {main_task_to_delete}")
    
    st.subheader("Sub-task Management")
    main_task_for_subtask = st.selectbox("Select main task for sub-task", options=list(st.session_state.templates[st.session_state.current_template]['tasks'].keys()))
    
    # Drag and drop for sub-tasks
    sub_tasks = list(st.session_state.templates[st.session_state.current_template]['tasks'][main_task_for_subtask]['sub_tasks'].keys())
    updated_sub_tasks = st_dragndrop(sub_tasks, key="sub_tasks")
    
    if updated_sub_tasks != sub_tasks:
        st.session_state.templates[st.session_state.current_template]['tasks'][main_task_for_subtask]['sub_tasks'] = {
            task: st.session_state.templates[st.session_state.current_template]['tasks'][main_task_for_subtask]['sub_tasks'][task] for task in updated_sub_tasks
        }
    
    new_sub_task = st.text_input("Add new sub-task")
    if st.button("Add Sub-task"):
        if new_sub_task and new_sub_task not in st.session_state.templates[st.session_state.current_template]['tasks'][main_task_for_subtask]['sub_tasks']:
            st.session_state.templates[st.session_state.current_template]['tasks'][main_task_for_subtask]['sub_tasks'][new_sub_task] = {
                'description': '',
                'deliverable': '',
                'hours': {role: 0 for role in st.session_state.templates[st.session_state.current_template]['roles']}
            }
            st.success(f"Added sub-task: {new_sub_task} to {main_task_for_subtask}")
    
    sub_task_to_delete = st.selectbox("Select sub-task to delete", options=list(st.session_state.templates[st.session_state.current_template]['tasks'][main_task_for_subtask]['sub_tasks'].keys()))
    if st.button("Delete Sub-task"):
        del st.session_state.templates[st.session_state.current_template]['tasks'][main_task_for_subtask]['sub_tasks'][sub_task_to_delete]
        st.success(f"Deleted sub-task: {sub_task_to_delete} from {main_task_for_subtask}")

with tab3:
    st.subheader('Role Assignment and Fee Input')
    for role in st.session_state.templates[st.session_state.current_template]['roles']:
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.templates[st.session_state.current_template]['roles'][role]['name'] = st.text_input(f'Assign name to {role}', key=f"name_{role}")
        with col2:
            st.session_state.templates[st.session_state.current_template]['roles'][role]['fee'] = st.number_input(f'Fee for {role} (£/hr)', min_value=0.0, step=0.1, key=f"fee_{role}")

    st.subheader('Task and Hours Assignment')
    for main_task, main_details in st.session_state.templates[st.session_state.current_template]['tasks'].items():
        st.write(f"## {main_task}")
        main_details['description'] = st.text_area(f"Description for {main_task}", value=main_details['description'])
        for sub_task, details in main_details['sub_tasks'].items():
            st.write(f"### {sub_task}")
            details['description'] = st.text_area(f"Description for {sub_task}", value=details['description'])
            details['deliverable'] = st.text_input(f"Deliverable for {sub_task}", value=details['deliverable'])
            for role in st.session_state.templates[st.session_state.current_template]['roles']:
                details['hours'][role] = st.number_input(f'Hours for {role}', min_value=0, step=1, key=f"{main_task}_{sub_task}_{role}")

# Generate CSV
if st.button('Generate CSV'):
    data = []
    total_hours = {role: 0 for role in st.session_state.templates[st.session_state.current_template]['roles']}
    total_cost = {role: 0 for role in st.session_state.templates[st.session_state.current_template]['roles']}
    
    for main_task, main_details in st.session_state.templates[st.session_state.current_template]['tasks'].items():
        for sub_task, details in main_details['sub_tasks'].items():
            row = {
                'Task': main_task,
                'Sub-task': sub_task,
                'Description': details['description'],
                'Deliverable': details['deliverable'],
            }
            for role in st.session_state.templates[st.session_state.current_template]['roles']:
                hours = details['hours'].get(role, 0)
                fee = st.session_state.templates[st.session_state.current_template]['roles'][role]['fee']
                row[f'{role} Hours'] = hours
                row[f'{role} Cost'] = hours * fee
                total_hours[role] += hours
                total_cost[role] += hours * fee
            data.append(row)
    
    # Add total row
    total_row = {'Task': 'Total', 'Sub-task': '', 'Description': '', 'Deliverable': ''}
    for role in st.session_state.templates[st.session_state.current_template]['roles']:
        total_row[f'{role} Hours'] = total_hours[role]
        total_row[f'{role} Cost'] = total_cost[role]
    data.append(total_row)
    
    df = pd.DataFrame(data)
    
    # Reorder columns to match the example
    columns = ['Task', 'Sub-task', 'Description', 'Deliverable']
    for role in st.session_state.templates[st.session_state.current_template]['roles']:
        columns.extend([f'{role} Hours', f'{role} Cost'])
    df = df[columns]
    
    # Generate CSV
    csv = df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{st.session_state.current_template}_output.csv",
        mime="text/csv",
    )

# Display current assignments
st.header('Current Assignments')
for main_task, main_details in st.session_state.templates[st.session_state.current_template]['tasks'].items():
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
