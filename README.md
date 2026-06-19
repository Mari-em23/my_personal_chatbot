## Project's description :
A completely free RAG with searching capabilities for broke people.

## Architecture :
<img src="architecture.png" width="600"/>


## Preconfiguration :
To ensure the chatbot works correctly, create a virtual environment via this command in the root directory :

```
python -m venv .venv

```

Install Ollama
<br>
Follow the official installation guide:
https://ollama.com

Pull the model

```
ollama pull llama3.2:3b 

```
PS : you can choose any model you like, I chose llama 3.2 3B because it works well on my machine.

Second, you need to install the requirements :

```
pip install -r requirements.txt

```

Except if you want to keep working with the sample data, modify the internal_data.txt, configuration_data/mission.txt and configuration_data/rules.txt files according to your needs.

<b>VERY IMPORTANT STEPS :</b>
<br>
    Run create_db_and_table to set your infrastructure with :
    ```
    python create_db_and_table.py
    ```
    Run embeddings_generator.py with :
    ```
    python embeddings_generator.py
    ```

## Running the app :
Now every time you want to run the app :
1. Activate ollama
2. Run the Flask app with this exact command in the root folder:

```
python -m Flask.app 

```
### Notes :
<br>
Be specific if you want your chatbot to search something (it is quite dumb, mainly an architectural issue).
No matter how long the conversation is, only 60 messages are displayed.
The chat history does not persist, it changes every session (new session_id = new empty thread).
