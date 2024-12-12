`python -m venv .venv`

Cách 2. Build 
```bash
cd src/backend
docker build -t query-api .
docker run -d -p 5000:5000 -v ${pwd}/api/scripts/query_results:/app/api/scripts/query_results query-api
```


============
Đây là các lệnh curl để test API:

1. Health check:
````bash
curl http://localhost:5000/health
````

2. Chạy script rating:
````bash
curl -X POST http://localhost:5000/api/scripts/run/queryRating_logLarkbase
````

3. Chạy script workflow:
````bash
curl -X POST http://localhost:5000/api/scripts/run/queryRatingToolsWorkflowMindpal_logLarkbase
````

4. Để xem output chi tiết hơn (Windows PowerShell):
````powershell
# Health check
curl -v http://localhost:5000/health | ConvertFrom-Json | Format-List

# Run rating script
curl -v -X POST http://localhost:5000/api/scripts/run/queryRating_logLarkbase | ConvertFrom-Json | Format-List

# Run workflow script
curl -v -X POST http://localhost:5000/api/scripts/run/queryRatingToolsWorkflowMindpal_logLarkbase | ConvertFrom-Json | Format-List
````

5. Nếu dùng Windows CMD:
````batch
:: Health check
curl -v http://localhost:5000/health

:: Run rating script
curl -v -X POST http://localhost:5000/api/scripts/run/queryRating_logLarkbase

:: Run workflow script
curl -v -X POST http://localhost:5000/api/scripts/run/queryRatingToolsWorkflowMindpal_logLarkbase
````

Flag `-v` sẽ hiển thị thông tin chi tiết về request/response, giúp debug nếu có lỗi. Response sẽ có dạng:
```json
{
    "success": true,
    "message": "Script executed successfully",
    "output": "Found 100 total records in database..."
}
```

hoặc nếu có lỗi:
```json
{
    "success": false,
    "error": "Error message here",
    "stdout": "Any output before error..."
}
```
