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
    phone - display existing contact as:phone Name [Surname],\n \
    show all - display all existing contacts,\n \
    exit, close, good bye - close conversation",
    "default": "Invalid command. Type 'help' for available commands.",
}
commands = {}  # disctionary of command objects
contacts = {}  # disctionary of contacts "Name": "phone number"


# decorator for command parser
def input_error(func):
    def inner(string):
        print_msg = ""

        try:
            command_list = func(string)
        except KeyError:
            return ["", "", ""], messages["default"]
        except ValueError:
            return ["", "", ""], "Invalid value. Try again."
        except IndexError:
            return ["", "", ""], "Invalid index. Try again."

        if not command_list[0]:
            print_msg = messages["default"]
        return command_list, print_msg

    return inner


# decorator for command handler
def handler_error(func):
    def inner(command_list):
        try:
            status, print_msg = func(command_list)
        except KeyError:
            return True, messages["default"]
        except ValueError:
            return True, "Invalid value. Try again."
        except IndexError:
            return True, "Invalid index. Try again."
        return True, print_msg

    return inner


# Greeting user
def hello(command_list):
    return True, messages["hello"]


# add new contact
@handler_error
def add(command_list):
    if not (command_list[1] and command_list[2]):
        print_msg = messages["add"]

    elif command_list[1] in contacts.keys():
        print_msg = f"{command_list[1]} is already in contact list with phone {contacts[command_list[1]]}"

    else:
        contacts[command_list[1]] = command_list[2]
        print_msg = f"{command_list[1]} added with {command_list[2]}"
    return True, print_msg


# change existing contact
@handler_error
def change(command_list):
    if not (command_list[1] and command_list[2]):
        print_msg = messages["change"]

    elif not (command_list[1] in contacts.keys()):
        print_msg = f"There is no {command_list[1]} in your contacts"

    else:
        contacts[command_list[1]] = command_list[2]
        print_msg = f"{command_list[1]} updated with {command_list[2]}"
    return True, print_msg


# display existing contact
@handler_error
def phone(command_list):
    if command_list[1] not in contacts.keys():
        print_msg = f"There is no {command_list[1]} in your contacts"

    else:
        print_msg = f"{contacts[command_list[1]]}"
    return (True, print_msg)


# display all existing contacts
@handler_error
def show_all(command_list):
    print_msg = messages["show_all"]
    if contacts:
        for name, phone in contacts.items():
            print_msg += f"\n{name} {phone}"
    else:
        print_msg += "...empty"
    return True, print_msg


# exit CLI
def exit(command_list):
    print_msg = messages["exit"]
    return (False, print_msg)


# display commands list
def help(command_list):
    print_msg = messages["help"]
    return True, print_msg


# command_parser decorated for input errors
@input_error
def command_parser(user_input):
    pattern = r"\+?\d+"  # pattern for phone number selection
    command_list = ["", "", ""]  # list: command, contact, phone number

    command = user_input.strip().casefold()
    # commands without parameters
    if command == "exit":
        command_list[0] = "exit"
        return command_list

    if command == "good bye":
        command_list[0] = "exit"
        return command_list

    if command == "close":
        command_list[0] = "exit"
        return command_list

    if command == "show all":
        command_list[0] = "show_all"
        return command_list
    # commands with parameters
    try:
        str = re.search(pattern, user_input)  # search phone number
        command_list[2] = str.group()
        user_input = user_input[: str.span()[0]]
    except:
        command_list[2] = ""

    # search contact name
    fields = user_input.split()
    if fields[0].strip().casefold() in messages.keys():
        command_list[0] = fields[0].strip().casefold()
        user_input = user_input.replace(fields[0], "")

    command_list[1] = user_input.strip()

    return command_list


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
        command_list, print_msg = command_parser(user_input)

        if not command_list[0]:
            print(print_msg)
            continue

        if commands[command_list[0]]:
            command = commands[command_list[0]]
            status, print_msg = command(command_list)
            print(print_msg)
            if not status:
                break
        else:
            print(messages["default"])
    return


if __name__ == "__main__":
    main()
