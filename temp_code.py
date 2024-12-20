Sure, here's a simple example of a Flask API that includes a single route.

```python
# Import necessary modules
from flask import Flask, jsonify, request

# Initialize Flask application
app = Flask(__name__)

# Define a simple route
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message' : 'Welcome to our Flask API'})

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
```

This code creates a Flask application and defines a single route ("/") that returns a JSON response with the message "Welcome to our Flask API".

You can start the server by running this script. The server will start in debug mode on your local machine (typically accessible via localhost:5000 in your web browser).

This is a very basic example. In a real-world application, you'd likely have many more routes, and you'd be interacting with a database to create, read, update, and delete resources based on