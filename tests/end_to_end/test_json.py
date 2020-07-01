"""This tests a set of edge cases with json output."""
import pytest


def run_json(client: object, json_body: dict):
    _ = client.put("/people/1", json=json_body)
    resp = client.get("/people/1")

    body = resp.json

    assert body["object"] == json_body["object"]


@pytest.mark.requiresdb
def test_json_posts_and_returns_correctly(all_types_generated_e2e_client):
    json_body = {"object": {"key": "value"}}
    run_json(all_types_generated_e2e_client, json_body)


@pytest.mark.requiresdb
def test_nested_str_in_json_posts_and_returns_correctly(all_types_generated_e2e_client):
    json_body = {"object": r'{"key": "value"\}'}
    run_json(all_types_generated_e2e_client, json_body)


@pytest.mark.requiresdb
def test_nested_nested_str_in_json_posts_and_returns_correctly(
    all_types_generated_e2e_client
):
    json_body = {"object": {"but what about this": r'{"key": "value"\}'}}
    run_json(all_types_generated_e2e_client, json_body)


@pytest.mark.requiresdb
def test_long_str(all_types_generated_e2e_client):
    json_body = {
        "object": '{"uuid": "e997a2f7-2809-4543-b55e-edff65d66c62", "first_name": "Aniya", "last_name": "Sauer", "gender": "Female/Woman", "email": "lambda-test-Tate_Emard64@yahoo.com", "phone": null, "phone_type": null, "resume": null, "street": null, "street2": null, "city": null, "state": null, "zipcode": null, "country": "US", "birthdate": "1990-12-12", "highest_education": null, "work_authorized": true, "preferred_language": "english", "unemployment_insurance": null, "race": null, "selective_service": null, "veteran": "{\\"non_veteran\\": true}", "created_at": "2019-10-01 08:45:35 -0600", "last_login": "", "journey_role": null, "ssn_last4": null, "high_school_graduation_year": null, "associated_organization": null, "legacy_data_consent": null, "work_histories": [], "most_recent_completed_assessment": null, "user_employment": {"currently_employed": null, "laid_off": null, "mass_layoff": null, "fired": null, "changing_careers": null, "current_industry": null, "seasonal": true}, "military_histories": [], "certifications": [], "education_histories": [], "language_proficiency": [], "user_question_data": {"job_difficulties": null, "assistance": null, "looking_for": "{\\"job\\": true}", "va_benefits": null, "homeless_risk": null, "incarcerated": null, "divorced": null, "looking_change_self_employment": null, "low_income": null, "housing_situation": null, "satisfied_income": null, "aspired_education": null, "education_training_info": null}'
    }
    run_json(all_types_generated_e2e_client, json_body)
