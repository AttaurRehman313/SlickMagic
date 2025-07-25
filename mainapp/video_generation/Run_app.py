from mainapp.model.scripts_generation import refine_scripts
from mainapp.model.image_generation import loop_image_generation
from mainapp.video_editting.creatomate import combined_thread_audio_srt_generation,Generate_slideshow,merge_aud_vid,generate_subtitles
from time import time, sleep
from tinytag import TinyTag

def run(
    script,
    font_family,
    aspect_ratio,
    font_size,
    transcript_effect,
    stroke_color,
    font_weight,
    fill_color,
    max_length,
    height,
    width,
    theme,
    count,):
    """
    run8 is use for for normal request for video and subtitle
    """

    print("Script ### : ", script)
    scripts_start_time = time()
    # Extract intent Words From the Script
    script = refine_scripts(script)
    end_scripts_time = time()
    total_scripts_time = (end_scripts_time - scripts_start_time)/60
    print(f"************************Total Time for Refining Script : {total_scripts_time} minutes************************") # print(total_scripts_time)
    print("Refined Script : ", script)

    audio, intent_words_list, prompts_list, new_keywords = (
        combined_thread_audio_srt_generation(
            script=script, theme=theme, ratio=aspect_ratio
        )
    )
    tag = TinyTag.get(audio).duration
    time_stamp = list(tag / len(intent_words_list) for i in intent_words_list)
    print("timestamp ", time_stamp)

    # Calculate number of intent words
    num = len(intent_words_list)
    print("intent word length :", num)

    # Generating images
    image_generation_start_time = time()
    print("generating images .......")
    img_urls = loop_image_generation(prompts=prompts_list, aspect_ratio=aspect_ratio)
    image_generation_end_time = time()
    total_image_generation_time = (image_generation_end_time - image_generation_start_time)/60
    print(f"************************Total Time for Image Generation : {total_image_generation_time} minutes************************")
    print("image urls :", img_urls)

    # Generate Video and download it with name "downloaded_video.mp4"
    print("Generating simple video ....")
    video1_start_time = time()
    video1 = Generate_slideshow(
        time_stamp=time_stamp, images_urls=img_urls, height=height, width=width
    )
    video1_end_time = time()
    total_video_generation_time = (video1_end_time - video1_start_time)/60
    print(f"************************Total Time for Video Generation : {total_video_generation_time} minutes************************")

    # Merge Audio and Video Together and save it as (video_with_audio.mp4)
    print("Merging Audio and Video...........")
    video2_start_time = time()
    video2 = merge_aud_vid(aud=audio, vid=video1, count=count)
    print("Audio Video Merged :) ")
    video2_end_time = time()
    total_video_with_audio_time = (video2_end_time - video2_start_time)/60
    print(f"************************Total Time for Audio Video Merging : {total_video_with_audio_time} minutes************************")
    # Upload the Video2/ Video with audio to Github/server and take its link
    print("Uploading Video on server...........")

    video_with_audio_url = f"http://127.0.0.1:5000/video/{video2}"
    print("Uploaded to server :) ", video_with_audio_url)
    sleep(10)

    # Post link of video with audio to creatomate to generate subtitles
    print("Generating Subtitles...........")
    video3_start_time = time()
    video3_url = generate_subtitles(
        video_url=video2,
        fill_color=fill_color,
        transcript_effect=transcript_effect,
        font_family=font_family,
        max_length=max_length,
        stroke_color=stroke_color,
        font_weight=font_weight,
        font_size=font_size,
    )
    print("\nfinal_video_link :", video3_url)
    video3_end_time = time()
    total_video_with_subtitles_time = (video3_end_time - video3_start_time)/60
    print(f"************************Total Time for Audio Video Merging : {total_video_with_subtitles_time} minutes************************")
    sleep(25)


    # Download Video3/Final Video in your local folder
    # output_path = download_video(url = video3_url)
    return video3_url