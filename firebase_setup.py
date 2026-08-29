#!/usr/bin/env python3
"""
SMRITHI Firebase Setup Helper Script
This script helps configure Firebase credentials and verify the connection.
"""

import os
import json
import sys
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_firebase_file():
    """Check if Firebase credentials file exists"""
    backend_dir = Path(__file__).parent / "backend"
    cred_file = backend_dir / "serviceAccountKey.json"
    
    print_header("Checking Firebase Credentials")
    
    if cred_file.exists() and cred_file.stat().st_size > 0:
        print(f"✅ Found: {cred_file}")
        try:
            with open(cred_file) as f:
                cred = json.load(f)
            print(f"✅ Valid JSON")
            print(f"   Project ID: {cred.get('project_id', 'N/A')}")
            print(f"   Service Account: {cred.get('client_email', 'N/A')}")
            return True
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON format")
            return False
    else:
        print(f"❌ Not found: {cred_file}")
        print("\n📋 Steps to add Firebase credentials:")
        print("   1. Download serviceAccountKey.json from Firebase Console")
        print("   2. Place it in: backend/serviceAccountKey.json")
        print("   3. OR set FIREBASE_CRED_PATH environment variable")
        return False


def check_environment_variable():
    """Check if FIREBASE_CRED_PATH environment variable is set"""
    print_header("Checking Environment Variable")
    
    cred_path = os.getenv("FIREBASE_CRED_PATH")
    
    if cred_path:
        print(f"✅ FIREBASE_CRED_PATH is set: {cred_path}")
        if os.path.exists(cred_path):
            print(f"✅ File exists at path")
            return True
        else:
            print(f"❌ File not found at path")
            return False
    else:
        print("⚠️  FIREBASE_CRED_PATH not set")
        print("   Backend will look for: backend/serviceAccountKey.json")
        return None


def check_dependencies():
    """Check if Firebase dependencies are installed"""
    print_header("Checking Dependencies")
    
    required = ["firebase_admin", "google_cloud_firestore"]
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n📦 Install missing packages:")
        print(f"   pip install {' '.join(missing)}")
        return False
    return True


def check_firestore_rules():
    """Provide guidance on Firestore security rules"""
    print_header("Firestore Security Rules")
    
    print("⚠️  Important: Set up Firestore security rules")
    print("\n📝 For development (TESTING ONLY):")
    print("""
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
    """)
    
    print("\n🔒 For production (SECURE):")
    print("""
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
    """)
    
    print("\n👉 Apply rules in Firebase Console:")
    print("   Firestore Database → Rules → Paste rules → Publish")


def create_sample_env():
    """Create a .env file with Firebase configuration"""
    print_header("Setting Up .env File")
    
    env_file = Path(__file__).parent / ".env"
    
    if env_file.exists():
        print(f"✅ .env file already exists at {env_file}")
        print("   (Not overwriting)")
    else:
        print(f"📝 Creating .env file at {env_file}")
        with open(env_file, "w") as f:
            f.write("""# SMRITHI Environment Configuration

# Backend Settings
APP_ENV=development
DEBUG=True

# Firebase Configuration
FIREBASE_CRED_PATH=./backend/serviceAccountKey.json
USE_IN_MEMORY_FALLBACK=True

# API Settings
VITE_API_BASE_URL=http://localhost:8000

# Optional: Firebase Web SDK (if using client-side Firebase)
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_API_KEY=your-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
""")
        print("✅ .env file created")


def print_next_steps():
    """Print next steps for user"""
    print_header("Next Steps")
    
    print("""
1. 📥 Download Firebase Service Account Key:
   - Go to: https://console.firebase.google.com/
   - Settings ⚙️  → Service Accounts
   - Generate New Private Key
   - Save as: backend/serviceAccountKey.json

2. 🔐 Set Firestore Security Rules:
   - Firestore Database → Rules
   - Copy rules from above (see output above)
   - Click "Publish"

3. ▶️  Start the backend:
   - npm run backend:dev
   
4. ✅ Verify connection:
   - Check logs for: "Firebase Admin SDK initialized"
   - Visit: http://localhost:8000/docs
   - Test any GET endpoint
   - Data should persist after restart!

5. 🚀 Deploy to production:
   - Set FIREBASE_CRED_PATH to production credentials
   - Set USE_IN_MEMORY_FALLBACK=False
   - Deploy backend
    """)


def main():
    """Run all checks"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  🔥  SMRITHI Firebase Setup Helper  🔥".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # Run all checks
    file_ok = check_firebase_file()
    env_ok = check_environment_variable()
    deps_ok = check_dependencies()
    
    check_firestore_rules()
    create_sample_env()
    
    # Summary
    print_header("Summary")
    
    if file_ok or env_ok:
        print("✅ Firebase credentials found!")
        print("✅ Dependencies installed!")
        if deps_ok:
            print("\n🎉 Firebase is ready to use!")
            print("   Start backend: npm run backend:dev")
        else:
            print("\n📦 Install missing dependencies first")
            sys.exit(1)
    else:
        print("⚠️  Firebase credentials not configured")
        print("\n📋 Please follow these steps:")
        print("   1. Create Firebase project (https://console.firebase.google.com/)")
        print("   2. Download service account key")
        print("   3. Save to: backend/serviceAccountKey.json")
        print("   4. Run this script again")
    
    print_next_steps()
    
    print("=" * 60)
    print("For detailed setup guide, see: FIREBASE_SETUP.md")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
