from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.concatenate import concatenate_videoclips

from loguru import logger


def generate_telemarketing_video(
    image_paths: list[str],
    music_path: str,
    voiceover_path: str,
    total_length: int,
    output: str = "telemarketing.mp4",
):
    img_length = total_length / len(image_paths)
    logger.info(
        f"Creating {len(image_paths)} ImageClips of duration {img_length}s each..."
    )
    image_clips = []
    for path in image_paths:
        clip = ImageClip(path).set_duration(img_length).resize(lambda t: (768, 768))
        image_clips.append(clip)

    logger.info("Concatenating video...")
    video = concatenate_videoclips(image_clips, method="compose")

    logger.info("Loading audio...")
    soundtrack = AudioFileClip(music_path)
    if total_length < soundtrack.duration:
        soundtrack = soundtrack.subclip(0, total_length)

    logger.info("Loading voiceover...")
    voiceover = AudioFileClip(voiceover_path)
    if total_length < voiceover.duration:
        voiceover = voiceover.subclip(0, total_length)

    logger.info("Mixing audio...")
    final_audio = CompositeAudioClip([soundtrack, voiceover])

    logger.info("Adding audio to video...")
    video = video.set_audio(final_audio)

    logger.info(f"Saving final video to: {output}")
    video.write_videofile(output, codec="libx264", audio_codec="aac", fps=16)
