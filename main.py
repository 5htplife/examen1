import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import plotnine


@st.cache
def get_data():
    data_url = "Fat_Supply_Quantity_Data.csv"
    return pd.read_csv(data_url)

df = get_data()

df





#def print_hi(name):

#    print(f'Hi, {name}')
#if __name__ == '__main__':
#    print_hi('PyCharm')

