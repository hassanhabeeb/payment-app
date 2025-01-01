# backend/payment_service/src/main.py
from fastapi import FastAPI, Depends, HTTPException, Path, Request
from typing import Optional
from .auth import get_current_user
from .models import PaymentCreate, Payment
from .services import get_user_payments,get_single_payment,get_payment_status,cancel_payment_service,create_payment,serialize_payment
from common.logging_config import setup_logging
import aioredis
from json import dumps, loads



app = FastAPI()
logger = setup_logging("payment_service")

redis = aioredis.from_url("redis://redis:6379", decode_responses=True)
CACHE_EXPIRATION = 3600



@app.get("/api/payments/payments/{payment_id}")
async def get_payment_details(
    payment_id: str = Path(..., description="The ID of the payment to retrieve"),
    current_user: str = Depends(get_current_user)
):
    """Get details of a specific payment"""
    
    try:

        cache_key = f"payment:{payment_id}:{current_user}"
        cached_payment = await redis.get(cache_key)
        if cached_payment:
            return loads(cached_payment)

        # Await the async function
        payment = get_single_payment(payment_id, current_user)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        payment_dict = serialize_payment(payment)
        await redis.set(cache_key, dumps(payment_dict), ex=CACHE_EXPIRATION)

        return payment_dict
    except Exception as e:
        logger.error(f"Error retrieving payment {payment_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


# @app.get("/api/payments/status/{payment_id}")
# async def check_payment_status(
#     payment_id: str = Path(..., description="The ID of the payment to check"),
#     current_user: str = Depends(get_current_user)
# ):
#     """Check the status of a specific payment"""
#     try:
#         status = await get_payment_status(payment_id, current_user)
#         print(payment_id,"the damn id")
#         if not status:
#             raise HTTPException(status_code=404, detail="Payment not found")
#         return {"status": status}
#     except Exception as e:
#         logger.error(f"Error checking payment status {payment_id}: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/payments/payments/", response_model=Payment)
async def create_payment_endpoint(
    request: Request,
    payment: PaymentCreate,
    current_user: str = Depends(get_current_user)
):
    logger.debug(f"Received payment creation request for user: {current_user}")
    
    try:
        logger.info(f"Creating payment for user: {current_user}")
        payment_result = await create_payment(payment, current_user)
        logger.info(f"Payment created successfully for user: {current_user}, Payment ID: {payment_result.id}")
        return payment_result
    
    except ValueError as ve:
        logger.warning(f"Payment validation failed: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    
    except Exception as e:
        logger.error(f"Unexpected error in payment creation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/payments/history")
async def get_payment_history(current_user: str = Depends(get_current_user)):
    logger.debug(f"Attempting to get payment history")
    logger.debug(f"Current user: {current_user}")
    
    try:
        payments = await get_user_payments(current_user)
        logger.info(f"Retrieved {len(payments)} payments for user: {current_user}")
        return payments
    except Exception as e:
        logger.error(f"Error retrieving payment history: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Unable to retrieve payment history")

@app.patch("/api/payments/payments/{payment_id}/cancel")
async def cancel_payment(
    payment_id: str = Path(..., description="The ID of the payment to cancel"),
    current_user: str = Depends(get_current_user)
):
    """Cancel a pending payment"""
    try:
        updated_payment = await cancel_payment_service(payment_id, current_user)
        if not updated_payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return updated_payment
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error canceling payment {payment_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")




# @app.get("/api/payments/summary")
# async def get_payment_summary(
#     period: str = Query(..., description="Period for summary (daily/weekly/monthly/yearly)"),
#     current_user: str = Depends(get_current_user)
# ):
#     """Get payment summary statistics"""
#     try:
#         summary = await generate_payment_summary(current_user, period)
#         return summary
#     except Exception as e:
#         logger.error(f"Error generating payment summary: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal server error")



# @app.get("/api/payments/health")
# async def health_check():
#     """Health check endpoint"""
#     try:
#         # Check database connection
#         await check_db_connection()
#         # Check Elasticsearch connection
#         es_status = es.ping()
        
#         return {
#             "status": "healthy",
#             "database": "connected",
#             "elasticsearch": "connected" if es_status else "disconnected",
#             "timestamp": datetime.utcnow()
#         }
#     except Exception as e:
#         logger.error(f"Health check failed: {str(e)}")
#         return JSONResponse(
#             status_code=503,
#             content={
#                 "status": "unhealthy",
#                 "error": str(e),
#                 "timestamp": datetime.utcnow()
#             }
#         )