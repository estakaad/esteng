import openai
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ.get("CHATGPT4")

def translate_meaning(to_be_translated):
    openai.api_key = api_key
    prompt_translate = f"Input is word and its definition: '{to_be_translated}'. Output: English words which mean the same thing."

    messages_translate = [
        {"role": "system",
         "content": "You are an assistant for translating words. "
                    "Provide the closest English equivalent terms, separated by semicolons."},
        {"role": "user", "content": prompt_translate}
    ]

    response_translate = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages_translate
    )

    token_usage = response_translate['usage']['total_tokens']
    print(f"Tokens used for meaning '{to_be_translated}': {token_usage}")

    raw_translation = response_translate['choices'][0]['message']['content'].strip()
    return raw_translation

if __name__ == '__main__':
    estonian_words_meanings = ['tulema: lähenedes, lähemale liikuma',
                               'tulema: (kohale) saabuma, kuhugi pärale jõudma',
                               'tulema: ajaliselt järgnema, olema hakkama, tulevikus olema',
                               'vanaisa: isa või ema isa',
                               'lamp: valgust andev tarbeese, mis hrl koosneb ühest või mitmest valgusallikast ja kuplist vm kattest',
                               'pirn: pirnipuu kerajas või piklik, hrl tipust jämedam magus vili',
                               'pirn: klaasist pirni- või torukujuline elektrivalguse allikas, mis hrl on kaetud või ümbritsetud kupliga'
                               ]

    translations = []

    for meaning in estonian_words_meanings:
        result = translate_meaning(meaning)

        if not result:
            print(f"Skipping '{meaning}' due to unexpected response format.")
            continue

        translations.append([meaning, result])

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"output/{timestamp}_chatgpt4_translations.json"

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(translations, f, indent=2, ensure_ascii=False)
