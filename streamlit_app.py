import streamlit as st
import pandas as pd
import io

# Judul aplikasi
st.title("Pembaca dan Pembersih Data Excel")

# Definisi fungsi clean_and_convert
def clean_and_convert(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates(subset=['waktu'], keep='first')
    df['waktu'] = pd.to_datetime(df['waktu'])

    start = df['waktu'].min()
    end = start + pd.Timedelta(days=366)
    time_index = pd.date_range(start=start, end=end, freq='10T')

    df = (
        df.set_index('waktu')
        .reindex(time_index)
        .rename_axis('waktu')
        .reset_index()
    )
    return df

# Uploader file
uploaded_file = st.file_uploader("Pilih file Excel", type=['xlsx'])
