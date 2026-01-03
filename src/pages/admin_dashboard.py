import streamlit as st
from src.components.sidebar import render_sidebar
from src.ui.styles import apply_custom_styles
from src.components.auth import require_auth


@require_auth(roles=['admin'])
def main():
    """Main function for the admin dashboard page."""
    # Apply custom styles
    apply_custom_styles()

    # Render sidebar
    render_sidebar()

    # Admin Dashboard page content
    st.title("🔐 Admin Dashboard")

    # Centered card layout
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.container(border=True):
            st.subheader("Admin Actions")

            # Add Commissioner Records button
            if st.button("➕ Add Commissioner Records", use_container_width=True, type="primary"):
                st.session_state.current_page = 'add_commissioner'
                st.rerun()

            st.write("Add new commissioner records to the system")

            st.divider()

            # Add Court Records button
            if st.button("➕ Add Court Records", use_container_width=True, type="primary"):
                st.session_state.current_page = 'add_court'
                st.rerun()

            st.write("Add new court records to the system")


if __name__ == "__main__":
    main()