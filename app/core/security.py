from fastapi.security import OAuth2PasswordBearer

# tokenUrl must match the route that issues the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")