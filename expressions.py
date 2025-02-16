import os
import sys
import json
import urllib.request
import urllib.error
import base64
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read API_URL and output folder from environment variables
SD_API_URL = os.getenv("SD_API_URL", "http://127.0.0.1:7860/sdapi/v1/txt2img")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "generated_sprites")

def setup_output_folder(path=OUTPUT_FOLDER):
    """Ensure the output folder exists."""
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        print(f"Error: Unable to create or access output folder: {e}")
        exit(1)
    return path

def load_prompts(prompt_file):
    """Load prompts configuration from the given JSON file."""
    try:
        with open(prompt_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {prompt_file} was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to parse {prompt_file}. Ensure it's valid JSON.")
        sys.exit(1)

def get_next_versioned_filename(output_folder, expression):
    """Find the next versioned filename to avoid overwriting existing files."""
    version = 1
    base_filename = os.path.join(output_folder, expression)
    while os.path.exists(f"{base_filename}_{version}.png"):
        version += 1
    return f"{base_filename}_{version}.png"

def generate_image(api_url, payload, output_folder, expression):
    """Call the API to generate the image and save it in the output folder."""
    try:
        # Prepare the HTTP request
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(api_url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=20) as response:
            response_data = json.loads(response.read().decode('utf-8'))

            # Validate and process the images response
            if "images" in response_data and len(response_data["images"]) > 0:
                img_data = response_data["images"][0]

                # Decode base64-encoded image data and save the image
                img_path = get_next_versioned_filename(output_folder, expression)
                with open(img_path, "wb") as f:
                    f.write(base64.b64decode(img_data))  # Decode and write the binary image data
                print(f"Saved: {img_path}")
            else:
                print(
                    f"Error: Unexpected API response format or empty 'images' field for {expression}: {response_data}")
    except urllib.error.URLError as e:
        print(f"Error generating image for {expression}: {e}")
    except Exception as ex:
        print(f"Unexpected error while processing {expression}: {ex}")

def parse_arguments():
    """Parse command-line arguments for payload settings."""
    parser = argparse.ArgumentParser(description="Generate images using SD WebUI API.")
    parser.add_argument("--prompt_file", type=str, default="prompts.json",
                        help="Path to the prompt file (default: prompts.json)")
    parser.add_argument("--width", type=int, default=1024, help="Image width (default: 1024)")
    parser.add_argument("--height", type=int, default=1024, help="Image height (default: 1024)")
    parser.add_argument("--steps", type=int, default=30, help="Number of steps (default: 30)")
    parser.add_argument("--cfg_scale", type=float, default=7.5, help="CFG scale (default: 7.5)")
    parser.add_argument("--sampler", type=str, default="SA Solver", help="Sampling method (default: SA Solver)")
    parser.add_argument("--seed", type=int, default=2472820057,
                        help="Seed for consistent generation (default: 2472820057)")
    parser.add_argument("--expressions", type=str, help="Comma-separated list of expressions to generate. (default: All expressions)")
    return parser.parse_args()

def main():
    """Main entry point of the script."""
    output_folder = setup_output_folder()
    args = parse_arguments()

    # Load prompts from the specified file or default to "prompts.json"
    prompts = load_prompts(args.prompt_file)

    # Determine which expressions to generate
    expressions = prompts["expressions"]
    if args.expressions:
        requested_expressions = set(args.expressions.split(","))
        expressions = {k: v for k, v in expressions.items() if k in requested_expressions}
        if not expressions:
            print("Error: None of the requested expressions match available expressions.")
            sys.exit(1)

    # Loop through expressions and generate images
    total_expressions = len(expressions)
    success_count = 0
    error_count = 0
    for idx, (expression, description) in enumerate(expressions.items(), start=1):
        print(f"[{idx}/{total_expressions}] Generating: {expression}...")

        # Create the payload with user-specified overrides
        payload = {
            "prompt": f"{prompts['base_prompt']}, {description}, {prompts['character_details']}",
            "negative_prompt": prompts["negative_prompt"],
            "steps": args.steps,
            "cfg_scale": args.cfg_scale,
            "width": args.width,
            "height": args.height,
            "seed": args.seed,
            "sampler_name": "SA Solver",
            "subseed": -1,
            "subseed_strength": 0.1,
            "save_images": "true",
            "send_images": "true",
            "do_not_save_grid": "false",
            "do_not_save_samples": "false"
        }
        # Generate images
        try:
            generate_image(SD_API_URL, payload, output_folder, expression)
            success_count += 1
        except:
            error_count += 1
    print(f"Batch processing complete: {success_count} succeeded, {error_count} failed.")

if __name__ == "__main__":
    main()
