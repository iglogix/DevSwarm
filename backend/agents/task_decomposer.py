import openai
from config import OPENAI_API_KEY

class TaskDecomposerAI:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)

    def decompose(self, user_request):
        """
        Use OpenAI to decompose a complex user request into structured subtasks.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """
                     You are an expert task decomposer for software development. Break down the user's query into a JSON array of tasks with keys 'task' and 'details'. Ensure the response is valid JSON and does not exceed 150 tokens.

                        For example:
                        [
                            {"task": "generate_code", "details": "Create a Flask API"},
                            {"task": "generate_code", "details": "Integrate database with Flask API"},
                            {"task": "test_code", "details": "Write unit tests for the API"},
                            {"task": "document_code", "details": "Generate API documentation"}
                        ]
                     """},
                    {"role": "user", "content": f"Decompose this request into subtasks: {user_request}"}
                ],
                max_tokens=200,
                temperature=0.3
            )
            print("Raw OpenAI Response:", response.choices[0].message.content.strip())
            subtasks_json = response.choices[0].message.content.strip()
            

            return eval(subtasks_json)  # Safely evaluate the JSON string as a Python list
        except Exception as e:
            return {"error": str(e)}
