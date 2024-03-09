from openai import OpenAI
import json
from dotenv import load_dotenv, find_dotenv
import re
from openai.types.beta import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads.run import Run
from openai.types.beta.threads.thread_message import ThreadMessage
import time

# Load environment variables
_ : bool = load_dotenv(find_dotenv())

# Initialize OpenAI client
client : OpenAI = OpenAI()

def extract_dependencies(code):
    python_code_pattern = re.compile(r'```dependencies(.*?)```', re.DOTALL)
    matches = re.findall(python_code_pattern, code)

    if matches:
        # Combine the matches into a single string
        extracted_python_code = "\n".join(matches)

        # Write the extracted Python code to a .py file
        with open("requirements.txt", 'w') as file:
            file.write(extracted_python_code)

        


def extract_and_write_code(file_name, code):
    # Extract Python code from the message
    python_code_pattern = re.compile(r'```python(.*?)```', re.DOTALL)
    matches = re.findall(python_code_pattern, code)

    if matches:
        # Combine the matches into a single string
        extracted_python_code = "\n".join(matches)

        # Write the extracted Python code to a .py file
        with open(f"{file_name}.py", 'w') as file:
            file.write(extracted_python_code)

        print(f"Python code extracted and written to {file_name}.py. Run the file and check for any errors.")
    else:
        print("No valid Python code found in the message.")

# User input
user_message: str = input("Enter your message: ")
opsys: str = input("Enter your operating system: ")
file_name: str = input("Enter the name for the script file: ")

# Create an assistant
assistant: Assistant = client.beta.assistants.create(
    name="python automation expert",
    instructions=f'Your task is to build automation scripts in Python. Output the specific Python script directly to the .py file. If there are specific instructions needed for the script, ask for them first and then output the script. The script should run fine according to the OS: {opsys}',
    tools=[{"type": "code_interpreter"}],
    model="gpt-3.5-turbo-1106"
)

# Create a thread
thread: Thread  = client.beta.threads.create()

while True:
    # User message
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )

    # Create a run
    run: Run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please just output the Python script only. Do not output any text or instructions. You can use comments if needed. If the code encounters any errors, resolve it and update the code until it works fine. mark the updated part with comments. if any dependencies needed write it inside ```dependencies ```  "
    )

    # Wait for the run to complete
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        time.sleep(1)

    # Get messages
    messages: list[ThreadMessage] = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    # Process messages
    for m in reversed(messages.data):
        print(m.role + ": " + m.content[0].text.value)

        # If there's an error message, update the script
        if m.role == "user" and "error" in m.content[0].text.value.lower():
            print("Updating the script based on the error message.")
            user_message = m.content[0].text.value  # Use the error message as the new input
            extract_and_write_code(file_name, m.content[0].text.value)
        elif m.role == "assistant":
            # Extract and write the Python code to a file
            extract_and_write_code(file_name, m.content[0].text.value)
            extract_dependencies(m.content[0].text.value)

    # Prompt for the next action
    user_message = input("Paste your error here or type 'quit' if there is none: ")
    if user_message.lower() == 'quit':
        break
