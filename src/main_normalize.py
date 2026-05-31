import sys
import os
import src.util.pdf_util as putil

if __name__ == '__main__':
    RE_PATTERN = r"PERFIL(.*?)(?=1\.)"

    try:
        input_dir, output_dir = str(sys.argv[1]), str(sys.argv[2])

        for dir in os.listdir(input_dir):
            full_dir_path = os.path.join(input_dir, dir)

            # ==== TEXT ====
            pdf_report_file_path = os.path.join(full_dir_path, "report.pdf")

            extracted_text = putil.extract_text_from_pdf(pdf_report_file_path)
            filtered_text = putil.filter_text(extracted_text, RE_PATTERN)
            # ==============

            # ==== IMAGES ===
            # ===============

            # ==== OUTPUT_DIR ===
            full_out_dir_path = os.path.join(output_dir, dir)
            os.mkdir(full_out_dir_path)
            
            # -- text
            text_out_path = os.path.join(full_out_dir_path, "report.txt")
            with open(text_out_path, "w") as report_file:
                report_file.write(filtered_text)
            report_file.close()
            # --

            # ===================

    except Exception as e:
        print("Erro: " + e)
