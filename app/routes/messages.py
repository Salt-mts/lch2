from fastapi import APIRouter, HTTPException, Depends, status, UploadFile
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session 
from typing import List
from sqlalchemy import or_, desc
from ..utils import generate_unique_id
from fastapi.responses import JSONResponse
import shutil
import os
import uuid

router = APIRouter(
    tags=['messages']
)

def verify_owner(conversation_id, user_id, db):    
    msg = db.query(models.Messages).filter(models.Messages.conversation_id == conversation_id).first()
    if user_id == msg.sender_id:
        return True
    elif user_id == msg.receiver_id:
        return True
    else:
        return False


# ***************UPLOAD MESSAGE IMAGE*******************
@router.post("/message/upload/")
def upload_message_image(file: UploadFile ):

    # Define the directory to save uploaded images
    UPLOAD_DIRECTORY = "uploads/messages/"

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
 

# ***************ADD Message*******************
@router.post("/message/{receiver_id}", status_code=status.HTTP_200_OK)
def send_message(receiver_id: int, msg: schemas.Message, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    if not current_user.firstname:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Update your firstname and lastname to send a message")
    
    query = db.query(models.Conversations).filter(or_(models.Conversations.sender_id == current_user.id, models.Conversations.receiver_id == current_user.id))
    
    if query.first():
        conversation_id = query.first().conversation_id

        # insert into messages table
        insert = models.Messages(conversation_id = conversation_id, **msg.model_dump())
        db.add(insert)
        db.commit()
        db.refresh(insert)
        return insert
    
    else:
        conversation_id = generate_unique_id(10) 

        # insert into messages table   
        insert = models.Messages(conversation_id = conversation_id, **msg.model_dump())
        db.add(insert)
        db.commit()
        db.refresh(insert)
    
        # insert into conversation table   
        conv = models.Conversations(conversation_id = conversation_id, receiver_id = receiver_id, sender_id = current_user.id)
        db.add(conv)
        db.commit()
        db.refresh(conv)
        return conv


# ***************UPDATE COMMENT*******************
# @router.put("/comment/{comment_id}", status_code=status.HTTP_200_OK)
# def update_comment(comment_id: int, comment: schemas.Comment, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

#     query = db.query(models.Comments).filter(models.Comments.id == comment_id)
#     if query.first() is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment not found")
    
#     if not verify_owner(comment_id, current_user.id, db):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not authorized to edit someone else's comment")
    
#     query.update(comment.model_dump(), synchronize_session=False)
#     db.commit()
#     return query.first()




 

# ***************DELETE COMMENT*******************
# @router.delete('/comment/{comment_id}')
# def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
#     query = db.query(models.Comments).filter(models.Comments.id == comment_id)
#     if not query.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment not found")


#     if not verify_owner(comment_id, current_user.id, db):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not authorized to delete someone else's comment")


#     query.delete(synchronize_session=False)
#     db.commit()
#     return{"data":"deleted"}


# ***************GET MESSAGES*******************
@router.get('/message', status_code=status.HTTP_200_OK)
def get_my_messages(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    
    # query = db.query(models.Messages).distinct(models.Messages.conversation_id).filter(or_(models.Messages.sender_id == current_user.id, models.Messages.receiver_id == current_user.id)).all()

    query = db.query(models.Conversations).filter(or_(models.Conversations.sender_id == current_user.id, models.Conversations.receiver_id == current_user.id)).order_by(desc(models.Conversations.id)).all()
    
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No messages found")  
    
    # return query
    my_list=[]
    for i in query:
        if i.sender_id is not current_user.id:
            chat_with = i.sender_id
        else:
            chat_with = i.receiver_id
        
        my_list.append({"chat_with": chat_with})
        return my_list

        # return {"conversation_id": i, "chat_with": chat_with}
     



# ***************GET ONE MESSAGING*******************
@router.get('/message/{conversation_id}', status_code=status.HTTP_200_OK, response_model=List[schemas.MessageResponse])
def get_single_message(conversation_id: str, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    query = db.query(models.Messages).filter(models.Messages.conversation_id == conversation_id)

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No conversation with id of {conversation_id}")  
    
    if not verify_owner(conversation_id, current_user.id, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You not autorized to view this message {conversation_id}")  
     
    return query