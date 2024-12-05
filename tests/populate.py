from midnite.models.database.users import Users as UserDBModel
from midnite.models.validation.users import Users as UserValidation
from midnite.methods.db_engine import get_db
from loguru import logger

try:
    db = next(get_db())
    user_id = 1
    name = "John Doe"
    email = "johndoe@example.com"

    user = {"user_id": user_id, "name": name, "email": email}
    UserValidation.model_validate(user)
    db.add(UserDBModel(**user))
    db.commit()
except Exception as e:
    logger.error(f"Error creating the demo user: {e}")
    raise
logger.success("Demo user created successfully")
