from faker import Faker

class BaseContact:
    def __init__(self, first_name, last_name, private_phone, email):
        self.first_name = first_name
        self.last_name = last_name
        self.private_phone = private_phone
        self.email = email

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email} - {self.format_phone(self.private_phone)}'

    @property
    def full_name_length(self):
        return len(f"{self.first_name} {self.last_name}")

    @property
    def contact_phone(self):
        return self.private_phone

    def contact(self):
        print(f'Wybieram numer {self.format_phone(self.contact_phone)} i dzwonię do {self.first_name} {self.last_name}')

    @staticmethod
    def format_phone(phone):
        return f'+48 {phone[:3]} {phone[3:6]} {phone[6:]}'

    @staticmethod
    def generate_phone_number():
        return ''.join([str(Faker().random_int(min=0, max=9)) for _ in range(9)])

    @classmethod
    def generate_contact(cls, fake, business=False):
        phone = cls.generate_phone_number()
        contact_data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'private_phone': phone,
            'email': fake.email()
        }
        if business:
            contact_data.update({
                'job_title': fake.job(),
                'company_name': fake.company(),
                'work_phone': cls.generate_phone_number()
            })
        return contact_data


class BusinessContact(BaseContact):
    def __init__(self, first_name, last_name, private_phone, email, job_title, company_name, work_phone):
        super().__init__(first_name, last_name, private_phone, email)
        self.job_title = job_title
        self.company_name = company_name
        self.work_phone = work_phone

    def __str__(self):
        contact = super().__str__()
        contact += f" | Zatrudnienie: {self.job_title}, Firma: {self.company_name}, " \
                   f"Telefon służbowy: {self.format_phone(self.work_phone)}"
        return contact

    @property
    def contact_phone(self):
        return self.work_phone


def create_contact(contact_type, fake):
    data = BaseContact.generate_contact(fake, business=(contact_type == "business"))
    if contact_type == "business":
        return BusinessContact(**data)
    return BaseContact(**data)


def create_contacts(contact_type, count):
    fake = Faker()
    return [create_contact(contact_type, fake) for _ in range(count)]


base_contacts = create_contacts("base", 3)
business_contacts = create_contacts("business", 3)

print("Podstawowe kontakty:")
for contact in base_contacts:
    print(contact)
    contact.contact()
    print(f'Długość pełnego imienia i nazwiska: {contact.full_name_length} znaków.')

print("\nFirmowe kontakty:")
for contact in business_contacts:
    print(contact)
    contact.contact()
    print(f'Długość pełnego imienia i nazwiska: {contact.full_name_length} znaków.')
