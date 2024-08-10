from error_decorators import input_error
from address_book import AddressBook, Record


@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Please, enter Command Name Phone")
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 3:
        raise ValueError("Please, enter Command Name OldPhone NewPhone")
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    record.edit_phone(old_phone, new_phone)
    return f"Phone number updated for {name}."


@input_error
def show_phone(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError("Please, enter Command Name")
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    return f"{name}'s phone numbers: {', '.join(phone.value for phone in record.phones)}"


@input_error
def show_all_contacts(book: AddressBook):
    return str(book)


@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Please, enter Command Name Birthday")
    name, birthday, *_ = args
    return book.add_birthday(name, birthday)


@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError("Please, enter Command Name")
    name, *_ = args
    return book.show_birthday(name)


@input_error
def birthdays(args, book: AddressBook):
    return book.birthdays()

@input_error
def delete_contact(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError("Please, enter Command Name")
    name, *_ = args
    book.delete(name)
    return f"Contact {name} deleted."