# Gen Z Translator

A simple single-page web app that translates between standard English and Gen Z slang using AI.

## Features

- **Bidirectional Translation**: Convert normal English to Gen Z speak or vice versa
- **Auto-detection**: Automatically detects the input language style
- **Manual Override**: Choose translation direction manually if needed
- **Copy to Clipboard**: Easy copying of translated text
- **Secure**: API key is stored server-side, never exposed to frontend

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: Vanilla HTML/CSS/JS
- **AI**: OpenRouter API (free models available)
- **Deployment**: Ready for VPS deployment with Gunicorn

## Setup

### Prerequisites

This project can use either **uv** (recommended - faster) or **pip** for dependency management.

#### Option A: Using uv (Recommended)

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Create virtual environment and install dependencies**:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

#### Option B: Using pip

1. **Create virtual environment and install dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Configuration

1. **Copy environment template**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenRouter API key
   ```

2. **Get OpenRouter API Key**:
   - Go to https://openrouter.ai/
   - Create an account (free)
   - Generate an API key
   - Add it to your `.env` file

3. **Run locally**:
   ```bash
   python app.py
   ```
   
   The app will be available at `http://localhost:5000`

## Deployment to VPS

### Using Gunicorn

1. **Install dependencies on your VPS** (choose one):
   
   **Using uv (recommended):**
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```
   
   **Using pip:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Set environment variable** (don't use .env file in production):
   ```bash
   export OPENROUTER_API_KEY=your_api_key_here
   ```

3. **Run with Gunicorn**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Using Systemd (Recommended)

Create a systemd service file `/etc/systemd/system/gen-z-translator.service`:

```ini
[Unit]
Description=Gen Z Translator
After=network.target

[Service]
User=your_user
WorkingDirectory=/path/to/your/app
Environment="OPENROUTER_API_KEY=your_api_key_here"
ExecStart=/path/to/your/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable gen-z-translator
sudo systemctl start gen-z-translator
```

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t gen-z-translator .
docker run -d -p 5000:5000 -e OPENROUTER_API_KEY=your_api_key_here gen-z-translator
```

### Using Nginx as Reverse Proxy

Add to your Nginx config:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Security Notes

- The OpenRouter API key is stored server-side only
- No API keys or sensitive data are exposed to the frontend
- The app uses POST requests for all translation operations
- For production, consider:
  - Using HTTPS (Let's Encrypt)
  - Adding rate limiting
  - Setting up a reverse proxy (Nginx/Apache)
  - Using a firewall (ufw)

## Free Models on OpenRouter

The app uses `openrouter/free` which automatically routes to available free models. This provides:
- Automatic fallback to free models
- No cost for usage
- Good quality for translation tasks

Check https://openrouter.ai/models?tab=free for available free models.

## License

MIT
