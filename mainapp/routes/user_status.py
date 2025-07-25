from mainapp.multi_users_process.queue_process import response_cache
from flask import Blueprint, jsonify

status = Blueprint("status", __name__)

@status.route("/status/<request_id>", methods=["GET"])
def check_status(request_id):
    """
    Endpoint to check the status of a queued request.
    - Returns the result if processing is complete.
    - Informs the user to wait if the request is still being processed.
    """

    # Debug: Print the cache state
    for key, value in response_cache.items():
        print(f"Key='{key}' : Value='{value}'\n")

    if request_id in response_cache:
        # Return the response but don't remove it from the cache immediately
        return jsonify(
            {"request_id": request_id, "response": response_cache[request_id]}
        )
    else:
        return jsonify(
            {"request_id": request_id, "message": "Still processing. Please wait."}
        )
