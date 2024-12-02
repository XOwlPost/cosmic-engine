import scripts.utils as utils
import os

class AppAgentREPL:
    def __init__(self):
        self.context = {}

    def start(self):
        print("Welcome to the AppAgent Interactive REPL!")
        print("Type 'help' for instructions or 'exit' to quit.")
        while True:
            try:
                # Prompt for user input
                command = input("\n[AppAgent] >>> ").strip()
                if command.lower() in ["exit", "quit"]:
                    print("Exiting AppAgent REPL. Goodbye!")
                    break
                elif command.lower() == "help":
                    self.print_help()
                else:
                    self.execute_command(command)
            except KeyboardInterrupt:
                print("\nInterrupted. Type 'exit' to quit.")
            except Exception as e:
                print(f"Error: {e}")

    def print_help(self):
        print("""
AppAgent Interactive REPL Commands:
- help: Show this help message.
- exit/quit: Exit the REPL.
- print_context: Show the current context of AppAgent.
- set_context key=value: Set a key-value pair in AppAgent's context.
- exec <Python Code>: Execute arbitrary Python code.
        """)

    def execute_command(self, command):
        if command.startswith("print_context"):
            print(f"Current Context: {self.context}")
        elif command.startswith("set_context"):
            try:
                key, value = command.split(" ", 1)[1].split("=")
                self.context[key.strip()] = value.strip()
                print(f"Set context: {key.strip()} = {value.strip()}")
            except ValueError:
                print("Invalid syntax. Use: set_context key=value")
        elif command.startswith("exec"):
            try:
                exec(command.split(" ", 1)[1], globals(), self.context)
            except Exception as e:
                print(f"Execution error: {e}")
        else:
            print("Unknown command. Type 'help' for instructions.")

# Start the REPL
if __name__ == "__main__":
    agent_repl = AppAgentREPL()
    agent_repl.start()
