import openai
from config import OPENAI_API_KEY
from agents.business_expert import BusinessDomainExpertAI
from agents.developer import DeveloperAI
from agents.tester import CodeTesterAI
from agents.documentation import DocumentationAI
from agents.data_specialist import DataSpecialistAI
from agents.task_decomposer import TaskDecomposerAI

class CoordinatorAI:
    def __init__(self):
        self.business_expert = BusinessDomainExpertAI()
        self.developer = DeveloperAI()
        self.tester = CodeTesterAI()
        self.documentation = DocumentationAI()
        self.data_specialist = DataSpecialistAI()
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.task_decomposer = TaskDecomposerAI()


    def classify_query_0(self, user_request):
        """
        Use OpenAI to classify the query and determine the appropriate agent.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a query classifier. Classify the following query into one of these categories: 'finance', 'code', 'data', or 'unknown'."},
                    {"role": "user", "content": f"Query: {user_request}"}
                ],
                max_tokens=10,
                temperature=0.0
            )
            return response.choices[0].message.content.strip().lower()
        except Exception as e:
            return "unknown"
        
    def classify_query(self, user_request):
        """
        Classify the query using keyword matching first, then fall back to OpenAI.
        """
        keywords = {
            "finance": ["investment", "option strategy", "stock", "market"],
            "code": ["generate code", "python", "flask", "programming"],
            "data": ["analyze", "csv", "data file", "data processing"],
        }

        for category, terms in keywords.items():
            if any(term in user_request.lower() for term in terms):
                return category

        # Fall back to OpenAI for complex classification
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Classify the query into 'finance', 'code', 'data', or 'unknown'."},
                    {"role": "user", "content": user_request}
                ],
                max_tokens=10,
                temperature=0.0
            )
            return response.choices[0].message.content.strip().lower()
        except Exception:
            return "unknown"

    def handle_request_2(self, user_request):
        response = {"status": "processing", "data": {"response": ""}, "errors": []}

        try:
            # Classify the query
            query_type = self.classify_query(user_request)

            # Delegate based on the classification
            if query_type == "finance":
                insights = self.business_expert.provide_insights(user_request)
                response["data"]["response"] = insights  # Map insights to response
            elif query_type == "code":
                code = self.developer.generate_code(user_request)
                documentation = self.documentation.generate_docs(code)
                tests = self.tester.run_tests(code)
                response["data"]["response"] = {
                    "code": code,
                    "documentation": documentation,
                    "tests": tests,
                }
            elif query_type == "data":
                analysis = self.data_specialist.analyze(user_request)
                response["data"]["response"] = analysis  # Map analysis to response
            else:
                response["errors"].append("Unable to classify the request type or unsupported query.")

            response["status"] = "completed"
        except Exception as e:
            response["status"] = "error"
            response["errors"].append(str(e))

        return response
    
    def decompose_request(self, user_request):
        """
        Break down the user request into subtasks.
        """
        tasks = []
        if "flask" in user_request.lower():
            tasks.append({"task": "generate_code", "details": "Create a Flask API"})
        if "database" in user_request.lower():
            tasks.append({"task": "generate_code", "details": "Add database integration"})
        tasks.append({"task": "test_code", "details": "Validate the generated code"})
        tasks.append({"task": "document_code", "details": "Generate documentation"})
        return tasks

    def handle_request_1(self, user_request):
        """
        Process the user request by delegating tasks to agents.
        """
        subtasks = self.decompose_request(user_request)
        results = []

        for subtask in subtasks:
            if subtask["task"] == "generate_code":
                result = self.developer.generate_code(subtask["details"])
            elif subtask["task"] == "test_code":
                result = self.tester.run_tests(subtask["details"])
            elif subtask["task"] == "document_code":
                result = self.documentation.generate_docs(subtask["details"])
            results.append({"task": subtask["task"], "result": result})

        return {"status": "completed", "data": results}

    def handle_request(self, user_request):
        """
        Process the user request by delegating tasks to agents.
        """
        try:
            # Decompose the request into structured subtasks
            subtasks = self.task_decomposer.decompose(user_request)

            if "error" in subtasks:
                return {"status": "error", "message": subtasks["error"]}

            results = []
            for subtask in subtasks:
                task_type = subtask.get("task")
                task_details = subtask.get("details")

                if task_type == "generate_code":
                    result = self.developer.generate_code(task_details)
                elif task_type == "test_code":
                    result = self.tester.run_tests(task_details)
                elif task_type == "document_code":
                    result = self.documentation.generate_docs(task_details)
                else:
                    result = {"error": f"Unknown task type: {task_type}"}

                results.append({"subtask": task_details, "result": result})

            return {"status": "completed", "data": results}

        except Exception as e:
            return {"status": "error", "message": str(e)}
