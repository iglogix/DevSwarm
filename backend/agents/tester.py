import subprocess
import openai
from config import OPENAI_API_KEY

class CodeTesterAI:
    """
    This agent validates the generated code by running tests and uses OpenAI for additional validation.
    """
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)

    def run_tests(self, code):
        """
        Validate the code by running it and using AI validation.
        """
        try:
            # Save code to a temporary file and run it with pytest
            with open("temp_code.py", "w") as temp_file:
                temp_file.write(code)

            result = subprocess.run(["pytest", "temp_code.py"], capture_output=True, text=True)
            if result.returncode == 0:
                return f"Tests Passed: {result.stdout}"
            else:
                return f"Tests Failed: {result.stderr}"

        except Exception as e:
            return f"Error running tests: {str(e)}"

    def validate_code(self, code_description, code):
        """
        Use OpenAI to validate the correctness of the code.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a code reviewer. Validate the following code."},
                    {"role": "user", "content": f"Description: {code_description}\n\nCode:\n{code}"}
                ],
                max_tokens=200,
                temperature=0.5
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error in AI validation: {str(e)}"
