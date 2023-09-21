from faker import Faker

from tests.factories import Factory
from apps.users.models import User

fake = Faker()


class UserFactory(Factory):
    class Meta:
        model = User

    name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    password = fake.password()
