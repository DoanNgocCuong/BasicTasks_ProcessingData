```bash
curl --location 'http://127.0.0.1:5000/api/create-many-records' \
--header 'Content-Type: application/json' \
--data '{
    "config": {
        "app_id": "cli_a7852e8dc6fc5010",
        "app_secret": "6SIj0RfQ0ZwROvUhkjAwLebhLfJkIwnT",
        "app_base_token": "O3EybGW4TaQ1SusAtukl9RXzgJd",
        "base_table_id": "tblwZ1BvvVgP4Ot7"
    },
    "records": [
        {
            "fields": {
                "user_name": "Example Text 1",
                "stt_question": 1
            }
        },
        {
            "fields": {
                "user_name": "Example Text 2",
                "stt_question": 2
            }
        }
    ]
}'
```

hoặc 
```bash
curl --location 'http://127.0.0.1:5000/api/create-many-records' \
--header 'Content-Type: application/json' \
--data '{
    "config": {
        "app_doannngoccuong_id": "cli_a7852e8dc6fc5010",
        "app_doannngoccuong_secret": "6SIj0RfQ0ZwROvUhkjAwLebhLfJkIwnT",
        "app_base_token": "O3EybGW4TaQ1SusAtukl9RXzgJd",
        "base_table_id": "tblwZ1BvvVgP4Ot7"
    },
    "records": [
        {
            "fields": {
                "user_name": "Example Text 1",
                "stt_question": 1
            }
        },
        {
            "fields": {
                "user_name": "Example Text 2",
                "stt_question": 2
            }
        }
    ]
}'
```

hoặc 
```bash
{
    "config": {
        "appid": "cli_a7852e8dc6fc5010",
        "appsecret": "6SIj0RfQ0ZwROvUhkjAwLebhLfJkIwnT",
        "app_base_token": "O3EybGW4TaQ1SusAtukl9RXzgJd",
        "base_table_id": "tblwZ1BvvVgP4Ot7"
    },
    "records": [
        {
            "fields": {
                "user_name": "Example Text 1",
                "stt_question": 1
            }
        },
        {
            "fields": {
                "user_name": "Example Text 2",
                "stt_question": 2
            }
        }
    ]
}
```



@im lặng
chị Mai Anh, em mới ĐÓNG THÀNH 1 API duy nhất như này, 
----------------
Sau log lên lark cho tiện ạ. 
-------------
- app_id, app secret là id, secret của App (chẳng hạn: app blue-scrape, ...) <điều kiện: Cần add Application App vào trang Base đích >