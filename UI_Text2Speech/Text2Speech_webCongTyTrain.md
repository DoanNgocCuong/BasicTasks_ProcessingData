http://103.253.20.14:8093/demo/path

========


Đây là cách gọi API bằng cURL:

```bash
curl -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=Xin chào tất cả mọi người&voiceId=Jenifer" \
     http://localhost/
```

Các phiên bản khác:

1. Sử dụng giọng Harry Kane:
```bash 
curl -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=Xin chào tất cả mọi người&voiceId=Kane" \
     http://localhost/
```

2. Sử dụng giọng Alloy:
```bash
curl -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=Xin chào tất cả mọi người&voiceId=Alloy" \
     http://localhost/
```

3. Với văn bản tiếng Anh:
```bash
curl -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=Hello everyone&voiceId=Jenifer" \
     http://localhost/
```

Lưu ý:
- Thay `http://localhost/` bằng URL thực tế của API
- API sẽ trả về file âm thanh (audio file) chứa giọng nói được tổng hợp
- API hỗ trợ cả tiếng Việt và tiếng Anh
- Content-Type phải là application/x-www-form-urlencoded

Bạn cần thêm thông tin gì về cách gọi API không?