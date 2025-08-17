import os
import pandas as pd
from PIL import Image
from dotenv import load_dotenv
from diffusers import StableDiffusionPipeline
import torch
from tqdm import tqdm

def load_stable_diffusion():
    """Load Stable Diffusion model with local cache."""
    model_id = "runwayml/stable-diffusion-v1-5"

    # Use a local cache folder inside the project
    cache_dir = os.path.join(os.getcwd(), "models_cache")
    os.makedirs(cache_dir, exist_ok=True)

    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        cache_dir=cache_dir   # ✅ cache weights here
    )
    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    return pipe

def main():
    # 1. Load CSV
    csv_path = r"C:\Projects\Personal\car-racing-fun-learn\docs\05_01_car_parts_game_style_2.csv"
    df = pd.read_csv(csv_path)

    # 2. Output folder
    output_dir = "generated_images"
    os.makedirs(output_dir, exist_ok=True)

    # 3. Load Stable Diffusion (cached)
    pipe = load_stable_diffusion()

    # 4. Generate images
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Generating car parts"):
        part_name = row["Part Name"]
        prompt = f"A highly detailed, realistic image of a futuristic car part: {part_name}. Game-style illustration."

        try:
            image = pipe(prompt).images[0]
            safe_name = part_name.replace(" ", "_").replace("/", "_")
            file_path = os.path.join(output_dir, f"{safe_name}.png")
            image.save(file_path)
            tqdm.write(f"✅ {part_name} → {file_path}")
        except Exception as e:
            tqdm.write(f"❌ Failed for {part_name}: {e}")

if __name__ == "__main__":
    main()
