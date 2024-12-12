import csv
import os

def save_query_to_csv(results, output_filename='query_results.csv', headers=None):
    """
    Save query results to a CSV file.

    Args:
        results (list): List of query result rows
        output_filename (str, optional): Name of the output CSV file. Defaults to 'query_results.csv'.
        headers (list, optional): List of column headers. If None, no headers will be written.
    """
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    try:
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            
            # Write headers if provided
            if headers:
                csv_writer.writerow(headers)
            
            # Write data rows
            csv_writer.writerows(results)
        
        print(f"Query results saved to {output_filename}")
        return True
    
    except Exception as e:
        print(f"Error saving CSV file: {e}")
        return False 