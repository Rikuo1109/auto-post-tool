class NameValidate:
    @staticmethod
    def check_contains_number(name: str):
        for char in name:
            if char.isdigit():
                return True
        return False
