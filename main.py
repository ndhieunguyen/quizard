import pandas as pd
import streamlit as st
import os

bank_path = os.path.join("data", "bank.csv")
df = pd.read_csv(bank_path, index_col=0)

st.dataframe(df)
