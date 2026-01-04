import streamlit as st
import pandas as pd

from datetime import datetime, date
from src.components.sidebar import render_sidebar
from src.ui.styles import apply_custom_styles
from src.components.auth import require_auth
from src.dao.court_dao import CourtDAO
from src.components.bulk_upload import BulkUploadHandler
from src.utils.template_generator import generate_court_template


@require_auth(roles=['admin'])
def main():
    """Main function for the add court page."""
    # Apply custom styles
    apply_custom_styles()

    # Render sidebar
    render_sidebar()

    # Add Court page content
    st.title("➕ Add Court Record")

    # Mode selection
    mode = st.radio(
        "Select input mode:",
        ["Add Single Record", "Upload Excel File"],
        horizontal=True
    )

    # Initialize DAO
    dao = CourtDAO()

    if mode == "Add Single Record":
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
                    date_from = st.date_input("Date From", min_value=date(1100,1,1), max_value=date(2036,12,31))
                    date_to = st.date_input("Date To", min_value=date(1100,1,1))
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
    else:  # Upload Excel File mode
        st.info("Upload an Excel file containing multiple court records")

        # Download template button
        template_data = generate_court_template()
        st.download_button(
            label="Download Court Records Template",
            data=template_data,
            file_name="court_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Initialize bulk upload handler
        bulk_handler = BulkUploadHandler("court")

        # Upload file
        uploaded_file = bulk_handler.upload_file()

        if uploaded_file is not None:
            # Validate file
            with st.spinner("Validating Excel file..."):
                validation_result = bulk_handler.validate_file(uploaded_file)

            if not validation_result['valid']:
                # Show validation errors
                if validation_result['column_errors']:
                    for error in validation_result['column_errors']:
                        st.error(error)

                if validation_result['data_errors']:
                    st.subheader("Data Validation Errors")
                    error_df = pd.DataFrame(validation_result['data_errors'])
                    st.dataframe(error_df)

                    # Provide download button for error report
                    error_csv = error_df.to_csv(index=False)
                    st.download_button(
                        label="Download Error Report",
                        data=error_csv,
                        file_name="court_validation_errors.csv",
                        mime="text/csv"
                    )
            else:
                # Show preview
                bulk_handler.preview_data(validation_result['data'])

                # Show confirmation
                if st.button("Confirm Bulk Upload", type="primary"):
                    with st.spinner("Processing records..."):
                        results = bulk_handler.bulk_insert(validation_result['data'], dao)

                    # Show results
                    st.success(f"Upload completed! Success: {results['success_count']}, Errors: {results['error_count']}")

                    if results['errors']:
                        st.subheader("Upload Errors")
                        error_df = pd.DataFrame(results['errors'])
                        st.dataframe(error_df)

                        # Provide download button for error report
                        error_csv = error_df.to_csv(index=False)
                        st.download_button(
                            label="Download Error Report",
                            data=error_csv,
                            file_name="court_upload_errors.csv",
                            mime="text/csv"
                        )


if __name__ == "__main__":
    main()