# Command Line Interface
import re

messages = {
    "hello": "How can I help you?",
    "add": "Add new contact as: add Name [Surname] [+38]0671234567",
    "change": "Change existing contact as: change Name [Surname] [+38]0671234567",
    "phone": "Display existing contact as: phone Name [Surname]",
    "show_all": "Your contacts list:",
    "exit": "Good bye!",
    "help": "Available commands:\n \
    add - add new contact as: add Name [Surname] [+38]0671234567,\n\
    change - change existing contact as: change Name [Surname] [+38]0671234567,\n\
    phone Name [Surname] - display existing contact as: Name [Surname],\n \
    show all - display all existing contacts,\n \
    exit, close, good bye - close conversation",
    "default": "Invalid command. Type 'help' for available commands.",
}
commands = {}
contacts = {}


# Greeting user
def hello(command_line):
    print(messages["hello"])
    return True


# add new contact
def add(command_line):
    contacts[command_line[1]] = command_line[2]
    return True


# change existing contact
def change(command_line):
    contacts[command_line[1]] = command_line[2]
    return True


# display existing contact
def phone(command_line):
    if contacts and command_line[1]:
        print(f"{contacts[command_line[1]]}")
    else:
        print(messages["phone"])
    return True


# display all existing contacts
def show_all(command_line):
    print(messages["show_all"])
    for name, phone in contacts.items():
        print(f"{name} {phone}")
    return True


# exit CLI
def exit(command_line):
    print(messages["exit"])
    return False


# display commands list
def help(command_line):
    print(messages["help"])
    return True


# decorator for command parser
def input_error(func):
    def inner(string):
        command_line = func(string)
        if command_line[0]:
            if command_line[0] == "add":
                if not (command_line[1] and command_line[2]):
                    print(messages["add"])
                    command_line[0] = ""
                elif command_line[1] in contacts.keys():
                    print(
                        f"{command_line[1]} is already in contacts with phone {contacts[command_line[1]]}"
                    )
                    command_line[0] = ""
            elif command_line[0] == "change":
                if not (command_line[1] and command_line[2]):
                    print(messages["change"])
                    command_line[0] = ""
                elif not (command_line[1] in contacts.keys()):
                    print(f"There is no {command_line[1]} in your contacts")
                    command_line[0] = ""
        else:
            print(messages["default"])
        return command_line

    return inner


# command_parser decorated for input errors 
@input_error
def command_parser(user_input):
    pattern = r"\+?\d+"
    command_line = ["", "", ""]
    command = user_input.strip().casefold()

    if command == "exit":
        command_line[0] = "exit"
        return command_line

    if command == "good bye":
        command_line[0] = "exit"
        return command_line

    if command == "close":
        command_line[0] = "exit"
        return command_line

    if command == "show all":
        command_line[0] = "show_all"
        return command_line

    try:
        str = re.search(pattern, user_input)
        command_line[2] = str.group()
        user_input = user_input[: str.span()[0]]
    except:
        command_line[2] = ""

    fields = user_input.split()
    if fields[0].strip().casefold() in commands.keys():
        command_line[0] = fields[0].strip().casefold()
        user_input = user_input.replace(fields[0], "")

    command_line[1] = user_input.strip()

    return command_line


def main():
    commands["hello"] = hello
    commands["add"] = add
    commands["change"] = change
    commands["phone"] = phone
    commands["show_all"] = show_all
    commands["exit"] = exit
    commands["help"] = help

    print("Welcome to contacts assistant, enter your command")
    while True:
        user_input = input(">")
        command_line = command_parser(user_input)
        if not command_line[0]:
            continue
        if commands[command_line[0]]:
            command = commands[command_line[0]]
            if not command(command_line):
                break
        else:
            print(messages["default"])
    return


if __name__ == "__main__":
    main()