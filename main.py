from Tools.pdfread import *
from Tools.TestMBTI import *
from Tools.CariProfil import *
from Tools.SkillsFinder import *
from Tools.UpdateSkills import *
import json
import os

def show_menu():
    print("=" * 50)
    print("📘  SELAMAT DATANG DI APLIKASI ANALISIS PROFIL MAHASISWA  📘")
    print("=" * 50)
    print("Silakan pilih opsi berikut:")
    print("1. 🔍 Cek Profil, MBTI, dan Skill berdasarkan Daftar Nilai")
    print("2. 🛠️  Perbarui Hard/Soft Skill Secara Manual")
    print("3. ❌ Keluar")
    print("=" * 50)

def tampilkan_hasil(data):
    print("\n===== HASIL ANALISIS MAHASISWA =====")
    print(f"NIM         : {data['NIM']}")
    print(f"Nama        : {data['Nama']}")
    print(f"Program Studi : {data['Prodi']}")
    print(f"IPK         : {data['IPK']}")
    print(f"MBTI        : {data['MBTI']}")
    print(f"Profil Lulusan : {data['Profil Lulusan']}")
    print("Hard Skills : " + ", ".join(data["Skill"]["Hard Skill"]))
    print("Soft Skills : " + ", ".join(data["Skill"]["Soft Skill"]))
    print("====================================\n")

def simpan_data(data, path="Json/hasil_nilai_mahasiswa.json"):
    os.makedirs("Json", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✅ Data berhasil disimpan ke: {path}\n")

def run_analysis():
    print("\nMasukkan file daftar nilai (PDF) ke folder `DaftarNilai/` terlebih dahulu.")
    nim = input("Masukkan NIM Anda: ")

    path = f"DaftarNilai/daftarnilai{nim}.pdf"
    if not os.path.exists(path):
        print(f"❗ File {path} tidak ditemukan.")
        return

    try:
        transcript_data = extract_transcript_data(path)

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
            }
        }

        # Tentukan profil, MBTI, dan skill
        mata_kuliah = output_data["Nilai Mata Kuliah"]
        output_data["Profil Lulusan"] = tentukan_profil(mata_kuliah)

        print("\n🧠 Jawab beberapa pertanyaan untuk menentukan MBTI Anda...")
        mbti = mbti_test()
        output_data["MBTI"] = mbti

        output_data["Skill"]["Hard Skill"] = tentukan_hard_skill(mata_kuliah)
        output_data["Skill"]["Soft Skill"] = tentukan_soft_skill(mbti)

        tampilkan_hasil(output_data)
        simpan_data(output_data)

    except Exception as e:
        print(f"\n❗ Terjadi kesalahan: {str(e)}")

def main():
    while True:
        show_menu()
        choice = input("Masukkan pilihan Anda (1/2/3): ").strip()
        if choice == "1":
            run_analysis()
        elif choice == "2":
            update_skills()
        elif choice == "3":
            print("👋 Terima kasih telah menggunakan aplikasi ini. Sampai jumpa!")
            break
        else:
            print("❗ Pilihan tidak valid. Silakan coba lagi.\n")

if __name__ == "__main__":
    main()
