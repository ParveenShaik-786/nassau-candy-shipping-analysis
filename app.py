import streamlit as st
from utils.preprocess import load_data

# Load dataset
df = load_data("data/Nassau_Candy_Distributor.csv")

st.title("🍬 Factory-to-Customer Shipping Analysis")

st.write("### Dataset Preview")
st.dataframe(df.head())

st.write("### Dataset Shape")
st.write(df.shape)

st.write("### Columns")
st.write(df.columns.tolist())