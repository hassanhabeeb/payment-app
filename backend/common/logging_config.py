# backend/common/logging_config.py
import logging
import json
from datetime import datetime
from logstash import TCPLogstashHandler
import socket

class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.hostname = socket.gethostname()
        return super().format(record)

def setup_logging(service_name):
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all levels
    
    # Clear any existing handlers
    logger.handlers = []
    
    # Formatter for console
    console_formatter = CustomFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    
    # Logstash handler
    class CustomLogstashHandler(TCPLogstashHandler):
        def formatters_prepare(self, record):
            # Add extra fields
            record.created = datetime.utcfromtimestamp(record.created)
            return {
                '@timestamp': record.created.isoformat(),
                'logger_name': record.name,
                'log_level': record.levelname,
                'message': record.getMessage(),
                'host': socket.gethostname(),
                'path': record.pathname,
                'function': record.funcName,
                'line_number': record.lineno
            }

    logstash_handler = CustomLogstashHandler(
        'logstash',
        5044,
        version=1
    )
    logstash_handler.setLevel(logging.DEBUG)
    logger.addHandler(logstash_handler)
    
    return logger