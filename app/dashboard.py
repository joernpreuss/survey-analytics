from pathlib import Path

import pandas as pd
import plotly.express as px  # pyright: ignore[reportMissingTypeStubs]
import streamlit as st

st.set_page_config(page_title="Survey Analytics", layout="wide")

DATA_PATH = Path(__file__).parent.parent / "data" / "survey.csv"


# Daten laden


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


df = load_data()


# Sidebar-Filter

st.sidebar.header("Filter")

classes = df["Class"].unique()
travel_types = df["Type of Travel"].unique()
customer_types = df["Customer Type"].unique()

sel_class = st.sidebar.multiselect("Class", classes, default=classes)
sel_travel = st.sidebar.multiselect(
    "Type of Travel", travel_types, default=travel_types
)
sel_customer = st.sidebar.multiselect(
    "Customer Type", customer_types, default=customer_types
)

filtered = df[
    df["Class"].isin(sel_class)
    & df["Type of Travel"].isin(sel_travel)
    & df["Customer Type"].isin(sel_customer)
]


# Seiten

st.title("Survey Analytics Dashboard")

tab1, tab2, tab3 = st.tabs(
    ["Zufriedenheitsübersicht", "Treiberanalyse", "Segmentierung"]
)

COLORS = {"satisfied": "#2ecc71", "neutral or dissatisfied": "#e74c3c"}

with tab1:
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

with tab2:
    st.info("Treiberanalyse — noch nicht implementiert")

with tab3:
    st.info("Segmentierung — noch nicht implementiert")
