from pydantic import BaseModel

class User(BaseModel):
    id: str or None
    username: str
    email: str

class UserMetadata(User):
    created_at : str
    last_modified: str
    is_new: bool
    is_active: bool
