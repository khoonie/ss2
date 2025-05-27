from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt


from sspackage import models, schemas, auth, database
from sspackage.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username Already Exists")
    hashed = auth.hash_password(user.password)
    new_user = models.User(username = user.username, hashed_password = hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model = schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code = 400, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub":user.username})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str=Depends(oauth2_scheme), db: Session=Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail = "Invalid credentials", headers = {"WWW-Authenticate": "Bearer"})
    try:
            payload = jwt.decode (token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            user = db.query(models.User).filter(models.User.username == username).first()
            if user is None:
                raise credentials_exception
            return user
    except JWTError:
            raise credentials_exception

@app.get("/me")
def read_me(current_user: schemas.UserOut = Depends(get_current_user)):
    return current_user

