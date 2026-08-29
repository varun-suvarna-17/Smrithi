# 🔥 Firebase Integration Guide

## **Overview**

SMRITHI is configured to use **Firebase Firestore** as the production database. The backend automatically switches from in-memory storage to Firebase when credentials are provided.

---

## **📋 Prerequisites**

- Google Cloud Account (free tier available at [https://cloud.google.com/free](https://cloud.google.com/free))
- Firebase Project created in Google Cloud Console
- Service Account with Firestore access

---

## **🚀 Quick Setup (4 Steps)**

### **Step 1: Create Firebase Project**

1. Go to **[Firebase Console](https://console.firebase.google.com/)**
2. Click **"Create a project"**
3. Enter project name: `SMRITHI` (or your preferred name)
4. Choose region (recommended: closest to your location)
5. Enable/disable Google Analytics (optional)
6. Click **"Create project"**

### **Step 2: Create Firestore Database**

1. In Firebase Console, go to **"Firestore Database"**
2. Click **"Create Database"**
3. Choose: **Start in production mode**
4. Select region (e.g., `us-central1`)
5. Click **"Create"**

⚠️ **Important**: Update Firestore security rules (see below)

### **Step 3: Create Service Account & Download Keys**

1. In Firebase Console, click **⚙️ Settings** (gear icon)
2. Go to **"Service Accounts"** tab
3. Click **"Generate new private key"**
4. A JSON file will download (e.g., `smrithi-xxxxx-firebase-adminsdk-xxxxx-xxxxxxxxxx.json`)
5. **Keep this file secure** - it contains credentials!

### **Step 4: Add Credentials to Project**

**Option A: Direct File (Development)**
```bash
# Copy the downloaded JSON file to backend directory
cp path/to/firebase-adminsdk-xxxxx-xxxxxxxxxx.json c:\Users\Dell\OneDrive\Desktop\SMRITHI\Smrithi\backend\serviceAccountKey.json
```

**Option B: Environment Variable (Recommended)**
```bash
# Set environment variable
$env:FIREBASE_CRED_PATH = "path/to/serviceAccountKey.json"

# Or add to .env file:
FIREBASE_CRED_PATH=./serviceAccountKey.json
```

---

## **🔒 Firestore Security Rules**

### **For Development (Testing)**
```javascript
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    // Allow all reads and writes (DEVELOPMENT ONLY)
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

### **For Production (Secure)**
```javascript
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    // Require authentication for all operations
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
    
    // Patient documents - accessed by patient or assigned caregiver
    match /patients/{patientId} {
      allow read: if request.auth.uid == resource.data.user_id || 
                     request.auth.uid in resource.data.caregiver_ids;
      allow write: if request.auth.uid == resource.data.user_id;
    }
    
    // Caregiver documents - accessed by caregiver or admin
    match /caregivers/{caregiverId} {
      allow read: if request.auth.uid == caregiverId;
      allow write: if request.auth.uid == caregiverId;
    }
  }
}
```

**To Apply Rules:**
1. In Firebase Console → **Firestore Database** → **Rules** tab
2. Copy and paste the rules above
3. Click **"Publish"**

---

## **📊 Firestore Collections Structure**

Your Firestore database will have these collections:

```
firestore/
├── patients/
│   ├── P001/
│   │   ├── name: "Asha Devi"
│   │   ├── age: 72
│   │   ├── mmse_score: 18
│   │   └── ...
│   └── P002/
│
├── caregivers/
│   ├── cg_001/
│   │   ├── name: "Ananya Sharma"
│   │   ├── email: "ananya@example.com"
│   │   └── ...
│
├── sessions/
│   ├── session_001/
│   │   ├── patient_id: "P001"
│   │   ├── game_id: "family_portrait"
│   │   └── ...
│
├── reminders/
├── progress_analytics/
└── game_attempts/
```

---

## **✅ Verify Firebase Connection**

After setting up, check if Firebase is connected:

### **In Backend Logs**
Look for this message when backend starts:
```
Firebase Admin SDK initialized using 'serviceAccountKey.json'.
```

✅ **If you see this**, Firebase is connected and working!

❌ **If you see warning messages**, check:
1. Service account file path is correct
2. File contains valid JSON
3. File has proper permissions

### **Test API with Swagger**
1. Open http://localhost:8000/docs
2. Test any GET endpoint (e.g., `/patients`)
3. If data persists after restart, Firebase is working!

---

## **🔄 Data Migration (MongoDB → Firebase)**

If you have existing MongoDB data, migrate to Firebase:

```python
# Run this script to migrate data
python backend/scripts/migrate_to_firebase.py
```

(Script provided in the repository)

---

## **💻 Frontend Firebase Integration**

### **Web App Configuration**
1. In Firebase Console → **Project Settings** → **General** tab
2. Scroll to **"Your apps"** section
3. Click on Web app
4. Copy Firebase config object
5. Add to `frontend/.env.local`:

```
VITE_FIREBASE_API_KEY=your-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-messaging-sender-id
VITE_FIREBASE_APP_ID=your-app-id
```

The frontend will automatically use Firebase for authentication and real-time data sync.

---

## **🐛 Troubleshooting**

### **"Firebase credentials not found"**
- ✅ Copy `serviceAccountKey.json` to backend directory
- ✅ Set `FIREBASE_CRED_PATH` environment variable
- ✅ Restart backend

### **"Permission denied" errors**
- ✅ Check Firestore security rules
- ✅ Verify service account has Firestore access
- ✅ Enable Firestore API in Google Cloud Console

### **"Invalid JSON credentials"**
- ✅ Download new service account key from Firebase
- ✅ Ensure JSON file is valid (use JSONLint to verify)
- ✅ Check file encoding is UTF-8

### **Still using in-memory database?**
- Backend will warn: `Firebase credential file is missing`
- This means Firebase isn't connected
- Check logs and ensure credentials are set up correctly

---

## **📚 Useful Links**

- **Firebase Console**: https://console.firebase.google.com/
- **Firestore Documentation**: https://firebase.google.com/docs/firestore
- **Service Account Setup**: https://firebase.google.com/docs/admin/setup
- **Security Rules Guide**: https://firebase.google.com/docs/firestore/security/start

---

## **🔐 Important Security Notes**

⚠️ **NEVER commit `serviceAccountKey.json` to Git!**

1. Add to `.gitignore`:
   ```
   serviceAccountKey.json
   *.env
   .env.local
   ```

2. Use environment variables for credentials in production

3. Rotate service account keys regularly

4. Limit service account permissions to Firestore only

---

## **Next Steps**

1. ✅ Create Firebase project
2. ✅ Download service account key
3. ✅ Add credentials to backend
4. ✅ Set Firestore security rules
5. ✅ Test connection
6. ✅ Deploy to production

**All done! Your SMRITHI backend is now using Firebase Firestore! 🎉**
