from collections import UserDict
from datetime import timedelta, date, datetime
from pickle import dump, load
import os.path


class Field:
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid value")
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid value")
        self.__value = value

    def __str__(self):
        return str(self.__value)

    def is_valid(self, value):  # new
        return True  # new


class Name(Field):
    pass


class Birthday(Field):
    def is_valid(self, value):
        try:
            datetime.strptime(value, "%d-%b")  # Expected DD-Mon format
            return True
        except ValueError:
            raise ValueError(f"Invalid birthday format {value}, enter DD-Mon")


class Phone(Field):
    def is_valid(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError(f"Invalid phone format {value}")
        return True


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        try:
            self.birthday = Birthday(birthday) if birthday else None
        except ValueError:
            self.birthday = None
            print(f"Invalid birthday format {birthday} for {name}, enter DD-Mon")

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
        return f"Contact name: {self.name.value}, {self.birthday}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value in self.data.keys():
            self.data[record.name.value] = record
            print(f"Record for {record.name.value} is overwritten with new data")
        else:
            self.data[record.name.value] = record
            print(f"Record added for {record.name.value}")

    def find(self, name):
        return self.data.get(name)

    def find_substr(self, sub_str):
        search_list = {}
        for name, record in book.data.items():
            if name.find(sub_str) != -1:
                search_list[record.name.value] = record
        return search_list

    def find_subnum(self, sub_num):
        search_list = {}
        for name, record in book.data.items():
            for phone in record.phones:
                if phone.value.find(sub_num):
                    search_list[record.name.value] = record
        return search_list

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            print(f"Record for {name} deleted")
        else:
            print(f"There is no record for {name}")

    def __iter__(self):
        print("Initiation")
        return iter(self.data.values())

    def iterate_N_lines(self, N):
        records = list(self.data.values())
        for i in range(0, len(records), N):
            yield records[i : i + N]

    def write_book_to_file(self, filename):
        with open(filename, "wb") as fh:
            dump(self.data, fh)
            print(f"AddressBook saved to file {filename}")

    def read_book_from_file(self, filename):
        with open(filename, "rb") as fh:
            self.data = load(fh)
            return book


# Створення нової адресної книги
book = AddressBook()
book_file = "my_addressbook.bin"
if os.path.isfile(f"./{book_file}"):
    book.read_book_from_file("my_addressbook.bin")
    print(f"Address book loaded from {book_file}")
    print(f"Contacts from {book_file}:")
    for name, record in book.data.items():
        print(record)
        n = record.days_to_birthday()
        if n:
            print(f"{record.days_to_birthday()} days to birthday")
else:
    print(f"AddressBook {book_file} is not found")

# Створення запису для Jonathan
try:
    jonathan_record = Record("Jonathan", "20-Mar")
    jonathan_record.add_phone("2244335566")
    jonathan_record.add_phone("9988776655")
    jonathan_record.add_phone("12345abcde")
except ValueError as err:
    print(err.args[0])

# Додавання запису Jonathan до адресної книги
book.add_record(jonathan_record)

# Створення та додавання новb[] записsd
jane_record = Record("Jane", "30-Dec")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Створення та додавання нових записів
john_record = Record("John", "10-Jan")
john_record.add_phone("5555555555")
john_record.add_phone("1112223333")
book.add_record(john_record)

tom_record = Record("Tom")
tom_record.add_phone("1223344556")
book.add_record(tom_record)

bill_record = Record("Bill", "30/09/1990")
try:
    bill_record.add_phone("567576576")
except ValueError as err:
    print(err.args[0])
book.add_record(bill_record)

# Знаходження та редагування телефону
try:
    john = book.find("John")
    if john:
        john.edit_phone("1234567890", "1112223333")
    else:
        print(f'There is no record for "John"')

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
# Пошук за літерами імені
search_list = book.find_substr("Jo")
if search_list:
    print('Contacts found with "Jo" in name:')
    for name, record in search_list.items():
        print(record)
# Пошук за цифрами в номері телефону
search_list = book.find_subnum("22")
if search_list:
    print('Contacts found with "22" in phone number')
    for name, record in search_list.items():
        print(record)

# Ітерація по n записів
print("Iteration check")
n = 2
for n_records in book.iterate_N_lines(n):
    for record in n_records:
        print(record)
    input("Click to continue")

# Видалення запису Jane
book.delete("Jane")
# Збереження книги у файл
book.write_book_to_file("my_addressbook.bin")
