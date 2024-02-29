import copy
import toml
from pathlib import Path
import google.generativeai as genai

from gen.utils import parse_first_json_snippet

def determine_model_name(given_image=None):
  if given_image is None:
    return "gemini-pro"
  else:
    return "gemini-pro-vision"

def construct_image_part(given_image):
  return {
    "mime_type": "image/jpeg",
    "data": given_image
  }

def call_gemini(prompt="", API_KEY=None, given_text=None, given_image=None, generation_config=None, safety_settings=None):
    genai.configure(api_key=API_KEY)

    if generation_config is None:
        generation_config = {
            "temperature": 0.8,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 8192,
        }

    if safety_settings is None:
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
        ]

    model_name = determine_model_name(given_image)
    model = genai.GenerativeModel(model_name=model_name,
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    USER_PROMPT = prompt
    if given_text is not None:
        USER_PROMPT += f"""{prompt}
    ------------------------------------------------
    {given_text}
    """
    prompt_parts = [USER_PROMPT]
    if given_image is not None:
        prompt_parts.append(construct_image_part(given_image))

    response = model.generate_content(prompt_parts)
    return response.text

def try_out(prompt, given_text, gemini_api_key, given_image=None, retry_num=3):
    qna_json = None
    cur_retry = 0

    while qna_json is None and cur_retry < retry_num:
        try:
            qna = call_gemini(
                prompt=prompt,
                given_text=given_text,
                given_image=given_image,
                API_KEY=gemini_api_key
            )

            qna_json = parse_first_json_snippet(qna)
        except:
            cur_retry = cur_retry + 1
            print("retry")

    return qna_json

def get_basic_qa(text, gemini_api_key, trucate=7000):
    prompts = toml.load(Path('.') / 'constants' / 'prompts.toml')
    basic_qa = try_out(prompts['basic_qa']['prompt'], text[:trucate], gemini_api_key=gemini_api_key)
    return basic_qa


def get_deep_qa(text, basic_qa, gemini_api_key, trucate=7000):
    prompts = toml.load(Path('.') / 'constants' / 'prompts.toml')

    qnas = copy.deepcopy(basic_qa['qna'])
    title = qnas['title']

    for qna in qnas:
        q = qna['question']
        a_expert = qna['answers']['expert']

        depth_search_prompt = prompts['deep_qa']['prompt'] % (title, q, a_expert, "in-depth")
        breath_search_prompt = prompts['deep_qa']['prompt'] % (title, q, a_expert, "broad")

        depth_search_response = {}
        breath_search_response = {}

        while 'follow up question' not in depth_search_response or \
            'answers' not in depth_search_response or \
            'eli5' not in depth_search_response['answers'] or \
            'expert' not in depth_search_response['answers']:
            depth_search_response = try_out(depth_search_prompt, text[:trucate], gemini_api_key=gemini_api_key)

        while 'follow up question' not in breath_search_response or \
            'answers' not in breath_search_response or \
            'eli5' not in breath_search_response['answers'] or \
            'expert' not in breath_search_response['answers']:
            breath_search_response = try_out(breath_search_prompt, text[:trucate], gemini_api_key=gemini_api_key)

        if depth_search_response is not None:
            qna['additional_depth_q'] = depth_search_response
        if breath_search_response is not None:
            qna['additional_breath_q'] = breath_search_response

    return qnas