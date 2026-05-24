from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt # type: ignore
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError # type: ignore
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()

            claims = get_jwt()

            if claims.get("role") != "admin":
                return jsonify({"message": "Admin access required"}), 403

        except NoAuthorizationError:
            return jsonify({"message": "Missing or invalid token"}), 401

        except InvalidHeaderError:
            return jsonify({"message": "Invalid authorization header"}), 401

        return fn(*args, **kwargs)

    return wrapper