Healthcare-Specific-Knowledge-Assistant
This project is a Streamlit-based interactive web application designed to provide users with accurate and context-specific answers to healthcare-related queries. By leveraging transformers, fuzzy matching, and a dataset of frequently asked questions (FAQs), the tool ensures users receive reliable and relevant information.

Key Features
Natural Language Question-Answering:

Utilizes the BioMedLM model from transformers to answer questions based on healthcare context.
Fuzzy Matching:

Implements rapidfuzz for comparing user questions to a preloaded dataset of healthcare FAQs.
Suggests similar questions and retrieves direct answers for highly matched queries.
Fallback Mechanism:

If an exact match isn't found in the dataset, the app uses a QA pipeline to extract answers from relevant contexts.
Feedback Collection:

Provides users with an option to give feedback on the answers.
Feedback is logged for continuous improvement.
Example Questions:

Offers a list of example queries, such as "What are the symptoms of flu?" or "How to prevent COVID-19?" to guide users.
Technologies Used
Streamlit: For creating the user interface.
Transformers: For implementing the BioMedLM model.
Rapidfuzz: For efficient fuzzy string matching.
Pandas: For managing and processing the healthcare FAQ dataset.
How It Works
Dataset: The application loads a CSV file (healthcare_faq.csv) containing a list of healthcare-related questions and answers.
Question Processing:
Matches user input against the dataset using fuzzy matching.
If no strong match is found, uses BioMedLM to answer based on relevant dataset contexts.
User Interaction:
Users can enter their questions, review answers, and provide feedback.
