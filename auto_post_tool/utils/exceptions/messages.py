# Default message code for exceptions
SUCCESS = "SUCCESS"
CONTACT_ADMIN_FOR_SUPPORT = "CONTACT_ADMIN_FOR_SUPPORT"

ERROR_MESSAGES = {
    SUCCESS: "Success",
    CONTACT_ADMIN_FOR_SUPPORT: "Contact admin for support",
    # Default message code for exceptions
    "VALIDATION_ERROR": "Validation error",
    "PARSE_ERROR": "Parse error",
    "AUTHENTICATION_FAILED": "Authentication failed",
    "NOT_AUTHENTICATED": "Not authenticated",
    "NOT_FOUND": "Not found",
    "SORT_TYPE_NOT_SUPPORT": "This sort type is not supported",
    # Permission errors
    "PERMISSION_DENIED": "Permission denied",
    "USER_DOES_NOT_HAVE_PERMISSIONS": "User does not have these permissions",
    # Raise when a required field is missing
    "MISSING_FIELD": "Missing field",
    # Raise when a field is invalid (e.g. wrong type)
    "INVALID_FIELD": "Invalid field",
    # Validation errors
    "INVALID_ARGUMENTS": "Invalid arguments",
    # Post errors
    "POST_NOT_FOUND": "Post not found",
    # Post management errors
    "POST_MANAGEMENT_NOT_FOUND": "Post management not found",
}
