import random
from loguru import logger
from openai import OpenAI
from anthropic import Anthropic
from transformers import pipeline

categories = [
    "home security",
    "household cleaning",
    "health and wellness",
    "consumer electronics",
    "automotive",
    "kitchenware",
    "personal grooming",
    "pet care",
    "children's toys",
    "fitness and exercise",
    "outdoor recreation",
    "home improvement",
    "home appliances",
    "office supplies",
    "personal accessories",
    "fashion and clothing",
    "jewelry and watches",
]


def generate_idea_on_local(hint: str = "in any random category") -> str:
    # Generate an idea for an innovative consumer product, based on the hint

    gen = pipeline("text-generation", model="openchat/openchat-3.5-0106")
    prompt = f"Generate a unique and interesting idea for an innovative consumer product. Return only one concise sentence with the description. Hint: {hint}"

    logger.info("Generating idea...")
    idea = gen([prompt], max_length=70, num_return_sequences=1, truncation=True)

    return idea[0][0]["generated_text"].split()[1]


def generate_idea_via_openai(hint: str = "in any random category") -> str:
    # Use OpanAI chat completion to generate an idea for an innovative consumer product, based on the hint

    client = OpenAI()
    prompt = f"Generate a unique and interesting idea for an innovative consumer product that can be telemarketed. Return only one concise sentence with the description. Hint: {hint}"

    logger.info("Generating idea...")
    idea = client.completions.create(
        model="gpt-4-0125-preview",
        prompt=prompt,
    )

    return idea.choices[0].message["content"]


def generate_idea_via_anthropic(hint: str | None = None) -> str:
    # Use Anthropic chat completion to generate an idea for an innovative consumer product, based on the hint

    hint = hint or random.choice(categories)
    client = Anthropic()
    prompt = f"Generate a unique and interesting idea for an innovative consumer product that can be telemarketed. Return ONLY one concise sentence with the description - no other output. Hint: {hint}"

    logger.info("Generating idea...")
    idea = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=30,
        messages=[{"role": "user", "content": prompt}],
    )

    return idea.content[0].text


def generate_description_for_idea_via_anthropic(idea: str) -> str:
    # Use Anthropic chat completion to generate a description for an innovative consumer product, based on the idea

    client = Anthropic()
    prompt = f"Write a brief 80-style telemarketing script for this innovative consumer product: {idea}"

    logger.info("Generating description...")
    description = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}],
    )

    return description.content[0].text
