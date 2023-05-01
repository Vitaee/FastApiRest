import time, jwt, os, datetime
from typing import Dict, Union, Any
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

class JwtHandler:

    def __init__(self) -> None:
        self.jwt_secret = os.getenv('JWT_SECRET')
        self.jwt_algorithm = os.getenv('JWT_ALGORITHM')

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

    def decode_jwt(self, token:str) -> Union[Dict[str,Any], None]:
        try:
            decoded_token = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
    
            if decoded_token['exp'] >= int(time.time()):
                return decoded_token  
            return None
        except Exception as err: pass

        #except jwt.ExpiredSignatureError:
        #   raise HTTPException(status_code=401, detail='Token expired')
        #except jwt.InvalidTokenError:
        #    raise HTTPException(status_code=401, detail='Invalid token')
