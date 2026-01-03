import streamlit as st
from datetime import datetime
from src.components.sidebar import render_sidebar
from src.ui.styles import apply_custom_styles
from src.components.auth import require_auth
from src.dao.court_dao import CourtDAO


@require_auth(roles=['admin'])
def main():
    """Main function for the add court page."""
    # Apply custom styles
    apply_custom_styles()

    # Render sidebar
    render_sidebar()

    # Add Court page content
    st.title("➕ Add Court Record")

    # Initialize DAO
    dao = CourtDAO()

    # Check if form was submitted successfully
    if st.session_state.get("court_form_submitted", False):
        st.toast("Court record added successfully!", icon="✅")
        # Reset the flag
        st.session_state.court_form_submitted = False

        # Option 1: Use a button to reset the form
        if st.button("Add Another Court Record"):
            st.rerun()
    else:
        # Form for adding court records
        with st.form("add_court_form"):
            st.write("Enter court record details")

            # Create columns for form layout
            col1, col2 = st.columns(2)

            with col1:
                acc_no = st.number_input("Account No.", min_value=1, step=1)
                court = st.text_input("Court")
                suit_no = st.text_input("Suit No.")
                plaintiff = st.text_input("Plaintiff")
                defendant = st.text_input("Defendant")

            with col2:
                claim_or_charge = st.text_area("Claim or Charge")
                date_from = st.date_input("Date From")
                date_to = st.date_input("Date To")
                language = st.text_input("Language", help="Example: English, Hindi")

            submitted = st.form_submit_button("Add Court Record", type="primary")

            if submitted:
                # Validate required fields
                errors = []
                if not court.strip():
                    errors.append("Court is required")
                if not suit_no.strip():
                    errors.append("Suit No. is required")
                if not plaintiff.strip():
                    errors.append("Plaintiff is required")
                if not defendant.strip():
                    errors.append("Defendant is required")
                if not claim_or_charge.strip():
                    errors.append("Claim or Charge is required")
                if not language.strip():
                    errors.append("Language is required")

                # Validate date range
                if date_from and date_to:
                    if date_to < date_from:
                        errors.append("Date To must be after Date From")

                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    try:
                        # Show loading indicator during record creation
                        with st.spinner("Adding court record..."):
                            # Prepare data for insertion
                            record_data = {
                                'acc_no': int(acc_no),
                                'court': court.strip(),
                                'suit_no': suit_no.strip(),
                                'plaintiff': plaintiff.strip(),
                                'defendant': defendant.strip(),
                                'claim_or_charge': claim_or_charge.strip(),
                                'date_from': date_from.strftime('%Y-%m-%d') if date_from else None,
                                'date_to': date_to.strftime('%Y-%m-%d') if date_to else None,
                                'language': language.strip()
                            }

                            # Insert the record
                            result = dao.create(record_data)

                        if result:
                            # Set flag to indicate successful submission
                            st.session_state.court_form_submitted = True
                            # Show success message by rerunning the page
                            st.rerun()
                        else:
                            st.error("Failed to add court record")
                    except Exception as e:
                        st.error(f"Error adding court record: {str(e)}")


if __name__ == "__main__":
    main()