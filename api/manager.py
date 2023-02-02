from django.contrib.auth.base_user import BaseUserManager

# base user manager is used because we need to use this work while applying migrations

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('phone number is required')
        
        user = self.model(phone_number=phone_number, **extra_fields)
        # password hashing -set_password bcoz overriding defaults
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # create user for password hashing
        return self.create_user(phone_number, password, **extra_fields)
