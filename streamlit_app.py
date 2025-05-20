import streamlit as st
import pandas as pd
import io

# Judul aplikasi
st.title("Pembaca dan Pembersih Data Excel")

# Definisi fungsi clean_and_convert
def clean_and_convert(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates(subset=['waktu'], keep='first')
    df['waktu'] = pd.to_datetime(df['waktu'])

    for col in ['temperatur', 'kecepatan angin', 'curah hujan']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

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
uploaded_file = st.file_uploader("Pilih file Excel", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        # Jika file Excel memiliki beberapa sheet, beri opsi untuk memilih
        xls = pd.ExcelFile(uploaded_file)
        if len(xls.sheet_names) > 1:
            sheet_name = st.selectbox("Pilih sheet", xls.sheet_names)
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Menampilkan data asli
        st.subheader("Data Asli")
        st.dataframe(df)
        
        # Memeriksa apakah kolom 'waktu' ada dalam DataFrame
        if 'waktu' in df.columns:
            # Membersihkan data
            cleaned_df = clean_and_convert(df)
            
            # Menampilkan data yang sudah dibersihkan
            st.subheader("Data yang Sudah Dibersihkan")
            st.dataframe(cleaned_df)
            
            # Opsi untuk mengunduh data yang sudah dibersihkan
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                cleaned_df.to_excel(writer, sheet_name="Data Bersih", index=False)
            
            buffer.seek(0)
            
            st.download_button(
                label="Unduh Data Bersih",
                data=buffer,
                file_name="data_bersih.xlsx",
                mime="application/vnd.ms-excel",
            )
        else:
            st.error("File Excel harus memiliki kolom 'waktu'")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
