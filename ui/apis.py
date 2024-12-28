import os

import requests


def predict_price(lotarea, overallqual, overallcond, centralair, fullbath, bedroomabvgr, garagecars):
    django_url = os.getenv("DJANGO_PUBLIC_URL")
    if not django_url:
        raise ValueError("DJANGO_PUBLIC_URL is not set")

    PREDICTION_ENDPOINT = f"{django_url}/api/learning/predict-price/"
    data = {
        "lotarea": lotarea,
        "overallqual": overallqual,
        "overallcond": overallcond,
        "centralair": centralair,
        "fullbath": fullbath,
        "bedroomabvgr": bedroomabvgr,
        "garagecars": garagecars,
    }
    response = requests.post(PREDICTION_ENDPOINT, json=data)
    if response.status_code == 200:
        return response.json().get("predicted_price", "Error in prediction")
    return f"Error: {response.status_code}, {response.text}"


def record_price(lotarea, overallqual, overallcond, centralair, fullbath, bedroomabvgr, garagecars, saleprice):
    django_url = os.getenv("DJANGO_PUBLIC_URL")
    if not django_url:
        raise ValueError("DJANGO_PUBLIC_URL is not set")
    CREATE_PROPERTY_ENDPOINT = f"{django_url}/api/properties/"
    data = {
        "lotarea": lotarea,
        "overallqual": overallqual,
        "overallcond": overallcond,
        "centralair": 1 if centralair == "Yes" else 0,
        "fullbath": fullbath,
        "bedroomabvgr": bedroomabvgr,
        "garagecars": garagecars,
        "saleprice": saleprice,
        "dataset": "user_submission",  # Indica que es un envío de usuario
        "data_source": 2,  # Verificado
    }
    response = requests.post(CREATE_PROPERTY_ENDPOINT, json=data)
    if response.status_code == 201:
        return response.json().get("message", "Property created successfully")
    return f"Error: {response.status_code}, {response.text}"


def search_property(lotarea, overallqual, overallcond, centralair, fullbath, bedroomabvgr, garagecars):
    centralair = True if centralair == 1 else False
    params = {
        "lotarea": lotarea,
        "overallqual": overallqual,
        "overallcond": overallcond,
        "centralair": centralair,
        "fullbath": fullbath,
        "bedroomabvgr": bedroomabvgr,
        "garagecars": garagecars,
    }
    response = requests.get(f"{os.getenv('DJANGO_PUBLIC_URL')}/api/properties/", params=params)
    if response.status_code == 200:
        return response.json()
    return f"Error: {response.status_code} - {response.text}"


def generate_listing(description, search_results):
    django_url = os.getenv("DJANGO_PUBLIC_URL")
    if not django_url:
        raise ValueError("DJANGO_PUBLIC_URL is not set")

    GENERATE_LISTING_ENDPOINT = f"{django_url}/api/properties/listings/"
    property_id = search_results.get("id")
    if not property_id:
        return "", "Error: No property selected from the search results"

    payload = {
        "property_id": property_id,
        "description": description
    }
    response = requests.post(GENERATE_LISTING_ENDPOINT, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data.get("generated_text", ""), data.get("id", None)
    return "", None


def vote_listing(vote, listing_id):
    django_url = os.getenv("DJANGO_PUBLIC_URL")
    if not django_url:
        raise ValueError("DJANGO_PUBLIC_URL is not set")

    PATCH_LISTING_ENDPOINT = f"{django_url}/api/properties/listings/{listing_id}/"
    print(f"Voting for Listing ID: {listing_id} with vote: {vote}. Calling {PATCH_LISTING_ENDPOINT}")
    # Enviar voto al backend
    payload = {"feedback_score": vote}
    response = requests.patch(PATCH_LISTING_ENDPOINT, json=payload)
    if response.status_code == 200:
        return "Vote registered successfully!"
    return f"Error: {response.status_code} - {response.text}"


def get_customer_profiles(listing_id):
    django_url = os.getenv("DJANGO_PUBLIC_URL")
    if not django_url:
        raise ValueError("DJANGO_PUBLIC_URL is not set")

    GET_PROFILES_ENDPOINT = f"{django_url}/api/properties/profiles/{listing_id}/"
    response = requests.get(GET_PROFILES_ENDPOINT)
    if response.status_code == 200:
        data = response.json()
        return data.get("profiles", [])
    return f"Error: {response.status_code} - {response.text}"
