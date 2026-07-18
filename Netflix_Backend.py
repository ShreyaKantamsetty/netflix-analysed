import pandas as pd

def process_data(df, profile_name):
    df = df.copy()
    df[['S_Date', 'S_Time']] = df['Start Time'].str.split(" ", n=1, expand=True)
    df_profile = df[df['Profile Name'] == profile_name].copy()
    return df_profile

def get_peak_hours(df_profile):
    df_profile['Hour'] = df_profile['S_Time'].str.split(":", expand=True)[0]
    peak_hours = df_profile['Hour'].value_counts().sort_index().reset_index()
    return peak_hours

def get_available_profiles(df):
    return sorted(df["Profile Name"].dropna().unique().tolist())

def get_monthly_trends(df_profile):
    df_profile["Month"]=df_profile["S_Date"].str.split("-",expand=True)[1]
    month_map = {"01": "Jan","02": "Feb","03": "Mar","04": "Apr","05": "May","06": "Jun","07": "July","08": "Aug","09": "Sept","10": "Oct","11": "Nov","12": "Dec"}
    df_profile["Watch Time"]=pd.to_timedelta(df_profile["Duration"]).dt.total_seconds()/3600
    monthly_trends=df_profile.groupby("Month")["Watch Time"].sum().reset_index()
    monthly_trends["Month"]=monthly_trends["Month"].map(month_map)
    return monthly_trends

def weekly_rythm(df_profile):
    df_profile["Watch Time"]=pd.to_timedelta(df_profile["Duration"]).dt.total_seconds()/3600
    df_profile["Day Type"]=pd.to_datetime(df_profile["S_Date"]).dt.weekday.map(lambda d:"Weekday" if d<5 else "Weekend")
    week_data=df_profile.groupby("Day Type")["Watch Time"].sum().reset_index()
    return week_data

def streak_finder(df):
    dates = pd.to_datetime(df['S_Date'].dropna().unique()).sort_values()

    # 2. Loop through and count
    max_streak = 0
    current_streak = 1
    current_start = dates[0]
    best_start = dates[0]
    best_end = dates[0]

    for i in range(len(dates)):
        # Check if this date is 1 day after the previous one
        if i>0 and ((dates[i]-dates[i-1])==pd.Timedelta(days=1)):
            current_streak+=1
        else:
        #streak broke check if thiswas the best steak
            if(current_streak>max_streak):
                max_streak=current_streak
                best_start=current_start
                best_end=dates[i-1]
            current_streak=1
            current_start=dates[i]
    result=[max_streak,best_start.date(),best_end.date()]
    return result

def seriesvsmovies(df):
    movie_series_data=df["Title"].str.contains(r"S\d:",regex=True).map({True:"Series",False:"Movies"}).value_counts().reset_index()
    return movie_series_data

def mostrewatched(df):
    def watchname(title):
        if "Episode" in title:  
            return title.split(":")[0]
        else:
            return title
    df["watch name"]=df["Title"].apply(watchname)
    result_series=df[df["Title"].str.contains("Episode")]["watch name"].value_counts().idxmax()
    result_movies=df[~(df["Title"].str.contains("Episode"))]["watch name"].value_counts().idxmax()
    return result_series,result_movies

def genre(df):
    genre_map = {
    # Series
    'Crash Landing on You': 'Romance',
    'Mirzapur': 'Crime',
    'Money Heist': 'Thriller',
    'Stranger Things': 'Sci-Fi',
    
    # Movies
    'Avengers: Endgame': 'Action',
    'Dangal': 'Sports',
    'Inception': 'Sci-Fi',
    'Interstellar': 'Sci-Fi',
    'Kabir Singh': 'Romance',
    'Parasite': 'Thriller',
    'Pathaan': 'Action',
    'RRR': 'Action',
    'The Dark Knight': 'Action',
    'Train to Busan': 'Horror',
    'Zindagi Na Milegi Dobara': 'Drama'
    }
    def watchname(title):
        if "Episode" in title:  
            return title.split(":")[0]
        else:
            return title
    df["watch name"]=df["Title"].apply(watchname)
    df["genre"]=df["watch name"].map(genre_map)
    return df["genre"].value_counts().reset_index()

def device_dominance(df):
    df["Watch Time"]=pd.to_timedelta(df["Duration"]).dt.total_seconds()/3600
    result=df.groupby("Device Type")["Watch Time"].sum().reset_index()
    return result

def countrydistribution(df):
    if len(df[df["Country"]=="IN"])/len(df)>0.60:
        desi=True
    else:
        desi=False
    return df["Country"].value_counts().reset_index(),desi

def costperhour(df,fee,month_no):
    df["S_Date"]=pd.to_datetime(df["S_Date"])
    df["Watch Time"]=pd.to_timedelta(df["Duration"]).dt.total_seconds()/3600
    return int(fee/df[df["S_Date"].dt.month==month_no]["Watch Time"].sum()) 


