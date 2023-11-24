from sqlalchemy import Boolean, Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Reviews(Base):

    __tablename__='reviews'

    id=Column(Integer, primary_key=True,autoincrement=True)
    text=Column(String(2048))
    is_tagged=(Boolean)

    new_review_relation = relationship("Review_tags", back_populates="review1")

   

class Tags(Base) :

    __tablename__="tags"  

    id=Column(Integer, primary_key=True,autoincrement=True)
    name=Column(String(50))

    new_tag_relation = relationship("Review_tags",back_populates="tag1")

    def __str__(self):
        return self.name
   
class Review_tags(Base):

    __tablename__='review_tag'

    id=Column(Integer, primary_key=True,autoincrement=True)
    is_ai_tag=Column(Boolean,default=False,nullable=False)
    tag_id=Column(Integer,ForeignKey('tags.id'))
    review_id=Column(Integer,ForeignKey('reviews.id'))

    review1 = relationship("Reviews", back_populates="new_review_relation")
    tag1 = relationship("Tags",back_populates="new_tag_relation")

class Review_review_tags(Base):

    __tablename__='reveiw_review_tags'

    id=Column(Integer, primary_key=True,autoincrement=True)
    review_id=Column(Integer,ForeignKey('reviews.id'))
    review_tag_id=Column(Integer,ForeignKey('review_tag.id'))

    review = relationship("Reviews")
    review_tag = relationship("Review_tags")