import re
from django.core.exceptions import ValidationError

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 12:
            raise ValidationError("La contraseña debe tener al menos 12 caracteres.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("La contraseña debe tener al menos una mayúscula.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("La contraseña debe tener al menos un número.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("La contraseña debe tener al menos un símbolo.")

    def get_help_text(self):
        return "Tu contraseña debe cumplir con los requisitos de seguridad de la USAC."
