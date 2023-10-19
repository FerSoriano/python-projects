def user_schema(user) -> dict:
    """
    Return a User class dict 
    """
    return {"id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"]}

def users_schema(users) -> list:
    """
    Return a User class list 
    """
    return [user_schema(user) for user in users]

def user_meta_schema(user) -> dict:
    """
    Return a UserMetadata class dict 
    """
    return {"id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"],
            "created_at" : user["created_at"],
            "last_modified": user["last_modified"],
            "is_new": user["is_new"],
            "is_active": user["is_active"]}

def users_meta_schema(users) -> list:
    """
    Return a UserMetadata class list 
    """
    return [user_meta_schema(user) for user in users]