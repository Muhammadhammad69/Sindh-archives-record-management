import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables first
load_dotenv()

from src.pages import home, commissioner_records, court_records, admin_login, admin_dashboard, add_commissioner, add_court


def main():
    """Main entry point for the Streamlit application."""
    st.set_page_config(
        page_title="Sindh Archives - Record Management System",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="auto"
    )

    # Initialize session state if not already done
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    
    
    if 'commissioner_form_submitted' not in st.session_state:
        st.session_state.commissioner_form_submitted = False
    
    if 'court_form_submitted' not in st.session_state:
        st.session_state.court_form_submitted = False

    # Route to the appropriate page based on session state
    current_page = st.session_state.get('current_page', 'home')

    if current_page == 'home':
        home.main()
    elif current_page == 'commissioner_records':
        commissioner_records.main()
    elif current_page == 'court_records':
        court_records.main()
    elif current_page == 'admin_login':
        admin_login.main()
    elif current_page == 'admin_dashboard':
        admin_dashboard.main()
    elif current_page == 'add_commissioner':
        add_commissioner.main()
    elif current_page == 'add_court':
        add_court.main()
    else:
        # Default to home if unknown page
        st.session_state.current_page = 'home'
        home.main()


if __name__ == "__main__":
    main()