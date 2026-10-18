"""
Sugar Cosmetics - Instagram Performance Analytics Web Application
Production-Ready Streamlit Cloud Application
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
    plot_interaction_proportions, SUGAR_COLORS
)
from src.pdf_generator import build_pdf_report

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sugar Cosmetics | Instagram Analytics",
    page_icon="💄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Modern CSS (Glassmorphism & Brand Palette)
# ---------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4 {
    font-family: 'Outfit', sans-serif;
    letter-spacing: -0.02em;
}

/* Main background */
.stApp {
    background-color: #0E1117;
    color: #F8FAFC;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141724 0%, #0E1117 100%);
    border-right: 1px solid rgba(230, 27, 114, 0.2);
}

/* Metric card glassmorphism */
.kpi-card {
    background: linear-gradient(135deg, rgba(26, 29, 40, 0.85) 0%, rgba(18, 20, 29, 0.95) 100%);
    border: 1px solid rgba(230, 27, 114, 0.25);
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    transition: all 0.25s ease-in-out;
    position: relative;
    overflow: hidden;
}

.kpi-card:hover {
    transform: translateY(-3px);
    border-color: rgba(230, 27, 114, 0.6);
    box-shadow: 0 12px 30px rgba(230, 27, 114, 0.2);
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #E61B72, #9D4EDD, #00F5D4);
}

.kpi-title {
    font-size: 0.82rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #94A3B8;
    margin-bottom: 6px;
}

.kpi-value {
    font-family: 'Outfit', sans-serif;
    font-size: 1.85rem;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1.1;
    margin-bottom: 4px;
}

.kpi-subtext {
    font-size: 0.75rem;
    color: #38BDF8;
    font-weight: 500;
}

/* Post preview cards */
.post-preview-card {
    background: #1A1D28;
    border: 1px solid #282E40;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 12px;
    transition: border 0.2s ease;
}

.post-preview-card:hover {
    border-color: #E61B72;
}

/* Custom badges */
.badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    margin-right: 6px;
}
.badge-reel { background: rgba(230, 27, 114, 0.2); color: #FF4081; border: 1px solid rgba(230, 27, 114, 0.4); }
.badge-story { background: rgba(157, 78, 221, 0.2); color: #C77DFF; border: 1px solid rgba(157, 78, 221, 0.4); }
.badge-video { background: rgba(255, 107, 139, 0.2); color: #FFA8BA; border: 1px solid rgba(255, 107, 139, 0.4); }
.badge-image { background: rgba(0, 245, 212, 0.2); color: #00F5D4; border: 1px solid rgba(0, 245, 212, 0.4); }

/* Streamlit tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #141724;
    padding: 6px;
    border-radius: 12px;
    border: 1px solid #282E40;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 18px;
    color: #94A3B8;
    font-weight: 600;
    font-size: 0.88rem;
}

.stTabs [aria-selected="true"] {
    background-color: #E61B72 !important;
    color: #FFFFFF !important;
}

/* Button overrides */
.stButton > button {
    background: linear-gradient(90deg, #E61B72 0%, #D81B60 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 20px;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    box-shadow: 0 4px 18px rgba(230, 27, 114, 0.4);
    transform: translateY(-1px);
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


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
    # 1. Load Data
    with st.spinner("Initializing Sugar Cosmetics Analytics Engine..."):
        df_raw = get_cached_dataset()

    # 2. Sidebar Filters
    st.sidebar.markdown(
        """
        <div style="text-align: center; padding: 10px 0 16px 0;">
            <div style="font-family: 'Outfit'; font-size: 1.35rem; font-weight: 800; color: #FFFFFF;">
                SUGAR <span style="color: #E61B72;">COSMETICS</span>
            </div>
            <div style="font-size: 0.72rem; color: #94A3B8; letter-spacing: 0.1em; text-transform: uppercase;">
                Instagram Performance Analytics
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("🎯 Global Cross-Filters")

    # Date Range Filter
    min_date = df_raw["Post Date"].min().date()
    max_date = df_raw["Post Date"].max().date()
    
    date_selection = st.sidebar.date_input(
        "📅 Date Window",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Post Type Multi-Select
    all_post_types = sorted(df_raw["Post Type"].unique().tolist())
    selected_post_types = st.sidebar.multiselect(
        "🎬 Post Formats",
        options=all_post_types,
        default=all_post_types
    )

    # Campaign Type Multi-Select
    all_campaigns = sorted(df_raw["Campaign Type"].unique().tolist())
    selected_campaigns = st.sidebar.multiselect(
        "🏷️ Campaign Archetypes",
        options=all_campaigns,
        default=all_campaigns
    )

    # Hashtags Filter
    available_hashtags = ["All Hashtags", "#CrueltyFree", "#MakeupGoals", "#VeganBeauty", "#BoldLooks", "#SugarCosmetics"]
    selected_tag = st.sidebar.selectbox("🔖 Target Hashtag", options=available_hashtags)

    # Engagement Source
    all_sources = sorted(df_raw["Engagement Source"].unique().tolist())
    selected_sources = st.sidebar.multiselect(
        "🚀 Engagement Source",
        options=all_sources,
        default=all_sources
    )

    # Apply Filters
    df = df_raw.copy()

    # Date Filter
    if isinstance(date_selection, tuple) and len(date_selection) == 2:
        start_d, end_d = date_selection
        df = df[(df["Post Date"].dt.date >= start_d) & (df["Post Date"].dt.date <= end_d)]

    # Post Type Filter
    if selected_post_types:
        df = df[df["Post Type"].isin(selected_post_types)]

    # Campaign Type Filter
    if selected_campaigns:
        df = df[df["Campaign Type"].isin(selected_campaigns)]

    # Hashtag Filter
    if selected_tag != "All Hashtags":
        df = df[df["Hashtags"].str.contains(selected_tag, case=False, na=False)]

    # Engagement Source Filter
    if selected_sources:
        df = df[df["Engagement Source"].isin(selected_sources)]

    # Filter Feedback
    st.sidebar.markdown(f"**Filtered Sample:** `{len(df):,}` / `{len(df_raw):,}` posts ({len(df)/len(df_raw)*100:.1f}%)")
    
    # PDF Report Download in Sidebar
    pdf_path = os.path.join("outputs", "Sugar_Cosmetics_Instagram_Performance_Analytics_Report.pdf")
    if not os.path.exists(pdf_path):
        build_pdf_report(pdf_path)

    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        st.sidebar.download_button(
            label="📄 Download Executive PDF Report",
            data=pdf_bytes,
            file_name="Sugar_Cosmetics_Instagram_Performance_Analytics_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    # 3. Top Banner
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        st.markdown(
            """
            <h1 style="margin-bottom: 2px;">
                💄 Instagram Performance Analytics
            </h1>
            <p style="color: #94A3B8; font-size: 0.95rem; margin-top: 0;">
                Executive Social Media Intelligence & Strategic Decision Framework for <b>Sugar Cosmetics</b>
            </p>
            """,
            unsafe_allow_html=True
        )
    with col_t2:
        st.markdown(
            f"""
            <div style="background: #1A1D28; border: 1px solid #282E40; border-radius: 10px; padding: 10px 14px; text-align: right;">
                <span style="font-size: 0.72rem; color: #94A3B8;">OBSERVATION WINDOW</span><br/>
                <span style="font-size: 0.88rem; font-weight: 700; color: #00F5D4;">
                    {min_date.strftime('%b %d, %Y')} – {max_date.strftime('%b %d, %Y')}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # 4. Top KPI Cards Row (Task 1)
    kpis = calculate_overview_kpis(df)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Posts</div>
                <div class="kpi-value">{kpis['total_posts']:,}</div>
                <div class="kpi-subtext">Verified Content Records</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Reach</div>
                <div class="kpi-value">{kpis['total_reach']/1e6:.1f}M</div>
                <div class="kpi-subtext">Avg: {kpis['avg_reach_per_post']:,.0f} / post</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Impressions</div>
                <div class="kpi-value">{kpis['total_impressions']/1e9:.2f}B</div>
                <div class="kpi-subtext">Total Brand Exposures</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Avg Engagement</div>
                <div class="kpi-value" style="color: #00F5D4;">{kpis['avg_engagement_rate']:.2f}%</div>
                <div class="kpi-subtext">Median: {kpis['median_engagement_rate']:.2f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c5:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Interactions</div>
                <div class="kpi-value">{kpis['total_interactions']/1e6:.1f}M</div>
                <div class="kpi-subtext">Likes, Comments, Saves, Shares</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c6:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Follows Gained</div>
                <div class="kpi-value">{kpis['total_follows']/1e6:.2f}M</div>
                <div class="kpi-subtext">{kpis['overall_follow_rate']:.1f}% Profile Conv.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # 5. Application Tabs Navigation
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Executive KPIs & Trends",
        "🎬 Content & Top Posts",
        "🏷️ Campaigns & Hashtags",
        "🔬 Statistical Tests & EDA",
        "💡 Strategic Recommendations",
        "📑 Capstone Report & Data Export"
    ])

    # =========================================================
    # TAB 1: EXECUTIVE KPIS & TRENDS (Tasks 1, 2, 6, 7)
    # =========================================================
    with tab1:
        st.markdown("### 📈 Monthly Posting Cadence & Funnel Dynamics")
        
        # Row 1: Monthly Posting Trend (Task 2)
        monthly_df = get_monthly_posting_trend(df)
        fig_monthly = plot_monthly_posting_trend(monthly_df)
        st.plotly_chart(fig_monthly, use_container_width=True)

        # Row 2: Day of Week (Task 6) & Conversion Funnel (Task 7)
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("#### 📅 Day-of-Week Engagement Heat (Task 6)")
            day_df = get_day_of_week_analysis(df)
            fig_day = plot_day_of_week_analysis(day_df)
            st.plotly_chart(fig_day, use_container_width=True)

            best_day = day_df.sort_values(by="Avg_Engagement_Rate", ascending=False).iloc[0]
            st.info(f"💡 **Peak Posting Window:** **{best_day['Day of Week']}** achieved highest average engagement (**{best_day['Avg_Engagement_Rate']:.2f}%**), followed closely by Saturday (**18.60%**).")

        with col_g2:
            st.markdown("#### 🎯 6-Stage Conversion Funnel (Task 7)")
            funnel_df = get_engagement_funnel_data(df)
            fig_funnel = plot_engagement_funnel(funnel_df)
            st.plotly_chart(fig_funnel, use_container_width=True)

            reach_to_likes_conv = funnel_df.loc[2, "Step Conversion %"]
            st.success(f"🎯 **Funnel Efficiency:** Direct Like conversion from Reach stands at **{reach_to_likes_conv:.2f}%**, with Saves representing the ultimate high-intent audience action (**{funnel_df.loc[5, 'Count']:,} bookmarks**).")

    # =========================================================
    # TAB 2: CONTENT & TOP POSTS (Tasks 3, 4, 5)
    # =========================================================
    with tab2:
        st.markdown("### 🎬 Post Format Intelligence & Creative Benchmarking")

        # Row 1: Post Type Comparison (Task 5)
        pt_df = get_post_type_performance(df)
        
        c_p1, c_p2 = st.columns([3, 2])
        with c_p1:
            fig_pt = plot_post_type_comparison(pt_df)
            st.plotly_chart(fig_pt, use_container_width=True)
        with c_p2:
            fig_proportions = plot_interaction_proportions(df)
            st.plotly_chart(fig_proportions, use_container_width=True)

        st.markdown("---")

        # Post Format Summary Table
        st.markdown("#### 📊 Post Format Detailed Benchmarking")
        st.dataframe(
            pt_df[[
                "Post Type", "Posts", "Share_of_Posts_%", "Avg_Reach",
                "Avg_Likes", "Avg_Comments", "Avg_Saves", "Avg_Shares",
                "Avg_Engagement_Rate"
            ]].rename(columns={
                "Share_of_Posts_%": "Catalog Share (%)",
                "Avg_Reach": "Average Reach",
                "Avg_Likes": "Average Likes",
                "Avg_Comments": "Average Comments",
                "Avg_Saves": "Average Saves",
                "Avg_Shares": "Average Shares",
                "Avg_Engagement_Rate": "Avg ER (%)"
            }),
            use_container_width=True
        )

        st.markdown("---")

        # Row 2: Top 10 Posts by Likes (Task 3) vs Top 10 by ER (Task 4)
        st.markdown("### 🏆 Top Content Spotlight: Likes vs Hidden Gems")
        
        view_mode = st.radio(
            "Select Ranking Criteria:",
            ["🔥 Top 10 by Likes Received (Brute-Force Reach - Task 3)", 
             "💎 Top 10 by Engagement Rate (High-Efficiency 'Hidden Gems' - Task 4)"],
            horizontal=True
        )

        metric_target = "Likes" if "Likes" in view_mode else "Engagement_Rate"
        top_posts_df = get_top_posts(df, metric=metric_target, n=10)

        col_chart, col_cards = st.columns([3, 2])
        with col_chart:
            fig_top = plot_top_posts_bar(top_posts_df, metric=metric_target)
            st.plotly_chart(fig_top, use_container_width=True)

        with col_cards:
            st.markdown(f"#### 🏅 Top 5 Spotlight ({metric_target})")
            for _, post in top_posts_df.head(5).iterrows():
                badge_class = f"badge-{post['Post Type'].lower()}"
                st.markdown(
                    f"""
                    <div class="post-preview-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <span style="font-weight: 700; color: #FFFFFF;">#{int(post['Rank'])} {post['Post_ID']}</span>
                            <div>
                                <span class="badge {badge_class}">{post['Post Type']}</span>
                                <span class="badge" style="background: rgba(255, 183, 3, 0.2); color: #FFB703;">{post['Campaign Type']}</span>
                            </div>
                        </div>
                        <div style="font-size: 0.8rem; color: #CBD5E1; margin-bottom: 8px; font-style: italic;">
                            "{post['Caption_Short']}"
                        </div>
                        <div style="display: flex; gap: 14px; font-size: 0.78rem; color: #94A3B8;">
                            <span>❤️ <b>{int(post['Likes']):,}</b> likes</span>
                            <span>💬 <b>{int(post['Comments']):,}</b> comments</span>
                            <span>🚀 <b>{post['Engagement_Rate']:.2f}%</b> ER</span>
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
        
        # Audience Emotion and Engagement Sources
        st.markdown("#### 🧠 Audience Sentiment & Acquisition Sources")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            emotion_counts = df["Audience Emotion"].value_counts().reset_index()
            fig_emotion = px.pie(
                emotion_counts,
                names="Audience Emotion",
                values="count",
                title="<b>Audience Emotion Breakdown</b>",
                color_discrete_sequence=["#E61B72", "#9D4EDD", "#00F5D4", "#FFB703", "#FF6B8B"],
                hole=0.5
            )
            fig_emotion.update_layout(
                template="plotly_dark",
                paper_bgcolor=SUGAR_COLORS["card_dark"],
                plot_bgcolor=SUGAR_COLORS["card_dark"]
            )
            st.plotly_chart(fig_emotion, use_container_width=True)

        with col_s2:
            source_counts = df["Engagement Source"].value_counts().reset_index()
            fig_source = px.bar(
                source_counts,
                x="Engagement Source",
                y="count",
                title="<b>Engagement Acquisition Channels</b>",
                color="Engagement Source",
                color_discrete_sequence=["#00F5D4", "#E61B72", "#9D4EDD", "#FFB703"]
            )
            fig_source.update_layout(
                template="plotly_dark",
                paper_bgcolor=SUGAR_COLORS["card_dark"],
                plot_bgcolor=SUGAR_COLORS["card_dark"],
                showlegend=False
            )
            st.plotly_chart(fig_source, use_container_width=True)

    # =========================================================
    # TAB 4: STATISTICAL TESTS & EDA
    # =========================================================
    with tab4:
        st.markdown("### 🔬 Rigorous Statistical Hypothesis Testing & Inferential EDA")
        st.write("Ensuring all dashboard insights are validated with formal inferential statistics as required by Capstone evaluation standards.")

        stats_res = get_statistical_tests(df)

        # Hypothesis test cards
        st.markdown("#### 🧪 One-Way ANOVA & Independence Tests")
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">ANOVA: Post Type vs ER</div>
                    <div class="kpi-value" style="font-size: 1.35rem;">F = {stats_res['anova_post_type']['f_stat']:.4f}</div>
                    <div class="kpi-subtext">p-value: {stats_res['anova_post_type']['p_value']:.4f}</div>
                    <p style="font-size: 0.78rem; color: #CBD5E1; margin-top: 8px;">
                        {stats_res['anova_post_type']['interpretation']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with sc2:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">ANOVA: Campaign vs ER</div>
                    <div class="kpi-value" style="font-size: 1.35rem;">F = {stats_res['anova_campaign_type']['f_stat']:.4f}</div>
                    <div class="kpi-subtext">p-value: {stats_res['anova_campaign_type']['p_value']:.4f}</div>
                    <p style="font-size: 0.78rem; color: #CBD5E1; margin-top: 8px;">
                        {stats_res['anova_campaign_type']['interpretation']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with sc3:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Chi-Square: Campaign vs Format</div>
                    <div class="kpi-value" style="font-size: 1.35rem;">Chi2 = {stats_res['chi2_campaign_post']['chi2_stat']:.2f}</div>
                    <div class="kpi-subtext">p-value: {stats_res['chi2_campaign_post']['p_value']:.4f} (df=12)</div>
                    <p style="font-size: 0.78rem; color: #CBD5E1; margin-top: 8px;">
                        {stats_res['chi2_campaign_post']['interpretation']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")

        # Correlation Heatmap
        st.markdown("#### 🔗 Inter-Metric Correlation Heatmap")
        fig_corr = plot_correlation_heatmap(stats_res["correlation_matrix"])
        st.plotly_chart(fig_corr, use_container_width=True)

        st.info("💡 **Key Statistical Discovery:** Profile Visits and Follower Gains exhibit an extraordinary **r = 0.8351 correlation**. Content that drives users to click into the brand profile is the single most predictive factor for account audience growth.")

    # =========================================================
    # TAB 5: STRATEGIC RECOMMENDATIONS (Task 10)
    # =========================================================
    with tab5:
        st.markdown("### 💡 Data-Driven Strategic Recommendations & Action Plan (Task 10)")
        st.write("Synthesized from empirical analysis of 50,000 posts to refine Sugar Cosmetics' organic and paid marketing playbook.")

        r1, r2 = st.columns(2)
        with r1:
            st.markdown(
                """
                <div class="post-preview-card" style="border-left: 4px solid #E61B72;">
                    <h4 style="color: #E61B72; margin-top: 0;">1. Prioritize High-Velocity Short-Form Video & Stories</h4>
                    <p style="font-size: 0.88rem; color: #CBD5E1;">
                        <b>Data Finding:</b> Reels lead in average engagement rate (18.61%) and virality ratio. Stories generate equal engagement with shorter production lead times.<br/>
                        <b>Action Plan:</b> Shift content calendar distribution to <b>40% Reels, 30% Stories, 20% Carousels/Images, and 10% Long Videos</b>. Pair high-reach Reels with interactive Story links for immediate purchase intent.
                    </p>
                </div>
                <div class="post-preview-card" style="border-left: 4px solid #00F5D4;">
                    <h4 style="color: #00F5D4; margin-top: 0;">2. Exploit Midweek & Saturday Posting Windows</h4>
                    <p style="font-size: 0.88rem; color: #CBD5E1;">
                        <b>Data Finding:</b> Wednesdays (18.63% ER) and Saturdays (18.60% ER) consistently capture audience engagement peaks, while Sundays experience relative fatigue.<br/>
                        <b>Action Plan:</b> Schedule product launches and high-budget influencer collabs exclusively on Wednesday evenings and Saturday mornings.
                    </p>
                </div>
                <div class="post-preview-card" style="border-left: 4px solid #FFB703;">
                    <h4 style="color: #FFB703; margin-top: 0;">3. Center Messaging Around #CrueltyFree & Clean Glam</h4>
                    <p style="font-size: 0.88rem; color: #CBD5E1;">
                        <b>Data Finding:</b> <code>#CrueltyFree</code> and <code>#VeganBeauty</code> drive top engagement efficiency across 40,000+ tag occurrences.<br/>
                        <b>Action Plan:</b> Prominently feature cruelty-free certifications in video hooks and captions to capitalize on conscious beauty consumer preferences.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with r2:
            st.markdown(
                """
                <div class="post-preview-card" style="border-left: 4px solid #9D4EDD;">
                    <h4 style="color: #9D4EDD; margin-top: 0;">4. Optimize the Profile-Visit Conversion Bridge (r = 0.835)</h4>
                    <p style="font-size: 0.88rem; color: #CBD5E1;">
                        <b>Data Finding:</b> Profile visits share a remarkable 83.5% correlation with follower acquisition.<br/>
                        <b>Action Plan:</b> Add explicit profile visit triggers in captions (e.g., <i>'Tap our bio link to claim your shade match test & exclusive giveaway entry'</i>).
                    </p>
                </div>
                <div class="post-preview-card" style="border-left: 4px solid #FF4081;">
                    <h4 style="color: #FF4081; margin-top: 0;">5. Scale Influencer Co-Creations & Collaborative Giveaways</h4>
                    <p style="font-size: 0.88rem; color: #CBD5E1;">
                        <b>Data Finding:</b> Influencer Collabs produce the highest unique reach (19,875 avg) and minimize drop-off in the engagement funnel.<br/>
                        <b>Action Plan:</b> Institutionalize bi-weekly collaborative posts with high-affinity beauty creators to continuously access new customer cohorts.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown("#### 🗓️ 90-Day Phased Implementation Timeline")
        st.markdown(
            """
            | Phase | Window | Focus & Core Deliverables | Target KPI Outcome |
            | :--- | :--- | :--- | :--- |
            | **Phase 1: Optimization** | Days 1–30 | Align posting cadence to Wed/Sat windows; overhaul bio CTAs; standardize #CrueltyFree branding | +8% Profile Visit Rate |
            | **Phase 2: Scale** | Days 31–60 | Expand Reels allocation to 40%; deploy weekly collaborative creator videos; run bi-weekly giveaways | +15% Reel Views & Reach |
            | **Phase 3: Conversion** | Days 61–90 | Integrate Instagram Shop link attribution; minimize funnel drop-off; automate continuous BI tracking | +20% Follower Growth Velocity |
            """
        )

    # =========================================================
    # TAB 6: CAPSTONE REPORT & DATA EXPORT
    # =========================================================
    with tab6:
        st.markdown("### 📑 Capstone Project Report & Mock Evaluation Suite")

        col_d1, col_d2 = st.columns([2, 1])
        with col_d1:
            st.markdown("#### 📄 Executive PDF Presentation")
            st.write("A complete, publication-quality 11-page report detailing the problem statement, ELT pipeline, EDA, statistical proofs, and business recommendations.")
            
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    pdf_bytes_full = f.read()
                st.download_button(
                    label="⬇️ Download Executive PDF Report (Full Document)",
                    data=pdf_bytes_full,
                    file_name="Sugar_Cosmetics_Instagram_Performance_Analytics_Report.pdf",
                    mime="application/pdf",
                    key="tab6_pdf_download"
                )
            else:
                if st.button("Generate PDF Report Now"):
                    build_pdf_report(pdf_path)
                    st.rerun()

        with col_d2:
            st.markdown("#### 💾 Export Cleaned Dataset")
            st.write(f"Export currently filtered dataset (`{len(df):,}` rows) as CSV for offline analysis or spreadsheet auditing.")
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download Filtered CSV Dataset",
                data=csv_data,
                file_name="sugar_cosmetics_filtered_data.csv",
                mime="text/csv",
                key="tab6_csv_download"
            )

        st.markdown("---")

        # Mock Evaluation Questions
        st.markdown("#### 🎓 Capstone Live Evaluation: 5 Core Technical & Business Q&A")
        
        with st.expander("Q1: How did you calculate the Engagement Rate, and why choose Reach over Impressions?"):
            st.write(
                """
                **Answer:** We defined Engagement Rate as `(Likes + Comments + Shares + Saves) / Reach * 100`.
                We selected unique Reach as the standard denominator because Impressions include repeat views by the same user, 
                which artificially depresses engagement metrics for viral short videos that users rewatch. 
                Reach provides an accurate measurement of true unique audience activation.
                """
            )

        with st.expander("Q2: What is the business significance of the 6-stage funnel, and where is the greatest drop-off?"):
            st.write(
                """
                **Answer:** The funnel models audience value: `Impressions → Reach → Likes → Comments → Shares → Saves`.
                The highest initial drop-off occurs from Reach to Likes (~15% conversion), while Shares and Saves represent 
                high-intent actions (peer referral and bookmarks for purchase). In beauty e-commerce, Saves correlate directly 
                with downstream cart conversion when users shop makeup looks later.
                """
            )

        with st.expander("Q3: Why did you run a One-Way ANOVA test instead of multiple t-tests?"):
            st.write(
                """
                **Answer:** When evaluating 4 post formats (Reel, Story, Video, Image), running multiple independent t-tests 
                compounds the Family-Wise Error Rate (FWER = 1 - (1-alpha)^k), drastically inflating the probability of false positives (Type I error). 
                One-Way ANOVA performs a single omnibus F-test testing whether any variance between format means exceeds random variance.
                """
            )

        with st.expander("Q4: What data-driven insight surprised you most, and how does it alter strategy?"):
            st.write(
                """
                **Answer:** The remarkably strong **r = 0.8351 correlation between Profile Visits and Follower Gains**. 
                Merely reaching users on Feed or Explore does not automatically translate into brand followers; users must be 
                compelled to view the profile bio. This discovery led directly to our recommendation to include profile-visit 
                call-to-actions in all video captions.
                """
            )

        with st.expander("Q5: Why choose Streamlit Cloud over Tableau for this enterprise BI project?"):
            st.write(
                """
                **Answer:** Streamlit Cloud empowers data scientists with 100% Python code reusability, programmatic feature engineering, 
                seamless SciPy statistical test integration, custom responsive glassmorphic UI design, instant GitHub CI/CD cloud deployment, 
                and zero per-seat licensing fees for corporate stakeholders.
                """
            )

        st.markdown("---")
        st.markdown("#### 🔍 Interactive Dataset Inspector")
        st.dataframe(
            df[[
                "Post_ID", "Post Date", "Post Type", "Campaign Type",
                "Hashtags", "Reach", "Impressions", "Likes", "Comments",
                "Shares", "Saves", "Engagement_Rate", "Caption_Short"
            ]].head(100),
            use_container_width=True
        )


if __name__ == "__main__":
    main()
