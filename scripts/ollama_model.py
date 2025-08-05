# ollama_model.py

class OllamaModel:
    def __init__(self, model_name):
        self.model_name = model_name
        # Load the model here if necessary
        # For example, you might have a function to load the model

    def summarize(self, job_description):
        """
        Summarizes the given job description using the TinyLlama model.

        Args:
            job_description (str): The job description text to summarize.

        Returns:
            str: The summarized text or an error message.
        """
        try:
            # Here you would call the TinyLlama model directly to get the summary
            summary = self._generate_summary(job_description)
            return summary
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def _generate_summary(self, job_description):
        # Placeholder for the actual summarization logic using TinyLlama
        # Replace this with the actual call to the TinyLlama model
        return f"Summary of: {job_description}"  # Example placeholder summary
