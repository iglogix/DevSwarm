from flask_caching import Cache
from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import logging
from agents.coordinator import CoordinatorAI
import config
from celery import Celery
import time

# Configure logging
logging.basicConfig(filename='myapp.log', level=logging.INFO)



# Initialize the Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Set your OpenAI API key
api_key = config.OPENAI_API_KEY
#"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"

# Global progress tracker
progress = {
    "status": "Initializing",
    "details": []
}

app.config['CELERY_BROKER_URL'] = 'redis://localhost:7777/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:7777/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Configure Flask-Caching
app.config["CACHE_TYPE"] = "SimpleCache"  # Simple in-memory cache
app.config["CACHE_DEFAULT_TIMEOUT"] = 300  # Cache timeout in seconds
cache = Cache(app)  # Initialize the Cache with the Flask app

coordinator_ai = CoordinatorAI()

@celery.task(bind=True)
def process_data_task(self, user_request):
    self.update_state(state='STARTED', meta={'progress': 10, 'info': 'Initializing task.'})
    
    app.logger.info("Request received: %s", user_request)
    # Simulated processing steps
    
    time.sleep(5)
    self.update_state(state='PROGRESS', meta={'progress': 50, 'info': 'Halfway done.'})

    # Call the actual processing function
    coordinator_ai = CoordinatorAI()
    result = coordinator_ai.handle_request(user_request)

    self.update_state(state='SUCCESS', meta={'progress': 100, 'info': 'Task completed.'})
    return result


# @app.route('/coordinator', methods=['POST'])
# @cache.cached(query_string=True)  # Cache responses based on query parameters
# def coordinator():
#     try:
#         user_request = request.json.get("query", "")
#         if not user_request:
#             return jsonify({"error": "Query is required"}), 400
#         print(f"User Query: {user_request}")  # Log the query

#         coordinator_ai = CoordinatorAI()
#         response = coordinator_ai.handle_request(user_request)
#         return jsonify(response), 200
#     except Exception as e:
#         print(f"Error: {str(e)}")  # Log the error
#         return jsonify({"error": str(e)}), 500

@app.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = process_data_task.AsyncResult(task_id)

    if task.state == 'PENDING':
        response = {
            'status': 'pending',
            'progress': 0,
            'info': 'Task is pending execution.'
        }
    elif task.state == 'STARTED':
        response = {
            'status': 'in-progress',
            'progress': 50,
            'info': 'Task is currently in progress.'
        }
    elif task.state == 'SUCCESS':
        response = {
            'status': 'completed',
            'result': task.result
        }
    elif task.state == 'FAILURE':
        response = {
            'status': 'failed',
            'error': str(task.info)  # Exception message
        }
    else:
        response = {
            'status': task.state,
            'info': str(task.info) or 'No additional information available.'
        }

    return jsonify(response)



@app.route('/coordinator', methods=['POST'])
#@cache.cached(query_string=True)  # Cache responses based on query parameters
def coordinator():
    try:
        user_request = request.json.get("query", "")
        if not user_request:
            return jsonify({"error": "Query is required"}), 400

        # Start background task
        task = process_data_task.delay(user_request)
        return jsonify({"task_id": task.id, "status": "processing"}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/status', methods=['GET'])
def status():
    """
    Endpoint to get the current progress status.
    """
    return jsonify(progress)


@app.route('/process', methods=['POST'])
def process():
    global progress
    data = request.json
    logging.info(f"Request received: {data}")

    global progress
    data = request.json

    # Input validation
    if not data or 'prompt' not in data:
        return jsonify({"error": "Invalid input: 'prompt' is required"}), 400

    prompt = data.get('prompt', '')

    try:
        # Update progress
        progress["status"] = "Processing"
        progress["details"].append(f"Received prompt: {prompt}")

        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )

        response_text = response.choices[0].message.content.strip()
        progress["status"] = "Completed"
        progress["details"].append("Task completed successfully")
        return jsonify({
            "status": "success",
            "data": {"response": response_text},
            "error": None
        })
    except openai.error.OpenAIError as e:
        progress["status"] = "Error"
        progress["details"].append(f"OpenAI API error: {str(e)}")
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        progress["status"] = "Error"
        progress["details"].append(f"Server error: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route('/reset', methods=['POST'])
def reset():
    """
    Endpoint to reset the progress tracker.
    """
    global progress
    progress = {
        "status": "Initializing",
        "details": []
    }
    return jsonify({"message": "Progress reset successfully"})


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=False)
