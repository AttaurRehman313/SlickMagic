from mainapp.video_editting.generate_animations import create_animation
from mainapp.video_editting.font_and_effect import *
from mainapp.model.scripts_generation import create_intent_words,generate_keywords_for_transitions,create_prompt
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, send_from_directory
from gtts import gTTS
from dotenv import load_dotenv
from time import time,sleep
import moviepy.editor as mp
import requests, os, re


load_dotenv()

# Get the API key
url = os.getenv("URL")
api_key = os.getenv("api_key")

time = time()


def sort_images_by_number(urls):
    """
    This function sorts a list of image URLs based on the numerical value
    extracted from the filenames before the '.png' extension. If no number
    is found, the filename is treated as having a default value of 0.
    """

    try:

        def sort_key(url):
            # Extract the number from the image filename using regular expression
            match = re.search(r"(\d+)\.png", url)
            if match:
                return int(match.group(1))
            else:
                return 0

        # Sort the URLs based on the extracted number
        url_imgs_sorted = sorted(urls, key=sort_key)
        return url_imgs_sorted
    except Exception as e:
        return {"Error": "sort_images_by_number ERROR"}, 404


def merge_aud_vid(aud, vid, count):
    """
    Merges an audio file with a video file, saves the resulting video with synchronized audio,
    and generates a unique output filename using the given count.
    """
    try:
        audio = mp.AudioFileClip(aud)
        video1 = mp.VideoFileClip(vid)
        final = video1.set_audio(audio)
        output_path = "video_with_audio" + str(count) + ".mp4"
        final.write_videofile(
            output_path,
            codec="libx264",
            bitrate="5000k",
            fps=video1.fps,
            audio_codec="aac",
        )
        return output_path
    except Exception as e:
        return {"Error": "GENERATE SUBTITLES ERROR"}, 404


# ***************************
def generate_subtitles(
    video_url,
    fill_color,
    transcript_effect,
    font_family,
    max_length,
    stroke_color,
    font_weight,
    font_size,
):
    """
    This function generates a video with subtitles using the Creatomate API.
    The video is customized based on the input parameters, including text appearance,
    font properties, colors, and transcript effects.
    """

    url = "https://api.creatomate.com/v1/renders"
    function_name = "generate_subtitles"

    # Print parameters to debug

    try:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        json_data = {
            "output_format": "mp4",
            "output_resolution": "720p",
            "output_bitrate": "4000k",
            "source": {
                "elements": [
                    {
                        "type": "video",
                        "id": "17ca2169-786f-477f-aaea-4a2598bf24eb",
                        "source": video_url,
                    },
                    {
                        "type": "text",
                        "text": "word",
                        "transcript_source": "17ca2169-786f-477f-aaea-4a2598bf24eb",
                        "transcript_effect": transcript_effect,
                        "transcript_split": "word",
                        "transcript_color": "white",
                        "transcript_maximum_length": max_length,
                        "y": "55%",
                        "width": "81%",
                        "height": "35%",
                        "x_alignment": "50%",
                        "y_alignment": "50%",
                        "fill_color": fill_color,
                        "stroke_color": stroke_color,
                        "stroke_width": "1.6 vmin",
                        "font_family": font_family,
                        "font_weight": font_weight,
                        "font_size": font_size,
                        "background_color": "rgba(216,216,216,0)",
                        "background_x_padding": "31%",
                        "background_y_padding": "17%",
                        "background_border_radius": "31%",
                    },
                ]
            },
        }

        # time.sleep(15)
        response = requests.post(url, headers=headers, json=json_data)

        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response content: {response.content}")
            response_json = response.json()
            video_info = response_json[0]
            print(
                f"from funtions.py API Response************************\nVideo info: {video_info}"
            )
            return video_info["url"]
        else:
            response_json = response.json()
            print(f"API Response: {response_json}")

            if isinstance(response_json, list) and len(response_json) > 0:
                video_info = response_json[0]
                # time.sleep(5)
                print(
                    f"from funtions.py API Response************************\nVideo info: {video_info}"
                )
                return video_info["url"]
            else:
                print("Error: Unexpected API response format")
                return None

    except requests.exceptions.HTTPError as http_err:
        error_message = f"{function_name} - HTTP error occurred: {http_err}"
        print(error_message)
        return {"Error": error_message}, 400

    except requests.exceptions.ConnectionError as conn_err:
        error_message = f"{function_name} - Connection error occurred: {conn_err}"
        print(error_message)
        return {"Error": error_message}, 503

    except requests.exceptions.Timeout as timeout_err:
        error_message = f"{function_name} - Timeout error occurred: {timeout_err}"
        print(error_message)
        return {"Error": error_message}, 504

    except requests.exceptions.RequestException as req_err:
        error_message = f"{function_name} - Request error occurred: {req_err}"
        print(error_message)
        return {"Error": error_message}, 500

    except ValueError as json_err:
        error_message = f"{function_name} - JSON decoding error: {json_err}"
        print(error_message)
        return {"Error": error_message}, 500

    except KeyError as key_err:
        error_message = f"{function_name} - Key error: {key_err}"
        print(error_message)
        return {"Error": error_message}, 500

    except Exception as e:
        error_message = f"{function_name} - General error occurred: {e}"
        print(error_message)
        return {"Error": error_message}, 500


# **************************DOWNLOAD
def download_video(url,count, max_retries=10):
    """
    This function attempts to download a video from the provided URL and save it
    to the specified output path. It retries the download process a specified
    number of times (default is 10) in case of errors, with a 20-second wait
    between attempts. If the video is successfully downloaded, the function
    returns the output file path. If all retries fail, it returns None.
    """
    attempt = 0
    while attempt < max_retries:
        try:
            # Send a GET request to the URL
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an exception for bad responses

            # Open a local file with write-binary mode
            output_path = "final_video" + str(count) + ".mp4"
            with open(output_path, "wb") as f:
                # Iterate through the response content in chunks
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Video downloaded successfully to {output_path}")
            return output_path
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

        attempt += 1
        if attempt < max_retries:
            print(f"Retrying in 20 seconds... (Attempt {attempt} of {max_retries})")
            sleep(20)

    print("Failed to download the video after multiple attempts.")
    return None


def Generate_slideshow(time_stamp, images_urls, height, width):
    """
    This function generates a slideshow video by sending a request to the Creatomate API.
    It processes a list of image URLs and corresponding timestamps, creating a sequence of images
    with specified durations and animations. The function also handles the API response and
    downloads the generated video in MP4 format. If any errors occur during the process,
    appropriate error messages are returned.
    """

    function_name = "Generate_slideshow"
    try:
        print(
            "Time stamps length:",
            len(time_stamp),
            "\nImage URLs length:",
            len(images_urls),
        )

        elements = []

        # First, handle the initial image display
        initial_time = time_stamp[
            0
        ]  # How long the first image should stay on the screen
        t_time_initial = initial_time * 0.05

        # Create the first element (first image with the initial time)
        initial_element = {
            "type": "image",
            "source": images_urls[0],  # First image
            "track": 1,
            "duration": initial_time + t_time_initial,
            "clip": True,
            "animations": [],  # No transition or animation for the first image
        }
        elements.append(initial_element)

        # Now handle the rest of the images and transitions
        for count in range(1, len(images_urls)):
            time = time_stamp[count]
            t_time = time * 0.05
            animation, transition = create_animation(time=time)

            element = {
                "type": "image",
                "source": images_urls[count],
                "track": 1,
                "duration": time + t_time,
                "clip": True,
                "animations": [animation, transition],
            }
            elements.append(element)

        json_data = {
            "source": {
                "output_format": "mp4",
                "width": width,
                "height": height,
                "elements": elements,
            }
        }

        # Sending the POST request to Creatomate API
        response = requests.post(
            "https://api.creatomate.com/v1/renders",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=json_data,
        )

        # Handle the API response
        if response.status_code == 200 or response.status_code == 202:
            print("Render started successfully!")
            link = response.json()[0].get("url")
            print("Video link:", link)
            output_file = "downloaded_video.mp4"
            download_video(link, output_file)
            return output_file
        else:
            print("Failed to start render")
            print("Status Code:", response.status_code)
            print("Response:", response.text)
            return None

    except Exception as e:
        print(f"{function_name} - Error occurred: {e}")
        return None

    except requests.exceptions.ConnectionError as conn_err:
        error_message = f"{function_name} - Connection error occurred: {conn_err}"
        print(error_message)
        return {"Error": error_message}, 503

    except requests.exceptions.Timeout as timeout_err:
        error_message = f"{function_name} - Timeout error occurred: {timeout_err}"
        print(error_message)
        return {"Error": error_message}, 504

    except requests.exceptions.RequestException as req_err:
        error_message = f"{function_name} - Request error occurred: {req_err}"
        print(error_message)
        return {"Error": error_message}, 500

    except KeyError as key_err:
        error_message = f"{function_name} - Key error occurred: {key_err}"
        print(error_message)
        return {"Error": error_message}, 500

    except Exception as e:
        error_message = f"{function_name} - General error occurred: {e}"
        print(error_message)
        return {"Error": error_message}, 500


def words(srt_file):
    with open(srt_file, "r") as f:
        lines = f.readlines()

    words = [lines[i + 1] for i in range(1, len(lines), 3)]
    words = [i.lower() for i in words]

    new_script = "".join(words).replace("\n", " ").strip()
    return new_script


def video_aspect_ratio(value):
    if value == "portrait":
        height = 1280
        width = 720
    elif value == "landscape":
        height = 720
        width = 1280
    else:
        height = 1280
        width = 720
    return height, width


def select_aspect_ratio(value):
    if not value:
        return "1024x1792"
    elif value.lower() == "landscape":
        return "1792x1024"
    elif value.lower() == "portrait":
        return "1024x1792"
    else:
        return value


def Generate_Audio(script,count):
    language = "en"
    speech = gTTS(text=script, lang=language, slow=False)
    speech_file = f"audio" + str(count) + ".mp3"
    speech.save(speech_file)
    return speech_file


def combined_thread_audio_srt_generation(script, theme, ratio):
    try:
        with ThreadPoolExecutor() as executor:
            # Run the Generate_Audio and create_intent_words functions concurrently
            audio_future = executor.submit(Generate_Audio, script)
            intent_words_future = executor.submit(create_intent_words, script)

            # Get results of the first two functions
            audio_result = audio_future.result()
            intent_words_result = intent_words_future.result()
            num = len(intent_words_result)

            # Now run the creation of prompts_list and new_keywords concurrently
            prompts_list_future = executor.submit(
                create_prompt, intent_words_result, num, theme, ratio
            )
            new_keywords_future = executor.submit(
                generate_keywords_for_transitions, script, intent_words_result, num
            )

            # Get results of the second set of functions
            prompts_list_result = prompts_list_future.result()
            new_keywords_result = new_keywords_future.result()
            print(
                "#@# : ",
                audio_result,
                intent_words_result,
                prompts_list_result,
                new_keywords_result,
            )

        # Return the four results as separate variables
        return (
            audio_result,
            intent_words_result,
            prompts_list_result,
            new_keywords_result,
        )
    except Exception as e:
        return {"error": f"Error occurred in combined_thread_audio_srt_generation: {e}"}
