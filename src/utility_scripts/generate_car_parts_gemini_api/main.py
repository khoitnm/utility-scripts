import os
import base64
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load environment variables from .env.pri
load_dotenv(".env.pri")

# 2. Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 3. Read the CSV file (absolute path)
csv_path = r"C:\Projects\Personal\car-racing-fun-learn\docs\05_01_car_parts_game_style_2.csv"
df = pd.read_csv(csv_path)

# 4. Choose Gemini model for image generation
model: genai.GenerativeModel = genai.GenerativeModel("gemini-1.5-flash")

# 5. Create output folder
output_dir = "generated_images"
os.makedirs(output_dir, exist_ok=True)

# 6. Loop through car parts and generate images
for idx, row in df.iterrows():
    part_name = row["Part Name"]  # Make sure your CSV has a column "Part Name"

    prompt = f"A highly detailed, realistic image of a futuristic car part: {part_name}. Game-style illustration."

    try:
        response = model.generate_images(
            prompt=prompt,
            size="1024x1024"
        )

        # Save the first image result
        image_data = response.images[0]
        if isinstance(image_data, str):
            image_bytes = base64.b64decode(image_data)
        else:
            image_bytes = image_data

        file_path = os.path.join(output_dir, f"{part_name.replace(' ', '_')}.png")
        with open(file_path, "wb") as f:
            f.write(image_bytes)

        print(f"✅ Generated: {part_name} → {file_path}")

    except Exception as e:
        print(f"❌ Failed for {part_name}: {e}")
