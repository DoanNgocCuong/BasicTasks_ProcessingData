1. Có cách nào để import nguyên 1 file excel lên Larkbase không??? 

2. Không thì xài cách cơ bản: 

```bash
curl --location 'http://103.253.20.13:25033/api/larkbase/create-many-records' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic KyVZLSVtLSVkVCVIOiVN' \
--data '{
    "config": {
        "app_id": "cli_a7852e8dc6fc5010",
        "app_secret": "6SIj0RfQ0ZwROvUhkjAwLebhLfJkIwnT",
        "app_base_token": "BtGmbls2CaqfHnsuwxelJNlpgvb",
        "base_table_id": "tblvifRIX8c9xGpp"
    },
    "records": [
        {
            "fields": {
                "Id": "lesson123",
                "Workflow name": "This is a test feedback"
            }
        }
    ]
}'
```


### log_rating_toLarkbase

- Sau khi return ra results. 
- So sánh results này so với file query_results/ratings_only
- Nếu nó có thêm dòng nào, thì lưu dòng đó vào Larkbase bằng API 
Dựa vào Query DBeaver -> python lưu data vào CSV không ổn - Excel oke (results thu được check với file Excel cũ, nếu có dòng mới sẽ lưu dòng mới đó vào Excel và Larkbase thông qua API). 

```
curl --location 'http://103.253.20.13:25033/api/larkbase/create-many-records' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic KyVZLSVtLSVkVCVIOiVN' \
--data '{
    "config": {
        "app_id": "cli_a7852e8dc6fc5010",
        "app_secret": "6SIj0RfQ0ZwROvUhkjAwLebhLfJkIwnT",
        "app_base_token": "BtGmbls2CaqfHnsuwxelJNlpgvb",
        "base_table_id": "tblvifRIX8c9xGpp"
    },
    "records": [
        {
            "fields": {
                "id": "id_value",
                "workflow_run_id": "workflow_run_id_value", 
                "app_id": "app_id_value",
                "title": "title_value",
                "node_type": "node_type_value",
                "inputs": "inputs_value",
                "outputs": "outputs_value",
                "provider_id": "provider_id_value",
                "user_inputs_text": "user_inputs_text_value",
                "rating": "rating_value",
                "rate_updated_at": "rate_updated_at_value",
                "rate_account_id": "rate_account_id_value"
            }
        }
    ]
}'
```