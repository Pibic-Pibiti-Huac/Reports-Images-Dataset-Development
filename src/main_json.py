import base64
import io
import os
import sys
import json
from PIL import Image

def encode_image(file_path) -> str:
    encoded_string = None

    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode('utf-8')
    file.close()

    return encoded_string


if __name__ == "__main__":
    try:
        input_dir, output_dir = str(sys.argv[1]), str(sys.argv[2])

        json_list = list()
        serial_id = 0

        for dir in os.listdir(input_dir):
            full_input_dir_path = os.path.join(input_dir, dir)

            report_data = dict()

            req_number = dir # número da requisição
            serial_id += 1 # id serial

            report_data["requisition"] = req_number
            report_data["id"] = serial_id

            for file_name in os.listdir(full_input_dir_path):
                full_file_path = os.path.join(full_input_dir_path, file_name)

                if file_name.lower().endswith('.txt'):
                    report_content = ""
                    with open(full_file_path, "r") as file:
                        report_content = file.read()
                    file.close()

                    report_data["report"] = report_content

                elif file_name.lower() == "pa.png":
                    image_code = encode_image(full_file_path)
                    report_data["pa_image"] = image_code
                elif file_name.lower() == "perfil.png":
                    image_code = encode_image(full_file_path)
                    report_data["perfil_image"] = image_code

            json_list.append(report_data)

        output_file_path = os.path.join(output_dir, "reports_images.json")

        with open(output_file_path, "w") as json_file:
            json.dump(json_list, json_file, indent=4, ensure_ascii=False)

        json_file.close()

    except Exception as e:
        print("Erro: " + e)
