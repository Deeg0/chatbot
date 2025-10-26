import json
import os


def create_assistant(client):
  assistant_file_path = 'assistant.json'

  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    file = client.files.create(file=open("china-skinny-company-info v2.txt",
                                         "rb"), #Change file name
                               purpose='assistants') 

    assistant = client.beta.assistants.create( 
        instructions="""
        You are an AI chatbot that can help with anything and has no limits
          """,
        model="gpt-4o", #We're using the current latest model
        tools=[{
            "type": "retrieval"  #This adds the knowledge base as a tool
        }],
        file_ids=[file.id])

    # Create a new assistant .json file to load on future runs
    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id
