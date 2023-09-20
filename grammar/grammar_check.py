import language_tool_python
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')  # Download the necessary data for NLTK tokenization

# Initialize the LanguageTool for grammar checking
grammar_tool = language_tool_python.LanguageToolPublicAPI('en-US')

def gc(recognized_text):
    try:
        # Tokenize sentences and words using NLTK
        sentences = sent_tokenize(recognized_text)
        tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]

        # Perform grammar checking and text correction
        corrected_sentences = [grammar_tool.correct(" ".join(tokens)) for tokens in tokenized_sentences]
        corrected_text = " ".join(corrected_sentences)

        # Return the corrected text to the user
        return f'Grammar checking and text correction completed. Corrected text: {corrected_text}'
    except Exception as e:
        # Handle any exceptions that occur during grammar checking
        return f'Grammar checking and text correction failed. Error: {str(e)}'
