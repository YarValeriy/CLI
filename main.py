from collections import UserDict
from datetime import timedelta, date, datetime


class Field:
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            datetime.strptime(value, "%d-%b")  # Expected DD-Mon format
        except ValueError:
            raise ValueError(f"Invalid birthday format {value}, enter DD-Mon")

    @Field.value.setter
    def value(self, new_value):
        try:
            datetime.strptime(new_value, "%d-%b")  # Expected DD-Mon format
        except ValueError:
            raise ValueError("Invalid birthday format {new_value}, enter DD-Mon")
        self.__value = new_value


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not value.isdigit() or len(value) != 10:
            raise ValueError(f"Invalid phone format {value}")

    @Field.value.setter
    def value(self, new_value):
        if not new_value.isdigit() or len(new_value) != 10:
            raise ValueError(f"Invalid phone format {new_value}")
        self.__value = new_value


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        phone_add = Phone(phone)
        if str(phone_add.value):
            self.phones.append(Phone(phone))
            print(f"Phone {phone_add} added for {self.name}")

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]
        print(f"Phone {phone} removed for {self.name}")

    def edit_phone(self, old_phone, new_phone):
        if not self.find_phone(old_phone):
            raise ValueError(f"There is no phone number {old_phone} for {self.name}")
        else:
            self.remove_phone(old_phone)
            self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def days_to_birthday(self):
        if self.birthday:
            bd_str = f'{self.birthday}-{date.today().strftime("%Y")}'
            bd_date = datetime.strptime(bd_str, "%d-%b-%Y").date()
            if bd_date < date.today():
                bd_date = bd_date.replace(year=bd_date.year + 1)
            return (bd_date - date.today()).days
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, {self.birthday.value}, phones: {'; '.join(p.value for p in self.phones)}"

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, new_value):
        if new_value and not isinstance(new_value, Birthday):
            raise ValueError(f"Invalid birthday format {new_value}, enter DD-Mon")
        self.__birthday = new_value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_value):
        if not isinstance(new_value, Name):
            raise ValueError("Invalid name format")
        self.__name = new_value

    @property
    def phones(self):
        return self.__phones

    @phones.setter
    def phones(self, new_value):
        if not all(isinstance(phone, Phone) for phone in new_value):
            raise ValueError("Invalid phone format {new_value}")
        self.__phones = new_value


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        print(f"Record added for {record.name.value}")

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            print(f"Record deleted with {name}")
        else:
            print(f"There is no record for {name}")

    def __iter__(self):
        print("Initiation")
        return iter(self.data.values())

    def iterate_N_lines(self, N):
        records = list(self.data.values())
        print(records)
        for i in range(0, len(records), N):
            yield records[i : i + N]


# Створення нової адресної книги
book = AddressBook()
# Створення запису для John
try:
    john_record = Record("John", "10-Jan")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_phone("12345abcde")
except ValueError as err:
    print(err.args[0])

# Додавання запису John до адресної книги
book.add_record(john_record)
# Створення та додавання нового запису для Jane
jane_record = Record("Jane", "30-Dec")
jane_record.add_phone("9876543210")
book.add_record(jane_record)
try:
    bill_record = Record("Bill", "30/09/1990")
    bill_record.add_phone("567576576")
    book.add_record(bill_record)
except ValueError as err:
    print(err.args[0])
# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)
    print(f"{record.days_to_birthday()} days to birthday")

# Знаходження та редагування телефону для John
try:
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    bill = book.find("Bill")
    if bill:
        bill.edit_phone("567576576", 1234567890)
    else:
        print(f'There is no record for "Bill"')
except ValueError as err:
    print(err.args[0])

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Ітерація по n записів
print("Iteration check")

n = 2
for n_records in book.iterate_N_lines(n):
    for record in n_records:
        print(record)
    input("Click to continue")

# Видалення запису Jane
book.delete("Jane")
