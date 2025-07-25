from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from openai import OpenAI
import ast, time
import os



load_dotenv()
# Get the API key
api_key = os.getenv("api_key")
openai_api_key = os.getenv("openai_api_key")
assembly_api_key = os.getenv("assembly_api_key")

def text_to_image(prompt, aspect_ratio):
    try:
        client = OpenAI(api_key=openai_api_key)
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=aspect_ratio,
            quality="standard",
            n=1,
        )
        # Check if response data is valid
        if not response.data:
            raise ValueError("No images returned in the response.")
        image_url = response.data[0].url
        return image_url

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}


def loop_image_generation(prompts, aspect_ratio, batch_size=15):
    all_images = []
    try:
        # Split prompts into batches of size batch_size
        for i in range(0, len(prompts), batch_size):
            batch = prompts[i : i + batch_size]
            print(
                f"Processing batch {i // batch_size + 1}/{(len(prompts) + batch_size - 1) // batch_size}"
            )
            start_time = time.time()
            with ThreadPoolExecutor() as executor:
                # Process the batch of prompts
                images = list(
                    executor.map(
                        lambda prompt: text_to_image(prompt, aspect_ratio), batch
                    )
                )
                all_images.extend(images)
            end_time = time.time()
            batch_duration = end_time - start_time
            print(
                f"************************Batch Duration : {batch_duration} seconds************************"
            )
            target_delay = 60  # Adjust this to your API rate limit
            remaining_time = max(0, target_delay - batch_duration)
            # Wait for the specified delay before processing the next batch
            if i + batch_size < len(prompts):  # Avoid sleeping after the last batch
                print(
                    f"Waiting for {remaining_time} seconds to comply with rate limits..."
                )
                time.sleep(remaining_time)

        return all_images
    except Exception as e:
        return {"error": "loop_image_generation", "details": str(e)}, 400
