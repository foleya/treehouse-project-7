from django.core.exceptions import ValidationError
from django.utils.translation import gettext, ngettext


class MinimumLengthValidator:
    """
    Validate whether the password is of a minimum length (14 char).
    """
    def __init__(self, min_length=14):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    ("This password is too short. "
                     "It must contain at least %(min_length)d "
                     "character."),
                    ("This password is too short. "
                     "It must contain at least %(min_length)d "
                     "characters."),
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            ("Your password must contain at least %(min_length)d "
             "character."),
            ("Your password must contain at least %(min_length)d "
             "characters."),
            self.min_length
        ) % {'min_length': self.min_length}


class NumberValidator:
    """
    Validate whether password contains at least one number.
    """
    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        if not any(character.isdigit() for character in password):
            raise ValidationError(gettext(
                'Your password must contain at least one number.'
            ))

    def get_help_text(self):
        return "Your password must contain at least one number."


class SpecialCharacterValidator:
    """
    Validate whether the password contains a special character.
    """
    def __init__(self, min_length=1):
        self.min_length = min_length
        self.special_characters = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

    def validate(self, password, user=None):
        if not any(character in self.special_characters
                   for character in password):
                raise ValidationError(gettext(
                    'Your password must contain at least'
                    ' one special character (such as ' +
                    self.special_characters + ')')
                )

    def get_help_text(self):
        return (
            'Your password must contain at least one special character'
            ' (such as ' + self.special_characters + ')'
        )


class CaseValidator:
    """
    Validate whether password contains at least one uppercase
    and one lowercase letter.
    """
    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        if not any(character.isupper() for character in password):
            raise ValidationError(gettext(
                'Your password must contain at least one uppercase '
                'letter.'
            ))
        if not any(character.islower() for character in password):
            raise ValidationError(gettext(
                'Your password must contain at least one lowercase '
                'letter.'
            ))

    def get_help_text(self):
        return ("Your password must contain at least one uppercase "
                "and one lowercase letter.")


class NameSimilarityValidator:
    """
    Validate whether the password contains the user's username,
    first name, or last name.
    """
    USER_ATTRIBUTES = ('username', 'first_name', 'last_name')

    def __init__(self, user_attributes=USER_ATTRIBUTES):
        self.user_attributes = user_attributes

    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue

            if value.lower() in password.lower():
                raise ValidationError(gettext(
                    "Your password cannot contain your {}.".format(
                        attribute_name.replace("_", " ")
                    )
                ))

    def get_help_text(self):
        return (
            "Your password can't contain your username, first name, "
            "or last name."
        )
