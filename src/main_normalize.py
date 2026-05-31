import sys
import os
import src.util.pdf_util as putil
import src.util.dcm_util as dutil

if __name__ == '__main__':
    # === CONSTANTES GLOBAIS ===
    RE_PATTERN = r"PERFIL(.*?)(?=1\.)" # regex para extração de texto
    FORMAT = "PNG" # formato final das imagens .dcm (lossless)
    # ==========================

    try:
        # Diretórios de input e output recebidos da linha de comando
        input_dir, output_dir = str(sys.argv[1]), str(sys.argv[2])
        
        for dir in os.listdir(input_dir): # Itera por cada diretório (paciente) no input_dir
            full_input_dir_path = os.path.join(input_dir, dir) # path completo do diretório
            full_output_dir_path = os.path.join(output_dir, dir) # path completo do diretório em output_dir

            if not os.path.exists(full_output_dir_path): # cria o path do diretório em output_dir se não existir
                os.mkdir(full_output_dir_path)

            for file_name in os.listdir(full_input_dir_path): # Itera por cada arquivo do diretório de cada paciente
                full_file_path = os.path.join(full_input_dir_path, file_name)
                # === TEXT ===
                if file_name.lower().endswith('.pdf'):
                    extracted_text = putil.extract_text_from_pdf(full_file_path)
                    filtered_text = putil.filter_text(extracted_text, RE_PATTERN)

                    full_output_file_path = os.path.join(full_output_dir_path, "report.txt")

                    with open(full_output_file_path, "w") as file:
                        file.write(filtered_text if filtered_text else "None")
                    file.close()
                # ============
                # === IMAGES ===
                elif file_name.lower().endswith('.dcm'):
                    image_suffix = dutil.get_suffix(full_file_path).lower()

                    raw_data = dutil.load_dicom_image(full_file_path)
                    data_8bit = dutil.normalize_to_8bit(raw_data)
                    final_image = dutil.resize_with_padding(data_8bit, size=(512, 512))

                    full_output_file_path = os.path.join(full_output_dir_path, f"{image_suffix}.{FORMAT.lower()}")

                    final_image.save(full_output_file_path, format=FORMAT, quality=95)
                # ==============



    except Exception as e:
        print("Erro: " + e)
