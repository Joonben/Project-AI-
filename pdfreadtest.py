'''
tabrakan
'''
import pdfplumber
import re
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class Config:
    INPUT_PDF = "Project-AI-/daftarnilai71210793.pdf"
    OUTPUT_JSON = "Project-AI-/hasil_nilai_mahasiswa.json"
    OUTPUT_PDF = "Project-AI-/output_json_printed.pdf"
    MBTI_TYPE = "INFP"
    GRADUATE_PROFILE = "IN"

def extract_transcript_data(pdf_path):
    data = {
        "nim": "",
        "nama": "",
        "fakultas": "",
        "program_studi": "",
        "mata_kuliah": [],
        "total_sks": 0,
        "ipk": 0.0
    }

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            # Extract student information
            if not data["nim"]:
                nim_match = re.search(r"No\. Mahasiswa\s*:\s*(\d+)", text)
                if nim_match:
                    data["nim"] = nim_match.group(1)

            if not data["nama"]:
                nama_match = re.search(r"Nama\s*:\s*(.+)", text)
                if nama_match:
                    data["nama"] = nama_match.group(1).strip()

            if not data["fakultas"]:
                fakultas_match = re.search(r"Fakultas\s*:\s*(.+)", text)
                if fakultas_match:
                    data["fakultas"] = fakultas_match.group(1).strip()

            if not data["program_studi"]:
                program_match = re.search(r"Program\s*:\s*(.+)", text)
                if program_match:
                    data["program_studi"] = program_match.group(1).strip()

            # Extract SKS and IPK
            if data["total_sks"] == 0:
                sks_match = re.search(r"Total SKS\s*:\s*(\d+)", text)
                if sks_match:
                    data["total_sks"] = int(sks_match.group(1))

            if data["ipk"] == 0.0:
                ipk_match = re.search(r"IP Kumulatif\s*:\s*([\d.]+)", text)
                if ipk_match:
                    data["ipk"] = float(ipk_match.group(1))

            # Extract courses - improved pattern to match course rows
            course_pattern = re.compile(r"^(\d+)\s+([A-Z]+\d+)\s+(.+?)\s+(\d+)\s+([A-Z+-]+)$", re.MULTILINE)
            for match in course_pattern.finditer(text):
                # Skip header rows
                if match.group(3).startswith(('MBNP', 'MPBP', 'MPWP', 'WAJIB')):
                    continue
                    
                data["mata_kuliah"].append({
                    "no": match.group(1),
                    "kode": match.group(2),
                    "nama": match.group(3).strip(),
                    "sks": int(match.group(4)),
                    "nilai": match.group(5)
                })

    return data

def create_pdf_report(data, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y_position = height - 40
    line_height = 14
    
    c.setFont("Courier", 10)
    
    json_str = json.dumps(data, indent=4, ensure_ascii=False)
    
    for line in json_str.split('\n'):
        if y_position < 40:
            c.showPage()
            y_position = height - 40
        c.drawString(40, y_position, line)
        y_position -= line_height
    
    c.save()

def main():
    try:
        # Extract data from PDF
        transcript_data = extract_transcript_data(Config.INPUT_PDF)
        
        # Prepare JSON output
        output_data = [{
            "nama": transcript_data["nama"],
            "mbti": Config.MBTI_TYPE,
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mata_kuliah": {
                course["nama"]: course["nilai"] 
                for course in transcript_data["mata_kuliah"]
            },
            "profil_lulusan": Config.GRADUATE_PROFILE
        }]
        
        # Save to JSON
        with open(Config.OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
        
        # Generate PDF
        create_pdf_report(output_data, Config.OUTPUT_PDF)
        
        print(f"Success! JSON saved to {Config.OUTPUT_JSON} and PDF to {Config.OUTPUT_PDF}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()








'''
print saja
'''
# import pdfplumber
# import re

# def extract_transcript_data(pdf_path):
#     data = {
#         "nim": "",
#         "nama": "",
#         "fakultas": "",
#         "program_studi": "",
#         "mata_kuliah": [],
#         "total_sks": 0,
#         "total_angka_kualitas": 0.0,
#         "ipk": 0.0
#     }

#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text = page.extract_text()
#             if not text:
#                 continue

#             # Ekstrak informasi mahasiswa
#             nim_match = re.search(r"No\. Mahasiswa\s*:\s*(\d+)", text)
#             if nim_match:
#                 data["nim"] = nim_match.group(1)
                
#             nama_match = re.search(r"Nama\s*:\s*(.+)", text)
#             if nama_match:
#                 data["nama"] = nama_match.group(1).strip()
                
#             fakultas_match = re.search(r"Fakultas\s*:\s*(.+)", text)
#             if fakultas_match:
#                 data["fakultas"] = fakultas_match.group(1).strip()
                
#             program_match = re.search(r"Program\s*:\s*(.+)", text)
#             if program_match:
#                 data["program_studi"] = program_match.group(1).strip()

#             # Ekstrak total SKS dan IPK
#             sks_match = re.search(r"Total SKS\s*:\s*(\d+)", text)
#             if sks_match:
#                 data["total_sks"] = int(sks_match.group(1))
                
#             ipk_match = re.search(r"IP Kumulatif\s*:\s*([\d.]+)", text)
#             if ipk_match:
#                 data["ipk"] = float(ipk_match.group(1))

#             # Ekstrak mata kuliah dari tabel
#             # Pola untuk mendeteksi baris mata kuliah (contoh: "1   | T10453 | BAHASA INGGRIS INFORMATIKA | 3 | A")
#             course_pattern = re.compile(r"^\s*(\d+)\s*\ \s*([A-Z0-9]+)\s*\ \s*(.+?)\s*\ \s*(\d+)\s*\ \s*([A-Z+-]+)\s*$", re.MULTILINE)
            
#             for match in course_pattern.finditer(text):
#                 no = match.group(1)
#                 kode = match.group(2)
#                 nama = match.group(3)
#                 sks = int(match.group(4))
#                 nilai = match.group(5)
                
#                 # Skip baris header (MPBP Matakuliah Pilihan Bebas Prodi, dll)
#                 if not kode.isdigit() and not kode[0].isalpha():
#                     continue
                    
#                 data["mata_kuliah"].append({
#                     "no": no,
#                     "kode": kode,
#                     "nama": nama,
#                     "sks": sks,
#                     "nilai": nilai
#                 })

#     return data

# # Contoh penggunaan
# pdf_path = "Project-AI-/daftarnilai71210793.pdf"
# transcript_data = extract_transcript_data(pdf_path)

# # Cetak hasil ekstraksi
# print("=== Informasi Mahasiswa ===")
# print(f"NIM: {transcript_data['nim']}")
# print(f"Nama: {transcript_data['nama']}")
# print(f"Fakultas: {transcript_data['fakultas']}")
# print(f"Program Studi: {transcript_data['program_studi']}")
# print(f"Total SKS: {transcript_data['total_sks']}")
# print(f"IPK: {transcript_data['ipk']}\n")

# print("=== Daftar Mata Kuliah ===")
# for mk in transcript_data["mata_kuliah"]:
#     print(f"{mk['no']}. {mk['nama']} : {mk['nilai']}")