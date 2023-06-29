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
    # Check user existence
    "USER_NOT_FOUND": "User not found",
    "EMAIL_HAS_BEEN_USED": "Email has been used",
    # Check login information
    "INVALID_PASSWORD": "Password must contain at least 8 character and not contain any special character",
    # Check new password and old password
    "SAME_PASSWORD": "New password is the same with current password",
    # Check login token
    "LOGIN_TOKEN_NOT_FOUND": "Login token not found",
    "INVALID_LOGIN_TOKEN": "Invalid login token",
    # Check reset token
    "RESET_TOKEN_NOT_FOUND": "Reset token not found",
    "RESET_TOKEN_EXPIRED": "Reset token has expired",
    "INVALID_LOGIN_TOKEN": "Invalid login token",
    # Check reset token
    "RESET_TOKEN_INVALID_OR_EXPIRED": "Reset token is invalid or expired",
    # Check data format
    "INVALID_NAME": "First name and last name must contain no numbers",
    "INVALID_EMAIL": "Wrong email format",
    "INVALID_PASSWORD": "Password must contain at least 8 characters and contain at least 1 number and 1 letter",
    "INVALID_USERNAME": "Username must contain 8 characters",
    "INVALID_EMAIL_PASSWORD": "Invalid email or password",
    "DATA_MISSING": "Missing data input",
    # Facebook errors
    "INVALID_FACEBOOK_TOKEN": "Invalid facebook token",
    "FACEBOOK_NOT_CONNECTED": "Facebook not connected",
    "MATERIAL_NOT_FOUND": "Material not found",
    "FACEBOOK_ID_NOT_FOUND": "Facebook ID not found",
    "FACEBOOK_PAGE_NOT_FOUND": "Facebook page not found",
    # Zalo errors
    "INVALID_OAUTH_TOKEN": "Invalid oauth token",
    "INVALID_ZALO_REFRESH_TOKEN": "Invalid zalo refresh token",
    "ZALO_TOKEN_NOT_CONNECTED": "Zalo not connected",
    # Post errors
    "POST_NOT_FOUND": "Post not found",
    # Post management errors
    "POST_MANAGEMENT_NOT_FOUND": "Post management not found",
    # Facebook errors
    "INVALID_FACEBOOK_TOKEN": "Invalid facebook token",
    "INVALID_SCHEDULED_PUBLISH_TIME": "The specified scheduled publish time is invalid",
}
