from connect_PostgresSQLDBeaver import connect_to_database

def query_ratings():
    """
    Query rating data from workflow_node_execution_mindpal table.
    """
    try:
        # Connect to database
        tunnel, connection = connect_to_database()

        # Create cursor and execute query
        cursor = connection.cursor()
        query = """
        WITH tool_nodes AS (
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
                AND execution_metadata::jsonb ? 'rate'
        )
        SELECT *
        FROM public.workflow_node_execution_mindpal
        WHERE workflow_run_id IN (SELECT workflow_run_id FROM tool_nodes);
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # Display results
        print("Query results:")
        for row in results:
            print(row)

        # Close connection
        cursor.close()
        connection.close()
        tunnel.stop()
        print("PostgreSQL and SSH Tunnel connection closed.")

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    query_ratings()
