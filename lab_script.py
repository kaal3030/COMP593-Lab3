# LAB-3 (Business Process Automation).

import sys
import os
from datetime import datetime
import pandas as pd
import xlsxwriter

def get_sales_csv():
    if len(sys.argv) < 2:
        print("Error: No CSV file path provided.")
        sys.exit(1)

    csv_path = sys.argv[1]
    if not os.path.exists(csv_path):
        print(f"Error: The file {csv_path} does not exist.")
        sys.exit(1)

    return csv_path

def create_orders_dir(base_path):
    today = datetime.now().strftime("%Y-%m-%d")
    orders_dir = os.path.join(base_path, f"Orders_{today}")
    if not os.path.exists(orders_dir):
        os.makedirs(orders_dir)
    return orders_dir

def process_sales_data(sales_csv, orders_dir):
       data = pd.read_csv(sales_csv)
       data['TOTAL PRICE'] = data['ITEM QUANTITY'] * data['ITEM PRICE']

       grouped = data.groupby('ORDER ID')
       for name, group in grouped:
           filepath = os.path.join(orders_dir, f'order_{name}.xlsx')
           with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
               group.to_excel(writer, index=False)

# main function
def main():
    sales_csv = get_sales_csv()
    orders_dir = create_orders_dir(os.path.dirname(sales_csv))
    process_sales_data(sales_csv, orders_dir)

if __name__ == '__main__':
    main()