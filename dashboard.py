import pandas as pd
import plotly.express as px  # pyright: ignore[reportMissingTypeStubs]
import streamlit as st

st.set_page_config(page_title="Survey Analytics", layout="wide")


# Daten laden


@st.cache_data
def load_data():
    # errors="ignore": Kaggle-Export liefert je nach Version mal mit, mal ohne Index-/id-Spalte
    df = pd.concat(
        [pd.read_csv("data/train.csv"), pd.read_csv("data/test.csv")],
        ignore_index=True,
    ).drop(columns=["Unnamed: 0", "id"], errors="ignore")
    return df


df = load_data()


# Sidebar-Filter

st.sidebar.header("Filter")

sel_class = st.sidebar.multiselect(
    "Class", df["Class"].unique(), default=df["Class"].unique()
)
sel_travel = st.sidebar.multiselect(
    "Type of Travel",
    df["Type of Travel"].unique(),
    default=df["Type of Travel"].unique(),
)
sel_customer = st.sidebar.multiselect(
    "Customer Type", df["Customer Type"].unique(), default=df["Customer Type"].unique()
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
