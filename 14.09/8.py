from string import ascii_lowercase, digits


class CardCheck:
    CHARS_FOR_NAME = ascii_lowercase.upper() + digits

    @staticmethod
    def check_card_number(number):
        parts = number.split("-")
        if len(parts) != 4:
            return False
        for part in parts:
            if len(part) != 4:
                return False
            for ch in part:
                if ch not in digits:
                    return False
        return True

    @classmethod
    def check_name(cls, name):
        parts = name.split()
        if len(parts) != 2:
            return False
        for part in parts:
            for ch in part:
                if ch not in cls.CHARS_FOR_NAME:
                    return False
        return True


print(CardCheck.check_card_number("1234-5678-9012-0000"))  
print(CardCheck.check_card_number("1234-5678-9012-00"))    
print(CardCheck.check_name("IVAN IVANOV"))                 
print(CardCheck.check_name("ivan ivanov"))                 