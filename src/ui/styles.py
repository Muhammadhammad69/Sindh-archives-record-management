import streamlit as st


def apply_custom_styles():
    """Apply custom CSS styles to the application."""
    st.markdown("""
    <style>
        /* Centered card styling */
        .centered-card {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 300px;
            padding: 2rem;
            margin: 1rem 0;
        }

        /* Button styling */
        .stButton>button {
            width: 100%;
            margin: 0.5rem 0;
        }

        /* Form styling */
        .form-container {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #f8f9fa;
        }

        /* Record count display */
        .record-count {
            font-size: 0.9rem;
            color: #6c757d;
            margin-bottom: 1rem;
        }

        /* Empty state message */
        .empty-state {
            text-align: center;
            padding: 2rem;
            color: #6c757d;
        }

        /* Responsive table */
        .dataframe-container {
            overflow-x: auto;
        }

        /* Success message styling */
        .success-message {
            padding: 0.75rem;
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
            border-radius: 0.375rem;
            margin: 1rem 0;
        }

        /* Error message styling */
        .error-message {
            padding: 0.75rem;
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            border-radius: 0.375rem;
            margin: 1rem 0;
        }

        /* Consistent spacing */
        .section-spacing {
            margin: 1.5rem 0;
        }
    </style>
    """, unsafe_allow_html=True)


def center_element():
    """CSS to center elements using flexbox."""
    st.markdown("""
    <style>
        .center-flex {
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
    """, unsafe_allow_html=True)