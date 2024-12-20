import openai
from config import OPENAI_API_KEY

class BusinessDomainExpertAI:
    """
    This agent provides insights and recommendations for finance-related queries.
    """
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)

    def provide_insights(self, query):
        # Use OpenAI's updated API for generating insights
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a financial expert."},
                    {"role": "user", "content": query}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating insights: {str(e)}"
