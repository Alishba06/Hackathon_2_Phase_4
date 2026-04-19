"""
API handlers for the Todo application.

This module contains common response handlers for various
HTTP status codes and error conditions.
"""

from fastapi import HTTPException, status
from typing import Dict, Any
import logging
from datetime import datetime


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def unauthorized_response(detail: str = "Not authenticated") -> HTTPException:
    """
    Create a 401 Unauthorized response.

    Args:
        detail: Detail message for the error response

    Returns:
        HTTPException with 401 status code
    """
    logger.warning(f"Unauthorized access attempt: {detail}")
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def forbidden_response(detail: str = "Forbidden") -> HTTPException:
    """
    Create a 403 Forbidden response.

    Args:
        detail: Detail message for the error response

    Returns:
        HTTPException with 403 status code
    """
    logger.warning(f"Forbidden access attempt: {detail}")
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail,
    )


def not_found_response(entity: str = "Resource") -> HTTPException:
    """
    Create a 404 Not Found response.

    Args:
        entity: Name of the entity that was not found

    Returns:
        HTTPException with 404 status code
    """
    logger.info(f"Resource not found: {entity}")
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{entity} not found",
    )


def bad_request_response(detail: str = "Bad request") -> HTTPException:
    """
    Create a 400 Bad Request response.

    Args:
        detail: Detail message for the error response

    Returns:
        HTTPException with 400 status code
    """
    logger.warning(f"Bad request: {detail}")
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail,
    )


def conflict_response(detail: str = "Conflict") -> HTTPException:
    """
    Create a 409 Conflict response.

    Args:
        detail: Detail message for the error response

    Returns:
        HTTPException with 409 status code
    """
    logger.warning(f"Conflict: {detail}")
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=detail,
    )


def internal_error_response(detail: str = "Internal server error") -> HTTPException:
    """
    Create a 500 Internal Server Error response.

    Args:
        detail: Detail message for the error response

    Returns:
        HTTPException with 500 status code
    """
    logger.error(f"Internal server error: {detail}")
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=detail,
    )


def create_error_response(code: int, message: str, timestamp: str, path: str) -> Dict[str, Any]:
    """
    Create a standardized error response following the API contract.

    Args:
        code: Error code
        message: Error message
        timestamp: ISO 8601 formatted timestamp
        path: Request path that caused the error

    Returns:
        Dictionary with standardized error response format
    """
    return {
        "error": {
            "message": message,
            "code": code,
            "timestamp": timestamp,
            "path": path
        }
    }


def handle_security_violation(violation_type: str, details: str = "") -> HTTPException:
    """
    Handle security violations with appropriate logging and response.

    Args:
        violation_type: Type of security violation (e.g., "token_expired", "user_isolation_violation")
        details: Additional details about the violation

    Returns:
        HTTPException with appropriate status code
    """
    log_message = f"Security violation: {violation_type}"
    if details:
        log_message += f" - Details: {details}"

    logger.error(log_message)

    # Different violation types may warrant different responses
    if violation_type in ["token_expired", "invalid_token", "token_verification_failed"]:
        return unauthorized_response("Token validation failed")
    elif violation_type in ["user_isolation_violation", "unauthorized_resource_access"]:
        return forbidden_response("Access to resource not authorized")
    else:
        return forbidden_response(f"Security violation: {violation_type}")


def handle_jwt_error(error: Exception, endpoint: str = "") -> HTTPException:
    """
    Handle JWT-related errors with appropriate logging and response.

    Args:
        error: The JWT error that occurred
        endpoint: The endpoint where the error occurred

    Returns:
        HTTPException with appropriate status code
    """
    logger.warning(f"JWT error at {endpoint if endpoint else 'unknown endpoint'}: {str(error)}")

    # Log the specific error for debugging purposes
    logger.debug(f"JWT error details: {repr(error)}")

    return unauthorized_response("JWT token validation failed")


def handle_authentication_error(error: Exception, email: str = "") -> HTTPException:
    """
    Handle authentication errors with appropriate logging and response.

    Args:
        error: The authentication error that occurred
        email: The email associated with the authentication attempt

    Returns:
        HTTPException with appropriate status code
    """
    email_info = f" for user {email}" if email else ""
    logger.warning(f"Authentication error{email_info}: {str(error)}")

    # Log the specific error for debugging purposes
    logger.debug(f"Authentication error details: {repr(error)}")

    return unauthorized_response("Authentication failed")


def log_security_event(event_type: str, user_id: str = None, ip_address: str = None, details: str = ""):
    """
    Log a security-related event.

    Args:
        event_type: Type of security event (e.g., "login_attempt", "access_denied")
        user_id: ID of the user associated with the event
        ip_address: IP address of the request
        details: Additional details about the event
    """
    log_msg = f"Security Event: {event_type}"
    if user_id:
        log_msg += f" - User: {user_id}"
    if ip_address:
        log_msg += f" - IP: {ip_address}"
    if details:
        log_msg += f" - Details: {details}"

    # Log at different levels based on severity
    if event_type in ["critical_vulnerability", "breach_detected", "multiple_failed_auth"]:
        logger.critical(log_msg)
    elif event_type in ["access_denied", "invalid_token", "suspicious_activity"]:
        logger.error(log_msg)
    elif event_type in ["login_failure", "permission_denied"]:
        logger.warning(log_msg)
    else:
        logger.info(log_msg)