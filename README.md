# 🚨 Stop Putting Sensitive Information On Public Tools like Wheregoes.com

## ⚡ Overview
This project automates the tracking of URLs by scraping and logging them. If a URL contains trigger keywords (e.g., `X`, `Y`), it alerts a designated Discord channel via a webhook.

This project was developed in response to a security concern: users may inadvertently disclose sensitive links when utilizing public URL tracing services.

## ⚙️ Configuration

### 1. Set Up Discord Webhook
Replace the placeholder webhook URL in `DISCORD_WEBHOOK_URL`:
```python
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
```

### 2. Define Trigger Keywords
Modify the list of trigger keywords to match the URLs you want to monitor:
```python
TRIGGER_KEYWORDS = ["X", "Y"]
```

### 3. Change Page ID
Modify the page ID from which you want to start:
```python
page_id = YOUR_STARTING_PAGE_ID
```

## ⚠️ Disclaimer
This project is provided **as-is** for informational and educational purposes only. The developers and contributors assume **no liability** for any misuse, unintended consequences, or legal issues arising from its use. 

Users are solely responsible for ensuring that their activities comply with applicable laws, regulations, and ethical standards. By using this project, you agree that the authors shall not be held liable for any damages, 
direct or indirect, resulting from its use or misuse.

