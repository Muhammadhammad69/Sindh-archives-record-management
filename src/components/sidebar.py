import streamlit as st
from .auth import is_authenticated, is_admin, logout_user


def render_sidebar():
    """Render the persistent sidebar navigation."""
    with st.sidebar:
        st.title("🏛️ Sindh Archives")

        # Home link
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = 'home'
            st.rerun()

        st.divider()

        # Public links (always visible)
        if st.button("📋 Commissioner Records", use_container_width=True):
            st.session_state.current_page = 'commissioner_records'
            st.rerun()

        if st.button("⚖️ Court Records", use_container_width=True):
            st.session_state.current_page = 'court_records'
            st.rerun()

        st.divider()

        # Admin link (conditionally visible)
        if is_authenticated() and is_admin():
            if st.button("🔐 Admin Dashboard", use_container_width=True):
                st.session_state.current_page = 'admin_dashboard'
                st.rerun()

            if st.button("➕ Add Commissioner Records", use_container_width=True):
                st.session_state.current_page = 'add_commissioner'
                st.rerun()

            if st.button("➕ Add Court Records", use_container_width=True):
                st.session_state.current_page = 'add_court'
                st.rerun()

        # Admin login/logout (conditionally visible)
        if is_authenticated():
            st.write(f"👤 {st.session_state.user_email}")
            if st.button("🚪 Logout", use_container_width=True):
                logout_user()
                st.session_state.current_page = 'home'
                st.rerun()
        else:
            if st.button("🔐 Admin Login", use_container_width=True):
                st.session_state.current_page = 'admin_login'
                st.rerun()