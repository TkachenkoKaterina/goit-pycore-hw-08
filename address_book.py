import pickle
from collections import UserDict
from datetime import datetime, timedelta
from validators import validate_phone, validate_name


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name should not be empty")
        if not validate_name(value):
            raise ValueError("Name should only contain letters")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not validate_phone(value):
            raise ValueError("Invalid phone number. Should be 10 digits")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        if self.birthday:
            return self.birthday.value.strftime("%d.%m.%Y")
        else:
            return "No birthday recorded"

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone, new_phone):
        found = False
        for p in self.phones:
            if p.value == old_phone:
                self.phones.remove(p)
                self.phones.append(Phone(new_phone))
                found = True
                break
        if not found:
            raise ValueError(f'Old phone number not found for {self.name.value}. Please, try again.')

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phone_list = '; '.join(p.value for p in self.phones)
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "No birthday"
        return f"Contact name: {self.name.value}, phones: {phone_list}, birthday: {birthday_str}"


class AddressBook(UserDict):
    def add_birthday(self, name, birthday):
        record = self.find(name)
        if record:
            record.add_birthday(birthday)
            return f"Birthday added for {name}: {birthday}"
        else:
            raise KeyError("Contact not found.")

    def show_birthday(self, name):
        record = self.find(name)
        if record:
            birthday = record.show_birthday()
            return f"{name}'s birthday is: {birthday}"
        else:
            raise KeyError("Contact not found.")

    def birthdays(self):
        upcoming = self.get_upcoming_birthdays()
        if upcoming:
            result = "Upcoming Birthdays: "
            for birthday in upcoming:
                result += f"Name: {birthday['name']}, Congratulation Date: {birthday['congratulation_date']}"
            return result
        else:
            return "No upcoming birthdays in the next week."

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue
            birthday_this_year = record.birthday.value.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if today <= birthday_this_year <= next_week:
                congratulation_date = birthday_this_year

                if congratulation_date.weekday() in [5, 6]:
                    congratulation_date += timedelta(days=(7 - congratulation_date.weekday()))

                upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                    })

        return upcoming_birthdays

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())
    

    
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
