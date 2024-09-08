import time
import logging
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class CustomLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Create a logger for this middleware
        self.logger = logging.getLogger('custom_logger')
        log_file_path = getattr(settings, 'LOGGING_FILE_PATH', 'logs/request.log')

        # Check if the logger already has handlers to avoid duplicate logs
        if not self.logger.hasHandlers():
            handler = logging.FileHandler(log_file_path)
            handler.setLevel(logging.INFO)
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)

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


class AdminLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response

        # Create a logger for admin requests
        self.logger = logging.getLogger('admin_logger')
        log_file_path = getattr(settings, 'ADMIN_LOGGING_FILE_PATH', 'logs/admin-logs.logs')

        # Check if the logger already has handlers to avoid duplicate logs
        if not self.logger.hasHandlers():
            handler = logging.FileHandler(log_file_path)
            handler.setLevel(logging.INFO)
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)

    def __call__(self, request):
        admin_path = getattr(settings, 'ADMIN_PANEL_URL', '/admin/')

        if admin_path in request.path and request.user.is_superuser:
            # Start timing
            start = time.time()

            # Get the client's IP address
            ip_address = self.get_client_ip(request)

            try:
                response = self.get_response(request)
            except Exception as e:
                # Log the exception with trace
                self.logger.error(f'Exception: {str(e)} | User: {request.user.username} | IP: {ip_address}',
                                  exc_info=True)
                raise

            # Time taken to process the request
            duration = time.time() - start

            # Log details including user, IP, method, status, and timing
            self.logger.info(
                f'Admin Request: {request.method} {request.path} | Status: {response.status_code}'
                f' | Duration: {duration:.2f}s | '
                f'User: {request.user.username} | IP: {ip_address} | '
                f'User-Agent: {request.META.get("HTTP_USER_AGENT", "Unknown")}'
            )

            return response
        else:
            # Process non-admin requests as usual
            return self.get_response(request)

    def get_client_ip(self, request):
        """Get client IP address from request headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
