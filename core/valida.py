import re
from django.core.exceptions import ValidationError

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 12:
            raise ValidationError("La contrasena debe tener al menos 12 caracteres.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("La contrasena debe tener al menos una mayuscula.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("La contrasena debe tener al menos un numero.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("La contrasena debe tener al menos un simbolo.")

    def get_help_text(self):
        return "Tu contrasena debe cumplir con los requisitos de seguridad de la USAC."
