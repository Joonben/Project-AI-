from Tools.pdfread import *
from Tools.TestMBTI import *
from Tools.CariProfil import *
from Tools.SkillsFinder import *
from Tools.UpdateSkills import *
from Tools.JobFinder import *
from Tools.Job_forward_chaining import *

import json
import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def tampilkan_hasil(data):
    print(f"\n===== HASIL ANALISIS MAHASISWA {data['Nama']} =====")
    print(f"NIM            : {data['NIM']}")
    print(f"Nama           : {data['Nama']}")
    print(f"Program Studi  : {data['Prodi']}")
    print(f"IPK            : {data['IPK']}")
    print(f"MBTI           : {data['MBTI']}")
    print(f"Profil Lulusan : {data['Profil Lulusan']}")
    print("Hard Skills    : " + ", ".join(data["Skill"]["Hard Skill"]))
    print("Soft Skills    : " + ", ".join(data["Skill"]["Soft Skill"]))
    print("==============================================\n")

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
                "Tidak Cocok": None
            }
        }

        # Tentukan profil lulusan
        mata_kuliah = output_data["Nilai Mata Kuliah"]
        output_data["Profil Lulusan"] = tentukan_profil(mata_kuliah)

        # Jawab pertanyaan MBTI
        print("\n🧠 Jawab beberapa pertanyaan untuk menentukan MBTI Anda...")
        output_data["MBTI"] = mbti_test()

        # Tentukan hard skill dan soft skill
        output_data["Skill"]["Hard Skill"] = tentukan_hard_skill(mata_kuliah)
        output_data["Skill"]["Soft Skill"] = tentukan_soft_skill(output_data["MBTI"])

        # Tentukan pekerjaan yang cocok

        # # Load data pekerjaan dari file JSON
        # JobData = load_JobData()
        # if not JobData or "Bidang" not in JobData:
        #     print("❗ Data pekerjaan tidak valid atau 'Bidang' tidak ditemukan.")
        #     return

        # # Variabel untuk melacak pekerjaan paling cocok dan tidak cocok
        # best_match = None
        # best_non_match = None
        # highest_match_score = -1
        # lowest_match_score = float("inf")

        # # Periksa kecocokan pekerjaan
        # for bidang, roles in JobData["Bidang"].items():
        #     for role in roles:
        #         hard_skills = output_data["Skill"]["Hard Skill"]
        #         soft_skills = output_data["Skill"]["Soft Skill"]

        #         matching_hard_skills = [skill for skill in hard_skills if skill in role]
        #         matching_soft_skills = [skill for skill in soft_skills if skill in role]

        #         hard_skill_match = (len(matching_hard_skills) / len(hard_skills)) * 100 if hard_skills else 0
        #         soft_skill_match = (len(matching_soft_skills) / len(soft_skills)) * 100 if soft_skills else 0

        #         match_score = hard_skill_match + soft_skill_match

        #         # Cari pekerjaan yang paling cocok
        #         if match_score > highest_match_score:
        #             highest_match_score = match_score
        #             best_match = {
        #                 "Bidang": bidang,
        #                 "Role": role,
        #                 "Hard Skill Match (%)": round(hard_skill_match, 2),
        #                 "Soft Skill Match (%)": round(soft_skill_match, 2)
        #             }

        #         # Cari pekerjaan yang paling tidak cocok
        #         if match_score < lowest_match_score:
        #             lowest_match_score = match_score
        #             best_non_match = {
        #                 "Bidang": bidang,
        #                 "Role": role,
        #                 "Hard Skill Match (%)": None,
        #                 "Soft Skill Match (%)": None
        #             }

        # # Tentukan pekerjaan yang cocok dan tidak cocok
        # if best_match:
        #     output_data["Job"]["Cocok"] = best_match
        # else:
        #     print("\n⚠ Tidak ditemukan pekerjaan yang cocok berdasarkan analisis.")

        # if best_non_match:
        #     output_data["Job"]["Tidak Cocok"] = best_non_match

        # # Tampilkan hasil pekerjaan
        # if output_data["Job"]["Cocok"]:
        #     cocok = output_data["Job"]["Cocok"]
        #     print("\n💼 Pekerjaan yang paling cocok:")
        #     print(f"  - Bidang: {cocok['Bidang']}")
        #     print(f"  - Role: {cocok['Role']}")
        #     print(f"  - Hard Skill Match: {cocok['Hard Skill Match (%)']}%")
        #     print(f"  - Soft Skill Match: {cocok['Soft Skill Match (%)']}%")
        # else:
        #     print("\n⚠ Tidak ada pekerjaan yang cocok berdasarkan analisis.")

        # if output_data["Job"]["Tidak Cocok"]:
        #     tidak_cocok = output_data["Job"]["Tidak Cocok"]
        #     print("\n🚫 Pekerjaan yang paling tidak cocok:")
        #     print(f"  - Bidang: {tidak_cocok['Bidang']}")
        #     print(f"  - Role: {tidak_cocok['Role']}")
        #     print(f"  - Hard Skill Match: {tidak_cocok['Hard Skill Match (%)']}")
        #     print(f"  - Soft Skill Match: {tidak_cocok['Soft Skill Match (%)']}")

        # # Simpan data hasil analisis
        simpan_data(output_data)

    except Exception as e:
        print(f"\n❗ Terjadi kesalahan: {str(e)}")