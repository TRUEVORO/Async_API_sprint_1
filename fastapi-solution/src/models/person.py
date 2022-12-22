from utils import OrjsonMixin, UUIDMixin


class Person(UUIDMixin, OrjsonMixin):
    full_name: str
    role: str
