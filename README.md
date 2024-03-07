# telemarketgen
API for telemarketing video generation using generative AI

## The big idea

This app generates complete telemarketing videos from scratch, using generative AI. You can proide a hint of the kind of product you want to advertise, or just let the AI come up with its own unique ideas! 

The process involves the following steps:

1. Generate an idea (takinga possible hint as input) for a new consumer product. This can be done either locally, using the `openchat` transformers model from Hugging Face, or remotely, using the OpenAI GPT-4 API or Anthropic's Claude model API.
2. Generate a script for a telemarketing video advertising the product. 
3. Generate 3 different images of the product (locally, using Stable Diffusion 2 from Hugging Face)
4. Convert the telemarketing script to voice using a text-to-speech model (locally, using the Suno Bark model via Hugging Face)
5. Generate background music for the video (locally, using the Facebook Musicgen model from OpenAI)
6. Finally, put it all together into a complete video using MoviePy.

## Installation

Make sure you have Python 3.10 or newer and Poetry installed. Then just run `poetry install` in the root of the repository.

## Usage

There are two modes of operation: CLI and API. All tasks can be performed using either the CLI or the API. 

### CLI

To see the available CLI commands, run `poetry run cli.py --help`

To do a complete video generation from scratch, just run `poetry run cli.py gen`. The AI will come up with its own idea and will generate a complete video advertising it.

### API

The API is implemented using FastAPI. You can start the server with `make run` and open it in any browser at 'http://0.0.0.0:8000/'

On the main (index) page, you will see a form where you can input a hint for the product you want to advertise. If you leave it empty, the AI will come up with its own idea. Just press the "Generate" button and wait for the video to be generated.

As soon as the idea and the telemarketing script are complete, you will see it show on the index page - even while the video is still being generated. Clicking on the "Details" button will take you to a page where you can see the progress of the video generation (look for 'Generation phase: ') and play the final video once it's ready.

Generation happens in a FastAPI Background Task, so you can close the browser and come back later to check on the progress (as long as the server is still running).


### Samples

Look at the MP4 video files in the `samples/` folder. Or create your own using the CLI or the API!
