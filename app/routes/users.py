from fastapi import APIRouter, HTTPException, Depends, status
from .. import models, schemas, oauth2
from ..database import engine, get_db
from sqlalchemy.orm import Session 
from ..utils import get_password_hash, verify_password

models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    tags=["User"]
)



@router.get("/")
def root():
    return {"message": "Hello Userssssssssss"}

# ***************REGISTER USER******************
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.RegResponse)
def register(user: schemas.RegisterUser, db: Session = Depends(get_db)):
    user.email = user.email.lower()
    #email exist
    email_exist = db.query(models.User).filter(models.User.email == user.email).first()
    if email_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email exist in our database")
    

    user.password = get_password_hash(user.password)
    new_uza =  models.User(**user.model_dump())
    db.add(new_uza)
    db.commit()
    db.refresh(new_uza)
    return new_uza


# ***************PERSONAL DETAILS*******************
@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def update_personal_details(user: schemas.Personal, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.User).filter(models.User.id == current_user.id)
    
    #details exist
    details_exist = query.first()
    if details_exist:
        query.update(user.model_dump(), synchronize_session=False)
        db.commit()
        return query.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    


# ***************UPDATE PASSWORD*******************
@router.post("/user/password", status_code=status.HTTP_202_ACCEPTED)
def update_password(user: schemas.Password, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    user.password = get_password_hash(user.password)

    query = db.query(models.User).filter(models.User.id == current_user.id)
    
    #user exist
    user_exist = query.first()
    if user_exist:
        verfy_pass = verify_password(user.old_password, user_exist.password)
        if not verfy_pass:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid password")
        
        query.update({"password": user.password}, synchronize_session=False)
        db.commit()
        return {"data": "success"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User doesn't exist")
    

# ***************GET USER DETAILS*******************
@router.get("/user", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_personal_details(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    results =  db.query(models.User).filter(current_user.id == models.User.id).first()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No personal details found.")
    
    return results


#get all users
# @router.get("/users", status_code=status.HTTP_200_OK, response_model=List[schemas.UserResponse])
# def get_users(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
#     uza =  db.query(models.User).all()
#     return uza