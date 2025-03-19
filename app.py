import streamlit as st
import pandas as pd
import json
import os
import time
from wms_preprocessing import WMSPreprocessor
from database import upload_to_airtable
from dotenv import load_dotenv

load_dotenv()

st.title("📊 Warehouse Management System (WMS)")

uploaded_file = st.file_uploader("Upload Sales Data (CSV/JSON)", type=["csv", "json"])

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1]
    
    if file_extension == "csv":
        df = pd.read_csv(uploaded_file)
    elif file_extension == "json":
        df = pd.read_json(uploaded_file)
    
    st.write("📌 Available Columns in Uploaded File:", df.columns.tolist())
    
    possible_quantity_columns = ["quantity", "Quantity Sold", "qty", "units"]
    quantity_col = next((col for col in possible_quantity_columns if col in df.columns), None)
    
    if not quantity_col:
        st.error("❌ No valid 'quantity' column found in the uploaded file!")
        st.stop()
    
    st.write("### Data Preview:")
    st.dataframe(df.head())
    
    if st.button("📤 Process & Upload Data"):
        df.to_json("data/sales_data.json", orient="records", indent=4)
        
        preprocessor = WMSPreprocessor(
            "data/sku_mapping.json",
            "data/inventory.json",
            "data/combo_mapping.json"
        )
        preprocessor.process_sales_data(
            "data/sales_data.json",
            "data/processed_sales.json",
            "data/updated_inventory.json"
        )
        
        with open("data/processed_sales.json", "r") as file:
            processed_sales = json.load(file)
        
        upload_to_airtable(processed_sales)
        st.success("✅ Data processed and uploaded successfully!")
        time.sleep(2)
        st.experimental_rerun()
    
    total_sales = df[quantity_col].sum()
    unique_skus = df["sku"].nunique() if "sku" in df.columns else "N/A"
    unique_mskus = df["msku"].nunique() if "msku" in df.columns else "N/A"
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Sales", total_sales)
    col2.metric("📊 Unique SKUs", unique_skus)
    col3.metric("🔄 Unique MSKUs", unique_mskus)
    
    st.write("### 📊 SKU & MSKU Visualizations")
    
    skus_chart_path = "data/unique_skus_chart.png"
    mskus_chart_path = "data/unique_mskus_chart.png"
    
    if os.path.exists(skus_chart_path):
        st.image(skus_chart_path, caption="📊 Unique SKUs Processed")
        with open(skus_chart_path, "rb") as file:
            st.download_button("⬇ Download Unique SKU Chart", file, file_name="unique_skus_chart.png")
    else:
        st.warning("⚠ Unique SKU chart not found. Please reprocess the data.")
    
    if os.path.exists(mskus_chart_path):
        st.image(mskus_chart_path, caption="📊 Unique MSKUs Mapped")
        with open(mskus_chart_path, "rb") as file:
            st.download_button("⬇ Download Unique MSKU Chart", file, file_name="unique_mskus_chart.png")
    else:
        st.warning("⚠ Unique MSKU chart not found. Please reprocess the data.")
