import streamlit as st
import pandas as pd
from datetime import datetime
from src.components.sidebar import render_sidebar
from src.dao.court_dao import CourtDAO
from src.ui.styles import apply_custom_styles


def format_date(date_obj):
    """Format date as dd/mm/yyyy."""
    if date_obj is None:
        return ""
    if isinstance(date_obj, str):
        date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
    return date_obj.strftime("%d/%m/%Y")


def main():
    """Main function for the court records page."""
    # Apply custom styles
    apply_custom_styles()

    # Render sidebar
    render_sidebar()

    # Court Records page content
    st.title("🏛️ Court Records")

    # Initialize DAO
    dao = CourtDAO()

    try:
        # Fetch all court records with loading indicator
        with st.spinner("Loading court records..."):
            records = dao.get_all()

        if records:
            # Convert to DataFrame for display

            df = pd.DataFrame(records)

            # Remove internal columns (id, created_at, updated_at) to hide from display
            internal_columns = ['id', 'created_at', 'updated_at']
            df_display = df.drop(columns=[col for col in internal_columns if col in df.columns])

            # Format dates
            if 'date_from' in df_display.columns:
                df_display['date_from'] = df_display['date_from'].apply(format_date)
            if 'date_to' in df_display.columns:
                df_display['date_to'] = df_display['date_to'].apply(format_date)

            # Rename columns for better display
            df_display = df_display.rename(columns={
                'acc_no': 'Accession No.',
                'court': 'Court',
                'suit_no': 'Suit No.',
                'plaintiff': 'Plaintiff',
                'defendant': 'Defendant',
                'claim_or_charge': 'Claim or Charge',
                'date_from': 'Date From',
                'date_to': 'Date To',
                'language': 'Language'
            })

            # Add search/filter functionality
            st.subheader("Search & Filter")

            # Create filter columns
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                acc_no_filter = st.text_input("Filter by Accession No.", "", placeholder="e.g., 456")

            with col2:
                court_filter = st.text_input("Filter by Court", "")

            with col3:
                plaintiff_filter = st.text_input("Filter by Plaintiff", "")

            # with col4:
            #     date_from_filte = st.date_input("Filter by Date From", value=None)

            # Apply filters
            filtered_df = df_display.copy()
            if acc_no_filter:
                filtered_df['acc_no_str'] = filtered_df['Accession No.'].astype(str)
                filtered_df = filtered_df[filtered_df['acc_no_str'].str.contains(acc_no_filter, case=False, na=False)]
                filtered_df = filtered_df.drop(columns=['acc_no_str'])
            if court_filter:
                filtered_df = filtered_df[filtered_df['Court'].str.contains(court_filter, case=False, na=False)]
            if plaintiff_filter:
                filtered_df = filtered_df[filtered_df['Plaintiff'].str.contains(plaintiff_filter, case=False, na=False)]
            # if date_from_filter:
            #     # Convert date to string format for comparison
            #     date_str = date_from_filter.strftime("%d/%m/%Y")
            #     filtered_df = filtered_df[filtered_df['Date From'] == date_str]

            # Display record count
            st.markdown(f"**Total Records: {len(filtered_df)} (showing {len(filtered_df)} after filtering)**")

            # Display the dataframe
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        else:
            # Display empty state message
            st.info("No court records found in the system.")

    except Exception as e:
        st.error(f"Error fetching court records: {str(e)}")


if __name__ == "__main__":
    main()