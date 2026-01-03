import streamlit as st
from src.components.sidebar import render_sidebar
from src.ui.styles import apply_custom_styles


def main():
    """Main function for the home page."""
    # Apply custom styles
    apply_custom_styles()

    # Render sidebar
    render_sidebar()

    # Home page content
    st.title("🏛️ Sindh Archives - Record Management System")
    st.write("Welcome to the Sindh Archives Record Management System")

    # Centered card layout
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.container(border=True):
            st.subheader("Select Record Type")

            # Commissioner Records button
            if st.button("📋 Commissioner Records", use_container_width=True, type="primary"):
                st.session_state.current_page = 'commissioner_records'
                st.rerun()

            st.write("View and search commissioner records")

            st.divider()

            # Court Records button
            if st.button("⚖️ Court Records", use_container_width=True, type="primary"):
                st.session_state.current_page = 'court_records'
                st.rerun()

            st.write("View and search court records")


if __name__ == "__main__":
    main()