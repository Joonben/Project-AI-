'''
minus tidak terbaca
'''
import pdfplumber
import re
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ==== CONFIGURATION ====
class Config:
    INPUT_PDF = "Project-AI-/daftarnilai71210793.pdf"
    OUTPUT_JSON = "Project-AI-/hasil_nilai_mahasiswa.json"
    OUTPUT_PDF = "Project-AI-/output_json_printed.pdf"
    MBTI_TYPE = "INFP"
    GRADUATE_PROFILE = "IN"

# ==== PDF EXTRACTION FUNCTION ====
def extract_transcript_data(pdf_path):
    data = {
        "nim": "",
        "nama": "",
        "fakultas": "",
        "program_studi": "",
        "mata_kuliah": [],
        "total_sks": 0,
        "total_angka_kualitas": 0.0,
        "ipk": 0.0
    }

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            # Ekstrak informasi mahasiswa
            nim_match = re.search(r"No\. Mahasiswa\s*:\s*(\d+)", text)
            if nim_match:
                data["nim"] = nim_match.group(1)

            nama_match = re.search(r"Nama\s*:\s*(.+)", text)
            if nama_match:
                data["nama"] = nama_match.group(1).strip()

            fakultas_match = re.search(r"Fakultas\s*:\s*(.+)", text)
            if fakultas_match:
                data["fakultas"] = fakultas_match.group(1).strip()

            program_match = re.search(r"Program\s*:\s*(.+)", text)
            if program_match:
                data["program_studi"] = program_match.group(1).strip()

            # Total SKS & IPK
            sks_match = re.search(r"Total SKS\s*:\s*(\d+)", text)
            if sks_match:
                data["total_sks"] = int(sks_match.group(1))

            ipk_match = re.search(r"IP Kumulatif\s*:\s*([\d.]+)", text)
            if ipk_match:
                data["ipk"] = float(ipk_match.group(1))

            # Ekstrak mata kuliah dari tabel
            course_pattern = re.compile(r"\b(\d+)\s+[A-Z]+\d+\s+(.+?)\s+(\d+)\s+([A-E][+-]?)\b")
            for match in course_pattern.finditer(text):
                no = match.group(1)
                nama = match.group(2).strip()
                sks = int(match.group(3))
                nilai = match.group(4).strip()

                data["mata_kuliah"].append({
                    "no": no,
                    "nama": nama,
                    "sks": sks,
                    "nilai": nilai
                })

    return data

# ==== PDF CREATION FUNCTION ====
def create_pdf_report(data: list, filename: str) -> None:
    c = canvas.Canvas(filename, pagesize=A4)
    text_obj = c.beginText(40, 800)
    text_obj.setFont("Courier", 9)

    json_str = json.dumps(data, indent=4, ensure_ascii=False)

    for line in json_str.splitlines():
        if text_obj.getY() < 40:
            c.drawText(text_obj)
            c.showPage()
            text_obj = c.beginText(40, 800)
            text_obj.setFont("Courier", 9)
        text_obj.textLine(line)

    c.drawText(text_obj)
    c.save()

# ==== MAIN ====
def main():
    try:
        # Step 1: Extract from PDF
        transcript_data = extract_transcript_data(Config.INPUT_PDF)

        # Step 2: Format for JSON output
        output_data = [{
            "nama": transcript_data["nama"] or "Unknown",
            "mbti": Config.MBTI_TYPE,
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mata_kuliah": {
                mk["nama"]: mk["nilai"]
                for mk in transcript_data["mata_kuliah"]
            },
            "profil_lulusan": Config.GRADUATE_PROFILE
        }]

        # Step 3: Save to JSON
        with open(Config.OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)

        # Step 4: Generate PDF output
        create_pdf_report(output_data, Config.OUTPUT_PDF)

        print(f"✅ Berhasil! File JSON disimpan di '{Config.OUTPUT_JSON}' dan PDF di '{Config.OUTPUT_PDF}'.")

    except Exception as e:
        print(f"❌ Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    main()

