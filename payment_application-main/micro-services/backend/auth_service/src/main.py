# backend/auth_service/src/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .models import UserCreate, User, Token
from .auth import create_access_token, verify_password, get_password_hash
from .database import get_user_collection
from common.logging_config import setup_logging
import logging
import uuid

# Setup logging
logger = setup_logging("auth_service")

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/auth/register", response_model=User)
async def register(user: UserCreate):
    # Debug level: Detailed request information
    logger.debug(f"Received registration request for email: {user.email}")
    
    try:
        users = get_user_collection()
        
        # Check if user already exists
        existing_user = users.find_one({"email": user.email})
        if existing_user:
            # Warning level: Duplicate registration attempt
            logger.warning(f"Registration attempt with existing email: {user.email}")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Info level: User registration process
        logger.info(f"Registering new user with email: {user.email}")
        
        # Hash password
        hashed_password = get_password_hash(user.password)
        
        # Prepare user dictionary
        user_dict = user.dict()
        user_dict["password"] = hashed_password
        user_dict["id"] = str(uuid.uuid4())  # Add a consistent ID
        
        # Insert user
        result = users.insert_one(user_dict)
        
        # Info level: Successful registration
        logger.info(f"User registered successfully: {user.email}")
        
        return {**user_dict, "id": user_dict["id"]}
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        # Error level: Unexpected registration errors
        logger.error(f"Unexpected error during user registration: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Registration failed")

@app.post("/api/auth/login", response_model=Token)
async def login(user_detail: UserCreate):
    # Debug level: Login attempt
    logger.debug(f"Login attempt for email: {user_detail.email}")
    
    try:
        users = get_user_collection()
        
        # Find user
        user = users.find_one({"email": user_detail.email})
        
        # Validate user credentials
        if not user:
            # Warning level: User not found
            logger.warning(f"Login attempt with non-existent email: {user_detail.email}")
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        
        # Verify password
        if not verify_password(user_detail.password, user["password"]):
            # Warning level: Invalid password
            logger.warning(f"Failed login attempt for email: {user_detail.email}")
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        
        # Info level: Successful login
        logger.info(f"Successful login for user: {user_detail.email}")
        
        # Create access token
        access_token = create_access_token(data={"sub": user_detail.email})
        
        return {"access_token": access_token, "token_type": "bearer"}
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        # Error level: Unexpected login errors
        logger.error(f"Unexpected error during login: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Login failed")

# Optional: Add a health check endpoint
@app.get("/health")
async def health_check():
    try:
        # Attempt to connect to database
        users = get_user_collection()
        users.find_one({})  # Simple query to check connection
        
        # Info level: Health check success
        logger.info("Health check successful")
        
        return {"status": "healthy"}
    
    except Exception as e:
        # Error level: Health check failure
        logger.error(f"Health check failed: {str(e)}")
        
        return {"status": "unhealthy", "error": str(e)}