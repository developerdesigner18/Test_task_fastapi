from pydantic import BaseModel


class ReviewBase(BaseModel):
   
   id:int
   text:str
   is_tagged:bool


class TagsBase(BaseModel):
    
    id:int
    name:str


