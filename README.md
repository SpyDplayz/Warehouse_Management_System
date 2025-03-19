📊 Warehouse Management System (WMS)

📌 Overview

This project is a Warehouse Management System (WMS) that helps with:

Mapping Localized SKUs to Master SKUs (MSKUs)

Processing and Cleaning Sales Data

Updating Warehouse Inventory

Visualizing Key Metrics

Uploading Processed Data to Airtable

🚀 Features

✅ Upload Sales Data (CSV/JSON)
✅ Process & Map SKUs to MSKUs
✅ Update Inventory with Processed Sales Data
✅ Visualize Unique SKUs and MSKUs
✅ Download Processed Data and Charts
✅ Auto-Refresh UI After Processing

🛠️ Setup Instructions

1️⃣ Clone the Repository

git clone <repository-url>
cd wms-project

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Set Up Environment Variables

Create a .env file and add your Airtable API Key and Base ID:

AIRTABLE_API_KEY=your_api_key_here
AIRTABLE_BASE_ID=your_base_id_here

4️⃣ Run the Streamlit App

streamlit run app.py

📂 File Structure

📦 wms-project
 ┣ 📂 data                # Processed data & visualizations
 ┣ 📜 app.py              # Streamlit dashboard
 ┣ 📜 wms_preprocessing.py # SKU Mapping & Inventory Processing
 ┣ 📜 database.py         # Airtable Upload Functionality
 ┣ 📜 requirements.txt    # Project dependencies
 ┣ 📜 .env                # API Keys (not included in repo)

📊 How It Works

1️⃣ Upload Sales Data (CSV/JSON) in the Streamlit UI.2️⃣ Click 'Process & Upload Data' to map SKUs, update inventory, and store results.3️⃣ View Key Metrics & Charts (Total Sales, Unique SKUs, Unique MSKUs).4️⃣ Download Processed Data & Charts directly from the app.

📝 Notes

Ensure that sku_mapping.json, inventory.json, and combo_mapping.json are placed in the data/ folder.

The app auto-refreshes after data processing to show updated charts.
