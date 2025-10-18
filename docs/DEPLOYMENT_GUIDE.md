# Deployment Guide for Sales Price Variance Audit Tool 🚀

This guide will walk you through deploying your Streamlit application to the cloud so it's accessible from anywhere.

## Option 1: Streamlit Cloud (Recommended - FREE & EASIEST) ⭐

### Prerequisites
- GitHub account (free)
- Your code in a GitHub repository

### Step-by-Step Instructions

1. **Prepare Your GitHub Repository**
   ```bash
   # Initialize git (if not already done)
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial commit - Sales Audit Tool"
   
   # Create a new repository on GitHub.com (https://github.com/new)
   # Then link and push:
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Choose branch: `main`
   - Main file path: `app.py`
   - Click "Deploy!"

3. **Your App is Live! 🎉**
   - URL will be: `https://YOUR_USERNAME-YOUR_REPO_NAME.streamlit.app`
   - Share this URL with anyone!
   - Free SSL certificate included
   - Automatic updates when you push to GitHub

### Streamlit Cloud Features
- ✅ Free hosting
- ✅ Automatic HTTPS
- ✅ Auto-updates from GitHub
- ✅ Custom domain support (paid plan)
- ✅ Password protection (paid plan)

---

## Option 2: Heroku (FREE Tier Available) 🟣

### Prerequisites
- Heroku account (free)
- Heroku CLI installed

### Files to Create

1. **Procfile** (create in project root):
```
web: sh setup.sh && streamlit run app.py
```

2. **setup.sh** (create in project root):
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

3. **runtime.txt** (create in project root):
```
python-3.11.9
```

### Deployment Steps

```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-app-name

# Deploy
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main

# Open your app
heroku open
```

Your app will be at: `https://your-app-name.herokuapp.com`

---

## Option 3: Railway (Modern & Easy) 🚂

### Steps
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Railway auto-detects Streamlit!
7. App deploys automatically

Features:
- ✅ Free $5 credit monthly
- ✅ Auto-scaling
- ✅ Custom domains
- ✅ Environment variables

---

## Option 4: Google Cloud Run (Scalable) ☁️

### Prerequisites
- Google Cloud account
- Docker installed
- gcloud CLI installed

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Deploy Commands

```bash
# Build image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/sales-audit-app

# Deploy to Cloud Run
gcloud run deploy sales-audit-app \
  --image gcr.io/YOUR_PROJECT_ID/sales-audit-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Your app URL will be provided
```

---

## Option 5: Azure App Service 🔷

### Prerequisites
- Azure account
- Azure CLI installed

### Deployment Steps

```bash
# Login to Azure
az login

# Create resource group
az group create --name sales-audit-rg --location eastus

# Create App Service plan
az appservice plan create --name sales-audit-plan --resource-group sales-audit-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group sales-audit-rg --plan sales-audit-plan --name your-app-name --runtime "PYTHON:3.11"

# Configure deployment
az webapp deployment source config-local-git --name your-app-name --resource-group sales-audit-rg

# Deploy
git remote add azure <DEPLOYMENT_URL_FROM_PREVIOUS_COMMAND>
git push azure main
```

---

## Option 6: DigitalOcean App Platform 🌊

### Steps
1. Sign up at [digitalocean.com](https://www.digitalocean.com)
2. Go to Apps section
3. Click "Create App"
4. Connect your GitHub repository
5. App Platform auto-detects Python/Streamlit
6. Configure:
   - Name: sales-audit-app
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `streamlit run app.py --server.port=8080`
7. Click "Deploy"

Cost: Starting at $5/month

---

## Option 7: Self-Hosting (Your Own Server) 🖥️

### Using a VPS (Ubuntu/Debian)

```bash
# SSH into your server
ssh user@your-server-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip -y

# Clone your repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# Install dependencies
pip3 install -r requirements.txt

# Install and configure Nginx (optional, for domain)
sudo apt install nginx -y

# Run with systemd (persistent)
sudo nano /etc/systemd/system/streamlit.service
```

**systemd service file:**
```ini
[Unit]
Description=Streamlit Sales Audit App
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/your/app
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable streamlit
sudo systemctl start streamlit

# Check status
sudo systemctl status streamlit
```

---

## Comparison Table

| Platform | Cost | Ease | Custom Domain | SSL | Auto-Scale |
|----------|------|------|---------------|-----|------------|
| **Streamlit Cloud** | Free | ⭐⭐⭐⭐⭐ | ✅ (paid) | ✅ | ❌ |
| **Heroku** | Free-$7/mo | ⭐⭐⭐⭐ | ✅ | ✅ | ✅ |
| **Railway** | $5/mo | ⭐⭐⭐⭐⭐ | ✅ | ✅ | ✅ |
| **Google Cloud Run** | Pay-per-use | ⭐⭐⭐ | ✅ | ✅ | ✅ |
| **Azure** | ~$13/mo | ⭐⭐⭐ | ✅ | ✅ | ✅ |
| **DigitalOcean** | $5/mo | ⭐⭐⭐⭐ | ✅ | ✅ | ✅ |
| **Self-Hosted VPS** | $5/mo | ⭐⭐ | ✅ | Manual | Manual |

---

## Recommended Approach for Beginners

**Start with Streamlit Cloud:**
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy in 2 minutes
4. Get free HTTPS URL
5. Share with team!

**For Production/Business:**
- Use **Railway** or **Google Cloud Run** for better control
- Add custom domain
- Enable authentication if needed
- Monitor usage and costs

---

## Environment Variables (for sensitive data)

If you need to store API keys or passwords:

### Streamlit Cloud
1. Go to app settings
2. Click "Secrets"
3. Add secrets in TOML format:
```toml
[passwords]
admin = "your_password_here"
```

### Other Platforms
Set environment variables in platform dashboard or via CLI:
```bash
heroku config:set SECRET_KEY=your_secret_here
```

---

## Troubleshooting

### App not starting
- Check requirements.txt has all dependencies
- Verify Python version compatibility
- Check logs in platform dashboard

### Slow performance
- Upgrade to paid tier for more resources
- Optimize data loading (use caching)
- Consider Cloud Run for auto-scaling

### Custom domain not working
- Verify DNS settings (CNAME or A record)
- Wait for DNS propagation (up to 48 hours)
- Check SSL certificate status

---

## Post-Deployment Checklist ✅

- [ ] App loads without errors
- [ ] File upload works correctly
- [ ] Download functionality works
- [ ] Charts display properly
- [ ] Mobile responsive (test on phone)
- [ ] Share URL with stakeholders
- [ ] Set up monitoring/alerts (optional)
- [ ] Add Google Analytics (optional)

---

## Support & Updates

To update your deployed app:
```bash
git add .
git commit -m "Update: description of changes"
git push origin main
```

Most platforms auto-deploy on push!

---

**Need help?** Check platform documentation:
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [Heroku Python Docs](https://devcenter.heroku.com/articles/getting-started-with-python)
- [Railway Docs](https://docs.railway.app/)

Good luck with your deployment! 🚀
