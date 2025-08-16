import os
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

def main():
    # 1. Load API key
    load_dotenv(".env.pri")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("❌ GEMINI_API_KEY not found in .env.pri")
    client = genai.Client(api_key=api_key)

    # 2. Load CSV
    csv_path = r"C:\Projects\Personal\car-racing-fun-learn\docs\05_01_car_parts_game_style_2.csv"
    df = pd.read_csv(csv_path)

    # 3. Create output folder
    output_dir = "generated_images"
    os.makedirs(output_dir, exist_ok=True)

    # 4. Generate images
    for idx, row in df.iterrows():
        part_name = row["Part Name"]

        prompt = f"A highly detailed, realistic image of a futuristic car part: {part_name}. Game-style illustration."

        try:
            response = client.models.generate_images(
                model="imagen-4.0-generate-001",
                prompt=prompt,
                config=types.GenerateImagesConfig(number_of_images=1)
            )

            for i, gen_image in enumerate(response.generated_images):
                img: Image.Image = gen_image.image
                safe_name = part_name.replace(" ", "_").replace("/", "_")
                file_path = os.path.join(output_dir, f"{safe_name}_{i}.png")
                img.save(file_path)
                print(f"✅ Generated: {part_name} → {file_path}")

        except Exception as e:
            print(f"❌ Failed for {part_name}: {e}")

if __name__ == "__main__":
    main()
