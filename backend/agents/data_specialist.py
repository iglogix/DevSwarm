import pandas as pd
import matplotlib.pyplot as plt
import openai
from config import OPENAI_API_KEY

class DataSpecialistAI:
    """
    This agent processes and analyzes user-provided data.
    """
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)

    def extract_file_path(self, query):
        """
        Use OpenAI to extract the file path from the query.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a smart assistant. Extract the file path (e.g., a .csv file) from the following query."},
                    {"role": "user", "content": query}
                ],
                max_tokens=50,
                temperature=0.0
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return None

    def analyze(self, query):
        """
        Analyze the data from the extracted CSV file.
        """
        try:
            # Use OpenAI to extract the file path
            csv_file_path = self.extract_file_path(query)
            if not csv_file_path or not csv_file_path.endswith(".csv"):
                return {"error": "No valid CSV file path found in the query."}

            # Read the CSV file
            df = pd.read_csv(csv_file_path)

            # Generate a summary and save a histogram
            summary = df.describe().to_dict()
            plt.figure(figsize=(10, 6))
            df.hist()
            plt.savefig("data_analysis.png")

            return {"summary": summary, "visualization": "data_analysis.png"}
        except FileNotFoundError:
            return {"error": f"File not found: {csv_file_path}"}
        except Exception as e:
            return {"error": str(e)}
