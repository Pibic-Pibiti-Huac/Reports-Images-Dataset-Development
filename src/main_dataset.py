import sys
import json
import tempfile
import base64
import io
import os
from PIL import Image
from datasets import Dataset, Features, Value, Image as HFImage
from huggingface_hub import login

if __name__ == '__main__':
    
    # try:
    hf_token = str(sys.argv[1])
    hf_repo_id = str(sys.argv[2])
    json_path = str(sys.argv[3])

    TEST_SIZE = 0.25

    # =========================
    # LOAD JSON
    # =========================

    with open(json_path, "r") as file:
        data = json.load(file)

    # =========================
    # TEMP DIR FOR IMAGES
    # =========================

    temp_dir = tempfile.mkdtemp()

    processed_data = []

    # =========================
    # PROCESS DATA
    # =========================

    for idx, item in enumerate(data):

        # -------- PA IMAGE --------

        pa_bytes = base64.b64decode(item["pa_image"])

        pa_image = Image.open(io.BytesIO(pa_bytes)).convert("RGB")

        pa_path = os.path.join(temp_dir, f"{idx}_pa.png")

        pa_image.save(pa_path)

        # -------- PERFIL IMAGE --------

        perfil_bytes = base64.b64decode(item["perfil_image"])

        perfil_image = Image.open(io.BytesIO(perfil_bytes)).convert("RGB")

        perfil_path = os.path.join(temp_dir, f"{idx}_perfil.png")

        perfil_image.save(perfil_path)

        # -------- DATA ENTRY --------

        processed_data.append({
            "id": str(item["id"]),
            "requisition": item["requisition"],
            "report": item["report"],
            # "label": item["label"],
            # "feedback": item["feedback"]
            # IMPORTANT:
            # Must be {"path": "..."}
            "pa_image": {
                "path": pa_path
            },

            "perfil_image": {
                "path": perfil_path
            }
        })

    # =========================
    # DATASET FEATURES
    # =========================

    features = Features({
        "id": Value("string"),
        "requisition": Value("string"),
        "report": Value("string"),
        # "label": Value("string"),
        # "feedback": Value("string")
        "pa_image": HFImage(),
        "perfil_image": HFImage()
    })

    # =========================
    # CREATE DATASET
    # =========================

    dataset = Dataset.from_list(
        processed_data,
        features=features
    )

    # =========================
    # TRAIN / TEST SPLIT
    # =========================

    dataset_split = dataset.train_test_split(
        test_size=TEST_SIZE,
        seed=42
    )

    # =========================
    # LOGIN HF
    # =========================

    login(hf_token)

    # =========================
    # PUSH TO HUB
    # =========================

    dataset_split.push_to_hub(hf_repo_id)

    print("Dataset enviado com sucesso!")
    # except Exception as e:
    #     print(e)
