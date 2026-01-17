import streamlit as st
import requests
import json
from datetime import datetime, timedelta, timezone

API_URL = "http://api:8000"

if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "show_update_form" not in st.session_state:
    st.session_state.show_update_form = {}

headers = (
    {"Authorization": f"Bearer {st.session_state.token}"}
    if st.session_state.token
    else {}
)

st.sidebar.title("Task Scheduler")
menu = st.sidebar.selectbox("Menu", ["Register", "Login", "Dashboard"])

if menu == "Register":
    st.header("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        try:
            data = {"username": username, "password": password}
            r = requests.post(f"{API_URL}/register", json=data)
            if r.status_code in [200, 201]:
                st.success("Registered successfully! Please login.")
            else:
                st.error(f"Error: {r.text}")
        except Exception as e:
            st.error(f"Failed to register: {e}")

elif menu == "Login":
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            data = {"username": username, "password": password}
            r = requests.post(f"{API_URL}/login", data=data)
            if r.status_code == 200:
                token = r.json().get("access_token")
                st.session_state.token = token
                st.session_state.user = username
                st.success(f"Logged in as {username}")
            else:
                st.error(f"Login failed: {r.text}")
        except Exception as e:
            st.error(f"Failed to login: {e}")

elif menu == "Dashboard":
    if not st.session_state.token:
        st.warning("Please login first to access your tasks!")
    else:
        st.header(f"Welcome, {st.session_state.user}!")

        def fetch_tasks():
            try:
                r = requests.get(f"{API_URL}/tasks", headers=headers)
                if r.status_code == 200:
                    return r.json()
                else:
                    st.error(f"Failed to fetch tasks: {r.text}")
                    return []
            except Exception as e:
                st.error(f"Failed to fetch tasks: {e}")
                return []

        tasks = fetch_tasks()

        st.subheader("Your Tasks")
        if tasks:
            for task in tasks:
                status_color = (
                    "🟢"
                    if task["status"] == "active"
                    else (
                        "🟡"
                        if task["status"] == "paused"
                        else "⚪" if task["status"] == "finished" else "🔴"
                    )
                )
                status_text = task["status"].capitalize()

                next_run = task.get("next_run")
                next_run_display = (
                    next_run if next_run and task["schedule_type"] != "once" else "N/A"
                )

                st.markdown(
                    f"**{task['name']}** {status_color}  _(Status: {status_text})_  |  "
                    f"Next Run: {next_run_display}"
                )

                col_run, col_pause, col_resume, col_delete, col_update, col_runs = (
                    st.columns(6)
                )

                with col_run:
                    if st.button("🔄", key=f"run_{task['id']}"):
                        try:
                            r = requests.post(
                                f"{API_URL}/tasks/{task['id']}/run", headers=headers
                            )
                            st.success(
                                f"Task triggered! Run ID: {r.json().get('task_run_id')}"
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to run task: {e}")

                with col_pause:
                    if st.button("⏸", key=f"pause_{task['id']}"):
                        try:
                            r = requests.patch(
                                f"{API_URL}/tasks/{task['id']}/pause", headers=headers
                            )
                            st.success("Task paused!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to pause task: {e}")

                with col_resume:
                    if st.button("▶️", key=f"resume_{task['id']}"):
                        try:
                            r = requests.patch(
                                f"{API_URL}/tasks/{task['id']}/resume", headers=headers
                            )
                            st.success("Task resumed!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to resume task: {e}")

                with col_delete:
                    if st.button("❌", key=f"delete_{task['id']}"):
                        try:
                            r = requests.delete(
                                f"{API_URL}/tasks/{task['id']}", headers=headers
                            )
                            st.success("Task deleted!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to delete task: {e}")

                with col_update:
                    if st.button("✏️", key=f"update_btn_{task['id']}"):
                        st.session_state.show_update_form[task["id"]] = (
                            not st.session_state.show_update_form.get(task["id"], False)
                        )

                with col_runs:
                    if st.button("📜", key=f"runs_{task['id']}"):
                        try:
                            runs = requests.get(
                                f"{API_URL}/tasks/{task['id']}/runs", headers=headers
                            ).json()
                            if not runs:
                                st.info("No runs yet")
                            else:
                                for run in runs:
                                    run_color = (
                                        "🟢"
                                        if run["status"] == "finished"
                                        else "🟡" if run["status"] == "active" else "🔴"
                                    )
                                    st.markdown(
                                        f"{run_color} Run ID: {run['id']} | Status: {run['status']} | "
                                        f"Started: {run['started_at']} | Finished: {run['finished_at']}"
                                    )
                        except Exception as e:
                            st.error(f"Failed to fetch runs: {e}")

                if st.session_state.show_update_form.get(task["id"]):
                    with st.form(f"update_form_{task['id']}"):
                        new_name = st.text_input("Task Name", value=task["name"])
                        new_description = st.text_area(
                            "Description", value=task["description"]
                        )
                        new_schedule_type = st.selectbox(
                            "Schedule Type",
                            ["once", "interval"],
                            index=0 if task["schedule_type"] == "once" else 1,
                        )
                        new_schedule_value = st.text_input(
                            "Schedule Value", value=task["schedule_value"]
                        )
                        new_payload = st.text_area(
                            "Payload JSON", value=json.dumps(task["payload"])
                        )
                        submitted = st.form_submit_button("Update Task")
                        if submitted:
                            try:
                                payload_dict = json.loads(new_payload)
                                data = {
                                    "name": new_name,
                                    "description": new_description,
                                    "schedule_type": new_schedule_type,
                                    "schedule_value": new_schedule_value,
                                    "payload": payload_dict,
                                }
                                r = requests.patch(
                                    f"{API_URL}/tasks/{task['id']}",
                                    json=data,
                                    headers=headers,
                                )
                                if r.status_code == 200:
                                    st.success("Task updated successfully!")
                                    st.rerun()
                                else:
                                    st.error(f"Failed to update task: {r.text}")
                            except Exception as e:
                                st.error(f"Invalid payload JSON: {e}")

                st.markdown("---")
        else:
            st.info("No tasks yet.")

        st.subheader("Create New Task")
        with st.form("create_task_form"):
            name = st.text_input("Task Name")
            description = st.text_area("Description (optional)")

            schedule_type = st.selectbox("Schedule Type", ["once", "interval"])

            if schedule_type == "once":
                run_date = st.date_input("Run Date")
                run_time = st.time_input("Run Time")
            else:
                interval = st.number_input(
                    "Interval in seconds", min_value=1, step=1, value=3600
                )

            st.markdown("**Email Details**")
            recipient = st.text_input("Recipient Email")
            subject = st.text_input("Email Subject", f"Reminder: {name}")
            message = st.text_area("Message", "")
            max_runs = st.number_input(
                "Max Runs (leave empty for unlimited)", min_value=1, step=1, value=1
            )

            submitted = st.form_submit_button("Create Task")
            if submitted:
                try:
                    if schedule_type == "once":
                        utc_datetime = datetime.combine(run_date, run_time).replace(
                            tzinfo=timezone.utc
                        )
                        if utc_datetime <= datetime.now(timezone.utc):
                            st.error("Scheduled time must be in the future")
                            st.stop()
                        schedule_value = utc_datetime.isoformat()
                    else:
                        schedule_value = str(interval)

                    payload_dict = {
                        "recipient": recipient,
                        "subject": subject,
                        "message": message,
                    }

                    data = {
                        "name": name,
                        "description": description,
                        "schedule_type": schedule_type,
                        "schedule_value": schedule_value,
                        "max_runs": max_runs,
                        "payload": payload_dict,
                    }

                    r = requests.post(f"{API_URL}/tasks", json=data, headers=headers)
                    if r.status_code in [200, 201]:
                        st.success(f"Task '{name}' created successfully!")
                        st.rerun()
                    else:
                        st.error(f"Failed to create task: {r.text}")
                except Exception as e:
                    st.error(f"Failed to create task: {e}")
