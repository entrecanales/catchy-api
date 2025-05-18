from core.logger import get_logger
import uuid


class BusinessException(Exception):
    def __init__(self, message):
        super().__init__(message)
        # error logging
        logger = get_logger('catchy')
        error_uuid = str(uuid.uuid4())
        logger.error(f"[UUID - {error_uuid}] {self}")
