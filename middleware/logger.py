import time
import logging
from django.conf import settings


class CustomLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Configure logging
        log_file_path = getattr(settings, 'LOGGING_FILE_PATH', 'logs/request.log')
        logging.basicConfig(
            filename=log_file_path,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
        )
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        start = time.time()

        try:
            # Process the request
            response = self.get_response(request)
        except Exception as e:
            # Log the exception
            self.logger.error(f'Exception: {str(e)}', exc_info=True)
            raise

        duration = time.time() - start

        # Log request details
        self.logger.info(
            f'New Request: {request.method} {request.path} | Status: {response.status_code} | Duration: {duration:.2f}s\n\n'
        )

        return response
