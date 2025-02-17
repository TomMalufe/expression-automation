# Sprite Generator with Stable Diffusion

A flexible tool to create unique sprite/images using the Stable Diffusion WebUI API. This application is tailored for users who run Stable Diffusion locally and want to automate sprite generation with detailed control over settings.

---

## Key Features

- **Customizable Sprite Generation**: Define prompts, expressions, image size, and quality to suit your needs. Ideal for creating character sprites and assets.
- **Batch Processing**: Generate multiple expressions (e.g., happy, sad, angry) in a single run using a JSON configuration.
- **Versioned Output Handling**: Automatically save images with versioned filenames to prevent overwriting.
- **Optional Background Removal**: Use `rembg` for post-processing to make images transparent-friendly.

---

## Why Use This Tool?

- **Designed for Local Setups**: Works seamlessly with local installations of Stable Diffusion.
- **Anime Support**: Recommended settings and models like [Lykon/AAM_XL_AnimeMix](https://huggingface.co/Lykon/AAM_XL_AnimeMix) for anime-styled art.
- **Flexible Input**: Input prompts via JSON files to easily customize image parameters and manage multiple expressions.

---

## Requirements

To get started, ensure the following are set up:

1. **Python 3.11 or newer**: The project uses Python scripts for API communication and file handling.
2. **Stable Diffusion WebUI** (Next or AUTOMATIC1111): Run locally at `http://127.0.0.1:7860/`.
3. **Python Libraries**: Install all dependencies using a `requirements.txt` file.
4. **Optional Tools (for Background Removal)**: Install [Rembg](https://github.com/danielgatis/rembg) for post-processing.

---

## Installation and Setup

1. **Clone Repository**:
   ```bash
   git clone https://github.com/TomMalufe/expression-automation.git
   cd expression-automation
   ```

2. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
    - Create and set the `.env` file in the project root with details such as:
      ```ini
      SD_API_URL=http://127.0.0.1:7860/sdapi/v1/txt2img
      OUTPUT_FOLDER=generated_sprites
      ```

4. **Prepare Prompt File**:
    - Customize a `prompts.json` file (or use an existing one). For example:
      ```json
      {
        "default_seed": 123456789,
        "prompt_prefix": "A beautiful, detailed sprite of",
        "prompt_suffix": "in a fantasy setting",
        "negative_prompt": "blurry, distorted, low quality",
        "character_prompt": "medieval warrior in armor",
        "expressions": {
          "happy": "smiling, cheerful expression",
          "angry": "furious look, intense gaze"
        }
      }
      ```

---

## Usage

Use the `expressions.py` script to generate sprites programmatically. Below are the available options:

### Command-Line Options:

| Parameter            | Description                                                                                      | Default             |
|----------------------|--------------------------------------------------------------------------------------------------|---------------------|
| `-p` `--prompt_file` | Path to the JSON file containing prompts.                                                       | `prompts.json`      |
| `-w` `--width`       | Width of the generated image (pixels).                                                          | `1024`              |
| `-h` `--height`      | Height of the generated image (pixels).                                                         | `1024`              |
| `-s` `--steps`       | Number of steps used by the algorithm.                                                          | `30`                |
| `-c` `--cfg_scale`   | Config scale value for model guidance.                                                          | `7.5`               |
| `-S` `--sampler`     | Sampling method.                                                                                | `SA Solver`         |
| `-e` `--seed`        | Seed for reproducible outputs. Overrides default seed in JSON prompt.                           | `2472820057`        |
| `-x` `--expressions` | Comma-separated list of expressions from the JSON file (`happy,angry`). Defaults to all.         | `All expressions`   |

### Example Commands:

1. Generate all sprites from the default `prompts.json` file:
   ```bash
   python expressions.py
   ```

2. Generate specific expressions (e.g., happy and sad):
   ```bash
   python expressions.py -x happy,sad
   ```

3. Override image dimensions and steps:
   ```bash
   python expressions.py -w 512 -h 512 -s 50
   ```

---

## Post-Processing with `rembg` (Optional)

To remove sprite backgrounds and create transparent images:

1. **Install `rembg`:**
   ```bash
   pip install rembg
   ```

2. **Process Images in the Output Folder**:
   ```bash
   rembg p -m birefnet-portrait generated_sprites/ output/
   ```
    - Replace `birefnet-portrait` with the model of your choice.
    - This saves the background-removed images in the `output/` subdirectory.

---

## Example Workflow

1. **Start Stable Diffusion WebUI**: Ensure the local server is running (`http://127.0.0.1:7860/`).
2. **Refine Prompts**: Use the WebUI to test your prompts and find the right seed, character, and settings.
3. **Update JSON File**: Add your refined prompt(s) and expressions to the `prompts.json` template.
4. **Run the Script**:
   ```bash
   python expressions.py --seed 987654321 --expressions happy,angry
   ```
5. **Process Results** (Optional):
   ```bash
   rembg p -m birefnet-portrait generated_sprites/ output/
   ```

---

## Troubleshooting

- **API URL Errors**: Ensure the `SD_API_URL` in the `.env` file matches the running WebUI server.
- **Invalid JSON**: Verify that the `prompts.json` file is properly formatted.
- **Background Removal Issues**: Check the `rembg` documentation [here](https://github.com/danielgatis/rembg).

---

## Credits

- **Stable Diffusion**: For enabling high-quality, AI-generated images.
- **Lykon/AAM_XL_AnimeMix**: Recommended model for anime art.
- **Rembg**: For optional background removal.
- **Community Support**: Contributions and open-source tools.

---

## License

This project is distributed under the MIT License.
