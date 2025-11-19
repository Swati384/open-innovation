# 🚀 Deployment Guide for SentiMind

## Option 1: Deploy on Render (Recommended - Free)

### Step 1: Prepare for Web Deployment
Create a `app.py` file to wrap SentiMind as a web API:

```python
from flask import Flask, request, jsonify
from sentimind import SentimentAnalyzer
import os

app = Flask(__name__)
analyzer = SentimentAnalyzer()

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'name': 'SentiMind API',
        'version': '1.0.0',
        'endpoints': {
            'analyze': '/api/analyze',
            'status': '/api/status'
        }
    })

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        result = analyzer.analyze(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({'status': 'running', 'service': 'SentiMind API'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

### Step 2: Update requirements.txt
Add Flask to dependencies:
```
textblob==0.17.1
colorama==0.4.6
click==8.1.7
flask==2.3.0
gunicorn==21.2.0
```

### Step 3: Create Procfile
```
web: gunicorn app:app
```

### Step 4: Deploy to Render
1. Push your code to GitHub
2. Go to [render.com](https://render.com)
3. Sign up with GitHub
4. Click "New +" → "Web Service"
5. Connect your repository
6. Set build command: `pip install -r requirements.txt`
7. Set start command: `gunicorn app:app`
8. Deploy!

Your API will be live at: `https://sentimind.onrender.com/api/analyze`

**Example API Request:**
```bash
curl -X POST https://sentimind.onrender.com/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this!"}'
```

---

## Option 2: Deploy on Railway (Free Tier)

1. Install Railway CLI: `npm install -g @railway/cli`
2. Run: `railway login`
3. Run: `railway init`
4. Run: `railway up`
5. Railway automatically detects Python and deploys!

---

## Option 3: Deploy on Vercel (Python Support)

1. Create `vercel.json`:
```json
{
  "buildCommand": "pip install -r requirements.txt",
  "functions": {
    "api/analyze.py": {
      "runtime": "python3.9"
    }
  }
}
```

2. Push to GitHub
3. Go to [vercel.com](https://vercel.com)
4. Import your repository
5. Deploy!

---

## Option 4: Docker Deployment (Advanced)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t sentimind .
docker run -p 5000:5000 sentimind
```

---

## Local Deployment

### Run as a Background Service (Windows)

Create a batch script `run_sentimind.bat`:
```batch
@echo off
C:\Python314\python.exe sentimind.py interactive
```

Schedule with Task Scheduler for periodic batch analysis.

### Run on Linux/Mac

Create `sentimind.service` for systemd:
```ini
[Unit]
Description=SentiMind Sentiment Analyzer
After=network.target

[Service]
Type=simple
User=username
WorkingDirectory=/path/to/sentimind
ExecStart=/usr/bin/python3 sentimind.py interactive

[Install]
WantedBy=multi-user.target
```

Enable: `sudo systemctl enable sentimind`
Start: `sudo systemctl start sentimind`

---

## Testing Deployed API

### Using curl:
```bash
# Positive sentiment
curl -X POST https://your-api.com/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "This is amazing!"}'

# Negative sentiment
curl -X POST https://your-api.com/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "This is terrible!"}'

# Neutral sentiment
curl -X POST https://your-api.com/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "The weather is nice."}'
```

### Using Python:
```python
import requests

url = "https://your-api.com/api/analyze"
payload = {"text": "I love this tool!"}
response = requests.post(url, json=payload)
print(response.json())
```

### Using JavaScript:
```javascript
fetch('https://your-api.com/api/analyze', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({text: "This is great!"})
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## Best Deployment Choice for You

| Platform | Best For | Cost | Setup Time |
|----------|----------|------|-----------|
| **Render** | REST API | Free | 5 mins |
| **Railway** | CLI + API | Free | 3 mins |
| **Vercel** | Web App | Free | 10 mins |
| **Docker** | Production | Variable | 15 mins |
| **Heroku** | Legacy | $7+/month | 5 mins |

**Recommended:** Start with Render for fastest deployment!

---

## Monitoring & Logs

### Render
- View logs in Render dashboard
- Set up alerts for errors

### Railway
- View logs: `railway logs`
- Monitor in web dashboard

### Local Monitoring
```bash
# Monitor resource usage
python sentimind.py analyze-file large_file.txt
```

---

Happy Deploying! 🚀
