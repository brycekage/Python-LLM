import json
import os
import inspect
from groq import Groq
from dotenv import load_dotenv
from tools.ls import ls, SCHEMA as ls_schema
from tools.cat import cat, SCHEMA as cat_schema
from tools.grep import grep, SCHEMA as grep_schema
from tools.calculate import calculate, SCHEMA as calculate_schema
from tools.compact import compact, SCHEMA as compact_schema
from tools.doctests import doctests, SCHEMA as doctests_schema
from tools.write_file import write_file, SCHEMA as write_file_schema
from tools.write_files import write_files, SCHEMA as write_files_schema
from tools.rm import rm, SCHEMA as rm_schema

load_dotenv()

TOOLS = [
    ls_schema,
    cat_schema,
    grep_schema,
    calculate_schema,
    compact_schema,
    doctests_schema,
    write_file_schema,
    write_files_schema,
    rm_schema
]

AVAILABLE_FUNCTIONS = {
    "ls": ls,
    "cat": cat,
    "grep": grep,
    "calculate": calculate,
    "compact": compact,
    "doctests": doctests,
    "write_file": write_file,
    "write_files": write_files,
    "rm": rm,
}


class Chat:
    """
    Manages a multi-turn conversation with a Groq LLM, maintaining message
    history across interactions. Supports tool use for math, file operations,
    and conversation summarization, and allows injection of slash command
    results into the conversation history.
    >>> chat = Chat()
    >>> isinstance(chat.send_message('my name is bob', temperature=0.0), str)
    True
    >>> isinstance(chat.send_message('what is my name?', temperature=0.0), str)
    True
    """

    client = Groq()

    def __init__(self):
        """
        Initializes the chat session with a system prompt defining
        the assistant's behavior and tool usage rules.
        """
        self.messages = [
            {
                "role": "system",
                "content": (
                    "Respond in 1-2 sentences. "
                    "Talk sophisticated like a butler, "
                    "but don't go over-the-top in acting like one. "
                    "If the user inputs any mathematical expression,"
                    "or asks any math question,"
                    "you MUST always call the calculate tool. "
                    "Never compute math yourself. "
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
        """
        Send prompt and calls tools if needed

        >>> chat = Chat()
        >>> isinstance(  # doctest: +ELLIPSIS
        ...     chat.send_message('my name is bob', temperature=0.0), str)
        True
        """
        self.messages.append({"role": "user", "content": message})
        last_tool_result = None
        for _ in range(10):
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
                fn_args = json.loads(tool_call.function.arguments) or {}
                valid_args = inspect.signature(fn).parameters
                fn_args = {
                    k: v for k, v in fn_args.items() if k in valid_args
                }
                if fn_name == "compact":
                    fn_result = fn(self.messages, **fn_args)
                else:
                    fn_result = fn(**fn_args)
                last_tool_result = fn_result
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": fn_name,
                    "content": fn_result,
                })
        return last_tool_result


def handle_slash_command(line, chat=None):
    """
    Parses and executes a slash command by mapping it to the corresponding
    tool in AVAILABLE_FUNCTIONS. Returns the tool output or an error string.

    >>> handle_slash_command('/ls tests')
    'tests/a.txt tests/b.txt tests/testV1.txt tests/test_write.txt'
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

    if command not in AVAILABLE_FUNCTIONS:
        return f"Unknown command: {command}"

    if command == "cat" and not args:
        return "Error: cat requires a file argument"
    if command == "grep" and len(args) < 2:
        return "Error: grep requires a pattern and a path"
    if command == "calculate" and not args:
        return "Error: calculate requires an expression"

    if command == "calculate":
        return AVAILABLE_FUNCTIONS[command](" ".join(args))
    if command == "compact":
        if chat is None:
            return "Error: no chat session available"
        convo = []
        for m in chat.messages:
            if isinstance(m, dict):
                role = m['role']
            else:
                role = getattr(m, 'role', None)
            if role in ('user', 'assistant'):
                convo.append(m)
        if not convo:
            return 'Nothing to summarize yet.'
        return compact(chat.messages)
    return (
        AVAILABLE_FUNCTIONS[command](*args)
        if args
        else AVAILABLE_FUNCTIONS[command]()
    )


def repl():
    """
    Starts an interactive chat loop. Checks for a .git folder and loads
    AGENTS.md if present. Slash commands are executed directly as tools
    and their output is injected into the conversation history. All other
    input is sent to the LLM. Exit with Ctrl+C or Ctrl+D.

    >>> def monkey_input(
    ...         prompt,
    ...         user_inputs=[
    ...             '/ls tests', 'Hello, I am monkey.', 'Goodbye.']):
    ...     try:
    ...         user_input = user_inputs.pop(0)
    ...         print(f'{prompt}{user_input}')
    ...         return user_input
    ...     except IndexError:
    ...         raise KeyboardInterrupt
    >>> import builtins
    >>> builtins.input = monkey_input
    >>> result = repl()
    chat> /ls tests
    tests/a.txt tests/b.txt tests/testV1.txt tests/test_write.txt
    chat> Hello, I am monkey.
    Good day, Monkey. It's a pleasure to make your acquaintance.
    chat> Goodbye.
    It was a brief but pleasant encounter, Monkey. Farewell.
    <BLANKLINE>
    """
    if not os.path.exists(".git"):
        print("Error: not a git repository")
        return

    chat = Chat()

    if os.path.exists("AGENTS.md"):
        agents_content = cat("AGENTS.md")
        chat.messages.append(
            {
                "role": "user",
                "content": f"AGENTS.md: {agents_content}",
            }
        )

    try:
        while True:
            user_input = input("chat> ")
            if user_input.startswith("/"):
                output = handle_slash_command(user_input, chat)
                print(output)
                command = user_input[1:].split()[0]
                if command != "compact":
                    chat.messages.append(
                        {
                            "role": "user",
                            "content": f"/{command} output: {output}",
                        }
                    )
            else:
                print(chat.send_message(user_input, temperature=0.0))
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == "__main__":
    repl()
