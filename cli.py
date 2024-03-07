from typer import Typer

from ai.audio import get_wav_duration, generate_music, generate_speech
from ai.images import generate_image
from ai.video import generate_telemarketing_video

cli = Typer()


@cli.command()
def gen_images(text: str, n: int = 1, output: str = "image.jpg"):
    # Split the file path from the extension:
    file_path, file_extension = output.rsplit(".", 1)
    for i in range(n):
        fn = f"{file_path}_{i}.{file_extension}"
        generate_image(text, fn)


@cli.command()
def gen_speech(text: str, output: str = "speech.wav"):
    generate_speech(text, output)


@cli.command()
def gen_music(text: str, duration: int = 12, output: str = "music.wav"):
    generate_music(text, duration, output)


@cli.command()
def gen_video(
    image_paths: list[str],
    music_path: str,
    voiceover_path: str,
    output: str = "telemarketing.mp4",
):
    total_length = get_wav_duration(voiceover_path) + 1
    generate_telemarketing_video(
        image_paths, music_path, voiceover_path, total_length, output
    )


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