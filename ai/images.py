from diffusers import StableDiffusionPipeline

from loguru import logger


def generate_image(description: str, output_img: str = "product.jpg"):
    model_id = "stabilityai/stable-diffusion-2"
    logger.info("Generating image...")
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    image = pipe(description).images[0]
    logger.info(f"Saving image to: {output_img}")
    image.save(output_img)
