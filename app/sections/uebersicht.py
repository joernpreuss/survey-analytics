import pandas as pd
import plotly.express as px  # pyright: ignore[reportMissingTypeStubs]
import streamlit as st

COLORS = {"satisfied": "#2ecc71", "neutral or dissatisfied": "#e74c3c"}


def render(filtered: pd.DataFrame) -> None:
    n = len(filtered)
    pct = f"{(filtered['satisfaction'] == 'satisfied').mean() * 100:.1f}%" if n else "—"
    avg_age = f"{filtered['Age'].mean():.0f}" if n else "—"

    col1, col2, col3 = st.columns(3)
    col1.metric("Zufriedene", pct)
    col2.metric("Befragte", f"{n:,}")
    col3.metric("Ø Alter", avg_age)

    for group_col in ["Class", "Type of Travel", "Customer Type"]:
        counts = (
            filtered.groupby([group_col, "satisfaction"])
            .size()
            .reset_index(name="Count")
        )
        fig = px.bar(  # pyright: ignore[reportUnknownMemberType]
            counts,
            x=group_col,
            y="Count",
            color="satisfaction",
            barmode="group",
            color_discrete_map=COLORS,
            title=f"Zufriedenheit nach <i>{group_col}</i>",
        )
        fig.update_layout(  # pyright: ignore[reportUnknownMemberType]
            xaxis_title="", legend_title_text=""
        )
        st.plotly_chart(fig, width="stretch")
