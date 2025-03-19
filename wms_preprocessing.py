import json
import os
import logging
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WMS_Preprocessing")

class WMSPreprocessor:
    """Handles SKU mapping, inventory updates, and warehouse stock adjustments."""

    def __init__(self, sku_mapping_file, inventory_file, combo_mapping_file):
        self.sku_to_msku_map = self.load_json(sku_mapping_file, "SKU Mapping")
        self.inventory = self.load_json(inventory_file, "Inventory")
        self.combo_skus = self.load_json(combo_mapping_file, "Combo Mapping")

        # Track unique SKUs & MSKUs
        self.unique_skus = set()
        self.unique_mskus = set()

    def load_json(self, file_path, name):
        """Load JSON data with error handling."""
        if not os.path.exists(file_path):
            logger.error(f"{name} file not found: {file_path}")
            return {}
        with open(file_path, "r") as file:
            return json.load(file)

    def process_sales_data(self, sales_file, output_sales_file, output_inventory_file):
        """Map SKUs to MSKUs, process combos, update inventory, and track unique SKUs/MSKUs."""
        if not os.path.exists(sales_file):
            logger.error(f"Sales data file not found: {sales_file}")
            return

        with open(sales_file, "r") as file:
            sales_data = json.load(file)

        processed_sales = []
        inventory_updates = defaultdict(lambda: defaultdict(int))  # {warehouse: {msku: qty}}

        for item in sales_data:
            sku = item.get("sku", "").strip()
            quantity = item.get("quantity", 0)
            warehouse = item.get("warehouse", "main")

            mapped_item = item.copy()
            self.unique_skus.add(sku)  # Track unique SKU

            # **Handle Combo SKUs**
            if sku in self.combo_skus:
                mapped_item["msku"] = sku  # Keep combo SKU
                mapped_item["is_combo"] = True
                mapped_item["component_mskus"] = self.combo_skus[sku]

                # Track unique MSKUs
                self.unique_mskus.update(self.combo_skus[sku])

                # Subtract components from inventory
                for component in self.combo_skus[sku]:
                    inventory_updates[warehouse][component] -= quantity

            # **Handle Regular SKUs**
            elif sku in self.sku_to_msku_map:
                msku = self.sku_to_msku_map[sku]
                mapped_item["msku"] = msku
                mapped_item["is_combo"] = False
                mapped_item["component_mskus"] = None

                self.unique_mskus.add(msku)  # Track unique MSKU

                # Subtract from inventory
                inventory_updates[warehouse][msku] -= quantity

            # **Unmapped SKUs**
            else:
                mapped_item["msku"] = None
                mapped_item["is_combo"] = False
                mapped_item["component_mskus"] = None
                logger.warning(f"No mapping found for SKU: {sku}")

            processed_sales.append(mapped_item)

        # **Update Inventory**
        for warehouse, items in inventory_updates.items():
            if warehouse not in self.inventory:
                self.inventory[warehouse] = {}
            for msku, qty in items.items():
                self.inventory[warehouse][msku] = self.inventory[warehouse].get(msku, 0) + qty

        # **Save Processed Sales**
        with open(output_sales_file, "w") as file:
            json.dump(processed_sales, file, indent=4)
        logger.info(f"Processed sales saved: {output_sales_file}")

        # **Save Updated Inventory**
        with open(output_inventory_file, "w") as file:
            json.dump(self.inventory, file, indent=4)
        logger.info(f"Updated inventory saved: {output_inventory_file}")

        # **Save Unique SKU & MSKU Lists**
        with open("data/unique_skus.json", "w") as file:
            json.dump(list(self.unique_skus), file, indent=4)
        with open("data/unique_mskus.json", "w") as file:
            json.dump(list(self.unique_mskus), file, indent=4)
        
        # **Log Unique SKU & MSKU Count**
        logger.info(f"Unique SKUs Processed: {len(self.unique_skus)}")
        logger.info(f"Unique MSKUs Mapped: {len(self.unique_mskus)}")

        # **Visualize Unique SKUs and MSKUs**
        self.visualize_unique_skus_mskus()

    def visualize_unique_skus_mskus(self):
        """Generates bar charts for unique SKUs and MSKUs and saves them as images."""
        plt.figure(figsize=(10,5))
        
        # Plot Unique SKUs
        plt.subplot(1,2,1)
        sns.barplot(x=list(range(len(self.unique_skus))), y=list(self.unique_skus))
        plt.title("Unique SKUs Processed")
        plt.xticks([])
        plt.ylabel("SKU Names")
        plt.savefig("data/unique_skus_chart.png")

        # Plot Unique MSKUs
        plt.subplot(1,2,2)
        sns.barplot(x=list(range(len(self.unique_mskus))), y=list(self.unique_mskus))
        plt.title("Unique MSKUs Mapped")
        plt.xticks([])
        plt.ylabel("MSKU Names")
        plt.savefig("data/unique_mskus_chart.png")
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
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

    # Streamlit App Integration
    st.title("📊 Warehouse Management System (WMS) Dashboard")
    st.image("data/unique_skus_chart.png", caption="Unique SKUs Processed")
    st.image("data/unique_mskus_chart.png", caption="Unique MSKUs Mapped")
