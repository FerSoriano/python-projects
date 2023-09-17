from fastapi import APIRouter,HTTPException,status
from datetime import datetime
from db.conection import db_client
from db.models.user_models import User, UserMetadata
from db.schemas.user_schema import user_schema, users_schema, users_meta_schema

router = APIRouter(prefix='/users',
                   responses={status.HTTP_404_NOT_FOUND: {"msg":"Usuario no encontrado."}})


def seach_user(field, key) -> User:
    try:
        user = db_client.new_users.find_one({field:key})
        return User(**user_schema(user))
    except:
        {"error": "No se ha encontrado usuario."}

# CREATE
@router.post('/',status_code=status.HTTP_201_CREATED,response_model=User)
async def create_user(user: User):
    
    if type(seach_user(field="email",key=user.email)) == User:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="El usuario ya existe en la base de datos.")   

    # El documento que se insertara debe ser de tipo json / dict
    user_dict = dict(user)
    del user_dict['id']

    # Agregamos a nuestra BD 'new_users' y obtenemos el id.
    id = db_client.new_users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.new_users.find_one({"_id":id}))
    
    # Agregamos a nuestra BD 'new_users_meta' para obtener los meta datos del registro.
    user_meta_dict = user_dict
    user_meta_dict['created_at'] = str(datetime.now())
    user_meta_dict['last_modified'] = str(datetime.now())
    user_meta_dict['is_new'] = True
    db_client.new_users_meta.insert_one(user_meta_dict)

    return User(**new_user)


# READ
@router.get('/', response_model=list[User], status_code=status.HTTP_200_OK)
async def getUsers():
    return users_schema(db_client.new_users.find())

@router.get('/meta', response_model=list[UserMetadata], status_code=status.HTTP_200_OK)
async def getUsersMeta():
    return users_meta_schema(db_client.new_users_meta.find())

# UPDATE
# DELETE
