from app import InvItem, db, app
import pandas as pd

def parse_excel_to_dict(file_path, sheet_name=0):
    """
    Parses an Excel file and returns its content as a dictionary.
    :param file_path: Path to the Excel file
    :param sheet_name: Name or index of the sheet to read (default is the first sheet)
    :return: Dictionary representation of the Excel data
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Convert DataFrame to dictionary
        data_dict = df.to_dict(orient='records')
        
        return data_dict
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

if __name__ == "__main__":
    file_path = r"C:\Users\Haris\Desktop\TEST_INV\New Inventory List.xlsx"
    sheet_name = 0
    data = parse_excel_to_dict(file_path, sheet_name)

    for x in data:
        inv =  InvItem()
        inv.location = x['LOCATION']
        inv.partNo = x['PARTNO']
        inv.partName = x['PARTNAME']
        inv.manufacturer = x['MANUFACTURER']
        inv.application = x['APPLICATION']
        inv.quantity = x['QUANTITY']
        inv.imageURL = x['IMAGEURL']
        inv.tags = x['TAGS']
        db.session.add(inv)
        
    print('DATABASE INITIALIZED')
        
    db.session.commit()