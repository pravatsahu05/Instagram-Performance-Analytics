"""
Sugar Cosmetics - Instagram Performance Analytics Web Application
Production-Ready Streamlit Cloud Application
Aesthetic: Official Instagram Dark Mode & Sunset Gradient Theme
Top Horizontal Filter Navigation Bar
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from src.data_loader import load_and_preprocess_data
from src.analytics import (
    calculate_overview_kpis, get_monthly_posting_trend, get_top_posts,
    get_post_type_performance, get_day_of_week_analysis,
    get_engagement_funnel_data, get_hashtag_analytics,
    get_campaign_analytics, get_statistical_tests
)
from src.visualizations import (
    plot_monthly_posting_trend, plot_top_posts_bar, plot_post_type_comparison,
    plot_post_type_rates, plot_day_of_week_analysis, plot_engagement_funnel,
    plot_hashtag_comparison, plot_campaign_performance, plot_correlation_heatmap,
    plot_interaction_proportions, INSTAGRAM_COLORS, POST_TYPE_COLORS, CAMPAIGN_COLORS
)
from src.pdf_generator import build_pdf_report

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sugar Cosmetics | Instagram Analytics",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="collapsed"  # Collapsed because filters are now TOP NAVBAR
)

# ---------------------------------------------------------
# Custom Modern CSS (Official Instagram Theme)
# ---------------------------------------------------------
INSTAGRAM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap');

/* Global Reset & Instagram Dark Typography */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #F5F5F5;
}

/* Pitch Black Background like Instagram Dark Mode */
.stApp {
    background-color: #000000;
    color: #F5F5F5;
}

/* Instagram Header Container */
.ig-profile-header {
    background: #000000;
    border-bottom: 1px solid #262626;
    padding: 18px 0 24px 0;
    margin-bottom: 20px;
}

/* Story Gradient Ring for Avatar */
.story-ring-container {
    display: inline-block;
    padding: 3px;
    background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
    border-radius: 50%;
    box-shadow: 0 4px 15px rgba(225, 48, 108, 0.4);
}

.story-avatar {
    width: 82px;
    height: 82px;
    background: #121212;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 3px solid #000000;
    font-size: 2.2rem;
}

/* Verified Badge */
.verified-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 18px;
    height: 18px;
    background-color: #0095F6;
    color: white;
    border-radius: 50%;
    font-size: 11px;
    font-weight: 800;
    margin-left: 6px;
    vertical-align: middle;
}

/* Action Buttons */
.ig-btn-primary {
    display: inline-block;
    padding: 7px 18px;
    background: linear-gradient(45deg, #E1306C, #FD1D1D, #F56040);
    color: white !important;
    font-weight: 600;
    font-size: 0.85rem;
    border-radius: 8px;
    text-decoration: none;
    box-shadow: 0 4px 12px rgba(225, 48, 108, 0.35);
    transition: all 0.2s ease;
    border: none;
}
.ig-btn-primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(225, 48, 108, 0.5);
}

.ig-btn-secondary {
    display: inline-block;
    padding: 7px 16px;
    background: #262626;
    color: #FFFFFF !important;
    font-weight: 600;
    font-size: 0.85rem;
    border-radius: 8px;
    text-decoration: none;
    border: 1px solid #363636;
    transition: all 0.2s ease;
}
.ig-btn-secondary:hover {
    background: #363636;
}

/* TOP FILTER NAVIGATION BAR */
.top-filter-bar {
    background: #121212;
    border: 1px solid #262626;
    border-radius: 16px;
    padding: 16px 20px 10px 20px;
    margin-bottom: 22px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
    position: relative;
}

.top-filter-bar::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #833AB4, #C13584, #E1306C, #FD1D1D, #F56040, #FCAF45);
    border-radius: 16px 16px 0 0;
}

.filter-bar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    border-bottom: 1px solid #1F1F1F;
    padding-bottom: 8px;
}

.filter-bar-title {
    font-size: 0.92rem;
    font-weight: 700;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    gap: 8px;
}

.filter-badge-counter {
    background: rgba(225, 48, 108, 0.15);
    color: #E1306C;
    border: 1px solid rgba(225, 48, 108, 0.35);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.76rem;
    font-weight: 600;
}

/* Instagram Story Highlights Bar */
.highlights-container {
    display: flex;
    gap: 18px;
    overflow-x: auto;
    padding: 6px 0 16px 0;
    margin-bottom: 16px;
    border-bottom: 1px solid #1F1F1F;
}

.highlight-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    cursor: pointer;
    text-decoration: none;
    min-width: 68px;
}

.highlight-ring {
    width: 60px;
    height: 60px;
    padding: 2px;
    background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
    border-radius: 50%;
    margin-bottom: 6px;
    transition: transform 0.2s ease;
}

.highlight-ring:hover {
    transform: scale(1.08);
}

.highlight-icon-box {
    width: 100%;
    height: 100%;
    background: #121212;
    border-radius: 50%;
    border: 2px solid #000000;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.35rem;
}

.highlight-label {
    font-size: 0.72rem;
    color: #A8A8A8;
    font-weight: 500;
    max-width: 70px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* Metric KPI Cards in Instagram Dark Theme */
.ig-kpi-card {
    background: #121212;
    border: 1px solid #262626;
    border-radius: 14px;
    padding: 16px 18px;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.4);
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}

.ig-kpi-card:hover {
    transform: translateY(-3px);
    border-color: #E1306C;
    box-shadow: 0 8px 25px rgba(225, 48, 108, 0.25);
}

.ig-kpi-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #A8A8A8;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 4px;
}

.ig-kpi-value {
    font-family: 'Outfit', -apple-system, sans-serif;
    font-size: 1.85rem;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.1;
    margin-bottom: 4px;
}

.ig-kpi-sub {
    font-size: 0.74rem;
    color: #0095F6;
    font-weight: 600;
}

/* Instagram Post Card (Tab 2) */
.ig-feed-card {
    background: #121212;
    border: 1px solid #262626;
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 16px;
    transition: border 0.2s ease;
}

.ig-feed-card:hover {
    border-color: #E1306C;
}

.ig-feed-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    border-bottom: 1px solid #1C1C1C;
}

.ig-feed-user {
    display: flex;
    align-items: center;
    gap: 10px;
}

.ig-avatar-sm {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: linear-gradient(45deg, #f09433, #dc2743, #bc1888);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    border: 2px solid #000;
}

.ig-feed-actions {
    padding: 10px 16px;
    display: flex;
    justify-content: space-between;
    font-size: 1.1rem;
    border-top: 1px solid #1C1C1C;
    background: #161616;
}

.ig-badge-pill {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.72rem;
    font-weight: 700;
}
.badge-reel { background: rgba(225, 48, 108, 0.2); color: #E1306C; border: 1px solid #E1306C; }
.badge-story { background: rgba(245, 96, 64, 0.2); color: #F56040; border: 1px solid #F56040; }
.badge-video { background: rgba(131, 58, 180, 0.2); color: #C13584; border: 1px solid #833AB4; }
.badge-image { background: rgba(252, 175, 69, 0.2); color: #FCAF45; border: 1px solid #FCAF45; }

/* Instagram Profile Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background-color: transparent;
    padding: 4px 0;
    border-top: 1px solid #262626;
    border-bottom: 1px solid #262626;
    border-radius: 0;
    justify-content: center;
    margin-bottom: 18px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 0;
    padding: 12px 22px;
    color: #8E8E8E;
    font-weight: 600;
    font-size: 0.86rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    border-top: 2px solid transparent;
}

.stTabs [aria-selected="true"] {
    background: transparent !important;
    color: #FFFFFF !important;
    border-top: 2px solid #FFFFFF !important;
}

/* Customizing Streamlit Widgets to Instagram Dark */
div[data-baseweb="select"] > div {
    background-color: #1A1A1A !important;
    border-color: #363636 !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
}

div[data-baseweb="input"] {
    background-color: #1A1A1A !important;
    border-color: #363636 !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
}

/* Custom buttons */
.stButton > button {
    background: linear-gradient(45deg, #E1306C 0%, #FD1D1D 50%, #F56040 100%);
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 18px;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    box-shadow: 0 4px 18px rgba(225, 48, 108, 0.45);
    transform: translateY(-1px);
}
</style>
"""
st.markdown(INSTAGRAM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------
# Cached Data Loader
# ---------------------------------------------------------
@st.cache_data(show_spinner=False)
def get_cached_dataset() -> pd.DataFrame:
    """Loads and caches the 50,000-post dataset."""
    return load_and_preprocess_data()


# ---------------------------------------------------------
# Main Application Flow
# ---------------------------------------------------------
def main():
    # Load Data
    df_raw = get_cached_dataset()

    # =========================================================
    # 1. INSTAGRAM VERIFIED PROFILE HEADER
    # =========================================================
    st.markdown(
        """
        <div class="ig-profile-header">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 20px;">
                <div style="display: flex; align-items: center; gap: 22px;">
                    <div class="story-ring-container">
                        <div class="story-avatar">💄</div>
                    </div>
                    <div>
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                            <span style="font-family: 'Outfit', sans-serif; font-size: 1.6rem; font-weight: 800; color: #FFFFFF;">
                                sugarcosmetics
                            </span>
                            <span class="verified-badge">✓</span>
                            <span style="background: #262626; color: #F56040; padding: 2px 8px; border-radius: 6px; font-size: 0.72rem; font-weight: 700;">
                                OFFICIAL BI DASHBOARD
                            </span>
                        </div>
                        <div style="display: flex; gap: 24px; font-size: 0.92rem; color: #E5E5E5; margin-bottom: 8px;">
                            <span><b>50,000</b> posts</span>
                            <span><b>987.4M</b> reach</span>
                            <span><b>147.7M</b> likes</span>
                            <span><b>8.87M</b> followers</span>
                        </div>
                        <div style="font-size: 0.85rem; color: #A8A8A8; line-height: 1.4;">
                            <b style="color: #FFFFFF;">SUGAR Cosmetics</b> • #RuleTheWorld ✨<br/>
                            High-performance makeup crafted for bold Indian beauty • 100% Cruelty-Free 🐰<br/>
                            <a href="https://sugarcosmetics.com" target="_blank" style="color: #0095F6; text-decoration: none; font-weight: 600;">🔗 sugarcosmetics.com</a>
                        </div>
                    </div>
                </div>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <a href="#kpi-section" class="ig-btn-primary">📊 View Insights</a>
                    <a href="#report-section" class="ig-btn-secondary">📑 PDF Report</a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================================================
    # 2. INSTAGRAM STORY HIGHLIGHTS BAR
    # =========================================================
    st.markdown(
        """
        <div class="highlights-container">
            <div class="highlight-item">
                <div class="highlight-ring"><div class="highlight-icon-box">📊</div></div>
                <span class="highlight-label">KPIs</span>
            </div>
            <div class="highlight-item">
                <div class="highlight-ring"><div class="highlight-icon-box">🎬</div></div>
                <span class="highlight-label">Reels</span>
            </div>
            <div class="highlight-item">
                <div class="highlight-ring"><div class="highlight-icon-box">💎</div></div>
                <span class="highlight-label">Top Posts</span>
            </div>
            <div class="highlight-item">
                <div class="highlight-ring"><div class="highlight-icon-box">🏷️</div></div>
                <span class="highlight-label">Campaigns</span>
            </div>
            <div class="highlight-item">
                <div class="highlight-ring"><div class="highlight-icon-box">🔖</div></div>
                <span class="highlight-label">Hashtags</span>
            </div>
            <div class="highlight-item">
                <div class="highlight-ring"><div class="highlight-icon-box">🎯</div></div>
                <span class="highlight-label">Funnel</span>
            </div>
            <div class="highlight-item">
                <div class="highlight-ring"><div class="highlight-icon-box">🔬</div></div>
                <span class="highlight-label">Stats</span>
            </div>
            <div class="highlight-item">
                <div class="highlight-ring"><div class="highlight-icon-box">💡</div></div>
                <span class="highlight-label">Strategy</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================================================
    # 3. TOP HORIZONTAL FILTER NAVIGATION BAR (NEW POSITION)
    # =========================================================
    min_date = df_raw["Post Date"].min().date()
    max_date = df_raw["Post Date"].max().date()
    all_post_types = sorted(df_raw["Post Type"].unique().tolist())
    all_campaigns = sorted(df_raw["Campaign Type"].unique().tolist())
    available_hashtags = ["All Hashtags", "#CrueltyFree", "#MakeupGoals", "#VeganBeauty", "#BoldLooks", "#SugarCosmetics"]
    all_sources = sorted(df_raw["Engagement Source"].unique().tolist())

    st.markdown(
        """
        <div class="top-filter-bar">
            <div class="filter-bar-header">
                <div class="filter-bar-title">
                    <span>⚡ Filter Control Center</span>
                    <span style="font-size: 0.78rem; font-weight: normal; color: #A8A8A8;">(Interactive Cross-Filtering Engine)</span>
                </div>
                <div>
                    <span class="filter-badge-counter" id="filter-status-tag">50,000 Verified Posts Loaded</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 5 Responsive Filter Columns on Top
    col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns([1.8, 1.4, 1.4, 1.4, 1.2])

    with col_f1:
        date_selection = st.date_input(
            "📅 Date Window",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="top_date_picker"
        )

    with col_f2:
        selected_post_types = st.multiselect(
            "🎬 Post Formats",
            options=all_post_types,
            default=all_post_types,
            key="top_post_types"
        )

    with col_f3:
        selected_campaigns = st.multiselect(
            "🏷️ Campaign Types",
            options=all_campaigns,
            default=all_campaigns,
            key="top_campaigns"
        )

    with col_f4:
        selected_tag = st.selectbox(
            "🔖 Target Hashtag",
            options=available_hashtags,
            key="top_hashtag"
        )

    with col_f5:
        selected_sources = st.multiselect(
            "🚀 Acquisition",
            options=all_sources,
            default=all_sources,
            key="top_sources"
        )

    # Apply Active Filters
    df = df_raw.copy()

    # 1. Date Filter
    if isinstance(date_selection, tuple) and len(date_selection) == 2:
        start_d, end_d = date_selection
        df = df[(df["Post Date"].dt.date >= start_d) & (df["Post Date"].dt.date <= end_d)]

    # 2. Post Type Filter
    if selected_post_types:
        df = df[df["Post Type"].isin(selected_post_types)]

    # 3. Campaign Type Filter
    if selected_campaigns:
        df = df[df["Campaign Type"].isin(selected_campaigns)]

    # 4. Hashtag Filter
    if selected_tag != "All Hashtags":
        df = df[df["Hashtags"].str.contains(selected_tag, case=False, na=False)]

    # 5. Engagement Source Filter
    if selected_sources:
        df = df[df["Engagement Source"].isin(selected_sources)]

    # Active Filter Status Bar
    filter_pct = (len(df) / len(df_raw)) * 100
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; background: #161616; padding: 6px 14px; border-radius: 8px; border: 1px solid #262626; margin-top: -10px; margin-bottom: 20px; font-size: 0.78rem; color: #A8A8A8;">
            <span>Displaying <b>{len(df):,}</b> of <b>{len(df_raw):,}</b> posts ({filter_pct:.1f}% of catalog)</span>
            <span>Active Formats: <b>{', '.join(selected_post_types) if selected_post_types else 'None'}</b> | Hashtag: <b>{selected_tag}</b></span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================================================
    # 4. TOP METRIC CARDS (INSTAGRAM INSIGHTS CARDS)
    # =========================================================
    kpis = calculate_overview_kpis(df)

    st.markdown("<div id='kpi-section'></div>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(
            f"""
            <div class="ig-kpi-card">
                <div class="ig-kpi-label">Total Posts</div>
                <div class="ig-kpi-value">{kpis['total_posts']:,}</div>
                <div class="ig-kpi-sub">Verified Records</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""
            <div class="ig-kpi-card">
                <div class="ig-kpi-label">Total Reach</div>
                <div class="ig-kpi-value" style="color: #FCAF45;">{kpis['total_reach']/1e6:.1f}M</div>
                <div class="ig-kpi-sub">Avg {kpis['avg_reach_per_post']:,.0f} / post</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f"""
            <div class="ig-kpi-card">
                <div class="ig-kpi-label">Total Impressions</div>
                <div class="ig-kpi-value">{kpis['total_impressions']/1e9:.2f}B</div>
                <div class="ig-kpi-sub">77.4% Reach Ratio</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c4:
        st.markdown(
            f"""
            <div class="ig-kpi-card">
                <div class="ig-kpi-label">Avg Engagement</div>
                <div class="ig-kpi-value" style="color: #E1306C;">{kpis['avg_engagement_rate']:.2f}%</div>
                <div class="ig-kpi-sub">Median {kpis['median_engagement_rate']:.2f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c5:
        st.markdown(
            f"""
            <div class="ig-kpi-card">
                <div class="ig-kpi-label">Interactions</div>
                <div class="ig-kpi-value">{kpis['total_interactions']/1e6:.1f}M</div>
                <div class="ig-kpi-sub">Likes + Comments + Saves</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c6:
        st.markdown(
            f"""
            <div class="ig-kpi-card">
                <div class="ig-kpi-label">Follows Gained</div>
                <div class="ig-kpi-value" style="color: #0095F6;">{kpis['total_follows']/1e6:.2f}M</div>
                <div class="ig-kpi-sub">{kpis['overall_follow_rate']:.1f}% Profile Conv.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # =========================================================
    # 5. INSTAGRAM PROFILE GRID TABS NAVIGATION
    # =========================================================
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "▦ OVERVIEW (Tasks 1, 2)",
        "🎬 REELS & CONTENT (Tasks 3, 4, 5)",
        "🏷️ CAMPAIGNS & TAGS (Task 8)",
        "🎯 AUDIENCE & FUNNEL (Tasks 6, 7)",
        "🔬 STATS & EDA (ANOVA / Corr)",
        "💡 STRATEGY & REPORT (Task 10 & PDF)"
    ])

    # =========================================================
    # TAB 1: OVERVIEW & CADENCE (Tasks 1 & 2)
    # =========================================================
    with tab1:
        st.markdown("### 📈 Monthly Publishing Cadence & Reach Dynamics (Task 2)")
        monthly_df = get_monthly_posting_trend(df)
        fig_monthly = plot_monthly_posting_trend(monthly_df)
        st.plotly_chart(fig_monthly, use_container_width=True)

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("#### 📊 Interaction Composition Mix")
            fig_mix = plot_interaction_proportions(df)
            st.plotly_chart(fig_mix, use_container_width=True)

        with col_m2:
            st.markdown("#### 🎯 Account Growth Efficiency")
            st.markdown(
                f"""
                <div style="background: #121212; border: 1px solid #262626; border-radius: 12px; padding: 20px;">
                    <div style="font-size: 0.95rem; font-weight: 700; color: #FFFFFF; margin-bottom: 12px;">
                        Conversion Funnel Efficiency Indicators
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #1F1F1F;">
                        <span style="color: #A8A8A8;">Unique Reach / Impressions Ratio</span>
                        <span style="font-weight: 700; color: #E1306C;">77.38%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #1F1F1F;">
                        <span style="color: #A8A8A8;">Profile Visit Conversion Rate</span>
                        <span style="font-weight: 700; color: #F56040;">3.00%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #1F1F1F;">
                        <span style="color: #A8A8A8;">Profile Visit to Follower Rate</span>
                        <span style="font-weight: 700; color: #0095F6;">29.92%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 8px 0;">
                        <span style="color: #A8A8A8;">Bookmark / Save Efficiency</span>
                        <span style="font-weight: 700; color: #FCAF45;">0.90%</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # =========================================================
    # TAB 2: REELS & CONTENT INTELLIGENCE (Tasks 3, 4, 5)
    # =========================================================
    with tab2:
        st.markdown("### 🎬 Media Format Intelligence & Top Posts (Tasks 3, 4, 5)")
        pt_df = get_post_type_performance(df)

        col_p1, col_p2 = st.columns([3, 2])
        with col_p1:
            fig_pt = plot_post_type_comparison(pt_df)
            st.plotly_chart(fig_pt, use_container_width=True)

        with col_p2:
            fig_er_format = plot_post_type_rates(pt_df)
            st.plotly_chart(fig_er_format, use_container_width=True)

        st.markdown("---")
        st.markdown("### 🏆 Top 10 Posts Spotlight: Likes vs High-Efficiency 'Hidden Gems'")

        view_mode = st.radio(
            "Select Ranking Criteria:",
            ["🔥 Top 10 by Likes Received (Brute-Force Reach - Task 3)", 
             "💎 Top 10 by Engagement Rate (High-Efficiency 'Hidden Gems' - Task 4)"],
            horizontal=True
        )

        metric_target = "Likes" if "Likes" in view_mode else "Engagement_Rate"
        top_posts_df = get_top_posts(df, metric=metric_target, n=10)

        col_chart, col_feed = st.columns([3, 2])
        with col_chart:
            fig_top = plot_top_posts_bar(top_posts_df, metric=metric_target)
            st.plotly_chart(fig_top, use_container_width=True)

        with col_feed:
            st.markdown(f"#### 📱 Instagram Post Preview ({metric_target})")
            for _, post in top_posts_df.head(4).iterrows():
                badge_class = f"badge-{post['Post Type'].lower()}"
                st.markdown(
                    f"""
                    <div class="ig-feed-card">
                        <div class="ig-feed-header">
                            <div class="ig-feed-user">
                                <div class="ig-avatar-sm">💄</div>
                                <div>
                                    <div style="font-size: 0.85rem; font-weight: 700; color: #FFFFFF;">
                                        sugarcosmetics <span class="verified-badge" style="width: 14px; height: 14px; font-size: 8px;">✓</span>
                                    </div>
                                    <div style="font-size: 0.72rem; color: #8E8E8E;">{post['Post_ID']} • {post['Post Date'].strftime('%b %d, %Y')}</div>
                                </div>
                            </div>
                            <span class="ig-badge-pill {badge_class}">{post['Post Type']}</span>
                        </div>
                        <div style="padding: 12px 16px; font-size: 0.82rem; color: #E5E5E5; line-height: 1.4;">
                            "{post['Caption_Short']}"
                        </div>
                        <div class="ig-feed-actions">
                            <span style="color: #E1306C;">❤️ <b>{int(post['Likes']):,}</b></span>
                            <span style="color: #C13584;">💬 <b>{int(post['Comments']):,}</b></span>
                            <span style="color: #F56040;">🚀 <b>{int(post['Shares']):,}</b></span>
                            <span style="color: #0095F6;">🔖 <b>{int(post['Saves']):,}</b></span>
                            <span style="color: #FCAF45; font-size: 0.78rem; font-weight: 700;">{post['Engagement_Rate']:.2f}% ER</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # =========================================================
    # TAB 3: CAMPAIGNS & HASHTAGS (Task 8)
    # =========================================================
    with tab3:
        st.markdown("### 🏷️ Campaign Archetypes & Hashtag Performance Matrix (Task 8)")

        col_h1, col_h2 = st.columns(2)
        with col_h1:
            st.markdown("#### 🔖 Hashtag Engagement Comparison")
            hash_df = get_hashtag_analytics(df)
            fig_hash = plot_hashtag_comparison(hash_df)
            st.plotly_chart(fig_hash, use_container_width=True)

        with col_h2:
            st.markdown("#### 🚀 Campaign Archetype Distribution")
            camp_df = get_campaign_analytics(df)
            fig_camp = plot_campaign_performance(camp_df)
            st.plotly_chart(fig_camp, use_container_width=True)

        st.markdown("---")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("#### 🧠 Audience Sentiment Emotions")
            emotion_counts = df["Audience Emotion"].value_counts().reset_index()
            fig_emotion = px.pie(
                emotion_counts,
                names="Audience Emotion",
                values="count",
                color_discrete_sequence=["#E1306C", "#C13584", "#F56040", "#FCAF45", "#0095F6"],
                hole=0.55
            )
            fig_emotion.update_layout(
                template="plotly_dark",
                paper_bgcolor="#121212",
                plot_bgcolor="#121212"
            )
            st.plotly_chart(fig_emotion, use_container_width=True)

        with col_s2:
            st.markdown("#### 🌐 Channel Acquisition Sources")
            source_counts = df["Engagement Source"].value_counts().reset_index()
            fig_source = px.bar(
                source_counts,
                x="Engagement Source",
                y="count",
                color="Engagement Source",
                color_discrete_sequence=["#0095F6", "#E1306C", "#C13584", "#FCAF45"]
            )
            fig_source.update_layout(
                template="plotly_dark",
                paper_bgcolor="#121212",
                plot_bgcolor="#121212",
                showlegend=False
            )
            st.plotly_chart(fig_source, use_container_width=True)

    # =========================================================
    # TAB 4: AUDIENCE & FUNNEL (Tasks 6 & 7)
    # =========================================================
    with tab4:
        st.markdown("### 🎯 Audience Timing & The 6-Stage Conversion Funnel (Tasks 6 & 7)")

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown("#### 📅 Day-of-Week Engagement Heat (Task 6)")
            day_df = get_day_of_week_analysis(df)
            fig_day = plot_day_of_week_analysis(day_df)
            st.plotly_chart(fig_day, use_container_width=True)

            best_day = day_df.sort_values(by="Avg_Engagement_Rate", ascending=False).iloc[0]
            st.info(f"💡 **Peak Posting Windows:** **{best_day['Day of Week']}** achieved highest average engagement (**{best_day['Avg_Engagement_Rate']:.2f}%**), followed by Saturday (**18.60%**). Sunday exhibits slight audience fatigue (**18.42%**).")

        with col_d2:
            st.markdown("#### 🎯 6-Stage Conversion Funnel (Task 7)")
            funnel_df = get_engagement_funnel_data(df)
            fig_funnel = plot_engagement_funnel(funnel_df)
            st.plotly_chart(fig_funnel, use_container_width=True)

            st.success(f"🎯 **Funnel Efficiency:** From **1.28 Billion Impressions**, **987.4 Million Unique Accounts** were reached, yielding **147.7M Likes**, **18.5M Comments**, **8.1M Shares**, and **8.86M High-Intent Saves**.")

    # =========================================================
    # TAB 5: STATISTICAL TESTS & EDA
    # =========================================================
    with tab5:
        st.markdown("### 🔬 Rigorous Statistical Hypothesis Testing & Correlation EDA")
        st.write("Ensuring all dashboard insights are validated with formal inferential statistics as required by Capstone evaluation standards.")

        stats_res = get_statistical_tests(df)

        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.markdown(
                f"""
                <div class="ig-kpi-card">
                    <div class="ig-kpi-label">ANOVA: Post Type vs ER</div>
                    <div class="ig-kpi-value" style="font-size: 1.35rem; color: #E1306C;">F = {stats_res['anova_post_type']['f_stat']:.4f}</div>
                    <div class="ig-kpi-sub">p-value: {stats_res['anova_post_type']['p_value']:.4f}</div>
                    <p style="font-size: 0.78rem; color: #A8A8A8; margin-top: 8px;">
                        {stats_res['anova_post_type']['interpretation']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with sc2:
            st.markdown(
                f"""
                <div class="ig-kpi-card">
                    <div class="ig-kpi-label">ANOVA: Campaign vs ER</div>
                    <div class="ig-kpi-value" style="font-size: 1.35rem; color: #F56040;">F = {stats_res['anova_campaign_type']['f_stat']:.4f}</div>
                    <div class="ig-kpi-sub">p-value: {stats_res['anova_campaign_type']['p_value']:.4f}</div>
                    <p style="font-size: 0.78rem; color: #A8A8A8; margin-top: 8px;">
                        {stats_res['anova_campaign_type']['interpretation']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with sc3:
            st.markdown(
                f"""
                <div class="ig-kpi-card">
                    <div class="ig-kpi-label">Chi-Square: Campaign vs Format</div>
                    <div class="ig-kpi-value" style="font-size: 1.35rem; color: #FCAF45;">Chi2 = {stats_res['chi2_campaign_post']['chi2_stat']:.2f}</div>
                    <div class="ig-kpi-sub">p-value: {stats_res['chi2_campaign_post']['p_value']:.4f} (df=12)</div>
                    <p style="font-size: 0.78rem; color: #A8A8A8; margin-top: 8px;">
                        {stats_res['chi2_campaign_post']['interpretation']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown("#### 🔗 Inter-Metric Pearson Correlation Heatmap")
        fig_corr = plot_correlation_heatmap(stats_res["correlation_matrix"])
        st.plotly_chart(fig_corr, use_container_width=True)

        st.info("💡 **Core Statistical Finding:** Profile Visits and Follows share an extraordinary **r = 0.8351 correlation**. Content reach alone does not build followers; users must be prompted to visit the bio profile to trigger account follows.")

    # =========================================================
    # TAB 6: STRATEGY, REPORT & DOWNLOADS (Task 10 & PDF)
    # =========================================================
    with tab6:
        st.markdown("<div id='report-section'></div>", unsafe_allow_html=True)
        st.markdown("### 💡 Strategic Playbook & Capstone Deliverables (Task 10)")

        col_r1, col_r2 = st.columns([3, 2])
        with col_r1:
            st.markdown(
                """
                <div style="background: #121212; border: 1px solid #262626; border-radius: 14px; padding: 18px 22px; margin-bottom: 14px; border-left: 4px solid #E1306C;">
                    <h4 style="color: #E1306C; margin-top: 0;">1. Prioritize High-Velocity Short-Form Video & Stories</h4>
                    <p style="font-size: 0.86rem; color: #A8A8A8;">
                        Shift content allocation to <b>40% Reels, 30% Stories, 20% Carousels, and 10% Long Videos</b>. Reels yield the highest organic virality and reach velocity, while Stories convert daily link clicks.
                    </p>
                </div>
                <div style="background: #121212; border: 1px solid #262626; border-radius: 14px; padding: 18px 22px; margin-bottom: 14px; border-left: 4px solid #F56040;">
                    <h4 style="color: #F56040; margin-top: 0;">2. Exploit Midweek & Saturday Posting Windows</h4>
                    <p style="font-size: 0.86rem; color: #A8A8A8;">
                        Concentrate tier-1 product announcements and influencer collaborations exclusively on <b>Wednesday evenings</b> (18.63% ER peak) and <b>Saturday mornings</b> (18.60% ER peak).
                    </p>
                </div>
                <div style="background: #121212; border: 1px solid #262626; border-radius: 14px; padding: 18px 22px; margin-bottom: 14px; border-left: 4px solid #FCAF45;">
                    <h4 style="color: #FCAF45; margin-top: 0;">3. Center Messaging Around #CrueltyFree & Clean Glam</h4>
                    <p style="font-size: 0.86rem; color: #A8A8A8;">
                        <code>#CrueltyFree</code> and <code>#VeganBeauty</code> drive top engagement efficiency across 40,000+ posts. Integrate ethical claims directly into on-screen video hooks.
                    </p>
                </div>
                <div style="background: #121212; border: 1px solid #262626; border-radius: 14px; padding: 18px 22px; border-left: 4px solid #0095F6;">
                    <h4 style="color: #0095F6; margin-top: 0;">4. Optimize the Profile-Visit Conversion Bridge (r = 0.835)</h4>
                    <p style="font-size: 0.86rem; color: #A8A8A8;">
                        Mandate explicit profile visit calls-to-action in captions (<i>'Tap our bio link to claim your shade match test'</i>) to convert reach into net follower gains.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_r2:
            st.markdown("#### 📄 Executive PDF Capstone Report")
            pdf_path = os.path.join("outputs", "Sugar_Cosmetics_Instagram_Performance_Analytics_Report.pdf")
            if not os.path.exists(pdf_path):
                build_pdf_report(pdf_path)

            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    pdf_bytes_full = f.read()
                st.download_button(
                    label="⬇️ Download Executive PDF Report",
                    data=pdf_bytes_full,
                    file_name="Sugar_Cosmetics_Instagram_Performance_Analytics_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            st.write("An 11-page publication-ready PDF report containing the complete Capstone evaluation sections, data dictionary, static high-res charts, ANOVA proofs, and 5 mock interview questions.")

            st.markdown("---")
            st.markdown("#### 💾 Export Filtered Dataset")
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Export Filtered CSV Data",
                data=csv_data,
                file_name="sugar_cosmetics_filtered_data.csv",
                mime="text/csv",
                use_container_width=True
            )

        st.markdown("---")
        st.markdown("#### 🎓 Capstone Live Evaluation: 5 Core Technical & Business Q&A")
        with st.expander("Q1: How did you calculate the Engagement Rate, and why choose Reach over Impressions?"):
            st.write(
                """
                **Answer:** We formulated Engagement Rate as:
                $$\\text{Engagement Rate} = \\frac{\\text{Likes} + \\text{Comments} + \\text{Shares} + \\text{Saves}}{\\text{Reach}} \\times 100$$
                We selected unique Reach because Impressions count repeated views by the same user, which artificially deflates engagement for viral short videos that users rewatch. Reach measures true unique audience conversion efficiency.
                """
            )
        with st.expander("Q2: What is the business significance of the 6-stage funnel, and where is the greatest drop-off?"):
            st.write(
                """
                **Answer:** The funnel models audience value: `Impressions → Reach → Likes → Comments → Shares → Saves`.
                The highest initial drop-off occurs from Reach to Likes (~15% conversion), while Shares and Saves represent high-intent actions. In beauty e-commerce, Saves correlate directly with downstream cart conversion when users shop makeup looks later.
                """
            )
        with st.expander("Q3: Why did you run a One-Way ANOVA test instead of multiple t-tests?"):
            st.write(
                """
                **Answer:** When evaluating 4 post formats (Reel, Story, Video, Image), running multiple independent t-tests compounds the Family-Wise Error Rate (FWER = $1 - (1-\\alpha)^k$), drastically inflating Type I error (false positives). One-Way ANOVA performs a single omnibus F-test testing whether any variance between format means exceeds random variance.
                """
            )
        with st.expander("Q4: What data-driven insight surprised you most, and how does it alter strategy?"):
            st.write(
                """
                **Answer:** The remarkably strong **r = 0.8351 correlation between Profile Visits and Follower Gains**. Merely reaching users on Feed or Explore does not automatically translate into brand followers; users must be compelled to view the profile bio. This discovery led directly to our recommendation to include profile-visit call-to-actions in all video captions.
                """
            )
        with st.expander("Q5: Why choose Streamlit Cloud over Tableau for this enterprise BI project?"):
            st.write(
                """
                **Answer:** Streamlit Cloud empowers data scientists with 100% Python code reusability, programmatic feature engineering, seamless SciPy statistical test integration, custom responsive glassmorphic UI design, instant GitHub CI/CD cloud deployment, and zero per-seat licensing fees for corporate stakeholders.
                """
            )


if __name__ == "__main__":
    main()
