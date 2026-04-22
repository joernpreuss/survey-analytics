from pathlib import Path

import pandas as pd
import streamlit as st

from sections import treiberanalyse, uebersicht

st.set_page_config(page_title="Survey Analytics", layout="wide")

DATA_PATH = Path(__file__).parent.parent / "data" / "survey.csv"


# Daten laden


@st.cache_data
def load_data() -> pd.DataFrame:
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

with tab1:
    uebersicht.render(filtered)

with tab2:
    treiberanalyse.render(df)

with tab3:
    st.info("Segmentierung — noch nicht implementiert")
