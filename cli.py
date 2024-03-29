import os
import typer
from pathlib import Path

from ai.audio import get_wav_duration, generate_music, generate_speech
from ai.ideas import (
    generate_idea_on_local,
    generate_idea_via_openai,
    generate_idea_via_anthropic,
    generate_description_for_idea_via_anthropic,
)
from ai.images import generate_image
from ai.video import generate_telemarketing_video

from api.settings import settings

cli = typer.Typer()


@cli.command()
def gen_images(text: str, n: int = 1, output: str = "image.jpg"):
    """
    Generate n images from the given text and save them to the output file path.
    """
    file_path, file_extension = output.rsplit(".", 1)
    for i in range(n):
        fn = f"{file_path}_{i}.{file_extension}"
        generate_image(text, fn)


@cli.command()
def gen_speech(text: str, output: str = "speech.wav"):
    """
    Convert the given text to speech and save it to the output file path.
    """
    generate_speech(text, output)


@cli.command()
def gen_music(text: str, duration: int = 12, output: str = "music.wav"):
    """
    Generate music from the given prompt and save it to the output file path.
    """
    generate_music(text, duration, output)


@cli.command()
def gen_video(
    image_paths: list[str],
    music_path: str,
    voiceover_path: str,
    output: str = "telemarketing.mp4",
):
    """
    Generate a telemarketing-style video by combining the given image paths, music, and voiceover.
    """
    total_length = get_wav_duration(voiceover_path) + 1
    generate_telemarketing_video(
        image_paths, music_path, voiceover_path, total_length, output
    )


@cli.command()
def gen_video_in_dir(directory: str):
    """
    Generate a telemarketing-style video by combining the images, music, and voiceover found in the given directory.
    """

    supported_img_extensions = [".jpg", ".jpeg", ".png", ".webp"]
    image_paths = []
    for file in os.listdir(directory):
        if file.endswith(tuple(supported_img_extensions)):
            image_paths.append(os.path.join(directory, file))

    # Set the path to the music.wav file, if it exists in that folder:
    music_path = os.path.join(directory, "music.wav")
    if not os.path.exists(music_path):
        music_path = None

    # Look for speech.wav or voiceover.wav in the directory:
    voiceover_path = os.path.join(directory, "speech.wav")
    if not os.path.exists(voiceover_path):
        voiceover_path = os.path.join(directory, "voiceover.wav")
        if not os.path.exists(voiceover_path):
            voiceover_path = None

    # Use the name of the innermost folder in the path as the output file name for the MP4:
    output = Path(directory).parts[-1] + ".mp4"

    # Generate the video:
    total_length = get_wav_duration(voiceover_path) + 1
    generate_telemarketing_video(
        image_paths, music_path, voiceover_path, total_length, output
    )

    typer.echo(f"Video generated in: {output}")


@cli.command()
def gen_idea(hint: str = ""):
    """
    Generate an idea for a novel, modern consumer product. Optionally, provide a hint to guide the generation.
    """
    if settings.anthropic_api_key:
        idea = generate_idea_via_anthropic(hint)
    elif settings.openai_api_key:
        idea = generate_idea_via_openai(hint)
    else:
        idea = generate_idea_on_local(hint)
    typer.echo(idea)


@cli.command()
def gen(hint: str = ""):
    """
    Starting with an optional hint, generates a full telemarketing video for a novel, modern consumer product.
    """
    idea = generate_idea_via_anthropic(hint)
    typer.echo(idea)

    description = generate_description_for_idea_via_anthropic(idea)
    typer.echo(description)

    # Generate 3 images
    generate_image(idea, "product1.jpg")
    generate_image(idea, "product2.jpg")
    generate_image(idea, "product3.jpg")

    # Generate speech
    generate_speech(description, "speech.wav")

    # Generate music
    generate_music(
        "Telemarketing-style background music to advertise a novel, modern consumer electronics product",
        30,
        "music.wav",
    )

    total_length = get_wav_duration("speech.wav")

    # Generate video
    generate_telemarketing_video(
        ["product1.jpg", "product2.jpg", "product3.jpg"],
        "music.wav",
        "speech.wav",
        total_length + 1,
        "product.mp4",
    )

    typer.echo("Video generated in: product.mp4")


@cli.command()
def populate_db_from_samples(samples_dir: str = "samples"):
    from api.utils import get_db
    from datetime import datetime
    from pathlib import Path
    from api.models import Base, VideoClip, engine

    Base.metadata.create_all(bind=engine)

    db = next(get_db())

    # The 'samples' directory has sub-folders with one mp4 file each. For the title use the name of the subfolder.
    for folder in Path(samples_dir).iterdir():
        if folder.is_dir():
            for video_file in folder.iterdir():
                if video_file.suffix == ".mp4":
                    title = folder.name
                    typer.echo(f"Adding video for product: {title}")
                    description = f"This is a sample video for the `{title}` product"
                    db_video = VideoClip(
                        generation_uuid=title,
                        generation_phase="Completed",
                        title=title,
                        description=description,
                        duration_seconds=30,
                        path_to_video=str(video_file),
                        initiated_at=datetime.now(),
                    )
                    db.add(db_video)
                    db.commit()
                    db.refresh(db_video)

    db.close()


if __name__ == "__main__":
    cli()

    # generate_image("An innovative consumer product: the VR-Sync Smartglasses! Telemarketing image. ")
    # generate_speech("Introducing the all-new VR-Sync Smartglasses! Experience your digital world like never before, with immersive augmented reality, intuitive voice commands, and seamless integration into your everyday life! All packed into a sleek, stylish frame that fits any face. ")
    # generate_music("Telemarketing-style background music to advertise a novel, modern consumer electronics product")

    # music_wav = "samples/vr_set/vr_music.wav"
    # voiceover_wav = "samples/vr_set/vr_voiceover.wav"
    # total_length = get_wav_duration(voiceover_wav)
    # generate_telemarketing_video(
    #     ["samples/vr_set/vr_img1.jpg", "samples/vr_set/vr_img2.jpg", "samples/vr_set/vr_img3.jpg"],
    #     music_wav,
    #     voiceover_wav,
    #     total_length + 1,
    #     "samples/vr_set/vr_product.mp4",
    # )
