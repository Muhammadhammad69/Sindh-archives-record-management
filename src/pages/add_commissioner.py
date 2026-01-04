import streamlit as st
import pandas as pd
from src.components.sidebar import render_sidebar
from src.ui.styles import apply_custom_styles
from src.components.auth import require_auth
from src.dao.commissioner_dao import CommissionerDAO
from src.components.bulk_upload import BulkUploadHandler
from src.utils.template_generator import generate_commissioner_template


@require_auth(roles=['admin'])
def main():
    """Main function for the add commissioner page."""
    # Apply custom styles
    apply_custom_styles()

    # Render sidebar
    render_sidebar()

    # Add Commissioner page content
    st.title("➕ Add Commissioner Record")

    # Informational message about independent acc_no sequences
    st.info("ℹ️ Note: Accession_no values must be unique within commissioner records, but can be reused in court records (separate numbering sequences)")

    # Mode selection
    mode = st.radio(
        "Select input mode:",
        ["Add Single Record", "Upload Excel File"],
        horizontal=True
    )

    # Initialize DAO
    dao = CommissionerDAO()

    if mode == "Add Single Record":
        # Check if form was submitted successfully
        if st.session_state.get("commissioner_form_submitted", False):
            st.toast("Commissioner record added successfully!", icon="✅")
            # Reset the flag
            st.session_state.commissioner_form_submitted = False

            # Option 1: Use a button to reset the form
            if st.button("Add Another Commissioner Record"):
                st.rerun()
        else:
            # Form for adding commissioner records
            with st.form("add_commissioner_form"):
                st.write("Enter commissioner record details")

                # Create columns for form layout
                col1, col2 = st.columns(2)

                with col1:
                    acc_no = st.number_input("Accession No.", min_value=1, step=1)
                    department = st.text_input("Department")
                    file_no = st.text_input("File No.")
                    subject = st.text_area("Subject")

                with col2:
                    year = st.number_input("Year", step=1)
                    page = st.number_input("Page", min_value=1, step=1)
                    condition = st.selectbox("Condition", ["FAIR/BOUND", "GOOD/BOUND", "POOR/UNBOUND", "EXCELLENT/BOUND"])
                    record_type = st.selectbox("Record Type", ["TEXTUAL RECORD", "PHOTOGRAPHIC RECORD", "DIGITAL RECORD"])

                submitted = st.form_submit_button("Add Commissioner Record", type="primary")

                if submitted:
                    # Validate required fields
                    errors = []
                    if not department.strip():
                        errors.append("Department is required")
                    if not file_no.strip():
                        errors.append("File No. is required")
                    if not subject.strip():
                        errors.append("Subject is required")

                    if errors:
                        for error in errors:
                            st.error(error)
                    else:
                        try:
                            # Check if acc_no already exists in commissioner records
                            if dao.acc_no_exists(int(acc_no)):
                                st.error(f"❌ This Accession_no ({int(acc_no)}) already exists in Commissioner Records. Please use a different Accession_no.")
                                # Preserve form data by not submitting
                                st.stop()
                            else:
                                # Show loading indicator during record creation
                                with st.spinner("Adding commissioner record..."):
                                    # Prepare data for insertion
                                    record_data = {
                                        'acc_no': int(acc_no),
                                        'department': department.strip(),
                                        'file_no': file_no.strip(),
                                        'subject': subject.strip(),
                                        'year': int(year),
                                        'page': int(page),
                                        'condition': condition,
                                        'record_type': record_type
                                    }

                                    # Insert the record
                                    result = dao.create(record_data)

                                if result:
                                    # Set flag to indicate successful submission
                                    st.session_state.commissioner_form_submitted = True
                                    # Show success message by rerunning the page
                                    st.rerun()
                                else:
                                    st.error("Failed to add commissioner record")
                        except Exception as e:
                            st.error(f"Error adding commissioner record: {str(e)}")
    else:  # Upload Excel File mode
        st.info("Upload an Excel file containing multiple commissioner records")

        # Informational message about acc_no validation in bulk upload
        st.info("ℹ️ During bulk upload, the system will check for duplicate Accession_no values in the database and within the uploaded file. Only records with unique Accession_no values will be inserted.")

        # Download template button
        template_data = generate_commissioner_template()
        st.download_button(
            label="Download Commissioner Records Template",
            data=template_data,
            file_name="commissioner_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Initialize bulk upload handler
        bulk_handler = BulkUploadHandler("commissioner")

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
                        file_name="commissioner_validation_errors.csv",
                        mime="text/csv"
                    )
            else:
                # Perform acc_no uniqueness validation for bulk upload
                from src.utils.acc_no_validator import validate_bulk_acc_numbers
                from src.utils.duplicate_detector import generate_skip_report

                with st.spinner("Checking for duplicate Accession_no values..."):
                    validation_results = validate_bulk_acc_numbers(validation_result['data'], 'commissioner')

                # Show validation summary
                summary = validation_results['summary']
                st.subheader("Validation Summary")

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Records", summary['total_records'])
                col2.metric("Valid Records", summary['valid_count'])
                col3.metric("Duplicate in DB", summary['duplicate_count'])
                col4.metric("Internal Duplicates", summary['internal_duplicate_count'])

                # Show details about duplicates if any exist
                if summary['duplicate_count'] > 0 or summary['internal_duplicate_count'] > 0:
                    st.subheader("Duplicate Records Details")

                    if summary['duplicate_count'] > 0:
                        st.error(f"⚠️ Found {summary['duplicate_count']} records with Accession_no values that already exist in the database")
                        duplicate_report = generate_skip_report(validation_results['duplicate_records'], "Duplicate Accession_no in database")
                        if not duplicate_report.empty:
                            st.dataframe(duplicate_report)

                    if summary['internal_duplicate_count'] > 0:
                        st.warning(f"⚠️ Found {summary['internal_duplicate_count']} records with duplicate Accession_no values within the uploaded file")
                        internal_duplicate_report = generate_skip_report(validation_results['internal_duplicates'], "Duplicate Accession_no within upload")
                        if not internal_duplicate_report.empty:
                            st.dataframe(internal_duplicate_report)

                # Show preview of valid records
                if not validation_results['valid_records'].empty:
                    st.subheader("Valid Records to be Inserted")
                    st.info(f"Preview of {min(5, len(validation_results['valid_records']))} records that will be inserted:")
                    st.dataframe(validation_results['valid_records'].head(5))

                    # Show confirmation with counts
                    if st.button("Confirm Bulk Upload", type="primary"):
                        with st.spinner("Processing records..."):
                            results = bulk_handler.bulk_insert(validation_results['valid_records'], dao)

                        # Show results
                        st.success(f"Upload completed! Success: {results['success_count']}, Errors: {results['error_count']}")
                        st.info(f"Successfully inserted {results['success_count']} records. {summary['duplicate_count'] + summary['internal_duplicate_count']} records were skipped due to duplicate Accession_no values.")

                        if results['errors']:
                            st.subheader("Upload Errors")
                            error_df = pd.DataFrame(results['errors'])
                            st.dataframe(error_df)

                            # Provide download button for error report
                            error_csv = error_df.to_csv(index=False)
                            st.download_button(
                                label="Download Error Report",
                                data=error_csv,
                                file_name="commissioner_upload_errors.csv",
                                mime="text/csv"
                            )
                else:
                    st.warning("⚠️ All records have duplicate Accession_no values. No new records to insert.")
                    if summary['duplicate_count'] > 0:
                        st.info("All records have Accession_no values that already exist in the database.")
                    if summary['internal_duplicate_count'] > 0:
                        st.info("All records have duplicate Accession_no values within the uploaded file.")

                    # Provide option to download skipped records list
                    all_skipped = pd.concat([validation_results['duplicate_records'], validation_results['internal_duplicates']], ignore_index=True)
                    if not all_skipped.empty:
                        skip_report = generate_skip_report(all_skipped, "Duplicate Accession_no")
                        csv = skip_report.to_csv(index=False)
                        st.download_button(
                            label="Download Skipped Records List",
                            data=csv,
                            file_name="skipped_commissioner_records.csv",
                            mime="text/csv"
                        )


if __name__ == "__main__":
    main()