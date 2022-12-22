from utils import OrjsonMixin, UUIDMixin


class Genre(UUIDMixin, OrjsonMixin):
    name: str
