'''Bot main module'''
from dataclasses import dataclass
from collections import UserDict
from bot_errors import PhoneNumberIncorrectError, AddContactAlreadyExistsError, ContactNotFoundError, PhoneNumberNotFoundError

@dataclass
class Field:
    '''Field  class'''
    value: str

    def __str__(self):
        return str(self.value)

@dataclass
class Name(Field):
    '''Field name class'''

@dataclass
class Phone(Field):
    '''Field phone class'''
    def __init__(self, value: str):
        '''Create phone field'''
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise PhoneNumberIncorrectError("The phone number must contain exactly 10 digits!")

class Record:
    '''Record class'''
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone: str):
        '''Add phone to record'''
        if Phone(phone) not in self.phones:
            self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        '''Remove phone'''
        if Phone(phone) not in self.phones:
            raise PhoneNumberNotFoundError("This phone not found!") 
        self.phones.remove(Phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str):
        '''Edit phone'''
        if Phone(old_phone) not in self.phones:
            raise PhoneNumberNotFoundError("This phone not found!")
        self.phones[self.phones.index(Phone(old_phone))] = Phone(new_phone)

    def find_phone(self, phone: str):
        '''Find phone'''
        if Phone(phone) in self.phones:
            return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p.value) for p in self.phones)}"

class AddressBook(UserDict):
    '''AddressBook class'''

    def add_record(self, record: Record):
        '''Add record to address book'''
        if self.data.get(str(record.name).upper()):
            raise AddContactAlreadyExistsError("This contact already exists!")
        self.data.update({str(record.name).upper(): record})

    def find(self, name: str) -> Record:
        '''Find record by name'''
        record = self.data.get(name.upper())
        if not record:
            raise ContactNotFoundError("This contact not found!")
        return record

    def delete(self, name: str):
        '''Delete record by name'''
        if not self.data.get(name.upper()):
            raise ContactNotFoundError("This contact not found!")
        self.data.pop(name.upper())
