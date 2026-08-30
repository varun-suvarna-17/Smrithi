import uuid
from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from app.utils.helpers import utc_now_iso
from app.database.db import db
from app.schemas import UserRegister, UserLogin, Token, UserResponse, UserRole
from app.services.auth_service import get_password_hash, verify_password, create_access_token
from app.middleware.auth_guard import require_auth
from app.core.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserRegister):
    """Registers a new caregiver, patient, or doctor."""
    existing = db.users.find_one({"email": user_in.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )

    user_id = f"usr_{uuid.uuid4().hex[:8]}"
    hashed_pwd = get_password_hash(user_in.password)

    user_doc = {
        "id": user_id,
        "_id": user_id,
        "email": user_in.email,
        "hashed_password": hashed_pwd,
        "full_name": user_in.full_name,
        "role": user_in.role.value,
        "phone": user_in.phone,
        "created_at": utc_now_iso()
    }
    db.users.insert_one(user_doc)

    # If registered as caregiver, automatically create matching caregiver entity
    if user_in.role == UserRole.CAREGIVER:
        caregiver_id = f"cg_{uuid.uuid4().hex[:8]}"
        db.caregivers.insert_one({
            "id": caregiver_id,
            "_id": caregiver_id,
            "name": user_in.full_name,
            "relationship": "Primary Caregiver",
            "phone": user_in.phone or "",
            "email": user_in.email,
            "user_id": user_id,
            "assigned_patients": [],
            "created_at": utc_now_iso()
        })

    return UserResponse(
        id=user_id,
        email=user_doc["email"],
        full_name=user_doc["full_name"],
        role=user_doc["role"],
        phone=user_doc.get("phone"),
        created_at=user_doc["created_at"]
    )

@router.post("/login", response_model=Token)
def login_user(login_in: UserLogin):
    """Authenticates user and generates Bearer JWT access token."""
    user = db.users.find_one({"email": login_in.email})
    if not user or not verify_password(login_in.password, user.get("hashed_password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email address or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token_payload = {
        "sub": user["id"],
        "user_id": user["id"],
        "email": user["email"],
        "role": user.get("role", UserRole.CAREGIVER.value),
        "name": user.get("full_name", "")
    }
    
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(token_payload, expires_delta=expires_delta)

    return Token(
        access_token=token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_id=user["id"],
        role=user.get("role", UserRole.CAREGIVER.value),
        full_name=user.get("full_name", "")
    )

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: dict = Depends(require_auth)):
    """Retrieves current logged-in user profile."""
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        full_name=current_user["full_name"],
        role=current_user.get("role", UserRole.CAREGIVER.value),
        phone=current_user.get("phone"),
        created_at=current_user.get("created_at")
    )
