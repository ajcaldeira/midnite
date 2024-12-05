from typing import Union
from midnite.models.enumerators.alert_codes import AlertCodes
from midnite.models.enumerators.transaction_types import TransactionTypes
from midnite.methods.db_engine import get_db
from midnite.config.constants import (
    WITHDRAWL_LIMIT,
    CONSECUTIVE_WITHDRAWLS_LIMIT,
    CONSECUTIVE_INCREASING_DEPOSITS_LIMIT,
    DEPOSIT_WINDOW_SECONDS,
    ACCUMULATE_DEPOSIT_LIMIT,
)
from midnite.models.database.users import Transactions
from sqlalchemy.orm import Session
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError


class FraudDetection:
    def __init__(self) -> None:
        self.db_session: Session = next(get_db())

    def check_withdrawl_limit(self, amount: Union[int, float]) -> AlertCodes | None:
        """
        Check if the withdrawl amount exceeds the limit

        Args:
            amount (Union[int, float]): The amount to be withdrawn

        Returns:
            int | None: The alert code if the withdrawl limit is exceeded

        """
        try:
            if amount > WITHDRAWL_LIMIT:
                return AlertCodes.CODE_1100
            return None
        except Exception as error:
            logger.error(f"An unknown error occured: {error}")
            raise

    def check_consecutive_withdrawls(self, user_id: str) -> AlertCodes | None:
        """
        Check if the user has exceeded the consecutive withdrawls limit

        Args:
            user_id (str): The user_id to check

        Returns:
            int | None: The alert code if the consecutive withdrawls limit is exceeded
        """
        # Query the Transactions table, order by second_received, filter by user_id
        try:
            transactions = (
                self.db_session.query(Transactions)
                .filter(
                    Transactions.user_id == user_id,
                )
                .order_by(Transactions.second_received.desc())
                .limit(2)
            )
            if transactions is None or transactions == []:
                return None
            # Check each transaction for withdraws and count them
            withdraw_count = 0
            for transaction in transactions:
                if transaction.transaction_type == TransactionTypes.WITHDRAW:
                    withdraw_count += 1
            # Add 1 here to account for the current transaction that would be processed
            if withdraw_count + 1 >= CONSECUTIVE_WITHDRAWLS_LIMIT:
                return AlertCodes.CODE_30
            return None

        except SQLAlchemyError as error:
            logger.error(f"An error occured while querying the database: {error}")
            raise

        except Exception as error:
            logger.error(f"An unknown error occured: {error}")
            raise

    def check_consecutive_increasing_deposits(
        self, user_id: str, deposit_amount: float
    ) -> AlertCodes | None:
        """
        Check if the user has exceeded the consecutive increasing deposits limit

        Args:
            user_id (str): The user_id to check
            deposit_amount (float): The amount of the deposit

        Returns:
            int | None: The alert code if the consecutive increasing deposits limit is exceeded
        """
        # Query the Transactions table, order by second_received, filter by user_id and transaction_type
        # Get the last 2 transactions which are deposits
        try:
            transactions = (
                self.db_session.query(Transactions)
                .filter(
                    Transactions.user_id == user_id,
                    Transactions.transaction_type == TransactionTypes.DEPOSIT,
                )
                .order_by(Transactions.second_received.desc())
                .limit(CONSECUTIVE_INCREASING_DEPOSITS_LIMIT)
                .all()
            )

            if len(transactions) == CONSECUTIVE_INCREASING_DEPOSITS_LIMIT:
                last, second_last = transactions
                if (
                    last.transaction_amount
                    > second_last.transaction_amount
                    < deposit_amount
                ):
                    return AlertCodes.CODE_300
            return None

        except SQLAlchemyError as error:
            logger.error(f"An error occured while querying the database: {error}")
            raise

        except Exception as error:
            logger.error(f"An unknown error occured: {error}")
            raise

    def check_accumulate_deposit_amount_over_window(
        self, user_id: str, transaction_amount: float, second_received: int
    ) -> AlertCodes | None:
        """
        Check if the user has exceeded the accumulated deposit limit over a 30 second window

        Args:
            user_id (str): The user_id to check
            transaction_amount (float): The amount of the deposit
            second_received (int): The time the transaction was received

        Returns:
            int | None: The alert code if the accumulated deposit limit is exceeded
        """
        # Query the Transactions table, order by second_received, filter by user_id and transaction_type
        try:
            transactions = (
                self.db_session.query(Transactions)
                .filter(
                    Transactions.user_id == user_id,
                    Transactions.transaction_type == TransactionTypes.DEPOSIT,
                )
                .order_by(Transactions.second_received.desc())
                .limit(DEPOSIT_WINDOW_SECONDS)
                .all()
            )

            # Identify those in the 30 second window
            accumulating_deposit = transaction_amount
            # Usint the most recent transaction, check if the difference between the current transaction and the last transaction is greater than 30 seconds
            for transaction in transactions:
                current_window = second_received - transaction.second_received
                if current_window > DEPOSIT_WINDOW_SECONDS:
                    break
                accumulating_deposit += transaction.transaction_amount

            if accumulating_deposit > ACCUMULATE_DEPOSIT_LIMIT:
                return AlertCodes.CODE_123
            return None
        except SQLAlchemyError as error:
            logger.error(f"An error occured while querying the database: {error}")
            raise
        except Exception as error:
            logger.error(f"An unknown error occured: {error}")
            raise

    def run_fraud_detection(
        self,
        transaction_amount: float,
        user_id: str,
        transaction_type: str,
        second_received: int,
    ) -> list[AlertCodes | None]:
        """
        Run the fraud detection checks

        Args:
            transaction_amount (float): The amount of the transaction
            user_id (str): The user_id to check
            transaction_type (str): The type of transaction
            second_received (int): The time the transaction was received

        Returns:
            List[int | None]: A list of alert codes
        """
        alert_codes = []
        match transaction_type:
            case TransactionTypes.DEPOSIT:
                alert_codes.append(
                    self.check_accumulate_deposit_amount_over_window(
                        user_id, transaction_amount, second_received
                    )
                )
                alert_codes.append(
                    self.check_consecutive_increasing_deposits(
                        user_id, transaction_amount
                    )
                )
            case TransactionTypes.WITHDRAW:
                alert_codes.append(
                    self.check_withdrawl_limit(amount=transaction_amount)
                )
                alert_codes.append(self.check_consecutive_withdrawls(user_id))
            case _:
                raise NotImplementedError(
                    f"Transaction type <{transaction_type}> not supported"
                )
        return alert_codes


def get_fraud_detection() -> FraudDetection:
    return FraudDetection()
