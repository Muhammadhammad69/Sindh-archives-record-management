import streamlit as st
from src.components.sidebar import render_sidebar
from src.ui.styles import apply_custom_styles
from src.dao.user_dao import UserDAO
from src.security.password_utils import verify_password
from src.components.auth import login_user


def main():
    """Main function for the admin login page."""
    # Apply custom styles
    apply_custom_styles()

    # Render sidebar
    render_sidebar()

    # Admin Login page content
    st.title("🔐 Admin Login")

    # Initialize DAO
    users_dao = UserDAO()

    # Login form
    with st.form("login_form"):
        st.write("Please enter your admin credentials")

        email = st.text_input("Email", key="email")
        password = st.text_input("Password", type="password", key="password")

        submitted = st.form_submit_button("Login", type="primary")

        if submitted:
            if email and password:
                try:
                    # Show loading indicator during authentication
                    with st.spinner("Authenticating..."):
                        # Fetch user by email
                        user = users_dao.get_by_email(email)

                        if user:
                            # Verify password using existing utility
                            if verify_password(password, user.password):
                                # Check if user has admin role
                                if user.role == 'admin':
                                    # Login the user
                                    login_user(user.id, user.email, user.role)
                                    st.session_state.current_page = 'admin_dashboard'
                                    st.rerun()
                                else:
                                    st.error("Access denied. Admin privileges required.")
                            else:
                                st.error("Invalid email or password")
                        else:
                            st.error("Invalid email or password")
                except Exception as e:
                    st.error(f"Error during authentication: {str(e)}")
            else:
                st.error("Please enter both email and password")


if __name__ == "__main__":
    main()