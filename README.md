
# Image Chatbot App

A Streamlit-based image analysis chatbot powered by Google's Gemini AI.

## Features

- Upload images or use image URLs
- Chat with AI about images
- Customize chatbot behavior and personality
- Download chat history
- Beautiful, modern UI

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory:
```
API_KEY=your_google_gemini_api_key_here
```

3. Run the app:
```bash
streamlit run app.py
```

## Deployment Options

> **Note:** Vercel is not suitable for Streamlit apps. Vercel is designed for Next.js/React apps, not Python web applications like Streamlit. Use one of the options below instead.

### Option 1: Streamlit Community Cloud (Recommended - Easiest & Free)

1. **Push to GitHub:**
   - Create a new repository on GitHub
   - Push your code (but NOT the `.env` file - add it to `.gitignore`)
   ```bash
   git init
   git add app.py requirements.txt README.md
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/your-repo.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set Main file path: `app.py`
   - Add your API key in "Secrets" section:
     ```
     API_KEY=your_google_gemini_api_key_here
     ```
   - Click "Deploy"

3. **Your app will be live at:** `https://your-app-name.streamlit.app`

### Option 2: Render (Free Tier Available)

1. **Push to GitHub** (same as Option 1)

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Sign up/login with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** your-app-name
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
   - Add environment variable: `API_KEY` = your_api_key
   - Click "Create Web Service"

3. **Your app will be live at:** `https://your-app-name.onrender.com`

### Option 3: Railway (Simple & Fast)

1. **Push to GitHub** (same as Option 1)

2. **Deploy on Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign up/login with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Add environment variable: `API_KEY` = your_api_key
   - Railway auto-detects Python and installs dependencies
   - Update start command in settings: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

3. **Your app will be live** (Railway provides a URL)

### Option 4: Docker

1. Create `Dockerfile`:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8501
   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. Build and run:
   ```bash
   docker build -t image-chatbot .
   docker run -p 8501:8501 -e API_KEY=your_api_key image-chatbot
   ```

### Option 5: AWS/Azure/GCP

- Use container services (ECS, Azure Container Instances, Cloud Run)
- Or use EC2/VM with Streamlit installed
- Set environment variable `API_KEY` in your cloud platform

## Environment Variables

- `API_KEY`: Your Google Gemini API key (required)

## Security Notes

- **Never commit your `.env` file to Git**
- Add `.env` to `.gitignore`
- Use platform secrets/environment variables for API keys in production

## Troubleshooting

- If models aren't found: The app will automatically detect available models
- If API errors occur: Check your API key and quota limits
- For deployment issues: Ensure all dependencies are in `requirements.txt`

