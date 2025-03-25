import logging,os
from src.config import Config

def setup_loggers():
    global error_logger, operation_logger

    error_logger = logging.getLogger('ErrorLogger')   
    error_logger.setLevel(logging.ERROR)

    operation_logger = logging.getLogger('OperationLogger')   
    operation_logger.setLevel(logging.INFO)

    config = Config()
    
    error_path = config.get('error_log')
    info_path = config.get('operation_log')
    os.makedirs(os.path.dirname(error_path), exist_ok=True)
    os.makedirs(os.path.dirname(info_path), exist_ok=True)

    error_handler = logging.FileHandler(error_path,encoding='utf-8')
    operation_handler = logging.FileHandler(info_path,encoding='utf-8')
    
    error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    operation_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    error_logger.addHandler(error_handler)
    operation_logger.addHandler(operation_handler)

def log_error(msg):
    error_logger.error(msg)

def log_info(msg):
    operation_logger.info(msg)