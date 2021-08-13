import time, jwt, os, datetime
from typing import Dict
from dotenv import load_dotenv
from pathlib import Path
from fastapi import HTTPException
from passlib.context import CryptContext

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)


class JwtHandler:

    def __init__(self) -> None:
        self.jwt_secret = os.getenv('JWT_SECRET')
        self.jwt_algorithm = os.getenv('JWT_ALGORITHM')

        self.hasher = CryptContext(schemes=['bcrypt'])
        

    def encode_password(self, password):
        return self.hasher.hash(password)

    def verify_password(self, password, encoded_password):
        return self.hasher.verify(password, encoded_password)

    def token_response(self, token:str) -> dict:
        return {'access_token': token}

    def sign_jwt(self, email: str) -> Dict[str, str]:
        payload ={
            "email":email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=2),
            "iat": datetime.datetime.utcnow()
        }

     
        token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)

        return self.token_response(token)

    def decode_jwt(self, token:str):
        try:
            decoded_token = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            token_time = datetime.datetime.fromtimestamp(decoded_token["exp"] / 1e3) # Wrong conversation
            print(token_time) # [BUG] decoded['exp'] is int 

            if token_time >= datetime.datetime.utcnow():
                return decoded_token  
            #raise HTTPException(status_code=401, detail='token is invalid')
            return None
        except Exception as err:
            print(err)

        #except jwt.ExpiredSignatureError:
        #   raise HTTPException(status_code=401, detail='Token expired')
        #except jwt.InvalidTokenError:
        #    raise HTTPException(status_code=401, detail='Invalid token')
