# app.py
import streamlit as st
import requests
import pandas as pd

# --- Configuration ---
# This URL should point to your running FastAPI server.
API_URL = "http://127.0.0.1:8000/todos/"

# --- Helper Functions ---
def get_all_todos():
    """Fetch all to-do items from the API."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the API: {e}")
        return []

# --- Streamlit App Layout ---

st.set_page_config(page_title="To-Do App", page_icon="📝", layout="centered")

st.title("My To-Do List App 📝")

# --- Section: Display All To-Dos ---
st.header("Current To-Do Items")

all_todos = get_all_todos()

if all_todos:
    # Convert list of dicts to a pandas DataFrame for better display
    df = pd.DataFrame(all_todos)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No to-do items found. Add one below!")

st.divider()

# --- Section: Create a New To-Do ---
st.header("Create a New To-Do")

# Use a form to group inputs for creating a to-do
with st.form("add_todo_form", clear_on_submit=True):
    new_title = st.text_input("Title", placeholder="e.g., Buy milk")
    submitted = st.form_submit_button("Add To-Do")

    if submitted:
        if not new_title:
            st.warning("Title cannot be empty.")
        else:
            payload = {"title": new_title, "completed": False}
            try:
                response = requests.post(API_URL, json=payload)
                response.raise_for_status()
                st.success("To-Do added successfully!")
                # We don't need to manually refresh; Streamlit's execution model handles it.
                # To be extra explicit and force an immediate re-run: st.rerun()
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to add to-do: {e}")

st.divider()

# --- Section: Find a To-Do by ID ---
st.header("Find a To-Do by ID")

todo_id_to_find = st.number_input("Enter To-Do ID", min_value=1, step=1)

if st.button("Find To-Do"):
    try:
        # Construct the URL for the specific to-do
        response = requests.get(f"{API_URL}{todo_id_to_find}")
        
        if response.status_code == 200:
            st.success("To-Do found!")
            st.json(response.json())
        elif response.status_code == 404:
            st.error("To-Do not found. Please check the ID.")
        else:
            response.raise_for_status() # Handle other potential HTTP errors
            
    except requests.exceptions.RequestException as e:
        st.error(f"Error finding to-do: {e}")