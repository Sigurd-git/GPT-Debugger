# GPT-Debugger

Interactively debug the prompt of chatgpt.


## Setup

1. Install the requirements
```bash
pip install openai
```

2. Add your API key (and api base if needed) to the environment. Login, and you can get your API key from [here](https://platform.openai.com/account/api-keys). 
```bash
export OPENAI_API_KEY=<your key>

# optional
export OPENAI_API_BASE=<optional>
```
Those 2 lines can be added to your .bashrc or .zshrc file to make it permanent. 
Please google how to add environment variables in windows if you are using windows.

3. Run the debugger
```bash
python3 main.py
```

## Usage

1. Enter the system prompt you are using now.
2. Enter the user prompt you are using now.
3. select a model
4. Submit to get the result from chatgpt(Temperature here will be set to 0 to get more accurate result)
5. Write your feedback, adjust temperature and press Adjust System Prompt. (Temperature will only be used here to get various new system prompts)
6. Select one of the new system prompts, double click to replace the old system prompt with this new system prompt (the user prompt should not be adjusted) and press Submit to get the result from chatgpt.
7. Repeat step 4 and 6 until you are satisfied with the result.

## Hint

Adding some examples in feedback is a good way to improve the system prompt.
