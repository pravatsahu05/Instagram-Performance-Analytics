"""
Interactive Visualizations Suite (Plotly)
Instagram Theme for Sugar Cosmetics Performance Analytics
Featuring Instagram's Signature Gradient Palette
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any

# Instagram Signature Color Palette & Dark Mode Theme
INSTAGRAM_COLORS = {
    "gradient_purple": "#833AB4",
    "gradient_magenta": "#C13584",
    "gradient_pink": "#E1306C",
    "gradient_red": "#FD1D1D",
    "gradient_orange": "#F56040",
    "gradient_yellow": "#FCAF45",
    "blue_accent": "#0095F6",      # Instagram Verified Blue
    "bg_pitch": "#000000",         # Instagram Pitch Black
    "card_dark": "#121212",        # Instagram Dark Card
    "card_surface": "#1E1E1E",     # Instagram Elevated Surface
    "border_gray": "#262626",      # Instagram Subtle Border
    "text_primary": "#FFFFFF",     # Clean White
    "text_secondary": "#A8A8A8",   # Instagram Muted Text
    "grid_color": "#212121"
}

# Format Colors aligned with Instagram
POST_TYPE_COLORS = {
    "Reel": "#E1306C",     # Instagram Pink
    "Story": "#F56040",    # Instagram Orange
    "Video": "#833AB4",    # Instagram Violet
    "Image": "#FCAF45"     # Instagram Gold
}

CAMPAIGN_COLORS = {
    "Tutorial": "#E1306C",
    "Giveaway": "#FCAF45",
    "Festive Offer": "#FD1D1D",
    "Product Launch": "#0095F6",
    "Influencer Collab": "#833AB4"
}

# Continuous Instagram Sunset Gradient Scale
INSTAGRAM_COLORSCALE = [
    [0.0, "#405DE6"],  # Royal Blue
    [0.2, "#833AB4"],  # Purple
    [0.4, "#C13584"],  # Magenta
    [0.6, "#E1306C"],  # Pink
    [0.8, "#FD1D1D"],  # Red
    [1.0, "#FCAF45"]   # Yellow-Orange
]


def apply_theme(fig: go.Figure, title: str = "", height: int = 420) -> go.Figure:
    """Applies authentic Instagram dark mode styling to Plotly figures."""
    fig.update_layout(
        title={
            "text": f"<b>{title}</b>",
            "x": 0.02,
            "y": 0.95,
            "xanchor": "left",
            "yanchor": "top",
            "font": {"size": 16, "color": INSTAGRAM_COLORS["text_primary"], "family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"}
        },
        template="plotly_dark",
        paper_bgcolor=INSTAGRAM_COLORS["card_dark"],
        plot_bgcolor=INSTAGRAM_COLORS["card_dark"],
        font={"color": INSTAGRAM_COLORS["text_secondary"], "family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"},
        height=height,
        margin={"l": 45, "r": 30, "t": 60, "b": 45},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
            "font": {"size": 12, "color": INSTAGRAM_COLORS["text_primary"]}
        },
        xaxis={
            "gridcolor": INSTAGRAM_COLORS["grid_color"],
            "zerolinecolor": INSTAGRAM_COLORS["grid_color"],
            "showline": True,
            "linecolor": INSTAGRAM_COLORS["border_gray"]
        },
        yaxis={
            "gridcolor": INSTAGRAM_COLORS["grid_color"],
            "zerolinecolor": INSTAGRAM_COLORS["grid_color"],
            "showline": True,
            "linecolor": INSTAGRAM_COLORS["border_gray"]
        }
    )
    return fig


def plot_monthly_posting_trend(monthly_df: pd.DataFrame) -> go.Figure:
    """Task 2: Monthly Posting Trend & Reach Volume with Instagram styling."""
    fig = go.Figure()

    # Reach Bar with Instagram Sunset Gradient fill
    fig.add_trace(go.Bar(
        x=monthly_df["Month_Name"],
        y=monthly_df["Total_Reach"] / 1_000_000,
        name="Total Reach (M)",
        marker={
            "color": monthly_df["Total_Reach"],
            "colorscale": INSTAGRAM_COLORSCALE,
            "opacity": 0.85,
            "line": {"color": "#262626", "width": 1}
        },
        yaxis="y"
    ))

    # Posts Published on Neon Instagram Pink Line
    fig.add_trace(go.Scatter(
        x=monthly_df["Month_Name"],
        y=monthly_df["Posts"],
        name="Posts Published",
        mode="lines+markers",
        line={"color": "#FFFFFF", "width": 3},
        marker={"size": 7, "color": INSTAGRAM_COLORS["gradient_pink"], "line": {"color": "#FFFFFF", "width": 1.5}},
        yaxis="y2"
    ))

    # Engagement Rate on Yellow Accent Line
    fig.add_trace(go.Scatter(
        x=monthly_df["Month_Name"],
        y=monthly_df["Avg_Engagement_Rate"],
        name="Avg Engagement Rate (%)",
        mode="lines+markers",
        line={"color": INSTAGRAM_COLORS["gradient_yellow"], "width": 2, "dash": "dot"},
        marker={"size": 6, "color": INSTAGRAM_COLORS["gradient_yellow"]},
        yaxis="y3",
        visible="legendonly"
    ))

    fig.update_layout(
        yaxis={
            "title": "Reach (Millions)",
            "title_font": {"color": INSTAGRAM_COLORS["gradient_pink"]},
            "tickfont": {"color": INSTAGRAM_COLORS["gradient_pink"]}
        },
        yaxis2={
            "title": "Posts Published",
            "title_font": {"color": "#FFFFFF"},
            "tickfont": {"color": "#FFFFFF"},
            "overlaying": "y",
            "side": "right",
            "showgrid": False
        },
        yaxis3={
            "title": "Engagement Rate (%)",
            "title_font": {"color": INSTAGRAM_COLORS["gradient_yellow"]},
            "tickfont": {"color": INSTAGRAM_COLORS["gradient_yellow"]},
            "overlaying": "y",
            "side": "right",
            "position": 0.95,
            "showgrid": False
        }
    )
    return apply_theme(fig, "📅 Monthly Cadence & Reach Velocity (Task 2)", height=430)


def plot_top_posts_bar(top_df: pd.DataFrame, metric: str = "Likes") -> go.Figure:
    """Task 3 & 4: Top Posts with Instagram Sunset Gradient bars."""
    sorted_df = top_df.sort_values(by=metric, ascending=True).copy()
    label_col = sorted_df["Post_ID"] + "  (" + sorted_df["Post Type"] + ")"
    
    hover_texts = [
        f"<b>{row['Post_ID']}</b><br>"
        f"Format: {row['Post Type']} | Campaign: {row['Campaign Type']}<br>"
        f"❤️ Likes: {row['Likes']:,} | 💬 Comments: {row['Comments']:,}<br>"
        f"🚀 Reach: {row['Reach']:,} | 📈 ER: {row['Engagement_Rate']}%<br>"
        f"Caption: {row['Caption_Short']}"
        for _, row in sorted_df.iterrows()
    ]

    metric_title = "Likes Received" if metric == "Likes" else "Engagement Rate (%)"

    fig = go.Figure(go.Bar(
        x=sorted_df[metric],
        y=label_col,
        orientation="h",
        marker={
            "color": sorted_df[metric],
            "colorscale": INSTAGRAM_COLORSCALE,
            "line": {"color": "rgba(255, 255, 255, 0.4)", "width": 1}
        },
        text=sorted_df[metric].apply(lambda x: f"{x:,}" if metric == "Likes" else f"{x:.2f}%"),
        textposition="outside",
        hoverinfo="text",
        hovertext=hover_texts
    ))

    title_text = f"🏆 Top 10 High-Performing Content by {metric_title}"
    return apply_theme(fig, title_text, height=440)


def plot_post_type_comparison(post_type_df: pd.DataFrame) -> go.Figure:
    """Task 5: Post Type Comparison in Instagram styling."""
    fig = go.Figure()

    metrics = [
        ("Avg_Likes", "❤️ Likes", INSTAGRAM_COLORS["gradient_pink"]),
        ("Avg_Comments", "💬 Comments", INSTAGRAM_COLORS["gradient_purple"]),
        ("Avg_Saves", "🔖 Saves", INSTAGRAM_COLORS["blue_accent"]),
        ("Avg_Shares", "🚀 Shares", INSTAGRAM_COLORS["gradient_yellow"])
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
    return apply_theme(fig, "🎬 Format Comparison: Likes, Comments, Saves & Shares (Task 5)", height=420)


def plot_post_type_rates(post_type_df: pd.DataFrame) -> go.Figure:
    """Task 5: Post Type Engagement Rate comparison."""
    fig = go.Figure()

    colors = [POST_TYPE_COLORS.get(pt, INSTAGRAM_COLORS["gradient_pink"]) for pt in post_type_df["Post Type"]]

    fig.add_trace(go.Bar(
        x=post_type_df["Post Type"],
        y=post_type_df["Avg_Engagement_Rate"],
        name="Avg Engagement Rate (%)",
        marker_color=colors,
        text=post_type_df["Avg_Engagement_Rate"].apply(lambda x: f"{x:.2f}%"),
        textposition="outside"
    ))

    fig.update_layout(yaxis={"range": [0, post_type_df["Avg_Engagement_Rate"].max() * 1.25]})
    return apply_theme(fig, "📊 Engagement Rate (%) by Media Format", height=380)


def plot_day_of_week_analysis(day_df: pd.DataFrame) -> go.Figure:
    """Task 6: Day of Week Engagement Heatmap / Bar."""
    fig = go.Figure()

    colors_day = [
        INSTAGRAM_COLORS["gradient_pink"] if d in ["Wednesday", "Saturday"] else "#3A3A3C"
        for d in day_df["Day of Week"]
    ]

    fig.add_trace(go.Bar(
        x=day_df["Day of Week"],
        y=day_df["Avg_Engagement_Rate"],
        name="Avg Engagement Rate (%)",
        marker={
            "color": colors_day,
            "line": {"color": "#FFFFFF", "width": 1}
        },
        text=day_df["Avg_Engagement_Rate"].apply(lambda x: f"{x:.2f}%"),
        textposition="outside"
    ))

    fig.add_trace(go.Scatter(
        x=day_df["Day of Week"],
        y=day_df["Avg_Reach"],
        name="Avg Reach per Post",
        mode="lines+markers",
        line={"color": INSTAGRAM_COLORS["gradient_yellow"], "width": 3},
        marker={"size": 8, "color": INSTAGRAM_COLORS["gradient_yellow"]},
        yaxis="y2"
    ))

    fig.update_layout(
        yaxis={"title": "Avg Engagement Rate (%)", "range": [17, 19.5]},
        yaxis2={
            "title": "Avg Reach per Post",
            "title_font": {"color": INSTAGRAM_COLORS["gradient_yellow"]},
            "tickfont": {"color": INSTAGRAM_COLORS["gradient_yellow"]},
            "overlaying": "y",
            "side": "right",
            "showgrid": False,
            "range": [18000, 21000]
        }
    )
    return apply_theme(fig, "📅 Day-of-Week Engagement & Reach Patterns (Task 6)", height=410)


def plot_engagement_funnel(funnel_df: pd.DataFrame) -> go.Figure:
    """Task 7: 6-Stage Conversion Funnel with Instagram Gradient."""
    funnel_colors = [
        "#833AB4",  # Impressions (Violet)
        "#C13584",  # Reach (Magenta)
        "#E1306C",  # Likes (Pink)
        "#FD1D1D",  # Comments (Red)
        "#F56040",  # Shares (Orange)
        "#FCAF45"   # Saves (Yellow)
    ]

    fig = go.Figure(go.Funnel(
        y=funnel_df["Stage"],
        x=funnel_df["Count"],
        textinfo="value+percent initial",
        opacity=0.92,
        marker={
            "color": funnel_colors,
            "line": {"width": 1.5, "color": "#FFFFFF"}
        },
        connector={"line": {"color": "rgba(255, 255, 255, 0.35)", "width": 1.5}}
    ))

    return apply_theme(fig, "🎯 Instagram Audience Engagement Funnel (Task 7)", height=450)


def plot_hashtag_comparison(hashtag_df: pd.DataFrame) -> go.Figure:
    """Task 8: Hashtag Performance Matrix."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=hashtag_df["Hashtag"],
        y=hashtag_df["Avg_Engagement_Rate"],
        name="Avg Engagement Rate (%)",
        marker={
            "color": hashtag_df["Avg_Engagement_Rate"],
            "colorscale": INSTAGRAM_COLORSCALE
        },
        text=hashtag_df["Avg_Engagement_Rate"].apply(lambda x: f"{x:.2f}%"),
        textposition="outside"
    ))

    fig.update_layout(
        yaxis={"title": "Average Engagement Rate (%)", "range": [17.5, 19.5]}
    )
    return apply_theme(fig, "🔖 Hashtag Engagement Efficiency (Task 8)", height=390)


def plot_campaign_performance(camp_df: pd.DataFrame) -> go.Figure:
    """Campaign Archetype Performance."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=camp_df["Campaign Type"],
        y=camp_df["Avg_Reach"],
        name="Avg Reach",
        marker_color=INSTAGRAM_COLORS["gradient_purple"],
        text=camp_df["Avg_Reach"].apply(lambda x: f"{x:,.0f}"),
        textposition="auto"
    ))

    fig.add_trace(go.Bar(
        x=camp_df["Campaign Type"],
        y=camp_df["Avg_Likes"],
        name="Avg Likes",
        marker_color=INSTAGRAM_COLORS["gradient_pink"],
        text=camp_df["Avg_Likes"].apply(lambda x: f"{x:,.0f}"),
        textposition="auto"
    ))

    fig.update_layout(barmode="group")
    return apply_theme(fig, "🏷️ Campaign Archetypes: Reach & Appreciation", height=410)


def plot_correlation_heatmap(corr_df: pd.DataFrame) -> go.Figure:
    """Correlation Heatmap styled in Instagram Dark Mode."""
    fig = go.Figure(go.Heatmap(
        z=corr_df.values,
        x=corr_df.columns,
        y=corr_df.index,
        colorscale=INSTAGRAM_COLORSCALE,
        text=corr_df.values.round(2),
        texttemplate="%{text}",
        textfont={"size": 11, "color": "#FFFFFF"},
        colorbar={"title": "Pearson r"}
    ))

    return apply_theme(fig, "🔗 Metric Correlation Matrix (Pearson r)", height=460)


def plot_interaction_proportions(df: pd.DataFrame) -> go.Figure:
    """Interaction Type Distribution Donut Chart."""
    totals = [
        df["Likes"].sum(),
        df["Comments"].sum(),
        df["Saves"].sum(),
        df["Shares"].sum()
    ]
    labels = ["Likes ❤️", "Comments 💬", "Saves 🔖", "Shares 🚀"]
    colors = [
        INSTAGRAM_COLORS["gradient_pink"],
        INSTAGRAM_COLORS["gradient_purple"],
        INSTAGRAM_COLORS["blue_accent"],
        INSTAGRAM_COLORS["gradient_yellow"]
    ]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=totals,
        hole=0.6,
        marker={"colors": colors, "line": {"color": "#121212", "width": 2.5}},
        textinfo="label+percent",
        textfont={"size": 13}
    ))
    return apply_theme(fig, "📊 Interaction Composition Mix", height=380)
