from app.config import settings


def generate_next_url(uri:str, skip: int, limit: int, order_field: str, order_direction: str):
    app_url = settings.api_domain
    next_skip = skip + limit
    return f"{app_url}/{uri}?skip={next_skip}&limit={limit}&order_field={order_field}&order_direction={order_direction}"