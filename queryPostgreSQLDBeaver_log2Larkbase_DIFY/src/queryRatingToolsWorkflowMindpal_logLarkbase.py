import json
import requests
import pandas as pd
import os
from connect_PostgresSQLDBeaver import connect_to_database
from utils_saveQueryExcel import save_query_to_excel

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

def save_to_larkbase(new_records):
    """Save new records to Larkbase via API"""
    url = 'http://103.253.20.13:25033/api/larkbase/create-many-records'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic KyVZLSVtLSVkVCVIOiVN'
    }
    
    payload = {
        "config": {
            "app_id": "cli_a7852e8dc6fc5010",
            "app_secret": "6SIj0RfQ0ZwROvUhkjAwLebhLfJkIwnT", 
            "app_base_token": "BtGmbls2CaqfHnsuwxelJNlpgvb",
            "base_table_id": "tblcmmgOlAYW4dXS"
        },
        "records": [
            {
                "fields": {
                    "id": str(record[0]),
                    "tenant_id": str(record[1]),
                    "app_id": str(record[2]),
                    "workflow_id": str(record[3]),
                    "triggered_from": str(record[4]),
                    "workflow_run_id": str(record[5]),
                    "workflow_node_execution_id": str(record[6]),
                    "index": str(record[7]),
                    "predecessor_node_id": str(record[8]),
                    "node_id": str(record[9]),
                    "node_type": str(record[10]),
                    "title": str(record[11]),
                    "inputs": str(record[12]),
                    "process_data": str(record[13]),
                    "outputs": str(record[14]),
                    "status": str(record[15]),
                    "error": str(record[16]),
                    "elapsed_time": str(record[17]),
                    "execution_metadata": str(record[18]),
                    "created_at": str(record[19]),
                    "created_by_role": str(record[20]),
                    "created_by": str(record[21]),
                    "finished_at": str(record[22]),
                    "node_execution_id": str(record[23])
                }
            } for record in new_records
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Successfully saved {len(new_records)} new records to Larkbase")
        else:
            print(f"Error saving to Larkbase: {response.text}")
    except Exception as e:
        print(f"Error making API request: {e}")

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
    tunnel = connection = cursor = None
    try:
        # Get existing records
        existing_df = get_existing_records()

        # Connect to database
        tunnel, connection = connect_to_database()
        cursor = connection.cursor()
        
        # Query database
        query = """
        WITH tool_nodes AS (
            SELECT *
            FROM public.workflow_node_execution_mindpal
            WHERE node_type = 'tool' 
            AND execution_metadata::jsonb ? 'rate'
        )
        SELECT *
        FROM public.workflow_node_execution_mindpal
        WHERE workflow_run_id IN (SELECT workflow_run_id FROM tool_nodes);
        """
        cursor.execute(query)
        
        # Convert results to DataFrame with all columns
        columns = [desc[0] for desc in cursor.description]
        new_df = pd.DataFrame(cursor.fetchall(), columns=columns)
        print(f"\nFound {len(new_df)} total records in database")

        # Find changes
        changed_records_df = compare_and_find_changes(existing_df, new_df)

        if not changed_records_df.empty:
            # Save changes to Larkbase
            save_to_larkbase(changed_records_df.values.tolist())
            
            # Update Excel file
            excel_path = './query_results/workflow_tools.xlsx'
            all_records = pd.concat([existing_df, changed_records_df], ignore_index=True)
            all_records.to_excel(excel_path, index=False)
            print(f"Updated Excel file with {len(changed_records_df)} new/modified records")
        else:
            print("No changes to save")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up connections
        if cursor: cursor.close()
        if connection: connection.close()
        if tunnel: tunnel.stop()
        print("Connections closed.")

if __name__ == "__main__":
    query_tools_in_workflow() 