import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from Netflix_Backend import process_data, get_peak_hours, get_available_profiles,get_monthly_trends,weekly_rythm,streak_finder,seriesvsmovies,mostrewatched,genre,device_dominance,countrydistribution,costperhour
import streamlit as st

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;700&display=swap');

    .stApp { background-color: #000000; color: #ffffff; }

    h1.netflix-title {
        font-family: 'Bebas Neue', sans-serif !important;
        color: #E50914 !important;
        font-size: 8vw !important; 
        text-align: center !important;
        margin-bottom: 0 !important;
        text-shadow: 0 0 40px rgba(229, 9, 20, 0.8) !important;
    }

    .netflix-sub {
        font-family: 'Inter', sans-serif;
        color: #808080;
        text-align: center;
        font-size: 18px;
        letter-spacing: 5px;
        margin-top: 0px !important;
        margin-bottom: 60px !important;
        text-transform: uppercase;
    }
    </style>

    <h1 class="netflix-title">NETFLIX ANALYSED</h1>
    <p class="netflix-sub">You Watched. We Analysed.</p>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

if "selected_profile" not in st.session_state:
    st.session_state.selected_profile = None
if "active_section" not in st.session_state:
    st.session_state.active_section = None

if st.session_state.selected_profile is None:
    uploaded_file = st.file_uploader("Upload your Netflix viewing history CSV", type=["csv"])

    st.markdown("**OR**")
    if st.button("Try with sample data"):
        st.session_state.data = load_data("sample_netflix_data.csv")

    if uploaded_file is not None:
        st.session_state.data = load_data(uploaded_file)

    if "data" in st.session_state:
        data = st.session_state.data
        profiles = get_available_profiles(data)
        chosen = st.selectbox("Choose a profile", options=profiles)

        if st.button("Confirm"):
            st.session_state.selected_profile = chosen
            st.rerun()

else:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Time-Series Analysis"):
            st.session_state.active_section = "time_series"
    with col2:
        if st.button("Content and Genre"):
            st.session_state.active_section = "content"    
    with col3:
        if st.button("Behavioral Insights"):
            st.session_state.active_section="behavior"
    with col4:
        st.button("Recommendations")
    

    # Time-Series Analysis (The "When")
    if st.session_state.active_section == "time_series":
        #1.Peak Viewing Hours: A distribution of watch time across the 24-hour clock
        df_profile = process_data(st.session_state.data, st.session_state.selected_profile)
        peak_hours = get_peak_hours(df_profile)

        st.subheader("Peak Viewing Hours")

        fig, ax = plt.subplots()
        ax.plot(peak_hours['Hour'], peak_hours['count'],marker="o")
        ax.set_xlabel("Hour of Day")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

        #2.Monthly Trends: A bar chart showing total hours watched per month
        monthly_trends=get_monthly_trends(df_profile)
        st.subheader("Monthly Trends")

        fig, ax=plt.subplots()
        ax.bar(monthly_trends['Month'],monthly_trends['Watch Time'])
        ax.set_xlabel("Name of the month")
        ax.set_ylabel("Hours")
        st.pyplot(fig)

        #3.The Weekly Rhythm: Average screen time on weekdays vs weekends
        week_data=weekly_rythm(df_profile)
        week_data["Watch Time"]=week_data["Watch Time"]
        st.subheader("Weekly Rythm")

        fig, ax=plt.subplots()
        ax.pie(week_data["Watch Time"],labels=week_data["Day Type"],autopct="%1.1f%%")
        st.pyplot(fig)

        #4.The "Streak" Finder: Longest consecutive days watched
        st.subheader("Highest Streak")
        result=streak_finder(df_profile)
        st.write(f"Highest streak was recorded for: {result[0]} days from {result[1]} to {result[2]}")

    #Content & Genre Deep-Dives (The "What")
    if st.session_state.active_section == "content":
        df_profile = process_data(st.session_state.data, st.session_state.selected_profile)

        #Series vs. Movies Split: A Pie chart showing the percentage of time spent on episodic content versus feature films.
        st.subheader("Series vs Movies")
        movie_data=seriesvsmovies(df_profile)

        fig,ax=plt.subplots()
        ax.pie(movie_data["count"],labels=movie_data["Title"],autopct="%1.1f%%")
        st.pyplot(fig)

        #The "Rewatch" Leaderboard: Identifying which specific title appears most frequently in your logs (your true "comfort" show).
        st.subheader("Most Rewatched")
        result=mostrewatched(df_profile)
        st.write(f"Your most rewatched series is: {result[0]}")
        st.write(f"Your most rewatched movies is: {result[1]}")

        #Genre Tagging: (Requires a mapping logic) Categorizing shows into "Thriller," "Romance," "Sci-Fi," etc.
        st.subheader("Genre Distribution")
        genre_data=genre(df_profile)

        fig,ax=plt.subplots()
        ax.bar(genre_data["genre"],genre_data["count"])
        ax.set_xlabel("Genre")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    #Behavioral & Device Insights (The "How")
    if st.session_state.active_section =="behavior":
        df_profile = process_data(st.session_state.data, st.session_state.selected_profile)
        #1.Device Dominance: Which device gets the most "Screen Time" (Smart TV, Phone, or Laptop)?
        st.subheader("Device Dominance")
        result=device_dominance(df_profile)

        fig,ax=plt.subplots()
        ax.bar(result["Device Type"],result["Watch Time"])
        ax.set_xlabel("Device Name")
        ax.set_ylabel("Hours Spent")
        st.pyplot(fig)
        
        #2.The "Bollywood Scale": Percentage of Indian vs. International content (to trigger that "Bollywood Paglu" title).
        st.subheader("Desi vs Videsi Split")
        result=countrydistribution(df_profile)

        fig,ax=plt.subplots()
        ax.pie(result[0]["count"],labels=result[0]["Country"],autopct="%1.1f%%")
        if result[1]==True: st.write("You are a Bollywood Paglu!!")
        st.pyplot(fig)

        #3.The "Cost Per Hour" (Optional): If you input your monthly subscription fee, we can calculate exactly how much each hour of entertainment "cost" you
        st.subheader("Cost Per Hour")
        subscription_fee = st.number_input("Enter your monthly subscription fee in INR", min_value=0)
        options = ["01","02","03","04","05","06","07","08","09","10","11","12"]
        month_no = st.selectbox("Choose the month", options)
        result=costperhour(df_profile,subscription_fee,int(month_no))
        if result is None:
            st.write("No viewing data available for this month.")
        else:
            st.write(f"You paid ₹{result} for each hour")