<div align="center">
  <img src="https://img.shields.io/badge/API-Pulse-FF3366?style=for-the-badge&logo=apache&logoColor=white" alt="API Pulse Logo" />
  
  <h1>⚡ API-Pulse</h1>
  <p><b>An Open-Source, High-Performance API Load Testing Dashboard</b></p>
  
  <p>
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
    <img src="https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E" alt="Vite" />
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  </p>

  <p>
    <a href="#features">Features</a> •
    <a href="#quick-start">Quick Start</a> •
    <a href="#architecture">Architecture</a>
  </p>
</div>

---

## 🚨 Why API-Pulse?
Stop using boring command-line tools to load test your APIs. **API-Pulse** gives you the sheer asynchronous power of `aiohttp` combined with a gorgeous, real-time React dashboard. Bombard your servers with thousands of requests per second and watch your server's breaking point visualize in real-time.

## ✨ Features
- **⚡ Extreme Throughput**: Built on Python's `asyncio` and `aiohttp`, capable of generating thousands of concurrent requests effortlessly.
- **🖥️ Stunning Real-Time Dashboard**: A glassmorphism React interface powered by Recharts that visualizes RPS and Latency live.
- **🔌 WebSocket Integration**: Near-instantaneous metric delivery from the load testing engine to your browser.
- **🧱 Zero Configuration**: No complex YAML files or scripts to write. Just enter your URL, set concurrency, and click *Launch Attack*.

## 🚀 Quick Start (Run it in 30 seconds)

### 1. Start the Backend Engine (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. Start the Frontend Dashboard (Vite)
Open a new terminal window:
```bash
cd frontend
npm install
npm run dev
```
*The beautiful UI is now live at `http://localhost:5173`.*

## 📄 License
MIT License. Completely free, forever. 
