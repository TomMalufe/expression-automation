# Sprite Generator with Stable Diffusion

This project generates custom sprite images using the Stable Diffusion WebUI API. It is optimized for local setups of Stable Diffusion.

---

## Features

- Generate sprites with customizable prompts, expressions, and image settings.
- Batch processing for multiple expressions defined in a JSON file.

## Recommended
- Install and run SD Next locally for easy, free image generation
- For Anime like characters, use [magnum-v4-22b-gguf](https://huggingface.co/anthracite-org/magnum-v4-22b-gguf) as the default model.
- If you would like to remove image backgrounds, consider using [Rembg](https://github.com/danielgatis/rembg).

---

## Prerequisites

Before you can use this project, ensure that the following requirements are met:

1. **Python 3.11 or later:** The project relies on Python scripts. Install necessary Python dependencies using `pip`.


---

## Installation

Follow these steps to set up and use the project:

1. Clone the repository:
   ```bash
   git clone https://github.com/TomMalufe/expression-automation.git
   cd expression-automation
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Edit up your `.env` environment variables:
    - Open the `.env` file in the root directory.
    - Update the following variables as needed:
      ```ini
      SD_API_URL=http://127.0.0.1:7860/sdapi/v1/txt2img
      OUTPUT_FOLDER=generated_sprites
      ```

4. Define your prompts in a JSON file (default: `prompts.json`) to control sprite generation. Example structure:
   ```json
   {
     "base_prompt": "A highly detailed sprite of",
     "negative_prompt": "blurred, low quality, distorted",
     "character_details": "fantasy character, medieval attire",
     "expressions": {
       "happy": "smiling, cheerful",
       "angry": "furious, intense gaze"
     }
   }
   ```

---

## Usage

Run the `expressions.py` script with the desired arguments:

```bash
python expressions.py [OPTIONS]
```

### Command-Line Options

Below are the main options available:

- **`--prompt_file`**: Path to the JSON file with prompts (default: `prompts.json`).
- **`--width`**: Width of the generated image (default: 1024).
- **`--height`**: Height of the generated image (default: 1024).
- **`--steps`**: Number of steps to generate the image (default: 30).
- **`--cfg_scale`**: Config scale for model guidance (default: 7.5).
- **`--sampler`**: Sampling method (default: `SA Solver`).
- **`--seed`**: Seed for consistent image generation (default: 2472820057).
- **`--expressions`**: Comma-separated list of expressions to generate / re-generate (e.g., `happy,angry`). Generates everything if left out.

Example to generate sprites for `happy` and `angry` expressions:

```bash
python expressions.py --expressions happy,angry
```

---

## Post-Processing (Optional)

If you prefer your sprites without backgrounds, you can process the generated images using `rembg`:

1. Install the Rembg model:
   ```bash
   pip install rembg
   ```

2. Use the following command to process your sprite images:
   ```bash
   rembg p -m birefnet-portrait generated_sprites/ output/
   ```

This will process all images in the `generated_sprites/` folder and save the results in the `output/` folder.

---

## Example Workflow

1. Start the SD WebUI with the **Magnum-v4-22b-gguf** model.
2. Run the script to generate sprites:
   ```bash
   python expressions.py
   ```
3. Run the script again to re-generate sprites that don't look right:
    ```bash
    python expressions.py --expressions happy,angry
    ```
4. (Optional) Remove sprite backgrounds:
   ```bash
   rembg p -m birefnet-portrait generated_sprites/ output/
   ```

---

## Troubleshooting and Tips

- **Stable Diffusion Errors:**
    - Ensure the SD WebUI is running and accessible at the URL specified in `SD_API_URL`.
    - Verify that the correct model is loaded.

- **File Not Found Errors:**
    - Check that the `prompts.json` file exists and is properly formatted.

- **Post-Processing Issues:**
    - Refer to the [Rembg documentation](https://github.com/danielgatis/rembg) for guidance if you encounter problems.

- **Customizing Prompts:**
    - Update the `prompts.json` file to personalize the character base, expressions, or additional details.

---

## License

This project is open-source and available under the MIT License.

---

## Acknowledgments

- [Stable Diffusion Next](https://github.com/AUTOMATIC1111/stable-diffusion-webui) and the [Magnum-v4-22b-gguf](https://huggingface.co/anthracite-org/magnum-v4-22b-gguf) model for enabling image generation.
- [Rembg](https://github.com/danielgatis/rembg) for the background removal utility.
