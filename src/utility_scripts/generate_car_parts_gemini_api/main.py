import os
import pandas as pd
from diffusers import AutoPipelineForText2Image, DPMSolverMultistepScheduler
import torch
from tqdm import tqdm

def load_dreamshaper_pipeline():
    """Load the DreamShaper XL Lightning model with local caching."""
    model_id = "lykon/dreamshaper-xl-lightning"
    cache_dir = os.path.join(os.getcwd(), "models_cache")
    os.makedirs(cache_dir, exist_ok=True)

    pipe = AutoPipelineForText2Image.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        variant="fp16",
        cache_dir=cache_dir
    )
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    return pipe

def main():
    # 1. Configuration
    # Assuming the script is run from the repository root.
    # The user should place their CSV file here.
    csv_path = "data/car_parts.csv"
    output_dir = "generated_images_dreamshaper"
    os.makedirs(output_dir, exist_ok=True)

    # Check if the CSV file exists.
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        print("Please create a CSV file with 'Part Name' and 'Description' columns.")
        # As a fallback, create a dummy dataframe
        print("Creating a dummy dataframe for demonstration.")
        data = {'Part Name': ['Alloy Wheel', 'Spoiler'], 'Description': ['A shiny chrome alloy wheel.', 'A sleek carbon fiber spoiler.']}
        df = pd.DataFrame(data)
    else:
        df = pd.read_csv(csv_path)

    print(f"Loaded {len(df)} car parts.")

    # 2. Load the pipeline
    pipe = load_dreamshaper_pipeline()

    # 3. Generate images
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Generating car parts"):
        part_name = row.get("Part Name") or row.get("Part")
        description = row.get("Description", "")

        if not part_name:
            tqdm.write(f"Skipping row {idx} due to missing 'Part Name'.")
            continue

        # A more descriptive prompt for better results with DreamShaper
        prompt = (
            f"masterpiece, best quality, photorealistic, game asset, futuristic car part, "
            f"{part_name}: {description}, "
            f"8k, detailed, intricate, elegant, highly detailed, sharp focus, vibrant colors"
        )

        try:
            image = pipe(
                prompt,
                num_inference_steps=6,
                guidance_scale=2.5,
                width=512,
                height=512
            ).images[0]

            safe_name = part_name.replace(" ", "_").replace("/", "_")
            file_path = os.path.join(output_dir, f"{safe_name}.png")
            image.save(file_path)
            tqdm.write(f"✅ {part_name} → {file_path}")
        except Exception as e:
            tqdm.write(f"❌ Failed for {part_name}: {e}")

if __name__ == "__main__":
    main()
