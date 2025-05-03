import requests

JAVA_API_BASE_URL = "https://glossary-java-api-production.up.railway.app"

def convert_sdltm_to_tmx(file_path: str) -> str:
    with open(file_path, "rb") as f:
        response = requests.post(
            f"{JAVA_API_BASE_URL}/convert/sdltm-to-tmx",
            files={"file": f}
        )
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Conversion failed: {response.status_code} - {response.text}")
