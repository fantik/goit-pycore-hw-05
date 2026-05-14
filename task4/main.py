from rich.console import Console
from rich.table import Table

console = Console()


#error handler decorator
def input_error(func):
  def inner(*args, **kwargs):
    
    try:
      return func(*args, **kwargs)
    except ValueError:
        return "Give me name and phone please." 
    except KeyError:
       return "Contact not found"
    except IndexError:
       return "Enter the argument for the command"
    
  return inner


#validate phone
def validate_phone(phone):
  if not phone.isdigit():
    raise ValueError

  return phone

#parse input
def parse_input(user_input):
  cmd, *args = user_input.split()
  cmd = cmd.strip().lower()

  return cmd, *args

#add contact
@input_error
def add_contact(args, contacts):
  if len(args) < 2:
    raise IndexError
    
  name, phone = args
  phone = validate_phone(phone)


  if name in contacts:
    return "This user already exists in the contact list, please use command 'change [name] [phone]' instead."
  contacts[name] = phone
  return "Contact added."

#change contact
@input_error
def change_contact(args, contacts):

  name, phone = args

  if name not in contacts:
    raise KeyError
  
  phone = validate_phone(phone)
  contacts[name] = phone
  return "Contact changed."

#Show phone
@input_error
def show_phone(args, contacts):
  name = args[0]

  if name not in contacts:
    return KeyError
  
  return f"The {name.capitalize()}'s phone is:  {contacts[name]}"

#Show all
@input_error
def show_all(contacts):
  if not contacts:
    return "No contacts found"
  
  table = Table(title="Contacts")
  table.add_column("Name", style="cyan")
  table.add_column("Phone", style="green")
  
  # list = []

  for name, phone in contacts.items():
    table.add_row(name.capitalize(), phone)

  console.print(table)


def main():
    contacts = {}
    #Optimise chain if elif with dictionary labdas.
    commands = {
      "hello": lambda args: "How can I help you?",
      "add": lambda args: add_contact(args, contacts),
      "change": lambda args: change_contact(args, contacts),
      "phone": lambda args: show_phone(args, contacts),
      "all": lambda args: show_all(contacts),
    }

    print("Welcome to the assistant bot!")

    while True:
      user_input = input("Enter a command: ")
      command, *args = parse_input(user_input)

      if command in ["close", "exit"]:
        print("Good bye!")
        break

      handler = commands.get(command)

      if handler:
        print(handler(args))
      else:
        print("Invalid command.")

if __name__ == "__main__":
    main()
