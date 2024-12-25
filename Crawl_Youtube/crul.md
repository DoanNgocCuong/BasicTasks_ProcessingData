1. Get transcript from YouTube: 
```bash
# Test API
curl "http://localhost:8080?youtube_url=https://www.youtube.com/watch?v=VIDEO_ID" \
-H "X-API-Key: yt2024_k8hj3n5m9p2q4w7r"
```

6. **Response format**:
```json
{
    "title": "Video Title",
    "description": "Video Description",
    "transcript": "Video Transcript",
    "comments": "Video Comments",
    ...
}
```

Lưu ý:
- Cần có RAPID_API_KEY trong environment variables
- URL YouTube phải hợp lệ
- API key trong header phải đúng
- Video phải có subtitles để lấy transcript
