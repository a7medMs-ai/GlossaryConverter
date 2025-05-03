import requests

# ✅ This is your deployed Java API on Railway
JAVA_API_BASE_URL = "https://glossary-java-api-production.up.railway.app"

def convert_sdltm_to_tmx(file_path: str) -> str:
    """
    Send an SDLTM file to the Java API and receive the converted TMX content.
    
    :param file_path: Path to the .sdltm file on disk
    :return: TMX content as a string
    :raises: Exception if the request fails or returns an error
    """
    url = f"{JAVA_API_BASE_URL}/convert/sdltm-to-tmx"
    
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(
            f"Conversion failed: {response.status_code} - {response.text}"
        )
