import json
from groq import Groq
from dotenv import load_dotenv
from tools.ls import ls
from tools.cat import cat
from tools.grep import grep
from tools.calculate import calculate
from tools.compact import compact

load_dotenv()

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "ls",
            "description": "List files in a directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory to list. Defaults to '.'."
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cat",
            "description": "Read the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File to read."}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "grep",
            "description": (
                "Search for lines matching a regex in files matching a glob."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Regex pattern to search for."
                    },
                    "path": {
                        "type": "string",
                        "description": "File path or glob to search in."
                    },
                },
                "required": ["pattern", "path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": (
                "Evaluate a mathematical expression. "
                "Always pass the raw expression as a string (e.g. '6 * 7'), "
                "never a pre-computed number."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": (
                            "The math expression to evaluate as a string, "
                            "e.g. '6 * 7'."
                        )
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compact",
            "description": (
                "Summarize the current chat session to reduce context length."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "summary_instructions": {
                        "type": "string",
                        "description": (
                            "Preserve all decisions made and summarize "
                            "in 1-5 sentences"
                        )
                    }
                },
                "required": [],
            },
        },
    },
]

AVAILABLE_FUNCTIONS = {
    "ls": ls,
    "cat": cat,
    "grep": grep,
    "calculate": calculate,
    "compact": compact,
}


class Chat:
    """
    >>> chat = Chat()
    >>> chat.send_message(  # doctest: +ELLIPSIS
    ...     'my name is bob', temperature=0.0)
    'Ye be Bob, eh?'
    >>> chat.send_message(  # doctest: +ELLIPSIS
    ...     'what is my name?', temperature=0.0)
    "...Bob..."
    """

    client = Groq()

    def __init__(self):
        self.messages = [
            {
                "role": "system",
                "content": (
                    "Respond in 1-2 sentences. "
                    "Talk sophisticated like a butler, "
                    "but don't go over-the-top in acting like one. "
                    "Use the calculate tool only when asked to do math. "
                    "When the user asks to summarize or compact the "
                    "conversation, you MUST call the compact tool first, "
                    "then repeat the summary returned by the tool word for "
                    "word to the user. "
                    "Do not summarize the conversation yourself without "
                    "calling the compact tool. "
                    "Use ls, cat, and grep only when explicitly asked about "
                    "files. "
                    "When the user provides output from a slash command, "
                    "use that information to answer their question directly "
                    "without calling any tools again."
                )
            }
        ]

    def send_message(self, message, temperature=0.8):
        # Send prompt and calls tools if needed

        """
        >>> chat = Chat()
        >>> chat.send_message(  # doctest: +ELLIPSIS
        ...     'my name is bob', temperature=0.0)
        'Ye be Bob, eh?'
        """
        self.messages.append({"role": "user", "content": message})
        while True:
            response = self.client.chat.completions.create(
                messages=self.messages,
                model="llama-3.1-8b-instant",
                temperature=temperature,
                tools=TOOLS,
                tool_choice="auto",
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if not tool_calls:
                result = response_message.content
                self.messages.append({"role": "assistant", "content": result})
                return result

            self.messages.append(response_message)
            for tool_call in tool_calls:
                fn_name = tool_call.function.name
                fn = AVAILABLE_FUNCTIONS.get(fn_name)
                if fn is None:
                    continue
                fn_args = json.loads(tool_call.function.arguments)

                if fn_name == "compact":
                    fn_result = fn(self.messages, **fn_args)
                else:
                    fn_result = fn(**fn_args)

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": fn_name,
                    "content": fn_result,
                })

    def inject_tool_result(self, name, output):
        """
        Injects a manually run tool result into conversation history
        as a user message.

        >>> chat = Chat()
        >>> chat.inject_tool_result('ls', 'file1.txt file2.txt')
        >>> chat.messages[-1]['role']
        'user'
        >>> chat.messages[-1]['content']
        '/ls output: file1.txt file2.txt'
        """
        self.messages.append({
            "role": "user",
            "content": f"/{name} output: {output}",
        })


def handle_slash_command(line, chat=None):
    """
    >>> handle_slash_command('/ls tests')
    'tests/testV1.txt'
    >>> handle_slash_command('/cat tests/testV1.txt')
    'This is a doctest for the cat tool'
    >>> handle_slash_command('/grep doctest tests/testV1.txt')
    'This is a doctest for the cat tool'
    >>> handle_slash_command('/calculate 2 + 2')
    '4'
    >>> handle_slash_command('/calculate')
    'Error: calculate requires an expression'
    >>> handle_slash_command('/cat')
    'Error: cat requires a file argument'
    >>> handle_slash_command('/grep hello')
    'Error: grep requires a pattern and a path'
    >>> 'chat.py' in handle_slash_command('/ls')
    True
    >>> handle_slash_command('/unknownCmd')
    'Unknown command: unknownCmd'
    """
    parts = line[1:].split()
    command = parts[0]
    args = parts[1:]

    if command == 'ls':
        return ls(args[0] if args else '.')
    elif command == 'cat':
        if not args:
            return 'Error: cat requires a file argument'
        return cat(args[0])
    elif command == 'grep':
        if len(args) < 2:
            return 'Error: grep requires a pattern and a path'
        return grep(args[0], args[1])
    elif command == 'calculate':
        if not args:
            return 'Error: calculate requires an expression'
        return calculate(' '.join(args))
    elif command == 'compact':
        if chat is None:
            return 'Error: no chat session available'
        convo = [
            m for m in chat.messages if m['role'] in ('user', 'assistant')
        ]
        if not convo:
            return 'Nothing to summarize yet.'
        return compact(chat.messages)
    else:
        return f'Unknown command: {command}'


def repl():
    """
    >>> inputs = ['/ls testCases', 'Hello, I am monkey.', 'Goodbye.']
    >>> def monkey_input(prompt, user_inputs=None):
    ...     if user_inputs is None:
    ...         user_inputs = inputs
    ...     try:
    ...         user_input = user_inputs.pop(0)
    ...         print(f'{prompt}{user_input}')
    ...         return user_input
    ...     except IndexError:
    ...         raise KeyboardInterrupt
    >>> import builtins
    >>> builtins.input = monkey_input
    >>> repl()  # doctest: +ELLIPSIS
    chat> /ls testCases
    ...
    chat> Hello, I am monkey.
    ...
    chat> Goodbye.
    ...
    <BLANKLINE>
    """
    chat = Chat()
    try:
        while True:
            user_input = input('chat> ')
            if user_input.startswith('/'):
                command = user_input[1:].split()[0]
                output = handle_slash_command(user_input, chat)
                print(output)
                if command != 'compact':
                    chat.inject_tool_result(command, output)
            else:
                print(chat.send_message(user_input, temperature=0.0))
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == '__main__':
    repl()
