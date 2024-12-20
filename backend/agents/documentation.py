import openai
from config import OPENAI_API_KEY

class DocumentationAI:
    """
    This agent generates user-facing and technical documentation for code.
    """
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)

    def generate_docs(self, code):
        """
        Use OpenAI to generate documentation for the provided code.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a technical writer. Document the following code in detail."},
                    {"role": "user", "content": f"Code:\n{code}"}
                ],
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating documentation: {str(e)}"
