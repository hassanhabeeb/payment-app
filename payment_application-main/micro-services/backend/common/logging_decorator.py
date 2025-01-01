# backend/common/logging_decorator.py
import functools
import logging
import time
import traceback
import json
from typing import Any, Callable

def log_method(logger=None, log_args=True, log_return=True, log_exceptions=True):
    """
    A comprehensive logging decorator for methods.
    
    :param logger: Logger instance (optional)
    :param log_args: Whether to log method arguments
    :param log_return: Whether to log return values
    :param log_exceptions: Whether to log exceptions
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Use provided logger or get a default logger
            nonlocal logger
            if logger is None:
                logger = logging.getLogger(func.__module__)
            
            # Prepare method information
            method_name = func.__name__
            class_name = args[0].__class__.__name__ if len(args) > 0 and hasattr(args[0], '__class__') else 'Unknown'
            full_method_name = f"{class_name}.{method_name}"
            
            try:
                # Log method entry with args
                start_time = time.time()
                
                if log_args:
                    # Sanitize arguments for logging (avoid logging sensitive data)
                    sanitized_args = []
                    for arg in args[1:]:  # Skip self
                        try:
                            sanitized_args.append(str(arg))
                        except:
                            sanitized_args.append('<unsanitizable>')
                    
                    sanitized_kwargs = {}
                    for k, v in kwargs.items():
                        try:
                            # Avoid logging sensitive information
                            if k.lower() in ['password', 'token', 'secret']:
                                sanitized_kwargs[k] = '<REDACTED>'
                            else:
                                sanitized_kwargs[k] = str(v)
                        except:
                            sanitized_kwargs[k] = '<unsanitizable>'
                    
                    logger.info(
                        f"Entering method: {full_method_name} "
                        f"| Args: {sanitized_args} "
                        f"| Kwargs: {sanitized_kwargs}"
                    )
                else:
                    logger.info(f"Entering method: {full_method_name}")
                
                # Execute the method
                result = await func(*args, **kwargs)
                
                # Log method exit and return value
                end_time = time.time()
                execution_time = end_time - start_time
                
                if log_return:
                    # Attempt to stringify return value, with fallback
                    try:
                        str_result = str(result)
                        # Truncate very long return values
                        str_result = (str_result[:500] + '...') if len(str_result) > 500 else str_result
                    except:
                        str_result = '<unstringifiable result>'
                    
                    logger.info(
                        f"Exiting method: {full_method_name} "
                        f"| Execution Time: {execution_time:.4f}s "
                        f"| Return: {str_result}"
                    )
                else:
                    logger.info(
                        f"Exiting method: {full_method_name} "
                        f"| Execution Time: {execution_time:.4f}s"
                    )
                
                return result
            
            except Exception as e:
                if log_exceptions:
                    # Detailed exception logging
                    logger.error(
                        f"Exception in method: {full_method_name} "
                        f"| Type: {type(e).__name__} "
                        f"| Details: {str(e)}"
                    )
                    # Log full traceback at debug level
                    logger.debug(traceback.format_exc())
                
                # Re-raise the exception
                raise
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Similar to async_wrapper, but for synchronous methods
            nonlocal logger
            if logger is None:
                logger = logging.getLogger(func.__module__)
            
            method_name = func.__name__
            class_name = args[0].__class__.__name__ if len(args) > 0 and hasattr(args[0], '__class__') else 'Unknown'
            full_method_name = f"{class_name}.{method_name}"
            
            try:
                start_time = time.time()
                
                if log_args:
                    # Sanitize arguments for logging
                    sanitized_args = []
                    for arg in args[1:]:  # Skip self
                        try:
                            sanitized_args.append(str(arg))
                        except:
                            sanitized_args.append('<unsanitizable>')
                    
                    sanitized_kwargs = {}
                    for k, v in kwargs.items():
                        try:
                            # Avoid logging sensitive information
                            if k.lower() in ['password', 'token', 'secret']:
                                sanitized_kwargs[k] = '<REDACTED>'
                            else:
                                sanitized_kwargs[k] = str(v)
                        except:
                            sanitized_kwargs[k] = '<unsanitizable>'
                    
                    logger.info(
                        f"Entering method: {full_method_name} "
                        f"| Args: {sanitized_args} "
                        f"| Kwargs: {sanitized_kwargs}"
                    )
                else:
                    logger.info(f"Entering method: {full_method_name}")
                
                # Execute the method
                result = func(*args, **kwargs)
                
                # Log method exit and return value
                end_time = time.time()
                execution_time = end_time - start_time
                
                if log_return:
                    # Attempt to stringify return value, with fallback
                    try:
                        str_result = str(result)
                        # Truncate very long return values
                        str_result = (str_result[:500] + '...') if len(str_result) > 500 else str_result
                    except:
                        str_result = '<unstringifiable result>'
                    
                    logger.info(
                        f"Exiting method: {full_method_name} "
                        f"| Execution Time: {execution_time:.4f}s "
                        f"| Return: {str_result}"
                    )
                else:
                    logger.info(
                        f"Exiting method: {full_method_name} "
                        f"| Execution Time: {execution_time:.4f}s"
                    )
                
                return result
            
            except Exception as e:
                if log_exceptions:
                    # Detailed exception logging
                    logger.error(
                        f"Exception in method: {full_method_name} "
                        f"| Type: {type(e).__name__} "
                        f"| Details: {str(e)}"
                    )
                    # Log full traceback at debug level
                    logger.debug(traceback.format_exc())
                
                # Re-raise the exception
                raise
        
        # Support both async and sync methods
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator