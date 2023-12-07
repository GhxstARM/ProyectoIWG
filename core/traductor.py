from google.cloud import translate_v2 as translate
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'C:/Users/Ghxst/OneDrive/Escritorio/Project/ProyectoIWG/credenciales/translingua-405222-5075717f91db.json' 

def traducir(archivo_srt, idioma_destino):
    translator = translate.Client()
    with open(archivo_srt, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    translated_lines = []
    for line in lines:
        translation = translator.translate(line, target_language=idioma_destino)
        translated_lines.append(translation['input'] + '\n' + translation['translatedText'])

    traduccion_srt = '\n'.join(translated_lines)

    return traduccion_srt
