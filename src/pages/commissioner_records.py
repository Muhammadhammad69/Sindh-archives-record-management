import streamlit as st
import pandas as pd
from src.components.sidebar import render_sidebar
from src.dao.commissioner_dao import CommissionerDAO
from src.ui.styles import apply_custom_styles


def main():
    """Main function for the commissioner records page."""
    # Apply custom styles
    apply_custom_styles()

    # Render sidebar
    render_sidebar()

    # Commissioner Records page content
    st.title("🏛️ Commissioner Records")

    # Initialize DAO
    dao = CommissionerDAO()

    try:
        # Fetch all commissioner records with loading indicator
        with st.spinner("Loading commissioner records..."):
            records = dao.get_all()

        if records:
            # Convert to DataFrame for display
            df = pd.DataFrame(records)

            # Rename columns for better display
            df = df.rename(columns={
                'acc_no': 'Account No.',
                'department': 'Department',
                'file_no': 'File No.',
                'subject': 'Subject',
                'year': 'Year',
                'page': 'Page',
                'condition': 'Condition',
                'record_type': 'Record Type'
            })

            # Add search/filter functionality
            st.subheader("Search & Filter")

            # Create filter columns
            col1, col2, col3 = st.columns(3)

            with col1:
                department_filter = st.text_input("Filter by Department", "")

            with col2:
                year_filter = st.number_input("Filter by Year", min_value=0, max_value=9999, value=0, format="%d")

            with col3:
                condition_filter = st.selectbox("Filter by Condition", ["All"] + list(df['Condition'].unique()) if 'Condition' in df.columns else ["All"])

            # Apply filters
            filtered_df = df.copy()
            if department_filter:
                filtered_df = filtered_df[filtered_df['Department'].str.contains(department_filter, case=False, na=False)]
            if year_filter > 0:
                filtered_df = filtered_df[filtered_df['Year'] == year_filter]
            if condition_filter != "All":
                filtered_df = filtered_df[filtered_df['Condition'] == condition_filter]

            # Display record count
            st.markdown(f"**Total Records: {len(filtered_df)} (showing {len(filtered_df)} after filtering)**")

            # Display the dataframe
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        else:
            # Display empty state message
            st.info("No commissioner records found in the system.")

    except Exception as e:
        st.error(f"Error fetching commissioner records: {str(e)}")


if __name__ == "__main__":
    main()