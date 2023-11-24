from fastapi import FastAPI ,Depends,Query                         #importing fastapi
from .import  models,schemas                         
from .database import engine,SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db ():

    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()    



@app.post("/tag")

def create_tags(request:schemas.TagsBase,db : Session = Depends(get_db)):

    new_tag=models.Tags(name=request.name)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag


@app.post("/review")

def create_review(request:schemas.ReviewBase,db : Session = Depends(get_db)):

    new_review=models.Reviews(text=request.text,is_tagged=request.is_tagged)
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@app.post("/review/{review_id}/tags")
def adding_tags_to_reviews(review_id:int,tag_id:list[int],db : Session = Depends(get_db)):

    review=db.query(models.Reviews).filter(models.Reviews.id == review_id).first()
    
    if not review:
       return 'Invalid id'
      
    else:

        for tag_id in tag_id:
            tag = db.query(models.Tags).filter(models.Tags.id == tag_id).first()

            if tag:

                review_tag=models.Review_tags(is_ai_tag=False,tag_id=tag.id)
                db.add(review_tag)
                
                review1_tag = models.Review_review_tags(review_id=review_id,review_tag_id=tag.id)
                db.add(review1_tag)

                return 'added'

            else:

                return 'Invalid tag id '
           


@app.get("/reviews")
def get_reviews(skip: int = Query(0, alias="page"), limit: int = Query(10),db: Session = Depends(get_db)):
   
        reviews = db.query(models.Reviews).offset(skip).limit(limit).all()

        response = []

        for review in reviews:

            tags = db.query(models.Tags).filter(models.Review_tags.tag_id == models.Tags.id,
                                                                      models.Review_review_tags.review_id == review.id).all()
            
            response.append({"review": review, "tags": tags})

        return response

    
    
@app.delete("/tags/{tag_id}")
def delete(tag_id:int,db : Session = Depends(get_db)):

    tag_id = db.query(models.Tags).filter(models.Tags.id ==tag_id)

    if not tag_id.first():
        return 'invalid id'
    
    tag_id.delete()
    db.commit()

    review_tags = db.query(models.Review_tags).filter(models.Review_tags.tag_id == tag_id).all()
    for review_tag in review_tags:
        db.delete(review_tag)

    db.commit()

    return 'done'



