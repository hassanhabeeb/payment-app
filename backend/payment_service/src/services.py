# backend/payment_service/src/services.py
from .database import get_payment_collection
from .models import PaymentCreate, Payment
from datetime import datetime
import uuid
from elasticsearch import Elasticsearch
from common.logging_config import setup_logging
import logging

# Setup logging
logger = setup_logging("payment_service")

# Correct initialization with scheme



es = None
try:
    es = Elasticsearch(['http://elasticsearch:9200'])
    if es.ping():
        logger.info("Connected to Elasticsearch")
    else:
        logger.warning("Could not connect to Elasticsearch - will continue without it")
except Exception as e:
    logger.warning(f"Elasticsearch not available: {str(e)} - will continue without it")


async def create_payment(payment: PaymentCreate, user_email: str):
    # Debug level: Detailed request information
    logger.debug(f"Attempting to create payment for user: {user_email}")
    
    try:
        payment_collection = get_payment_collection()
        
        # Validate payment amount
        if payment.amount <= 0:
            # Warning level: Validation error
            logger.warning(f"Invalid payment amount: {payment.amount} for user: {user_email}")
            raise ValueError("Payment amount must be positive")
        
        payment_dict = {
            "id": str(uuid.uuid4()),
            **payment.dict(),
            "status": "pending",
            "created_at": datetime.utcnow(),
            "user_email": user_email
        }
        
        # Info level: Key steps in payment processing
        logger.info(f"Processing payment for user: {user_email}, Amount: {payment.amount}")
        
        # Store in MongoDB
        payment_collection.insert_one(payment_dict)
        
        # Index in Elasticsearch
        try:
            es.index(index="payments", document=payment_dict)
            logger.info(f"Payment indexed in Elasticsearch for user: {user_email}")
        except Exception as es_error:
            # Error level: Elasticsearch indexing failure
            logger.error(f"Failed to index payment in Elasticsearch: {str(es_error)}")
        
        # Info level: Successful payment creation
        logger.info(f"Payment created successfully for user: {user_email}")
        
        return Payment(**payment_dict)
    
    except ValueError as ve:
        # Warning level: Validation or business logic error
        logger.warning(f"Payment creation failed: {str(ve)}")
        raise
    
    except Exception as e:
        # Error level: Unexpected errors
        logger.error(f"Unexpected error in payment creation for user {user_email}: {str(e)}", exc_info=True)
        raise

async def get_user_payments(user_email: str):
    # Debug level: Detailed request information
    logger.debug(f"Retrieving payment history for user: {user_email}")
    
    try:
        payment_collection = get_payment_collection()
        
        # Info level: Payment retrieval attempt
        logger.info(f"Fetching payment history for user: {user_email}")
        
        payments = payment_collection.find({"user_email": user_email})
        payment_list = [Payment(**payment) for payment in payments]
        
        # Info level: Successful retrieval
        logger.info(f"Retrieved {len(payment_list)} payments for user: {user_email}")
        
        return payment_list
    
    except Exception as e:
        # Error level: Retrieval failure
        logger.error(f"Failed to retrieve payments for user {user_email}: {str(e)}", exc_info=True)
        raise

def get_single_payment(payment_id: str, user_email: str):
    """Get a single payment by ID"""
    try:
        payment_collection = get_payment_collection()
    except Exception as e:
        # Error level: Retrieval failure
        logger.error(f"Failed to retrieve payments for user {user_email}: {str(e)}", exc_info=True)
        raise

    payment = payment_collection.find_one({"id": payment_id, "user_email": user_email})
    return Payment(**payment) if payment else None

async def get_payment_status(payment_id: str, user_email: str):
    """Get payment status"""

    try:
        payment_collection = get_payment_collection()
    except Exception as e:
        # Error level: Retrieval failure
        logger.error(f"Failed to retrieve payments for user {user_email}: {str(e)}", exc_info=True)
        raise
    payment = await payment_collection.find_one(
        {"id": payment_id, "user_email": user_email},
        {"status": 1}
    )
    return payment["status"] if payment else None

async def cancel_payment_service(payment_id: str, user_email: str):
    """Cancel a payment"""
    try:
        payment_collection = get_payment_collection()
    except Exception as e:
        # Error level: Retrieval failure
        logger.error(f"Failed to retrieve payments for user {user_email}: {str(e)}", exc_info=True)
        raise
    payment = await payment_collection.find_one({"id": payment_id, "user_email": user_email})
    
    if not payment:
        return None
    
    if payment["status"] != "pending":
        raise ValueError("Only pending payments can be cancelled")
    
    update_result = await payment_collection.update_one(
        {"id": payment_id, "user_email": user_email},
        {"$set": {"status": "cancelled"}}
    )
    
    if update_result.modified_count:
        return await get_single_payment(payment_id, user_email)
    return None



def serialize_payment(payment):
    if payment is None:
        return None
        
    return {
        'amount': payment.amount,
        'currency': payment.currency,
        'description': payment.description,
        'payment_method': payment.payment_method,
        'id': payment.id,
        'status': payment.status,
        'created_at': payment.created_at.isoformat() if payment.created_at else None,  # Convert datetime to ISO format string
        'user_email': payment.user_email
    }