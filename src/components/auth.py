import streamlit as st
from functools import wraps
from typing import List, Optional


def initialize_session_state():
    """Initialize default session state variables."""
    if 'is_authenticated' not in st.session_state:
        st.session_state.is_authenticated = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'


def is_authenticated() -> bool:
    """Check if user is authenticated."""
    return st.session_state.get('is_authenticated', False)


def is_admin() -> bool:
    """Check if user has admin role."""
    return st.session_state.get('user_role') == 'admin'


def login_user(user_id: int, email: str, role: str):
    """Store user information in session state."""
    st.session_state.is_authenticated = True
    st.session_state.user_id = user_id
    st.session_state.user_email = email
    st.session_state.user_role = role


def logout_user():
    """Clear session state to log out user."""
    st.session_state.is_authenticated = False
    st.session_state.user_id = None
    st.session_state.user_email = None
    st.session_state.user_role = None


def require_auth(roles: Optional[List[str]] = None):
    """
    Decorator to protect pages that require authentication.

    Args:
        roles: List of allowed roles. If None, any authenticated user is allowed.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Initialize session state if not already done
            initialize_session_state()

            # Check if user is authenticated
            if not is_authenticated():
                st.error("Access denied. Please log in.")
                st.session_state.current_page = 'admin_login'
                return None  # Return None to indicate authentication failure

            # Check if user has required role
            if roles and st.session_state.user_role not in roles:
                st.error("Access denied. Insufficient privileges.")
                st.session_state.current_page = 'admin_login'
                return None  # Return None to indicate role failure

            # User is authenticated and has proper role, proceed with the function
            return func(*args, **kwargs)
        return wrapper
    return decorator