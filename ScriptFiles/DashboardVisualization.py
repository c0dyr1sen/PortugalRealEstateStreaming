import time
import json
import os
import pandas as pd
import streamlit as st
import plotly.express as px
from Configs import aggregated_data_dir
import plotly.graph_objects as go

# Функция для получения объединённых данных из директории CombinedData
def get_all_data(input_dir: str) -> pd.DataFrame:
    all_data = []

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(input_dir, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                    all_data.extend(file_data)
            except Exception as e:
                print(f'Error While Processing File {file_path}: {e}')

    if all_data:
        return pd.DataFrame(all_data)
    else:
        raise FileNotFoundError('No Data For Processing.')

# Функция для группировки и агрегации данных
def process_data(input_dataframe: pd.DataFrame) -> pd.DataFrame:
    input_dataframe = input_dataframe[(input_dataframe['Price'] >= 50000) & (input_dataframe['TotalArea'] >= 20)]

    grouped = input_dataframe.groupby(['Type', 'District']).agg(
        AvgPrice=('Price', 'mean'),
        AvgArea=('TotalArea', 'mean'),
        Count=('Price', 'count'),
        AvgPricePerSqM=('Price', lambda x: (x / input_dataframe.loc[x.index, 'TotalArea']).mean())
    ).reset_index()

    return grouped.round({'AvgPrice': 2, 'AvgArea': 2, 'AvgPricePerSqM': 2})

# Функция для создания графика с помощью библиотеки Plotly
def create_plot(input_data: pd.DataFrame) -> go.Figure():
    dashboard = px.bar(input_data,
                 x='District',
                 y='AvgPrice',
                 color='Type',
                 title='Average Property Prices by District',
                 labels={'AvgPrice': 'Average Price (€)', 'District': 'District'})

    dashboard.update_layout(barmode='group',
                      xaxis={'categoryorder': 'total descending'},
                      yaxis=dict(tickformat='.2f'))

    return dashboard



# --- Main ---

while True:
    try:
        combined_data = get_all_data(aggregated_data_dir)

        grouped_data = process_data(combined_data)

        st.title('Real Estate Data Dashboard')

        st.subheader('Aggregated Data')
        st.write(grouped_data.to_html(index=False, escape=False), unsafe_allow_html=True)

        st.subheader('Price vs District')
        fig = create_plot(grouped_data)
        st.plotly_chart(fig)

        time.sleep(30)
        st.rerun()

    except FileNotFoundError:
        st.write('No data files found in the directory.')
        time.sleep(30)
        st.rerun()