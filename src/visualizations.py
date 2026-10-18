"""
Interactive Visualizations Suite (Plotly)
Sugar Cosmetics Instagram Performance Analytics
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any

# Brand Color Palette
SUGAR_COLORS = {
    "magenta": "#E61B72",
    "rose": "#FF4081",
    "coral": "#FF6B8B",
    "purple": "#9D4EDD",
    "dark_purple": "#5A189A",
    "cyan": "#00F5D4",
    "amber": "#FFB703",
    "bg_dark": "#0E1117",
    "card_dark": "#1A1D28",
    "text_light": "#F8FAFC",
    "text_muted": "#94A3B8",
    "grid_color": "#282E40"
}

POST_TYPE_COLORS = {
    "Reel": "#E61B72",
    "Story": "#9D4EDD",
    "Video": "#FF6B8B",
    "Image": "#00F5D4"
}

CAMPAIGN_COLORS = {
    "Tutorial": "#E61B72",
    "Giveaway": "#FFB703",
    "Festive Offer": "#FF6B8B",
    "Product Launch": "#00F5D4",
    "Influencer Collab": "#9D4EDD"
}


def apply_theme(fig: go.Figure, title: str = "", height: int = 420) -> go.Figure:
    """Applies a bespoke dark executive theme to Plotly figures."""
    fig.update_layout(
        title={
            "text": f"<b>{title}</b>",
            "x": 0.02,
            "y": 0.95,
            "xanchor": "left",
            "yanchor": "top",
            "font": {"size": 17, "color": SUGAR_COLORS["text_light"], "family": "Inter, sans-serif"}
        },
        template="plotly_dark",
        paper_bgcolor=SUGAR_COLORS["card_dark"],
        plot_bgcolor=SUGAR_COLORS["card_dark"],
        font={"color": SUGAR_COLORS["text_muted"], "family": "Inter, sans-serif"},
        height=height,
        margin={"l": 45, "r": 30, "t": 60, "b": 45},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
            "font": {"size": 12, "color": SUGAR_COLORS["text_light"]}
        },
        xaxis={
            "gridcolor": SUGAR_COLORS["grid_color"],
            "zerolinecolor": SUGAR_COLORS["grid_color"],
            "showline": True,
            "linecolor": SUGAR_COLORS["grid_color"]
        },
        yaxis={
            "gridcolor": SUGAR_COLORS["grid_color"],
            "zerolinecolor": SUGAR_COLORS["grid_color"],
            "showline": True,
            "linecolor": SUGAR_COLORS["grid_color"]
        }
    )
    return fig


def plot_monthly_posting_trend(monthly_df: pd.DataFrame) -> go.Figure:
    """Task 2: Monthly Posting Trend & Reach Volume."""
    fig = go.Figure()

    # Reach Bar on Secondary Y or Line
    fig.add_trace(go.Bar(
        x=monthly_df["Month_Name"],
        y=monthly_df["Total_Reach"] / 1_000_000,
        name="Total Reach (Millions)",
        marker_color="rgba(230, 27, 114, 0.4)",
        marker_line_color=SUGAR_COLORS["magenta"],
        marker_line_width=1.5,
        yaxis="y"
    ))

    # Posts Count on Line
    fig.add_trace(go.Scatter(
        x=monthly_df["Month_Name"],
        y=monthly_df["Posts"],
        name="Posts Published",
        mode="lines+markers",
        line={"color": SUGAR_COLORS["cyan"], "width": 3},
        marker={"size": 8, "color": SUGAR_COLORS["cyan"]},
        yaxis="y2"
    ))

    # Average Engagement Rate on Line
    fig.add_trace(go.Scatter(
        x=monthly_df["Month_Name"],
        y=monthly_df["Avg_Engagement_Rate"],
        name="Avg Engagement Rate (%)",
        mode="lines+markers",
        line={"color": SUGAR_COLORS["amber"], "width": 2, "dash": "dot"},
        marker={"size": 6, "color": SUGAR_COLORS["amber"]},
        yaxis="y3",
        visible="legendonly"
    ))

    fig.update_layout(
        yaxis={
            "title": "Total Reach (M)",
            "title_font": {"color": SUGAR_COLORS["magenta"]},
            "tickfont": {"color": SUGAR_COLORS["magenta"]}
        },
        yaxis2={
            "title": "Posts Published",
            "title_font": {"color": SUGAR_COLORS["cyan"]},
            "tickfont": {"color": SUGAR_COLORS["cyan"]},
            "overlaying": "y",
            "side": "right",
            "showgrid": False
        },
        yaxis3={
            "title": "Engagement Rate (%)",
            "title_font": {"color": SUGAR_COLORS["amber"]},
            "tickfont": {"color": SUGAR_COLORS["amber"]},
            "overlaying": "y",
            "side": "right",
            "position": 0.95,
            "showgrid": False
        }
    )
    return apply_theme(fig, "Monthly Content Cadence & Reach Velocity (Task 2)", height=430)


def plot_top_posts_bar(top_df: pd.DataFrame, metric: str = "Likes") -> go.Figure:
    """Task 3 & Task 4: Top 10 Posts Horizontal Bar Chart."""
    sorted_df = top_df.sort_values(by=metric, ascending=True).copy()
    
    label_col = sorted_df["Post_ID"] + " (" + sorted_df["Post Type"] + ")"
    
    hover_texts = [
        f"<b>{row['Post_ID']}</b><br>"
        f"Format: {row['Post Type']} | Campaign: {row['Campaign Type']}<br>"
        f"Likes: {row['Likes']:,} | Comments: {row['Comments']:,}<br>"
        f"Reach: {row['Reach']:,} | ER: {row['Engagement_Rate']}%<br>"
        f"Caption: {row['Caption_Short']}"
        for _, row in sorted_df.iterrows()
    ]

    metric_title = "Likes Received" if metric == "Likes" else "Engagement Rate (%)"
    bar_color = SUGAR_COLORS["magenta"] if metric == "Likes" else SUGAR_COLORS["amber"]

    fig = go.Figure(go.Bar(
        x=sorted_df[metric],
        y=label_col,
        orientation="h",
        marker={
            "color": sorted_df[metric],
            "colorscale": [[0, "#5A189A"], [0.5, "#E61B72"], [1.0, "#FFB703"]],
            "line": {"color": "#FFFFFF", "width": 1}
        },
        text=sorted_df[metric].apply(lambda x: f"{x:,}" if metric == "Likes" else f"{x:.2f}%"),
        textposition="outside",
        hoverinfo="text",
        hovertext=hover_texts
    ))

    title_text = f"Top 10 High-Impact Posts by {metric_title}"
    return apply_theme(fig, title_text, height=440)


def plot_post_type_comparison(post_type_df: pd.DataFrame) -> go.Figure:
    """Task 5: Post Type Performance Breakdown."""
    fig = go.Figure()

    metrics = [
        ("Avg_Likes", "Avg Likes", SUGAR_COLORS["magenta"]),
        ("Avg_Comments", "Avg Comments", SUGAR_COLORS["purple"]),
        ("Avg_Saves", "Avg Saves", SUGAR_COLORS["cyan"]),
        ("Avg_Shares", "Avg Shares", SUGAR_COLORS["amber"])
    ]

    for col, name, color in metrics:
        fig.add_trace(go.Bar(
            x=post_type_df["Post Type"],
            y=post_type_df[col],
            name=name,
            marker_color=color,
            text=post_type_df[col].apply(lambda x: f"{x:,.0f}"),
            textposition="auto"
        ))

    fig.update_layout(barmode="group")
    return apply_theme(fig, "Cross-Format Performance: Likes, Comments, Saves & Shares (Task 5)", height=420)


def plot_post_type_rates(post_type_df: pd.DataFrame) -> go.Figure:
    """Task 5: Post Type Engagement & Save Rates."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=post_type_df["Post Type"],
        y=post_type_df["Avg_Engagement_Rate"],
        name="Avg Engagement Rate (%)",
        marker_color=[POST_TYPE_COLORS.get(pt, SUGAR_COLORS["magenta"]) for pt in post_type_df["Post Type"]],
        text=post_type_df["Avg_Engagement_Rate"].apply(lambda x: f"{x:.2f}%"),
        textposition="outside"
    ))

    fig.update_layout(yaxis={"range": [0, post_type_df["Avg_Engagement_Rate"].max() * 1.25]})
    return apply_theme(fig, "Engagement Rate (%) by Post Format", height=380)


def plot_day_of_week_analysis(day_df: pd.DataFrame) -> go.Figure:
    """Task 6: Day of Week Engagement & Interactions."""
    fig = go.Figure()

    # Bar chart for Average Engagement Rate
    fig.add_trace(go.Bar(
        x=day_df["Day of Week"],
        y=day_df["Avg_Engagement_Rate"],
        name="Avg Engagement Rate (%)",
        marker={
            "color": day_df["Avg_Engagement_Rate"],
            "colorscale": [[0, "#3B185F"], [0.6, "#E61B72"], [1.0, "#00F5D4"]],
            "showscale": False
        },
        text=day_df["Avg_Engagement_Rate"].apply(lambda x: f"{x:.2f}%"),
        textposition="outside"
    ))

    # Line overlay for Average Reach
    fig.add_trace(go.Scatter(
        x=day_df["Day of Week"],
        y=day_df["Avg_Reach"],
        name="Avg Reach per Post",
        mode="lines+markers",
        line={"color": SUGAR_COLORS["amber"], "width": 3},
        marker={"size": 8, "color": SUGAR_COLORS["amber"]},
        yaxis="y2"
    ))

    fig.update_layout(
        yaxis={"title": "Avg Engagement Rate (%)", "range": [17, 19.5]},
        yaxis2={
            "title": "Avg Reach per Post",
            "title_font": {"color": SUGAR_COLORS["amber"]},
            "tickfont": {"color": SUGAR_COLORS["amber"]},
            "overlaying": "y",
            "side": "right",
            "showgrid": False,
            "range": [18000, 21000]
        }
    )
    return apply_theme(fig, "Day-of-Week Engagement Rate & Reach Patterns (Task 6)", height=410)


def plot_engagement_funnel(funnel_df: pd.DataFrame) -> go.Figure:
    """Task 7: Interactive Instagram Conversion Funnel."""
    fig = go.Figure(go.Funnel(
        y=funnel_df["Stage"],
        x=funnel_df["Count"],
        textinfo="value+percent initial",
        opacity=0.88,
        marker={
            "color": [
                "#9D4EDD",  # Impressions
                "#E61B72",  # Reach
                "#FF4081",  # Likes
                "#FF6B8B",  # Comments
                "#FFB703",  # Shares
                "#00F5D4"   # Saves
            ],
            "line": {"width": 1.5, "color": "#FFFFFF"}
        },
        connector={"line": {"color": "rgba(255, 255, 255, 0.4)", "width": 1.5}}
    ))

    return apply_theme(fig, "Audience Engagement & Conversion Funnel (Task 7)", height=450)


def plot_hashtag_comparison(hashtag_df: pd.DataFrame) -> go.Figure:
    """Task 8: Hashtag Performance Matrix."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=hashtag_df["Hashtag"],
        y=hashtag_df["Avg_Engagement_Rate"],
        name="Avg Engagement Rate (%)",
        marker={
            "color": hashtag_df["Avg_Engagement_Rate"],
            "colorscale": [[0, "#5A189A"], [0.5, "#E61B72"], [1.0, "#00F5D4"]]
        },
        text=hashtag_df["Avg_Engagement_Rate"].apply(lambda x: f"{x:.2f}%"),
        textposition="outside"
    ))

    fig.update_layout(
        yaxis={"title": "Average Engagement Rate (%)", "range": [17.5, 19.5]}
    )
    return apply_theme(fig, "Hashtag Engagement Efficiency (#CrueltyFree to #SugarCosmetics)", height=390)


def plot_campaign_performance(camp_df: pd.DataFrame) -> go.Figure:
    """Campaign Type Analysis."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=camp_df["Campaign Type"],
        y=camp_df["Avg_Reach"],
        name="Avg Reach",
        marker_color=SUGAR_COLORS["purple"],
        text=camp_df["Avg_Reach"].apply(lambda x: f"{x:,.0f}"),
        textposition="auto"
    ))

    fig.add_trace(go.Bar(
        x=camp_df["Campaign Type"],
        y=camp_df["Avg_Likes"],
        name="Avg Likes",
        marker_color=SUGAR_COLORS["magenta"],
        text=camp_df["Avg_Likes"].apply(lambda x: f"{x:,.0f}"),
        textposition="auto"
    ))

    fig.update_layout(barmode="group")
    return apply_theme(fig, "Campaign Archetype Reach & Appreciation Comparison", height=410)


def plot_correlation_heatmap(corr_df: pd.DataFrame) -> go.Figure:
    """Correlation Heatmap."""
    fig = go.Figure(go.Heatmap(
        z=corr_df.values,
        x=corr_df.columns,
        y=corr_df.index,
        colorscale=[
            [0.0, "#0E1117"],
            [0.2, "#240046"],
            [0.5, "#7B2CBF"],
            [0.8, "#E61B72"],
            [1.0, "#00F5D4"]
        ],
        text=corr_df.values.round(2),
        texttemplate="%{text}",
        textfont={"size": 11, "color": "#FFFFFF"},
        colorbar={"title": "Correlation"}
    ))

    return apply_theme(fig, "Metric Correlation Matrix (Pearson)", height=460)


def plot_interaction_proportions(df: pd.DataFrame) -> go.Figure:
    """Interaction Type Distribution Donut Chart."""
    totals = [
        df["Likes"].sum(),
        df["Comments"].sum(),
        df["Saves"].sum(),
        df["Shares"].sum()
    ]
    labels = ["Likes", "Comments", "Saves", "Shares"]
    colors = [SUGAR_COLORS["magenta"], SUGAR_COLORS["purple"], SUGAR_COLORS["cyan"], SUGAR_COLORS["amber"]]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=totals,
        hole=0.55,
        marker={"colors": colors, "line": {"color": "#1A1D28", "width": 2}},
        textinfo="label+percent",
        textfont={"size": 13}
    ))
    return apply_theme(fig, "Brand Interaction Composition", height=380)
