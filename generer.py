import os
import time

from dotenv import load_dotenv
from openai import OpenAI
import base64

from save import save_to_db

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def generer_haiku(mots_cles):
    """Génère un haïku avec les mots-clés donnés"""
    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"""Crée un haïku en français (5-7-5 syllabes) 
            incluant : {', '.join(mots_cles)}

            Réponds uniquement avec le haïku."""
        ,
        temperature=0.8
    )
    return response.output_text.strip()


def creer_prompt_image(haiku):
    """Transforme le haïku en prompt pour DALL-E"""
    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"""Analyse ce haïku et crée un prompt détaillé 
            en anglais pour DALL-E :

            {haiku}

            Style : aquarelle japonaise ou estampe traditionnelle.
            Réponds uniquement avec le prompt."""
        ,
        temperature=0.7
    )
    return response.output_text.strip()


def generer_image(prompt_image):
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt_image
    )

    image_base64 = response.data[0].b64_json

    img_bytes = base64.b64decode(image_base64)

    file_path = f"images/haiku_{int(time.time())}.png"

    with open(file_path, "wb") as f:
        f.write(img_bytes)

    return file_path


def creer_haiku_et_image(mots_cles):
    haiku = generer_haiku(mots_cles)
    prompt_image = creer_prompt_image(haiku)
    image_path = generer_image(prompt_image)
    print(prompt_image)
    save_to_db(mots_cles, haiku, image_path)

    return {
        "haiku": haiku,
        "prompt_image": prompt_image,
        "url_image": image_path
    }
