# Healthcare-Application


graph TD
A[Start] --> B(Download or Clone Project Files);
B --> C{Files in place?};
C -- Yes --> D[Create Virtual Environment];
C -- No --> B;
D --> E[Activate Virtual Environment];
E --> F[Install Dependencies from requirements.txt];
F --> G[Navigate to Project Directory];
G --> H[Run Streamlit App with streamlit run app.py];
H --> I(Application Runs on Local Server);
I --> J[Open App in Browser];
J --> K(Interact with the App);
K --> L[End];
