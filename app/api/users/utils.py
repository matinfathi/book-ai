from sqlmodel import Session

from app.api.users.models import User
from app.core.security import get_password_hash


def create_admin_user(db: Session, username: str, first_name: str, password: str):
    hashed_pw = get_password_hash(password)
    admin = User(
        username=username,
        first_name=first_name,
        hashed_password=hashed_pw,
        is_superuser=True,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin
