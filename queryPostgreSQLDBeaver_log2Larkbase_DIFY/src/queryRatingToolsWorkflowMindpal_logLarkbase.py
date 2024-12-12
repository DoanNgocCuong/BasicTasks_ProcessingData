import pandas as pd
import os
from utils_saveToLarkbase import save_workflow_tools_to_larkbase
from utils_query import execute_query_with_connection, query_workflow_tools_data

def get_existing_records():
    """Get records from workflow_tools.xlsx file"""
    try:
        excel_path = './query_results/workflow_tools.xlsx'
        if not os.path.exists(excel_path):
            print(f"File not found: {excel_path}")
            return pd.DataFrame()
            
        existing_df = pd.read_excel(excel_path)
        print(f"Found {len(existing_df)} existing records in workflow_tools.xlsx")
        return existing_df
    except Exception as e:
        print(f"Error reading workflow_tools.xlsx: {e}")
        return pd.DataFrame()

def compare_and_find_changes(existing_df, new_df):
    """Compare existing and new data to find execution_metadata changes"""
    if existing_df.empty:
        print("No existing data - all records are new")
        return new_df

    # Convert IDs to string for comparison
    existing_df['id'] = existing_df['id'].astype(str)
    new_df['id'] = new_df['id'].astype(str)
    
    # Find new records
    new_records = new_df[~new_df['id'].isin(existing_df['id'])]
    if not new_records.empty:
        print(f"\nFound {len(new_records)} new records")
    
    # Find updated execution_metadata
    changed_records = []
    for _, new_record in new_df[new_df['id'].isin(existing_df['id'])].iterrows():
        old_record = existing_df[existing_df['id'] == new_record['id']].iloc[0]
        
        # Only compare execution_metadata field
        if str(old_record['execution_metadata']) != str(new_record['execution_metadata']):
            print(f"\nExecution metadata changed for record ID {new_record['id']}")
            changed_records.append(new_record)
    
    if changed_records:
        changed_df = pd.DataFrame(changed_records)
        return pd.concat([new_records, changed_df], ignore_index=True)
    
    return new_records if not new_records.empty else pd.DataFrame(columns=new_df.columns)

def query_tools_in_workflow():
    """Query and update workflow tools data"""
    try:
        # Get existing records
        existing_df = get_existing_records()

        # Get new data from database
        new_df = execute_query_with_connection(query_workflow_tools_data)
        if new_df.empty:
            return

        # Find changes
        changed_records_df = compare_and_find_changes(existing_df, new_df)

        if not changed_records_df.empty:
            # Save changes to Larkbase
            save_workflow_tools_to_larkbase(changed_records_df.values.tolist())
            
            # Update Excel file
            excel_path = './query_results/workflow_tools.xlsx'
            all_records = pd.concat([existing_df, changed_records_df], ignore_index=True)
            all_records.to_excel(excel_path, index=False)
            print(f"Updated Excel file with {len(changed_records_df)} new/modified records")
        else:
            print("No changes to save")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    query_tools_in_workflow() 