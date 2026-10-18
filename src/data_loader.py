"""
Data Loader & Preprocessing Pipeline
Instagram Performance Analytics for Sugar Cosmetics
"""

import os
import pandas as pd
import numpy as np


def get_data_path() -> str:
    """Finds the dataset path either in data/ or root directory."""
    candidates = [
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sugar_cosmetics_instagram_data.csv"),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "sugar_cosmetics_instagram_data.csv"),
        "data/sugar_cosmetics_instagram_data.csv",
        "sugar_cosmetics_instagram_data.csv"
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("Could not locate sugar_cosmetics_instagram_data.csv in workspace.")


def generate_post_caption(row: pd.Series) -> str:
    """
    Synthesizes an authentic, engaging brand caption based on Campaign Type,
    Audience Emotion, and Hashtags for enhanced storytelling in the dashboard.
    """
    campaign = str(row.get("Campaign Type", "Brand Post"))
    emotion = str(row.get("Audience Emotion", "Inspired"))
    tags = str(row.get("Hashtags", "#SugarCosmetics"))

    templates = {
        "Tutorial": f"Master the signature look! ✨ Step-by-step beauty glam crafted to leave you feeling {emotion.lower()}. Save this for your next glam session! {tags}",
        "Giveaway": f"GIVEAWAY ALERT! 🎁 We're celebrating our amazing fam! Drop your favorite shade below and tag 2 besties to win our exclusive beauty bundle! {tags}",
        "Festive Offer": f"Festive glam season is here! 💄 Unleash your {emotion.lower()} festive beauty with irresistible deals on your favorites! {tags}",
        "Product Launch": f"INTRODUCING THE NEXT BIG THING! 🚀 Formulated for all-day perfection and {emotion.lower()} confidence. Shop the newest drop now! {tags}",
        "Influencer Collab": f"Serving iconic vibes with our beauty muse! 🌟 Flaunting the boldest shades that turn heads everywhere. {tags}"
    }
    return templates.get(campaign, f"Unleash your inner beauty with bold, high-performance makeup! {tags}")


def load_and_preprocess_data(filepath: str = None) -> pd.DataFrame:
    """
    Loads raw Instagram data, performs data cleaning, validation,
    and feature engineering for analytics and dashboarding.
    """
    if filepath is None:
        filepath = get_data_path()

    df = pd.read_csv(filepath)

    # 1. Standardize column names (strip whitespace)
    df.columns = [c.strip() for c in df.columns]

    # 2. Datetime parsing and temporal feature engineering
    df["Post Date"] = pd.to_datetime(df["Post Date"])
    df["Year"] = df["Post Date"].dt.year
    df["Month"] = df["Post Date"].dt.month
    df["Month_Name"] = df["Post Date"].dt.strftime("%b %Y")
    df["Month_Year"] = df["Post Date"].dt.to_period("M").astype(str)
    df["Day_Name"] = df["Post Date"].dt.day_name()
    df["Day_Of_Week"] = df["Post Date"].dt.dayofweek  # 0=Monday, 6=Sunday
    df["Is_Weekend"] = df["Day_Of_Week"].isin([5, 6]).astype(int)

    # 3. Numeric conversions & validation
    numeric_cols = [
        "Impressions", "Reach", "Likes", "Comments", 
        "Shares", "Saves", "Profile Visits", "Follows"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    # 4. Interaction Metrics & KPI Calculations
    # Total Interactions = Likes + Comments + Shares + Saves
    df["Total_Interactions"] = df["Likes"] + df["Comments"] + df["Shares"] + df["Saves"]
    
    # Engagement Rates (Standard Industry Definitions)
    # Reach-based Engagement Rate (%)
    df["Engagement_Rate"] = np.where(
        df["Reach"] > 0,
        (df["Total_Interactions"] / df["Reach"]) * 100,
        0.0
    ).round(2)

    # Impressions-based Engagement Rate (%)
    df["Engagement_Rate_Imp"] = np.where(
        df["Impressions"] > 0,
        (df["Total_Interactions"] / df["Impressions"]) * 100,
        0.0
    ).round(2)

    # Like-Comment Engagement Rate (%)
    df["Like_Comment_ER"] = np.where(
        df["Reach"] > 0,
        ((df["Likes"] + df["Comments"]) / df["Reach"]) * 100,
        0.0
    ).round(2)

    # Saves Rate (% of reach who found content valuable enough to bookmark)
    df["Save_Rate"] = np.where(df["Reach"] > 0, (df["Saves"] / df["Reach"]) * 100, 0.0).round(2)

    # Share Rate (% of reach who shared - virality indicator)
    df["Share_Rate"] = np.where(df["Reach"] > 0, (df["Shares"] / df["Reach"]) * 100, 0.0).round(2)

    # Profile Visit Conversion Rate (% of reach visiting profile)
    df["Profile_Visit_Rate"] = np.where(
        df["Reach"] > 0, 
        (df["Profile Visits"] / df["Reach"]) * 100, 
        0.0
    ).round(2)

    # Follower Conversion Rate (% of profile visits that resulted in follows)
    df["Follow_Conversion_Rate"] = np.where(
        df["Profile Visits"] > 0,
        (df["Follows"] / df["Profile Visits"]) * 100,
        0.0
    ).round(2)

    # Virality Ratio = Shares / Likes
    df["Virality_Ratio"] = np.where(
        df["Likes"] > 0,
        (df["Shares"] / df["Likes"]).round(4),
        0.0
    )

    # 5. Hashtag Parsing & List Representation
    df["Hashtags_Clean"] = df["Hashtags"].fillna("").astype(str)
    df["Hashtag_List"] = df["Hashtags_Clean"].apply(
        lambda x: [t.strip() for t in x.split(",") if t.strip()]
    )
    df["Hashtag_Count"] = df["Hashtag_List"].apply(len)

    # 6. Synthesized Realistic Brand Caption for Task 3 & 4
    df["Caption"] = df.apply(generate_post_caption, axis=1)
    df["Caption_Short"] = df["Caption"].apply(
        lambda x: (x[:75] + "...") if len(x) > 75 else x
    )

    # 7. Post ID for unique referencing
    df["Post_ID"] = [f"SUGAR-{i+1:05d}" for i in range(len(df))]

    return df


if __name__ == "__main__":
    data = load_and_preprocess_data()
    print(f"Data pipeline successfully loaded {len(data)} rows.")
    print("Columns:", data.columns.tolist())
