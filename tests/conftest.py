import pytest
from fastapi.testclient import TestClient
from midnite.models.database.users import Transactions as TransactionsDBModel
from midnite.models.validation.users import Transactions as TransactionsValidation
from midnite.models.validation.users import Users as UserValidation
from midnite.models.database.users import Users as UserDBModel
from midnite.methods.db_engine import get_db
from midnite.main import app


@pytest.fixture(scope="module")
def test_client():
    """Fixture to create a TestClient."""
    return TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    """Fixture to provide a fresh database session for each test."""
    db = next(get_db())
    try:
        yield db
    finally:
        db.query(TransactionsDBModel).delete()
        db.query(UserDBModel).delete()
        db.commit()


@pytest.fixture
def create_user(test_db):
    """Fixture to create a user in the database."""

    def _create_user(user_id, name, email):
        user = {"user_id": user_id, "name": name, "email": email}
        UserValidation.model_validate(user)
        test_db.add(UserDBModel(**user))
        test_db.commit()
        return user

    return _create_user


@pytest.fixture
def create_transaction(test_db):
    """Fixture to create a transaction in the database."""

    def _create_transaction(
        transaction_id, transaction_type, amount, second_received, user_id
    ):
        transaction = {
            "transaction_id": transaction_id,
            "transaction_type": transaction_type,
            "transaction_amount": amount,
            "second_received": second_received,
            "user_id": user_id,
        }
        TransactionsValidation.model_validate(transaction)
        test_db.add(TransactionsDBModel(**transaction))
        test_db.commit()
        return transaction

    return _create_transaction
