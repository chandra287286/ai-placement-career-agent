from ollama import chat


MODEL_NAME = "qwen2.5:3b"


def generate_structured_response(
    system_prompt: str,
    user_prompt: str,
    schema
):

    response = chat(
        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],

        format=schema.model_json_schema(),

        options={
            "temperature": 0
        }
    )

    return schema.model_validate_json(
        response.message.content
    )