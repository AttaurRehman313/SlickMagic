from dotenv import load_dotenv
from openai import OpenAI
import ast
import os


load_dotenv()
# Get the API key
api_key = os.getenv("api_key")
openai_api_key = os.getenv("openai_api_key")
assembly_api_key = os.getenv("assembly_api_key")


# *************************
def get_response(prompt):
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()


# *************************
def refine_scripts(script):
    prompt = f"""
    Correct only the spelling mistakes in the following text: "{script}". 
    Do not add, remove, or change the order of any words. 
    Return the text exactly as it is, but with the corrected spellings.
    """
    try:
        refined_script = get_response(prompt)
        return refined_script
    except Exception as e:
        return f"Error Occurred in refine_scripts: {e}"


def create_intent_words(script):
    # Calculate the approximate number of intent words needed
    script_length = len(script.split())
    num_intent_words = max(1, script_length // 4)  # Aim for 1 intent word per 4-5 words

    prompt = f"""Your task is to generate an array of the most significant intent keywords only (without duplications or unimportant words, preferably nouns and verbs, and avoid adjectives) from the script below. 
    Do not repeat similar words or relevantly similar in context words even if they are repeated, and do not choose unimportant words. 
    Choose only important words from the script (e.g., approximately {num_intent_words} words from a {script_length} word script). 
    The chosen words must be in the sequence as given in the script.
    Output should be an array, e.g., ["", "", "", ""]. 
    Output should only contain the list, no other explanation or keywords.
    Script <<<{script}>>>"""

    try:
        # Get the response from the model
        lst = get_response(prompt)

        # Process the response
        typecasted_list = ast.literal_eval(lst)

        # Print debug information
        print("List of Intent Words:", typecasted_list)
        print("Number of Intent Words:", len(typecasted_list))

        # Check if the number of intent words is within an acceptable range
        lower_bound = int(num_intent_words * 0.8)  # 80% of the expected count
        upper_bound = int(num_intent_words * 1.2)  # 120% of the expected count

        if len(typecasted_list) < lower_bound:
            print(f"Generated intent words are fewer than expected. Regenerating...")
            return create_intent_words(script)  # Recursively regenerate if too few
        elif len(typecasted_list) > upper_bound:
            print(f"Generated intent words are more than expected. Trimming...")
            return typecasted_list[:num_intent_words]  # Trim to the expected number

        return typecasted_list
    except Exception as e:
        return f"Error Occurred in create_intent_words: {e}"


# *********************************************************
def create_script(text, n, tolerance=6):
    def get_word_count(text):
        return len(text.split())

    while True:
        try:
            # Generate a prompt with the instruction for the model
            prompt = f"""Generate a script of exactly {n} words based on the following hint: "{text}". 
                        The script should be story-like (like for text="A lion in a jungle", script should be: "the lion was in ...") and should not start with an order like "Create a ..." or "Make a ... or once upon a time". The length of the generated script should be within {n - tolerance} to {n + tolerance} words."""

            # Get the response from the model
            script = get_response(prompt)

            # Check the word count of the generated script
            word_count = get_word_count(script)

            if n - tolerance <= word_count <= n + tolerance:
                print("Generated Script:", script)
                return script
            else:
                print(
                    f"Generated script has {word_count} words, which is outside the acceptable range of {n - tolerance} to {n + tolerance}. Generating again..."
                )

        except Exception as e:
            return f"Error Occurred in create_prompt: {e}"


# # *********************************************************
def generate_keywords_for_transitions(script, keywords_list, num):
    prompt = f"""generate a list of keywords of the length {num}, with same words as {keywords_list} but removing any comma or full stop attached to it and it only should have that word that is present in the {script}.
    Output should be a list of words with no other explanation or any other keyword.
    """
    try:
        lst = get_response(prompt)
        typecasted_list = ast.literal_eval(lst)
        print("List of Keywords for Transitions: ", typecasted_list)
        return typecasted_list
    except Exception as e:
        return f"Error Occurred: {e}"


# *************************


def prompt_logic(list, num, theme, ratio):
    prompt = f"""your task is to generate array of prompts from the list of intent words preserving the core context only.
    make concise and contextually relatable prompts to generate {theme} themed images that strictly must be in a sequence of given list and must be of aspect ratio :{ratio} (object in the image should be {ratio} aligned), which will then be given to other AI model to generate images.Do not make prompts that ends generating collage of images in a single image. 
    The number of image prompts must be exactly same as {num} as in the list and must be similar to words.
    output must be an array e.g ["","","",""]
    output should only contain list no other explanation or any other keyword
    number_of_image_prompts <<<{num}>>>
    script <<<{list}>>>
    """
    try:
        lst = get_response(prompt)
        typecasted_list = ast.literal_eval(lst)
        num = len(typecasted_list)
        return typecasted_list
    except Exception as e:
        return f"Error Occured : {e}"


def create_prompt(list, num, theme, ratio):
    list = prompt_logic(list, num, theme, ratio)
    if len(list) == num:
        print("number of prompts : ", num)
        print("List of prompts : ", list)
        return list
    else:
        while len(list) != num:
            list = prompt_logic(list, num, theme, ratio)
            print("number of prompts : ", num)
            print("List of prompts : ", list)
            return list
