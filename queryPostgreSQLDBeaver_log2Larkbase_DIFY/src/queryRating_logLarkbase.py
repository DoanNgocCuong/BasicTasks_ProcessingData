import json
import requests
import pandas as pd
from connect_PostgresSQLDBeaver import connect_to_database
from utils_saveQueryExcel import save_query_to_excel

def get_existing_records():
    # Read the latest ratings_only Excel file from query_results folder
    try:
        existing_df = pd.read_excel('query_results/ratings_only_latest.xlsx')
        return existing_df['id'].tolist()  # Return list of existing IDs
    except:
        return []  # Return empty list if file doesn't exist

def save_to_larkbase(new_records):
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
            "base_table_id": "tblvifRIX8c9xGpp"
        },
        "records": []
    }

    # Convert records to Larkbase format
    for record in new_records:
        formatted_record = {
            "fields": {
                "id": str(record[0]),
                "workflow_run_id": str(record[1]),
                "app_id": str(record[2]),
                "title": str(record[3]),
                "node_type": str(record[4]),
                "inputs": str(record[5]),
                "outputs": str(record[6]),
                "provider_id": str(record[7]),
                "user_inputs_text": str(record[8]),
                "rating": str(record[9]),
                "rate_updated_at": str(record[10]),
                "rate_account_id": str(record[11])
            }
        }
        payload["records"].append(formatted_record)

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Successfully saved {len(new_records)} new records to Larkbase")
        else:
            print(f"Error saving to Larkbase: {response.text}")
    except Exception as e:
        print(f"Error making API request: {e}")

def query_ratings():
    try:
        # Get existing records
        existing_ids = get_existing_records()

        # Connect to database and get new results
        tunnel, connection = connect_to_database()
        cursor = connection.cursor()
        query = """
        SELECT 
            id,
            workflow_run_id,
            app_id,
            title,
            node_type,
            inputs,
            outputs,
            execution_metadata::json -> 'tool_info' ->> 'provider_id' AS provider_id,
            execution_metadata::json -> 'user_inputs' ->> '#1733764453822.text#' AS user_inputs_text,
            execution_metadata::json -> 'rate' ->> 'rating' AS rating,
            execution_metadata::json -> 'rate' ->> 'updated_at' AS rate_updated_at,
            execution_metadata::json -> 'rate' ->> 'account_id' AS rate_account_id
        FROM 
            public.workflow_node_execution_mindpal
        WHERE 
            node_type = 'tool' 
            AND execution_metadata::jsonb ? 'rate';
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # Find new records
        new_records = [record for record in results if str(record[0]) not in existing_ids]

        if new_records:
            print(f"Found {len(new_records)} new records")
            # Save new records to Larkbase
            save_to_larkbase(new_records)
            
            # Save all results to Excel
            excel_path = save_query_to_excel(
                results, 
                cursor,
                query_type='ratings_only'
            )
        else:
            print("No new records found")

        # Close connections
        cursor.close()
        connection.close()
        tunnel.stop()
        print("PostgreSQL and SSH Tunnel connection closed.")

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    query_ratings()