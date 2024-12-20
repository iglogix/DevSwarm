import openai
from config import OPENAI_API_KEY

class DeveloperAI:
    """
    This agent generates code based on the user's requirements.
    """
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)

    def generate_code(self, task_description):
        # Use OpenAI's updated API for code generation
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a senior software engineer."},
                    {"role": "user", "content": f"Write code for: {task_description}"}
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating code: {str(e)}"
