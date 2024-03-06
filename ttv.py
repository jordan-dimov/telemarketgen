import scipy
from transformers import AutoProcessor, AutoModel, pipeline
from diffusers import StableDiffusionPipeline
from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips

def generate_telemarketing_video(image_paths: list[str], music_path: str, voiceover_path: str, total_length: int, output: str = "telemarketing.mp4"):
    img_length = total_length / len(image_paths)
    print(f"Creating {len(image_paths)} ImageClips of duration {img_length}s each...")
    image_clips = []
    for path in image_paths:
        clip = ImageClip(path).set_duration(img_length).resize(lambda t: (768, 768))
        image_clips.append(clip)

    print("Concatenating video...")
    video = concatenate_videoclips(image_clips, method="compose")

    print("Loading audio...")
    soundtrack = AudioFileClip(music_path)
    if total_length < soundtrack.duration:
        soundtrack = soundtrack.subclip(0, total_length)

    print("Loading voiceover...")
    voiceover = AudioFileClip(voiceover_path)
    if total_length < voiceover.duration:
        voiceover = voiceover.subclip(0, total_length)

    print("Mixing audio...")
    final_audio = CompositeAudioClip([soundtrack, voiceover])

    print("Adding audio to video...")
    video = video.set_audio(final_audio)

    print(f"Saving final video to: {output}")
    video.write_videofile(output, codec="libx264", audio_codec="aac", fps=16)


def generate_image(description: str, output_img: str = "product.jpg"):
    model_id = "stabilityai/stable-diffusion-2"
    print("Generating image...")
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    image = pipe(description).images[0]
    print(f"Saving image to: {output_img}")
    image.save(output_img)


def save_audio_to_wav(audio, output_wav: str, sampling_rate = 1000):
    print("Converting to array...")
    audio_np = speech.cpu().numpy().squeeze()
    sampling_rate = 22050

    print(f"Writing WAV @{sampling_rate} Hz")
    scipy.io.wavfile.write(output_wav, rate=sampling_rate, data=audio_np)


def generate_music(description: str, length_s: int = 30, output_wav: str = "chirp_out.wav"):
    synthesizer = pipeline('text-to-audio', model='facebook/musicgen-small')

    print("Generating music...")
    music = synthesizer(description, forward_params={'do_sample': True})
    
    print(f"Writing WAV...")
    scipy.io.wavfile.write(output_wav, rate=music['sampling_rate'], data=music['audio'])


def generate_audio(description: str, output_wav: str = "bark_out.wav"):
    processor = AutoProcessor.from_pretrained('suno/bark')
    model = AutoModel.from_pretrained('suno/bark')

    inputs = processor(
        text=[description],
        return_tensors="pt",
    )

    attention_mask = inputs["attention_mask"]
    pad_token_id = processor.tokenizer.pad_token_id

    print("Generating speech...")
    speech = model.generate(input_ids=inputs["input_ids"], attention_mask=attention_mask, pad_token_id=pad_token_id, do_sample=True)

    save_audio_to_wav(speech, output_wav=output_wav, sampling_rate=22050)

def get_wav_duration(file_path):
    sample_rate, data = scipy.io.wavfile.read(file_path)
    duration = len(data) / float(sample_rate)
    print(f"Duration of {file_path} is: {duration}s.")
    return duration


if __name__=="__main__":
    # generate_image("An innovative consumer product: the VR-Sync Smartglasses! Telemarketing image. ")
    # generate_audio("Introducing the all-new VR-Sync Smartglasses! Experience your digital world like never before, with immersive augmented reality, intuitive voice commands, and seamless integration into your everyday life! All packed into a sleek, stylish frame that fits any face. ")
    # generate_music("Telemarketing-style background music to advertise a novel, modern consumer electronics product")

    music_wav = "samples/vr_set/vr_music.wav"
    voiceover_wav = "samples/vr_set/vr_voiceover.wav"
    total_length = get_wav_duration(voiceover_wav)
    generate_telemarketing_video(
        ["samples/vr_set/vr_img1.jpg", "samples/vr_set/vr_img2.jpg", "samples/vr_set/vr_img3.jpg"],
        music_wav,
        voiceover_wav,
        total_length + 1,
        "samples/vr_set/vr_product.mp4",
    )
