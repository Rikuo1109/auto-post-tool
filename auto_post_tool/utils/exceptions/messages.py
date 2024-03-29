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
    "INVALID_UID": "Invalid uid",
    # Validation errors
    "INVALID_ARGUMENTS": "Invalid arguments",
    # Check user existence
    "USER_NOT_FOUND": "User not found",
    "EMAIL_HAS_BEEN_USED": "Email has been used",
    "USER_UNVERIFIED": "User is not verified",
    "USER_ALREADY_ACTIVE": "User is already active",
    # Check new password and old password
    "SAME_PASSWORD": "New password is the same with current password",
    # Check login token
    "LOGIN_TOKEN_NOT_FOUND": "Login token not found",
    "INVALID_LOGIN_TOKEN": "Invalid login token",
    # Check reset token
    "RESET_TOKEN_NOT_FOUND": "Reset token not found",
    # Check reset token
    "RESET_TOKEN_INVALID_OR_EXPIRED": "Reset token is invalid or expired",
    # Check register token
    "REGISTER_TOKEN_INVALID_OR_EXPIRED": "Register token is invalid or expired",
    # Check data format
    "INVALID_NAME": "First name and last name must contain no numbers, no spaces allowed at the beginning or at the end, and no two consecutive spaces in the middle.",
    "INVALID_EMAIL": "Wrong email format",
    "INVALID_PASSWORD": "Password must contain at least 8 characters and contain at least 1 number and 1 letter",
    "INVALID_USERNAME": "Username must contain 8 characters",
    "INVALID_EMAIL_PASSWORD": "Invalid email or password",
    "DATA_MISSING": "Missing data input",
    # Facebook errors
    "INVALID_FACEBOOK_TOKEN": "Invalid facebook token",
    "FACEBOOK_NOT_CONNECTED": "Facebook not connected",
    "MATERIAL_NOT_FOUND": "Material not found",
    "INVALID_SCHEDULED_PUBLISH_TIME": "The specified scheduled publish time is invalid",
    # Zalo errors
    "INVALID_OAUTH_TOKEN": "Invalid oauth token",
    "INVALID_ZALO_REFRESH_TOKEN": "Invalid zalo refresh token",
    "ZALO_NOT_CONNECTED": "Zalo not connected",
    # Twitter errors
    "INVALID_TWITTER_REFRESH_TOKEN": "Invalid twitter refresh token",
    "TWITTER_NOT_CONNECTED": "Twitter not connected",
    # Post errors
    "POST_NOT_FOUND": "Post not found",
    "MORE_THAN_ONE_POST_FOUND": "More than one post found",
    # Post management errors
    "POST_MANAGEMENT_NOT_FOUND": "Post management not found",
    "MORE_THAN_ONE_POST_MANAGEMENT_FOUND": "More than one post management found",
}
