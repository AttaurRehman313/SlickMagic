from mainapp.video_generation.Run_app import run
from collections import deque
from datetime import datetime
import threading
import time


# Queue functionality variables
# - `request_queue` holds incoming requests to be processed.
# - `response_cache` stores completed request results for retrieval.
# - `rate_limit` controls the rate of processing requests.
# - `last_request_time` tracks the last processed request time.
# - `active_tasks` keeps track of currently running tasks.

request_queue = deque()
response_cache = {}
rate_limit = 6
last_request_time = None
active_tasks = 0


# Background task for processing the request queue
def process_queue():
    """
    Continuously process requests from the queue at a controlled rate.
    This ensures that requests are processed one at a time with a delay between each.
    """
    global last_request_time, active_tasks
    lock = threading.Lock()  # Thread lock for shared resources

    while True:
        if not request_queue:
            time.sleep(0.1)  # Wait if the queue is empty
            continue

        print("in the queue process loop")
        # Debug: Print the cache state
        for key, value in response_cache.items():
            print(f"Key='{key}' : Value='{value}'\n")

        now = datetime.now()
        # Enforce rate limiting by checking the time since the last request
        if last_request_time and (now - last_request_time).total_seconds() < rate_limit:
            time.sleep(0.1)
            continue

        with lock:  # Ensure thread-safe access
            user_request = request_queue.popleft()  # Fetch the next request
        last_request_time = now
        active_tasks += 1

        try:
            # Process the request using the `run1` function
            final_url = run(**user_request["params"])
            with lock:
                response_cache[user_request["request_id"]] = final_url

        except Exception as e:
            with lock:
                response_cache[user_request["request_id"]] = f"Error: {str(e)}"
        finally:
            active_tasks -= 1  # Decrease the active task count
            time.sleep(rate_limit)  # Add delay between requests


# Start the background task in a separate thread
def start_background_tasks():
    """
    Launch the background thread to handle request queue processing.
    """
    threading.Thread(target=process_queue, daemon=True).start()


# Initialize the background task when the application starts
start_background_tasks()
