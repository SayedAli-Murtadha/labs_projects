import streamlit as st
import pandas as pd
import weather_logic as wl 

# PAGE SETUP & CSS 
st.set_page_config(page_title="Weather Tracker", layout="wide")

# Inject Custom CSS 
st.markdown("""
    <style>
        /* 1. Custom Button Styling with Smoother Animations */
        div.stButton > button {
            background-color: #2E86C1;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 24px;
            font-weight: bold;
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        
        div.stButton > button:hover {
            background-color: #1B4F72;
            box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.2);
            color: white;
            transform: translateY(-2px); /* Adds a smooth "lift" effect */
        }
        
        div.stButton > button:active {
            transform: translateY(1px); /* Pushes down slightly when clicked */
        }

        /* 2. Container & Form Hover Animations (Cards) */
        div[data-testid="stForm"], 
        div[data-testid="stVerticalBlockBorderWrapper"] {
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        
        div[data-testid="stForm"]:hover, 
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-3px);
            box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.08);
            border-color: #2E86C1; /* Highlights the border slightly on hover */
        }

        /* 3. Style the Metrics */
        div[data-testid="stMetricValue"] {
            font-size: 2rem;
            color: #2E86C1;
        }

        /* 4. Custom Sidebar fixing the invisible text issue */
        [data-testid="stSidebar"] {
            background-color: #F8F9F9 !important;
        }
        
        /* Force text colors in the sidebar to be dark so they don't vanish in dark mode */
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] span, 
        [data-testid="stSidebar"] label, 
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: #2C3E50 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title(" Weather Tracker Dashboard")
st.markdown("---")

# Initialize the CSV data on load
wl.initialize_data()

# SIDEBAR NAVIGATION 
# Using a dictionary to map pretty labels to your original choices
menu_options = {
    " Record Observation": "Record a new observation",
    " Weather Statistics": "View weather statistics",
    " Search by Date": "Search observations by date",
    " View All Records": "View all observations",
    " Record-Breaking Outliers": "View Record-Breaking Temperatures"
}

st.sidebar.title(" Navigation")
# The radio button displays the keys (pretty labels), but we pass the original string logic below
choice_label = st.sidebar.radio("Go to:", list(menu_options.keys()))
choice = menu_options[choice_label]

st.sidebar.markdown("---")
st.sidebar.info("Track, analyze, and manage weather data easily.")


# 1. RECORD OBSERVATION 
if choice == "Record a new observation":
    st.subheader(" Record a New Weather Observation")
    
    # Using a form to group inputs visually and prevent accidental mid-typing saves
    with st.form("record_weather_form", border=True):
        col1, col2 = st.columns(2)
        with col1:
            obs_date = st.date_input(" Date of Observation")
            temp = st.number_input( "Temperature (°C)", value=30.0, step=0.1)
            condition = st.selectbox(" Weather Condition", ['Sunny', 'Cloudy', 'Rainy', 'Snowy'])
        with col2:
            humidity = st.number_input(" Humidity (%)", min_value=1, max_value=100, value=50)
            wind_speed = st.number_input(" Wind Speed (km/h)", min_value=0.0, value=10.0, step=0.5)

        # Submit button for the form
        submitted = st.form_submit_button(" Save Observation")
        
        if submitted:
            wl.save_observation(obs_date, temp, condition, humidity, wind_speed)
            st.success(" Observation Data successfully saved!")

#  2. VIEW STATISTICS 
elif choice == "View weather statistics":
    st.subheader("Weather Statistics & Analysis")
    df = wl.get_all_data()
    
    if df.empty:
        st.warning("No data available.")
    else:
        df['Date'] = pd.to_datetime(df['Date'], format="%m-%d-%Y")
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        
        # Filter Card
        with st.container(border=True):
            st.markdown("####  Filter Options")
            col1, col2 = st.columns(2)
            with col1:
                filter_month = st.selectbox(" Filter by Month", ["All"] + list(range(1, 13)))
            with col2:
                available_years = sorted(df['Year'].dropna().unique())
                compare_year = st.selectbox("Compare Year against previous", ["None"] + available_years)

        # Apply logic filtering
        if filter_month != "All":
            df = df[df['Month'] == filter_month]
            
        if not df.empty:
            # Metrics Card
            with st.container(border=True):
                st.markdown("####  Current Filtered Summary")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Average Temp", f"{df['Temperature'].mean():.1f}°C")
                m2.metric("Max Temp", f"{df['Temperature'].max():.1f}°C")
                m3.metric("Min Temp", f"{df['Temperature'].min():.1f}°C")
                
                common_cond = df['Conditions'].mode()[0] if not df['Conditions'].mode().empty else "N/A"
                m4.metric("Common Condition", common_cond)

        if compare_year != "None":
            with st.container(border=True):
                st.markdown(f"####  Temperature Comparison: {compare_year} vs Previous")
                compare_df = df[df['Year'] <= compare_year].copy()
                compare_df['Period'] = compare_df['Year'].apply(lambda y: f"{compare_year}" if y == compare_year else "Previous Years")
                stats_table = compare_df.groupby('Period')['Temperature'].agg(['mean', 'max', 'min']).round(2)
                st.dataframe(stats_table, use_container_width=True)

#  3. SEARCH BY DATE 
elif choice == "Search observations by date":
    st.subheader(" Search Observations")
    
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            search_date = st.date_input("Select a date to search for:")
        with col2:
            st.write("") # spacing
            st.write("") # spacing
            search_btn = st.button(" Search Database", use_container_width=True)
    
    if search_btn:
        results = wl.search_by_date_logic(search_date)
        if results:
            st.success(f"Found observations for **{search_date}**")
            
            # Display results beautifully in mini-cards instead of plain text
            for r in results:
                with st.container(border=True):
                    c1, c2, c3, c4 = st.columns(4)
                    c1.markdown(f"** Condition**\n\n{r['Conditions']}")
                    c2.markdown(f"** Temp**\n\n{r['Temperature']}°C")
                    c3.markdown(f"** Humidity**\n\n{r['Humidity']}%")
                    c4.markdown(f"** Wind**\n\n{r['Wind_Speed']} km/h")
        else:
            st.error(f"No observation found for the date: {search_date}")

#  4. VIEW ALL & DELETE 
elif choice == "View all observations":
    st.subheader(" All Weather Observations")
    df = wl.get_all_data()
    
    if df.empty:
        st.warning("No data available. Please record an observation first.")
    else:
        # Display the data nicely
        st.dataframe(df, use_container_width=True, hide_index=False)
        
        # Hide the delete function inside an expander so it doesn't look cluttered
        st.markdown("---")
        with st.expander(" Danger Zone: Remove an Observation"):
            st.warning("Deleting a record cannot be undone.")
            col1, col2 = st.columns([2, 1])
            with col1:
                remove_index = st.number_input("Enter the Index number to remove", min_value=0, max_value=df.index.max(), step=1)
            with col2:
                st.write("")
                st.write("")
                if st.button("Delete Selected Record", type="primary", use_container_width=True):
                    success = wl.delete_observation(remove_index)
                    if success:
                        st.success("Observation data has been removed! Refreshing...")
                        st.rerun()
                    else:
                        st.error("Invalid index.")

#  5. RECORD BREAKING 
elif choice == "View Record-Breaking Temperatures":
    st.subheader(" Record-Breaking Temperatures (Outliers)")
    outliers = wl.get_record_breaking()
    
    if outliers.empty:
        st.info(" There are no temperature outliers in the current data!")
    else:
        st.error(" Found Record-Breaking Outliers:")
        # Display outliers with slightly different UI styling
        with st.container(border=True):
            st.dataframe(outliers, use_container_width=True)