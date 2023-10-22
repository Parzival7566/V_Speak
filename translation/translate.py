from translate import Translator

def translate_text(text, target_language):
    try:
        translator = Translator(to_lang=target_language)
        translated_text = translator.translate(text)
        return translated_text
    except Exception as e:
        print(f"Error during translation: {str(e)}")
        return None
