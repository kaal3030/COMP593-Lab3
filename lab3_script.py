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
       
       required_columns = [
        "ORDER ID", "ORDER DATE", "ITEM NUMBER", "PRODUCT LINE", "PRODUCT CODE",
        "ITEM QUANTITY", "ITEM PRICE", "TOTAL PRICE", "STATUS", "CUSTOMER NAME"
    ]
       data = data[required_columns]
       grouped = data.groupby('ORDER ID')
     
       for name, group in grouped:
           group = group.sort_values(by='ITEM NUMBER')
           group = group.drop(columns=['ORDER ID'])

           filepath = os.path.join(orders_dir, f'order_{name}.xlsx')
           sheet_name = "Order_Details"
           
           with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
               group.to_excel(writer, index=False, sheet_name=sheet_name)
               workbook  = writer.book
               worksheet = writer.sheets[sheet_name]

               money_format = workbook.add_format({'num_format': '$#,##0.00'})
               worksheet.set_column('F:F', None, money_format)
               worksheet.set_column('G:G', None, money_format)
                                                             
               worksheet.set_column('A:A', 12)
               worksheet.set_column('B:B', 14)
               worksheet.set_column('C:C', 13)
               worksheet.set_column('D:D', 15)
               worksheet.set_column('E:E', 15)
               worksheet.set_column('F:F', 11)
               worksheet.set_column('G:G', 13)
               worksheet.set_column('H:H', 10)
               worksheet.set_column('I:I', 26)


               grand_total = group['TOTAL PRICE'].sum()
               row_position = len(group) + 1 
               worksheet.write(row_position, 5,"Grand Total", workbook.add_format({'bold': True}))
               worksheet.write(row_position, 6, grand_total, money_format)

               
# main function
def main():
    sales_csv = get_sales_csv()
    orders_dir = create_orders_dir(os.path.dirname(sales_csv))
    process_sales_data(sales_csv, orders_dir)

if __name__ == '__main__':
    main()