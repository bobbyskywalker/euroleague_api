from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from config.env_loader import get_creds 

security = HTTPBasic()

def verify(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    valid = get_creds()
    if username == valid['username'] and password == valid['password']:
        print('Authentication Success')
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )