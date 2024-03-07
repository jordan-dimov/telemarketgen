import scipy
from transformers import pipeline, AutoProcessor, AutoModel

from loguru import logger


def save_audio_to_wav(audio, output_wav: str, sampling_rate=1000):
    logger.info("Converting to array...")
    audio_np = audio.cpu().numpy().squeeze()

    logger.info(f"Writing WAV @{sampling_rate} Hz")
    scipy.io.wavfile.write(output_wav, rate=sampling_rate, data=audio_np)


def get_wav_duration(file_path):
    sample_rate, data = scipy.io.wavfile.read(file_path)
    duration = len(data) / float(sample_rate)
    logger.info(f"Duration of {file_path} is: {duration}s.")
    return duration


def generate_music(
    description: str, length_s: int = 30, output_wav: str = "chirp_out.wav"
):
    synthesizer = pipeline("text-to-audio", model="facebook/musicgen-small")

    logger.info("Generating music...")
    music = synthesizer(
        description, forward_params={"do_sample": True, "max_length": length_s * 40}
    )

    logger.info("Writing WAV...")
    scipy.io.wavfile.write(output_wav, rate=music["sampling_rate"], data=music["audio"])


def generate_speech(description: str, output_wav: str = "bark_out.wav"):
    processor = AutoProcessor.from_pretrained("suno/bark")
    model = AutoModel.from_pretrained("suno/bark")

    inputs = processor(
        text=[description],
        return_tensors="pt",
    )

    attention_mask = inputs["attention_mask"]
    pad_token_id = processor.tokenizer.pad_token_id

    logger.info("Generating speech...")
    speech = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=attention_mask,
        pad_token_id=pad_token_id,
        do_sample=True,
    )

    save_audio_to_wav(speech, output_wav=output_wav, sampling_rate=22050)
