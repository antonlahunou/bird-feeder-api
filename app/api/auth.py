from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.auth import (
    authenticate_user, create_access_token, create_refresh_token,
    get_current_user, get_db
)
from app.models.user import RefreshToken, User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(user.id)

    db_refresh = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.add(db_refresh)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    token_entry = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.revoked == False
    ).first()

    if not token_entry or token_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user = token_entry.user
    new_access_token = create_access_token(data={"sub": user.username})
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    token_entry = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.user_id == current_user.id
    ).first()

    if token_entry:
        token_entry.revoked = True
        db.commit()

    return {"msg": "Successfully logged out"}