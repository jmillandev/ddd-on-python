from faker import Faker

from apps.users.models import User
from tests.factories import Factory

fake = Faker()


class UserFactory(Factory):
    class Meta:
        model = User

    name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    password = fake.password()
