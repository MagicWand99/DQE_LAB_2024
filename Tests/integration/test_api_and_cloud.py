import allure
import requests
import pytest

pytestmark = pytest.mark.integration

@allure.title("10 posts exist for user 3 (jsonplaceholder)")
def test_ten_posts_for_user_3(api_base_url):
    with allure.step("Request all posts for userId=3"):
        response = requests.get(f"{api_base_url}/posts", params={"userId": 3})

    with allure.step("Check the response status and post count"):
        assert response.status_code == 200, f"Unexpected status: {response.status_code}"
        posts = response.json()
        assert len(posts) == 10, f"Expected 10 posts for user 3, got {len(posts)}"

@allure.title("Source (GCP) and target (AWS) buckets both have data for the date")
def test_gcp_and_aws_buckets_not_empty(gcs_bucket, s3_client):
    target_date = "2026-09-21"

    with allure.step(f"Check GCP source bucket has objects for {target_date}"):
        gcp_objects = gcs_bucket.list_blobs(prefix=f"forecasts/{target_date}")
        assert len(gcp_objects) > 0, "GCP source bucket is empty for this date"

    with allure.step(f"Check AWS staging bucket has objects for {target_date}"):
        aws_objects = s3_client.list_objects_v2(
            Bucket="staging-bucket", Prefix=f"forecasts/{target_date}"
        )
        assert aws_objects.get("KeyCount", 0) > 0, "AWS staging bucket is empty for this date"
