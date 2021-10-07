from fastapi import APIRouter, Query, Depends

from app.response_schemas import APIResponseSchema, MetaData
from app.services.title_service import TitleService
from app.services.url_service import generate_next_url

router = APIRouter()


async def common_parameters(
        skip: int = Query(0, description="Offset of items to skip before querying for results"),
        limit: int = Query(10, description="Number of items to return"),
        order_field: str = Query('title', description="Field to order the results by."),
        order_direction: str = Query('ASC', description="Direction to order results by. ASC=ascending DESC=descending")
):
    return {"skip": skip, "limit": limit, "order_field": order_field, "order_direction": order_direction}


@router.get(
    "/movies",
    response_model=APIResponseSchema
)
def index(commons: dict = Depends(common_parameters)):
    """Get a list of all the movies."""
    title_service = TitleService()
    movies = title_service.get_movies(limit=commons['limit'], skip=commons['skip'], order_field=commons['order_field'],
                                      order_direction=commons['order_direction'])

    next_url = generate_next_url('movies', skip=commons['skip'], limit=commons['limit'],
                                 order_field=commons['order_field'], order_direction=commons['order_direction'])

    meta_data = MetaData(next_url=next_url)
    return APIResponseSchema(
        data=movies,
        meta_data=meta_data
    )
