# 🚗 Car Parts Image Generator

This utility script reads a CSV file of **car parts** and generates **game-style futuristic illustrations** for each part using **Stable Diffusion v1.5**.

Images are saved into a local `generated_images/` folder.

---

## 📦 Requirements

* Python **3.10+**
* [Poetry](https://python-poetry.org/docs/#installation) for dependency management
* (Optional) A **GPU with CUDA** for faster image generation

---

## ⚙️ Setup

1. Clone the repo or copy the script into your project:

   ```bash
   git clone <your-repo-url>
   cd utility-scripts
   ```

2. Install dependencies with **Poetry**:

   ```bash
   poetry install
   ```

3. Place your CSV file of car parts here:

   ```
   C:\Projects\Personal\car-racing-fun-learn\docs\05_01_car_parts_game_style_2.csv
   ```

   The CSV must contain a column named **`Part Name`**.

4. (Optional) Configure a custom cache folder by adding to `.env.pri`:

   ```env
   MODEL_CACHE=C:\Projects\model_cache
   ```

   If not set, the model cache defaults to `./models_cache/`.

---

## ▶️ Run

From the project root:

```bash
poetry run python src/utility-scripts/generate_car_parts_gemini_api/main.py
```

This will:

* Load the CSV
* Download Stable Diffusion v1.5 (first run only)
* Generate 1024×1024 PNG images
* Save results in:

  ```
  generated_images/
  ```

---

## 📂 Project Structure

```
utility-scripts/
│
├── pyproject.toml          # Poetry dependencies
├── README.md               # This file
├── .env.pri                # (Optional) env vars like MODEL_CACHE
│
└── src/
    └── utility-scripts/
        └── generate_car_parts_gemini_api/
            └── main.py     # Script entry point
```

---

## ⚡ Notes

* The first run will **download \~4GB model weights** into the cache.
* Subsequent runs will **reuse the local cache**.
* If you run on **CPU**, generation will be slow (\~30s per image). On **GPU**, much faster (\~2-4s per image).
* Images are generated **locally** → no API key or billing required.
