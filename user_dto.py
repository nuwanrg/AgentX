class UserDTO:
    def __init__(self, phone_number=None, whatsapp_id=None, whatsapp_name=None, first_name=None, last_name=None,
                 date_of_birth=None, email=None, gender=None, created_at=None, message_count=None):
        self.phone_number = phone_number
        self.whatsapp_id = whatsapp_id
        self.whatsapp_name = whatsapp_name
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.email = email
        self.gender = gender
        self.created_at = created_at
        self.message_count = message_count

    def __repr__(self):
        return f"UserDTO(phone_number={self.phone_number}, whatsapp_id={self.whatsapp_id}, " \
               f"whatsapp_name={self.whatsapp_name}, first_name={self.first_name}, last_name={self.last_name}, " \
               f"date_of_birth={self.date_of_birth}, email={self.email}, gender={self.gender}, " \
               f"created_at={self.created_at}, message_count={self.message_count} )"
