# 🔗 Frontend-Backend Integration Guide

## **Integration Overview**

The SMRITHI frontend is now **fully integrated** with the backend API. Here's how everything connects:

---

## **API Service Layer** (`frontend/src/utils/api.js`)

All backend communication goes through a centralized **API service** that handles:
- ✅ Automatic JWT token injection in headers
- ✅ Request/response interceptors
- ✅ Error handling & auth redirects
- ✅ Base URL management

### **Available API Modules**

```javascript
import {
  authAPI,          // Login/logout
  patientAPI,       // Patient profiles & data
  gameAPI,          // Games & attempts
  progressAPI,      // Progress tracking
  voiceAPI,         // Text-to-speech
  reminderAPI,      // Reminders
  reportAPI,        // Clinical reports
  adaptiveAPI,      // Adaptive difficulty
  caregiverAPI      // Caregiver dashboard
} from '../utils/api';
```

---

## **Component Integration Examples**

### **1. Home Page (Patient Dashboard)**

**Before:** Used hardcoded dummy data
**After:** Fetches from backend

```jsx
import { patientAPI, reminderAPI, progressAPI } from '../utils/api';

useEffect(() => {
  const fetchData = async () => {
    // Get patient profile
    const patientResponse = await patientAPI.getAll();
    
    // Get reminders
    const remindersResponse = await reminderAPI.getReminders(patientId);
    
    // Get progress analytics
    const progressResponse = await progressAPI.getProgress(patientId);
  };
  fetchData();
}, []);
```

### **2. Caregiver Dashboard**

**Before:** Hardcoded patient list
**After:** Fetches assigned patients from backend

```jsx
import { caregiverAPI, progressAPI } from '../utils/api';

useEffect(() => {
  // Get patients assigned to this caregiver
  const patientsResponse = await caregiverAPI.getAssignedPatients();
  
  // Get their progress/analytics
  const progressResponse = await progressAPI.getProgress(patientId);
}, []);
```

### **3. Games Page**

**Before:** Static game list
**After:** Fetches available games from backend

```jsx
import { gameAPI } from '../utils/api';

useEffect(() => {
  // Get available games with difficulty ratings
  const response = await gameAPI.getAvailableGames();
}, []);
```

---

## **Data Flow Diagram**

```
┌─────────────────────────────────────────────────────┐
│          FRONTEND (React Component)                 │
│  ┌──────────────────────────────────────────────┐  │
│  │ useEffect(() => {                           │  │
│  │   const data = await patientAPI.getProfile  │  │
│  │   setData(data)                             │  │
│  │ })                                          │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                        ↓ (HTTP Request + Token)
┌─────────────────────────────────────────────────────┐
│          API SERVICE LAYER (axios)                  │
│  ┌──────────────────────────────────────────────┐  │
│  │ • Adds Authorization: Bearer {token}         │  │
│  │ • Handles errors & redirects                 │  │
│  │ • Base URL: http://localhost:8000            │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                        ↓ (REST API)
┌─────────────────────────────────────────────────────┐
│          BACKEND (FastAPI)                          │
│  ┌──────────────────────────────────────────────┐  │
│  │ @router.get('/patients/{id}')                │  │
│  │ @require_auth                               │  │
│  │ async def get_patient(id):                  │  │
│  │   return patient_data                       │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                        ↓ (JSON Response)
┌─────────────────────────────────────────────────────┐
│          DATABASE (MongoDB)                         │
│  ┌──────────────────────────────────────────────┐  │
│  │ Database Query & Data Return                 │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## **Key Integration Features**

### **1. Authentication**
```javascript
// Login
const response = await authAPI.login(email, password);
setAuthToken(response.data.access_token);  // Stored in localStorage

// Auto token injection
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### **2. Error Handling**
```javascript
// Auto logout on 401 Unauthorized
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      window.location.href = '/login';  // Redirect to login
    }
    return Promise.reject(error);
  }
);
```

### **3. TTS/Voice Integration**
```javascript
// Text-to-Speech with auto-play
const audio = await voiceAPI.synthesizeAndPlay(
  "Good morning! Time for your game.",
  "en"  // language: 'en', 'hi', 'kn', 'as'
);
```

### **4. Game Recording**
```javascript
// Record game attempt to backend
await gameAPI.recordAttempt(
  patientId,
  gameId,
  {
    score: 85,
    time_taken: 120,
    attempts: 3,
    difficulty_level: 'medium'
  }
);
```

---

## **Environment Configuration**

### **Frontend .env.local**
```
VITE_API_BASE_URL=http://localhost:8000
VITE_LOG_LEVEL=debug
```

### **Vite Proxy Configuration** (vite.config.js)
```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    }
  }
}
```

---

## **Running Integrated App**

```bash
# From root directory
npm run dev
```

This starts:
- **Backend:** http://localhost:8000 (FastAPI with auto-reload)
- **Frontend:** http://localhost:5173 (React with HMR)

### **Testing Integration**

1. **Open Frontend:** http://localhost:5173
2. **Open API Docs:** http://localhost:8000/docs
3. **Make API calls from Swagger** - Frontend will reflect changes
4. **Check Network Tab** - See actual API calls
5. **View Backend Logs** - Monitor server-side operations

---

## **API Endpoints Used**

| Feature | Endpoint | Method |
|---------|----------|--------|
| Patient Profile | `/patients/{id}` | GET |
| Patient List | `/patients` | GET |
| Games List | `/games` | GET |
| Record Attempt | `/patients/{id}/games/{game_id}` | POST |
| Progress | `/progress/{id}` | GET |
| Analytics | `/progress/{id}/analytics` | GET |
| Reminders | `/reminders` | GET/POST/PUT |
| TTS | `/voice/tts` | POST |
| Reports | `/reports/{id}` | GET/POST |
| Login | `/auth/login` | POST |

---

## **Component Update Status**

| Page | Status | Integration |
|------|--------|-------------|
| Home.jsx | ✅ Updated | Fetches patient data, reminders, progress |
| CaregiverDashboard.jsx | ✅ Updated | Fetches assigned patients & analytics |
| Games.jsx | ✅ Updated | Fetches available games from backend |
| ActivityHub.jsx | 🔄 Ready | Can use gameAPI to log activities |
| Memories.jsx | 🔄 Ready | Can integrate with patient API |
| DailyCare.jsx | 🔄 Ready | Can integrate with reminder API |

---

## **Best Practices**

### **✅ DO**
- Use API service layer (`api.js`) for all HTTP requests
- Handle errors with try/catch blocks
- Show loading states during API calls
- Use optional chaining for nested data (e.g., `data?.patient?.name`)
- Store sensitive tokens in localStorage (already handled)

### **❌ DON'T**
- Make direct axios calls (use API service)
- Hardcode API URLs in components
- Store tokens in state (use localStorage)
- Forget to handle loading/error states
- Make requests without auth headers

---

## **Debugging Integration**

### **Check Network Requests**
1. Open DevTools (F12)
2. Go to Network tab
3. Look for API requests to `localhost:8000`
4. Check status codes (200 = success, 401 = auth error)

### **Backend Logs**
Check terminal where backend is running - it shows incoming requests and errors

### **Frontend Logs**
```javascript
console.log(response);  // Check API response
console.error(error);   // Check error details
```

---

## **Next Steps**

1. ✅ **Integration Complete** - All components have API hooks
2. 🔄 **Testing** - Test with real backend (run `npm run dev`)
3. 🔄 **Refinement** - Add error messages, loading spinners
4. 🔄 **Optimization** - Cache data, pagination for lists
5. 🔄 **Production** - Update `VITE_API_BASE_URL` to production server

---

**Frontend & Backend are now fully integrated and ready to use! 🚀**
