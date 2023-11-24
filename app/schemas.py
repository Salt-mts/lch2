from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# ***********USER SCHEMAS*************
class RegisterUser(BaseModel):
    email: EmailStr
    password: str


class Password(BaseModel):
    password: str
    old_password: str

class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    firstname: Optional[str]
    lastname: Optional[str]
    phone: Optional[str]
    sex: Optional[str]
    image: Optional[str]
    is_active: bool
    date_created: datetime
    verification_code: Optional[int]
    email_verified: Optional[int]

class UserOut(BaseModel):
    id: int
    email: EmailStr
    firstname: Optional[str]
    lastname: Optional[str]
    phone: Optional[str]
    sex: Optional[str]
    image: Optional[str]
    is_active: bool
    date_created: datetime
    email_verified: Optional[int]
    

class Personal(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    phone: Optional[str]
    sex: Optional[str]

class PersonalImg(BaseModel):
    user_id: int
    image: str

# authentication
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


#************ RESPOSNSE SCHEMAS ******************
class RegResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    date_created: datetime

    class Config:
        from_attributes = True


class UserResponse(RegResponse):
    pass
    # firstname: Optional[str]
    # lastname: Optional[str]
    # phone: Optional[int]
    # address: Optional[str]
    # city: Optional[str]
    # state: Optional[str]
    # country: Optional[str]

    class Config:
        from_attributes = True



#******************CATALOG SCHEMAS ***********************
class Catalog(BaseModel):
    name: str
    price: Optional[float] 
    description: Optional[str]
    image1: str
    image2: Optional[str]
    image3: Optional[str]

class CatalogResponse(Catalog):
    id: int

class CatalogImage(BaseModel):
    image1: str
    image2: Optional[str]
    image3: Optional[str]



#************ CERTIFICATION SCHEMAs ******************
class Cert(BaseModel):
    name: str
    image: str

class CertResponse(Cert):
    id: int


#******************COMMENTS SCHEMAS ***********************
class Comment(BaseModel):
    msg: str

class CommentResponse(Comment):
    id: int
    business_id: int
    user_id: int
    commenter: UserOut

class Commenter(BaseModel):
    user_id: int



#************ CONVERSATION SCHEMAS ******************
class Conversation(BaseModel):
    conversation_id: str
    sender_id: int
    receiver_id: int
    

#************ MESSAGE SCHEMAS ******************
class Message(BaseModel):
    message: Optional[str]
    image: Optional[str]

class MessageResponse(Message):
    id: int
    conversation_id: str
    read: int
    date_added: datetime


#************ RATING SCHEMAS ******************
class Rating(BaseModel):
    rating: int

class RatingResponse(Rating):
    id: int
    business_id: int
    user_id: int
    date_added: datetime
    

#************ BUSINESS SCHEMAS ******************

class Business(BaseModel):
    id: int
    name: str
    about: Optional[str]
    category: Optional[str]
    years_of_experience: Optional[int]
    work_experience: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    days: Optional[str]
    hour_from: Optional[str]
    hour_to: Optional[str]
    website: Optional[str]
    facebook: Optional[str]
    instagram: Optional[str]
    twitter: Optional[str]
    linkedin: Optional[str]
    owner: UserOut
    catalog: List[CatalogResponse]
    certifications: List[CertResponse]
    comments: List[CommentResponse]


class BusinessAbout(BaseModel):
    name: str
    about: Optional[str]
    category: Optional[str]

class BusinessExperience(BaseModel):
    work_experience: Optional[str]
    years_of_experience: Optional[int]

class BusinessAddress(BaseModel):
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]

class BusinessSocial(BaseModel):
    website: Optional[str]
    facebook: Optional[str]
    instagram: Optional[str]
    twitter: Optional[str]
    linkedin: Optional[str]

class BusinessHour(BaseModel):
    days: Optional[str]
    hour_from: Optional[str]
    hour_to: Optional[str]







#************ CATEGORY SCHEMA ******************
class Category(BaseModel):
    name: str
    image: Optional[str]
    description: Optional[str]
    parent_id: int

class CategoryResponse(Category):
    id: int

