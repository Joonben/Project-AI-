from Tools.pdfread import *
from Tools.TestMBTI import *
from Tools.CariProfil import *
from Tools.SkillsFinder import *
from Tools.UpdateSkills import *
from Tools.JobFinder import *

import json
import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def tampilkan_hasil(data):
    print(f"\n===== HASIL ANALISIS MAHASISWA {data['Nama'].upper()} =====")
    print(f"NIM            : {data['NIM']}")
    print(f"Nama           : {data['Nama']}")
    print(f"Program Studi  : {data['Prodi']}")
    print(f"IPK            : {data['IPK']}")
    print(f"MBTI           : {data['MBTI']}")
    print(f"Profil Lulusan : {data['Profil Lulusan']}")
    print("=" * 80)

    hard_skills = data["Skill"].get("Hard Skill", [])
    soft_skills = data["Skill"].get("Soft Skill", [])

    max_len = max(len(hard_skills), len(soft_skills))
    hard_skills += [""] * (max_len - len(hard_skills))
    soft_skills += [""] * (max_len - len(soft_skills))

    print(f"{'NO.':<5}{'Hard Skills':<40} | {'Soft Skills'}")
    print("-" * 80)
    for i, (h, s) in enumerate(zip(hard_skills, soft_skills), start=1):
        print(f"{i:<5}{h:<40} | {s}")
    print("=" * 80 + "\n")


def tampilkan_semua_data(path="Json/hasil_nilai_mahasiswa.json"):
    if not os.path.exists(path):
        print("❗ Belum ada data yang tersimpan.")
        return

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if not data:
                print("❗ Data kosong.")
                return

            for mahasiswa in data:
                tampilkan_hasil(mahasiswa)
        except json.JSONDecodeError:
            print("❗ Gagal membaca data JSON.")

def tampilkan_data_nim(nim, path="Json/hasil_nilai_mahasiswa.json"):
    if not os.path.exists(path):
        print("❗ File data tidak ditemukan.")
        return

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            for mahasiswa in data:
                if mahasiswa["NIM"] == nim:
                    tampilkan_hasil(mahasiswa)
                    return
            print(f"❗ Data dengan NIM {nim} tidak ditemukan.")
        except json.JSONDecodeError:
            print("❗ Format file JSON rusak.")

def simpan_data(data_baru, path="Json/hasil_nilai_mahasiswa.json"):
    os.makedirs("Json", exist_ok=True)

    # Baca data lama kalau ada
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                data_lama = json.load(f)
                if not isinstance(data_lama, list):
                    data_lama = []
            except json.JSONDecodeError:
                data_lama = []
    else:
        data_lama = []

    # Cek apakah NIM sudah ada
    nim_baru = data_baru["NIM"]
    ditemukan = False
    for i, mahasiswa in enumerate(data_lama):
        if mahasiswa["NIM"] == nim_baru:
            data_lama[i] = data_baru  # Update data lama
            ditemukan = True
            break

    if not ditemukan:
        data_lama.append(data_baru)  # Tambah data baru

    # Simpan kembali seluruh data
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data_lama, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Data berhasil disimpan {'(diperbarui)' if ditemukan else '(ditambahkan baru)'} ke: {path}\n")

def run_analysis(nim):
    path = f"DaftarNilai/daftarnilai{nim}.pdf"
    if not os.path.exists(path):
        print(f"❗ File {path} tidak ditemukan.")
        return

    try:
        # Load data dari PDF
        transcript_data = extract_transcript_data(path)

        # Template output
        output_data = {
            "NIM": transcript_data["nim"],
            "Nama": transcript_data["nama"] or "Unknown",
            "MBTI": "",
            "IPK": transcript_data["ipk"],
            "Prodi": transcript_data["program_studi"],
            "Profil Lulusan": "",
            "Nilai Mata Kuliah": {
                mk["nama"]: mk["nilai"]
                for mk in transcript_data["mata_kuliah"]
            },
            "Skill": {
                "Hard Skill": [],
                "Soft Skill": []
            },
            "Job": {
                "Cocok": None,
            }
        }

        # Tentukan profil lulusan
        mata_kuliah = output_data["Nilai Mata Kuliah"]
        output_data["Profil Lulusan"] = tentukan_profil(mata_kuliah)

        # Jawab pertanyaan MBTI
        print("\n🧠 Jawab beberapa pertanyaan untuk menentukan MBTI Anda...")
        output_data["MBTI"] = mbti_test()

        output_data["Skill"]["Hard Skill"] = tentukan_hard_skill(mata_kuliah)
        output_data["Skill"]["Soft Skill"] = tentukan_soft_skill(output_data["MBTI"])
         
        simpan_data(output_data)

    except Exception as e:
        print(f"\n❗ Terjadi kesalahan: {str(e)}")