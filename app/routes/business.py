from fastapi import APIRouter, HTTPException, Depends, status
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy import func, or_
from sqlalchemy.orm import Session 
from typing import List

router = APIRouter(
    tags=['business']
)

# ***************ADD/UPDATE BUSINESS NAME/ABOUT*******************
@router.post("/business", status_code=status.HTTP_201_CREATED, response_model=schemas.Business)
def add_business(biz: schemas.BusinessAbout, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    query = db.query(models.Business).filter(models.Business.owner_id == current_user.id)

    #details exist
    details_exist = query.first()
    if details_exist:
        query.update(biz.model_dump(), synchronize_session=False)
        db.commit()
        return query.first()
    else:
        # insert = models.Business(owner_id = current_user.id, name = biz.name, about = biz.about)
        insert = models.Business(owner_id = current_user.id, **biz.model_dump())
        db.add(insert)
        db.commit()
        db.refresh(insert)
        return insert
    

# ***************ADD/UPDATE EXPERIENCE*******************
@router.post("/business/experience", status_code = status.HTTP_201_CREATED, response_model=schemas.Business)
def update_experience(biz: schemas.BusinessExperience, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.Business).filter(models.Business.owner_id == current_user.id)

    biz_exist = query.first()
    if biz_exist:
        query.update(biz.model_dump(), synchronize_session=False)
        db.commit()
        return query.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found, create a business first")
    

# ***************ADD/UPDATE ADDRESS*******************
@router.post("/business/address", status_code = status.HTTP_201_CREATED, response_model=schemas.Business)
def update_address(biz: schemas.BusinessAddress, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.Business).filter(models.Business.owner_id == current_user.id)

    biz_exist = query.first()
    if biz_exist:
        query.update(biz.model_dump(), synchronize_session=False)
        db.commit()
        return query.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found, create a business first")
    


# ***************ADD/UPDATE WORKING DAYS AND TIME*******************
@router.post("/business/schedule", status_code = status.HTTP_201_CREATED, response_model=schemas.Business)
def update_schedule(biz: schemas.BusinessHour, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.Business).filter(models.Business.owner_id == current_user.id)

    biz_exist = query.first()
    if biz_exist:
        query.update(biz.model_dump(), synchronize_session=False)
        db.commit()
        return query.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found, create a business first")
    


# ***************ADD/UPDATE SOCIAL HANDLES*******************
@router.post("/business/social", status_code = status.HTTP_201_CREATED, response_model=schemas.Business)
def update_social_media(biz: schemas.BusinessSocial, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.Business).filter(models.Business.owner_id == current_user.id)

    biz_exist = query.first()
    if biz_exist:
        query.update(biz.model_dump(), synchronize_session=False)
        db.commit()
        return query.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found, create a business first")
    
# ***************GET LOGGED IN USER BUSINESS AND DETAILS*******************
@router.get("/business", status_code=status.HTTP_200_OK, response_model=schemas.Business)
def get_my_business(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    results =  db.query(models.Business).filter(current_user.id == models.Business.owner_id).first()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business no found, create a business.")
    
    return results


# ***************GET SINGLE BUSINESSES*******************
@router.get("/business/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Business)
def get_single_business( id: int, db: Session = Depends(get_db)):
    results =  db.query(models.Business).filter(models.Business.id == id).first()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business no found.")
    
    return results


# ***************GET ALL BUSINESSES*******************
@router.get("/businesses", status_code=status.HTTP_200_OK, response_model=List[schemas.Business])
def get_all_businesses(db: Session = Depends(get_db)):
    results =  db.query(models.Business).all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" NO business found.")
    
    return results


# ***************SEARCH/QUERY BUSINESSES*******************
@router.get("/search", status_code=status.HTTP_200_OK, response_model=List[schemas.Business])
def query_businesses(db: Session = Depends(get_db), search: str = 'carpenter', limit: int  = 50, location: str = 'lagos'):

  
    results =  db.query(models.Business).filter(or_(func.lower(models.Business.about).like('%' +func.lower(search) + '%'), func.lower(models.Business.city).like('%' +func.lower(location) + '%'))).limit(limit=limit).all()
    
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business no found.")
    
    return results

