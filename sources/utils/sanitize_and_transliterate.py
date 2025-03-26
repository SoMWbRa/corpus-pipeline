import re
import transliterate
import uuid


def sanitize_and_transliterate(filename: str) -> str:
    filename = transliterate.translit(filename, language_code='uk', reversed=True)

    filename = filename.replace(" ", "_")
    filename = re.sub(r'[^a-zA-Z_ ]', '', filename)

    if not filename:
        filename = f"id_{uuid.uuid4().hex[:8]}"

    return filename


if __name__ == "__main__":
    input = 'Волц: "Розбираємося, як журналіст потрапив у чат Signal"'
    expected_output = 'Volts_Rozbyrayemosja_jak_zhurnalist_potrapyv_u_chat_Signal'
    assert sanitize_and_transliterate(input) == expected_output