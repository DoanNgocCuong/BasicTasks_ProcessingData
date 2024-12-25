The error you're seeing is a 401 Unauthorized error, which means the authentication with Airtable failed. This is happening because the `AIRTABLE_API_KEY` is empty in your code.

Here's what you need to fix:

```python:tiktok_4_download_video.ipynb
# Airtable credentials
AIRTABLE_BASE_ID = 'app7mcJMf9O8GQRal'
AIRTABLE_API_KEY = ''  # You need to add your Airtable API key here
```

To resolve this:

1. Go to your Airtable account
2. Get your API key from your account settings (you can find this at https://airtable.com/account)
3. Insert the API key into the `AIRTABLE_API_KEY` variable

Also, I notice that `TIKTOK_API_KEY` is empty as well. You'll need to:

```python:tiktok_4_download_video.ipynb
# TikTok API credentials
TIKTOK_API_KEY = ""  # Add your RapidAPI key for the TikTok API here
```

Get your RapidAPI key from:
1. Go to RapidAPI
2. Subscribe to the TikTok API service
3. Copy your API key from your RapidAPI dashboard
4. Insert it into the `TIKTOK_API_KEY` variable

Without both of these API keys properly set, the script won't be able to authenticate with either service.
