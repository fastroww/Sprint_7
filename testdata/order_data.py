import random
from faker import Faker
import datetime

fake = Faker("ru_RU")

MAX_DELIVERY_DAYS = 7
COMMENT_WORDS = 6

FIRST_NAME = "firstName"
LAST_NAME = "lastName"
ADDRESS = "address"
METRO_STATION = "metroStation"
PHONE = "phone"
RENT_TIME = "rentTime"
DELIVERY_DATE = "deliveryDate"
COMMENT = "comment"
COLOR = "color"


def generate_fake_order_data(color=None):
    """
    Генерирует данные для заказа, используя Faker (ru_RU).
    :param color: список цветов (например, ["BLACK"] или ["GREY"]) или None.
    :return: dict - тело запроса для создания заказа.
    """
    # Придумываем дату доставки: возьмём сегодня + 1..max_delivery_days дней
    today = datetime.date.today()
    delta_days = random.randint(1, MAX_DELIVERY_DAYS)
    future_date = today + datetime.timedelta(days=delta_days)
    delivery_date_str = future_date.isoformat()

    payload = {
        FIRST_NAME: fake.first_name(),
        LAST_NAME: fake.last_name(),
        ADDRESS: fake.address().replace("\n", " "),
        METRO_STATION: str(random.randint(1, 200)),
        PHONE: fake.phone_number(),
        RENT_TIME: random.randint(1, 7),
        DELIVERY_DATE: delivery_date_str,
        COMMENT: fake.sentence(nb_words=COMMENT_WORDS)
    }

    if color:
        payload[COLOR] = color

    return payload