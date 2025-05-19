from pydantic import BaseModel, Field


class PagingParams(BaseModel):
    page: int = Field(1, gt=0, title="Page Number", description="Number of the page the data will be displayed on")
    rowsPerPage: int = Field(10, ge=0, le=1000, title="Rows per Page", description="Number of elements per page")
    search: str | None = Field(None, title="Search Text", description="Text to search in the database")
