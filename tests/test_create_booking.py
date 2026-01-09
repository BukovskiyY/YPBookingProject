import allure
import pytest
import requests
from pydantic import ValidationError
from core.models.booking import BookingResponse


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with custom data')
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        "firstname": "Ivan",
        "lastname": "Ivanovich",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-12-21",
            "checkout": "2025-12-31"
        },
        "additionalneeds": "Dinner"
    }
    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response['booking']['firstname'] == booking_data['firstname']
    assert response['booking']['lastname'] == booking_data['lastname']
    assert response['booking']['totalprice'] == booking_data['totalprice']
    assert response['booking']['depositpaid'] == booking_data['depositpaid']
    assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with random data')
def test_create_booking_generate_random_data(api_client, generate_random_booking_data):
    response = api_client.create_booking(generate_random_booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f'Response validation failed: {e}')

    assert response['booking']['firstname'] == generate_random_booking_data['firstname']
    assert response['booking']['lastname'] == generate_random_booking_data['lastname']
    assert response['booking']['totalprice'] == generate_random_booking_data['totalprice']
    assert response['booking']['depositpaid'] == generate_random_booking_data['depositpaid']
    assert response['booking']['bookingdates']['checkin'] == generate_random_booking_data['bookingdates']['checkin']
    assert response['booking']['bookingdates']["checkout"] == generate_random_booking_data['bookingdates']['checkout']
    assert response['booking']['additionalneeds'] == generate_random_booking_data['additionalneeds']


@allure.feature('Test creating booking')
@allure.story('Negative: creating booking with empty data')
def test_create_booking_with_empty_data(api_client):
    booking_data = {
        "firstname": None,
        "lastname": None,
        "totalprice": None,
        "depositpaid": None,
        "bookingdates": {
            "checkin": None,
            "checkout": None
        },
        "additionalneeds": None
    }

    with pytest.raises(requests.HTTPError) as exc_info:
        api_client.create_booking(booking_data)
    assert exc_info.value.response.status_code == 500, f'Expected status 500 but got {exc_info.value.response.status_code}'


@allure.feature('Test creating booking')
@allure.story('Negative: creating booking with wrong data format in firstname')
def test_create_booking_with_wrong_data_format_in_firstname(api_client, generate_random_booking_data):
    generate_random_booking_data['firstname'] = 100
    with pytest.raises(requests.HTTPError) as exc_info:
        api_client.create_booking(booking_data=generate_random_booking_data)
    assert exc_info.value.response.status_code == 500, f'Expected status 500 but got {exc_info.value.response.status_code}'
