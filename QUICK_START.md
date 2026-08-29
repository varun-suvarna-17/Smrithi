# 🚀 Quick Start Guide - Run SMRITHI with One Click/Command

## **Easiest Way to Run Everything**

### **Option 1: Double-Click (Easiest) 🖱️**

**Windows (Batch File):**
```
Double-click: run-app.bat
```

This file is in the root directory. Just double-click it and it will:
1. ✅ Check Node.js and Python are installed
2. ✅ Install all dependencies (root, backend, frontend)
3. ✅ Start Backend API (localhost:8000)
4. ✅ Start Frontend (localhost:5173)
5. ✅ Open Swagger Docs at localhost:8000/docs

---

### **Option 2: PowerShell Command (Windows) 💻**

```powershell
# Run from project root directory
.\run-app.ps1
```

Or run directly:
```powershell
cd c:\Users\Dell\OneDrive\Desktop\SMRITHI\Smrithi
.\run-app.ps1
```

---

### **Option 3: npm Command (Terminal) ⚡**

```bash
npm run dev
```

**From root directory only:**
```bash
cd c:\Users\Dell\OneDrive\Desktop\SMRITHI\Smrithi
npm run dev
```

---

### **Option 4: Manual Commands (If Scripts Fail)**

```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

---

## **What Gets Started**

When you run any of the above commands, you'll see:

| Component | URL | Description |
|-----------|-----|-------------|
| **Frontend** | http://localhost:5173 | React app for caregivers |
| **Backend API** | http://localhost:8000 | FastAPI REST API |
| **API Docs** | http://localhost:8000/docs | Interactive Swagger UI |
| **ReDoc** | http://localhost:8000/redoc | Alternative API documentation |

---

## **Troubleshooting**

### "Node.js is not installed"
- Download from: https://nodejs.org/
- Then restart the script

### "Python is not installed"
- Download from: https://www.python.org/
- Then restart the script

### "Port 8000/5173 already in use"
- Change port in files:
  - Backend: `backend/app/core/config.py` (PORT variable)
  - Frontend: `frontend/vite.config.js` (server.port)

### "Module not found" errors
- Delete `node_modules` folders and `venv`
- Re-run the script (it will reinstall everything)

---

## **Stop the Application**

- Press `Ctrl + C` in the terminal where the app is running
- Or close the terminal window

---

## **First Time Setup (One-Time)**

```bash
npm run install:all
```

This installs:
- Root npm packages (concurrently)
- Backend Python packages
- Frontend npm packages

Then run:
```bash
npm run dev
```

---

## **Next Steps After Starting**

1. **Open Frontend:** http://localhost:5173
2. **View API Docs:** http://localhost:8000/docs
3. **Test Backend:** Use Swagger UI or Postman
4. **Check Backend Logs:** Watch the terminal for API logs

---

## **Development**

- **Edit Frontend:** Changes auto-reload (Vite HMR)
- **Edit Backend:** Changes auto-reload (Uvicorn `--reload`)
- **Kill and Restart:** Press `Ctrl+C` to stop, then re-run script

---

**Enjoy developing with SMRITHI! 🎉**
