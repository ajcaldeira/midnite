def test_withdraw_consecutive_limit(test_client, test_db, create_transaction):
    """
    Test withdraw consecutive limit

    """
    # Arrange
    user_id = 1
    expected_alert_code = 30
    create_transaction("1", "withdraw", 50, 1, user_id)
    create_transaction("2", "withdraw", 20, 2, user_id)

    # Act
    response = test_client.post(
        "/event",
        json={"type": "withdraw", "amount": "5.00", "user_id": user_id, "t": 1},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "alert": True,
        "alert_codes": [expected_alert_code],
        "user_id": user_id,
    }


def test_withdraw_amount_limit(test_client, test_db, create_transaction):
    """
    Test withdraw amount limit.

    """
    # Arrange
    user_id = 1
    expected_alert_code = 1100

    create_transaction("1", "withdraw", 300, 1, user_id)

    # Act
    response = test_client.post(
        "/event",
        json={"type": "withdraw", "amount": "500.00", "user_id": user_id, "t": 1},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "alert": True,
        "alert_codes": [expected_alert_code],
        "user_id": user_id,
    }


def test_multiple_error_codes(test_client, test_db, create_transaction):
    """
    Test multiple error codes.

    """
    # Arrange
    user_id = 1

    create_transaction("1", "withdraw", 50, 1, user_id)
    create_transaction("2", "withdraw", 20, 2, user_id)

    # Act
    response = test_client.post(
        "/event",
        json={"type": "withdraw", "amount": "101.00", "user_id": user_id, "t": 1},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["alert"] is True
    assert response.json()["user_id"] == user_id
    assert 30 in response.json()["alert_codes"]
    assert 1100 in response.json()["alert_codes"]


def test_no_error_codes(test_client, test_db, create_transaction):
    """
    Test multiple error codes.

    """
    # Arrange
    user_id = 1

    create_transaction("1", "withdraw", 50, 1, user_id)
    create_transaction("2", "deposit", 60, 3, user_id)
    create_transaction("3", "withdraw", 80, 9, user_id)

    # Act
    response = test_client.post(
        "/event",
        json={"type": "withdraw", "amount": "11.00", "user_id": user_id, "t": 12},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["alert"] is False
    assert response.json()["user_id"] == user_id
    assert response.json()["alert_codes"] == []
