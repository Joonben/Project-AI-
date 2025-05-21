import pdfplumber
import re
import json
from datetime import datetime
from Tools.krs_parser import parse_krs

# class Config:
#     OUTPUT_JSON = "Json/hasil_nilai_mahasiswa.json"

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

            nama_match = re.search(r"Nama\s*:\s*(.+?)(?=\s*Program)", text)
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
            matkuls = parse_krs(text)
            for matkul in matkuls:
                data["mata_kuliah"].append({
                    "no": len(matkul['no']),
                    "nama": matkul["nama"],
                    "sks": len(matkul["sks"]),
                    "nilai": matkul["nilai"]
                })

    return data


 