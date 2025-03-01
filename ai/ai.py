from mistralai import Mistral

from config import AI_TOKEN, AI_MODEL
from ai.prompt import YTKER_sys_prompt

def ai_request(message, data_for_bot=''):
    client = Mistral(api_key=AI_TOKEN)
    chath = []
    # Системный промпт
    chath.append({
            "role": "system",
            "content": YTKER_sys_prompt
        })

    #Адишенал инфа
    if data_for_bot != '':
        chath.append({
            "role": "system",
            "content": data_for_bot
        })

    #Сообщение пользователя
    chath.append({
                "role": "user",
                "content": message
            })


    chat = client.chat.complete(
        model=AI_MODEL,
        messages=chath,
        response_format= {
            "type": "json_object"
        }
    )

    return chat.choices[0].message.content