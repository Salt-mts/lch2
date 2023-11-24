from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile
from .. import models, schemas, oauth2
from ..database import engine, get_db
from sqlalchemy.orm import Session 
from typing import List

from fastapi.responses import JSONResponse
import shutil
import os
import uuid



router = APIRouter(
    tags=['catalog']
)


def verify_owner(cid, uid, db):
    
    biz = db.query(models.Business).filter(models.Business.owner_id == uid).first()
    cert = db.query(models.Catalog).filter(models.Catalog.id == cid).first()
    if biz.id == cert.business_id:
        return True

# ***************ADD CATALOG*******************
@router.post("/catalog", status_code=status.HTTP_200_OK, response_model=schemas.CatalogResponse)
def add_catalog(catalog: schemas.Catalog, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    query = db.query(models.Business).filter(models.Business.owner_id == current_user.id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Business not found")
    
    biz_id = query.first().id
    insert = models.Catalog(business_id = biz_id, **catalog.model_dump())
    db.add(insert)
    db.commit()
    db.refresh(insert)
    return insert


# ***************UPDATE CATALOG*******************
@router.put("/catalog/{id}", status_code=status.HTTP_200_OK)
def update_catalog(id: int, catalog: schemas.Catalog, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    query = db.query(models.Catalog).filter(models.Catalog.id == id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Catalog not found")
    
    if not verify_owner(id, current_user.id, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not authorized to update this catalog")
    
    query.update(catalog.model_dump(), synchronize_session=False)
    db.commit()
    return query.first()




# ***************UPLOAD CATALOG IMAGE*******************
@router.post("/catalog/upload/")
def upload_catalog_image(file: UploadFile ):

    # Define the directory to save uploaded images
    UPLOAD_DIRECTORY = "uploads/catalog/"

    # Create the upload directory if it doesn't exist
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

    # Generate a unique filename for the uploaded image
    file_extension = file.filename.split(".")[-1]
    filename = f"{str(uuid.uuid4())}.{file_extension}"
    
    try:
        # Save the uploaded file to the specified directory
        with open(os.path.join(UPLOAD_DIRECTORY+filename), "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {"filename" : filename}
    
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to upload file: {str(e)}"}, status_code=500)
    

# ***************DELETE CATALOG*******************
@router.delete('/catalog/{id}')
def delete_catalog(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.Catalog).filter(models.Catalog.id == id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Catalog not found")


    if not verify_owner(id, current_user.id, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not authorized to delete this catalog")


    query.delete(synchronize_session=False)
    db.commit()
    return{"data":"deleted"}


# ***************GET CATALOG*******************
@router.get('/catalog/{business_id}', status_code=status.HTTP_200_OK, response_model=List[schemas.CatalogResponse])
def get_certificate(business_id: int, db: Session = Depends(get_db)):
    query = db.query(models.Catalog).filter(models.Catalog.business_id == business_id).all()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No certificates found")   
    return query