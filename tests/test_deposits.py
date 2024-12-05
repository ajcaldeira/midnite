def test_consecutive_increasing_deposits(test_client, test_db, create_transaction):
    """Test consecutive increasing deposits."""
    # Arrange
    user_id = 1

    create_transaction("1", "deposit", 50, 1, user_id)
    create_transaction("2", "deposit", 60, 3, user_id)

    # Act
    response = test_client.post(
        "/event",
        json={"type": "deposit", "amount": "70.00", "user_id": user_id, "t": 5},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"alert": True, "alert_codes": [300], "user_id": user_id}


def test_accumulate_deposit_amount_over_window(
    test_client, test_db, create_transaction
):
    """
    Test the accumulate deposit amount over a window
    """

    # Arrange
    user_id = 1

    create_transaction("1", "deposit", 150, 1, user_id)
    create_transaction("2", "deposit", 40, 9, user_id)

    # Act
    response = test_client.post(
        "/event",
        json={"type": "deposit", "amount": "70.00", "user_id": user_id, "t": 29},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"alert": True, "alert_codes": [123], "user_id": user_id}
