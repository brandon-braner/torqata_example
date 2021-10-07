from typing import List, Optional

from pydantic import BaseModel, Field

from app.response_schemas import BaseResponseSchema


class TitleSchema(BaseModel):
    date_added: Optional[str] = Field(description="Date the movie was added to Netflix")
    netflix_id: str = Field(description="Id of movie on netflix")
    release_year: Optional[str] = Field(description="Year the title was released")
    rating: Optional[str] = Field(description="Title viewer rating")
    description: Optional[str] = Field(description="Description / Synopsis of the title")
    title: str = Field(description="Title of the title")
    title_type: str = Field(description="Type of the title (Movie / TV Show")


class TitleResponseSchema(BaseResponseSchema):
    titles: List = List[TitleSchema]
