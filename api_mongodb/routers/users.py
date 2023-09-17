from fastapi import APIRouter,HTTPException,status
from datetime import datetime
from db.conection import db_client
from db.models.user_models import User, UserMetadata
from db.schemas.user_schema import user_schema, users_schema, user_meta_schema, users_meta_schema
from bson import ObjectId

router = APIRouter(prefix='/users',
                   responses={status.HTTP_404_NOT_FOUND: {"msg":"Usuario no encontrado."}})


def seach_user(field: str, key, meta = False) -> User:
    try:
        if not meta:
            user = db_client.new_users.find_one({field:key})
            return User(**user_schema(user))
        else:
            user = db_client.new_users_meta.find_one({field:key})
            return UserMetadata(**user_meta_schema(user))
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

    # Agregamos a nuestra BD 'new_users_meta' para obtener los meta datos del registro.
    user_meta_dict = user_dict
    user_meta_dict['created_at'] = str(datetime.now())
    user_meta_dict['last_modified'] = str(datetime.now())
    user_meta_dict['is_new'] = True
    user_meta_dict['is_active'] = True
    db_client.new_users_meta.insert_one(user_meta_dict)

    new_user = user_schema(db_client.new_users.find_one({"_id":id}))

    return User(**new_user)


# READ
@router.get('/count', status_code=status.HTTP_200_OK)
async def getUsersCount():
    return {"Total registros": len(users_schema(db_client.new_users.find()))}

@router.get('/', response_model=list[User], status_code=status.HTTP_200_OK)
async def getUsers():
    return users_schema(db_client.new_users.find())

@router.get('/id/{id}', status_code=status.HTTP_200_OK)
async def getUsersbyID(id: str):
    return seach_user("_id",ObjectId(id))

@router.get('/meta', response_model=list[UserMetadata], status_code=status.HTTP_200_OK)
async def getUsersMeta():
    return users_meta_schema(db_client.new_users_meta.find())

@router.get('/meta/id/{id}', status_code=status.HTTP_200_OK)
async def getUsersMetabyID(id: str):
    return seach_user(field="_id",key=ObjectId(id),meta=True)

@router.get('/meta/count', status_code=status.HTTP_200_OK)
async def getUsersMetaCount():
    return {"Total registros": len(users_meta_schema(db_client.new_users_meta.find()))}

# UPDATE
@router.put('/',status_code=status.HTTP_200_OK)
async def modifyUser(user: User):

    user_dict = dict(user)
    del user_dict['id']
    
    # Se actualizan los metadatos
    user_meta_dict = user_meta_schema(db_client.new_users_meta.find_one({"_id":ObjectId(user.id)}))
    user_meta_dict['last_modified'] = str(datetime.now())
    user_meta_dict['is_new'] = False

    try:
        db_client.new_users.find_one_and_replace({"_id":ObjectId(user.id)},user_dict)
        db_client.new_users_meta.find_one_and_replace({"_id":ObjectId(user.id)},user_meta_dict)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="El usuario no se encuentra en la base de datos.")
    return {"msg": "Usuario actualizado correctamente"}

# DELETE
@router.delete('/{id}',status_code=status.HTTP_200_OK)
async def deleteUser(id: str):
    
    exeption = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='No se pudo eliminar el usuario.')
         
    try:
        # Se actualizan los metadatos
        user_meta_dict = user_meta_schema(db_client.new_users_meta.find_one({"_id":ObjectId(id)}))
        user_meta_dict['last_modified'] = str(datetime.now())
        user_meta_dict['is_active'] = False

        found = db_client.new_users.find_one_and_delete({"_id": ObjectId(id)})
        if not found:
            raise exeption
        else:
            db_client.new_users_meta.find_one_and_replace({"_id":ObjectId(id)},user_meta_dict)
    except:
        raise exeption
    
    return {"msg": "Se elimino al usuario."}

