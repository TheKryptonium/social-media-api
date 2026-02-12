from dotenv import load_dotenv
from imagekitio import ImageKit
import os

load_dotenv()

# On vérifie d'abord que les variables existent (Fail-fast)
private_key = os.getenv("IMAGEKIT_PRIVATE_KEY")
public_key = os.getenv("IMAGEKIT_PUBLIC_KEY")
url_endpoint = os.getenv("IMAGEKIT_URL_ENDPOINT")

if not all([private_key, public_key, url_endpoint]):
    raise ValueError("Certaines variables d'environnement ImageKit sont manquantes !")

# L'instanciation doit regrouper les trois piliers
imagekit = ImageKit(
    private_key=private_key
)