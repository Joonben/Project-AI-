from Tools.pdfread import *
from Tools.TestMBTI import *
from Tools.CariProfil import *
from Tools.SkillsFinder import *
from Tools.UpdateSkills import *
import json
import os

def show_menu():
    print("=" * 50)
    print("SELAMAT DATANG DI APLIKASI ANALISIS PROFIL MAHASISWA")
    print("=" * 50)
    print("Silakan pilih opsi berikut:")
    print("1. Cek Profil, MBTI, dan Skill berdasarkan Daftar Nilai")
    print("2. Perbarui Hard/Soft Skill Secara Manual")
    print("3. Tampilkan Semua Data Mahasiswa")
    print("4. Tampilkan Data Berdasarkan NIM")
    print("5. Keluar")
    print("=" * 50)

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

def tampilkan_data_nim(path="Json/hasil_nilai_mahasiswa.json"):
    nim = input("Masukkan NIM yang ingin dicari: ").strip()
    
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
        output_data["Job"] = tentukan_job(mbti, output_data["Skill"]["Hard Skill"])
        

        tampilkan_hasil(output_data)
        simpan_data(output_data)

    except Exception as e:
        print(f"\n❗ Terjadi kesalahan: {str(e)}")

def main():
    while True:
        show_menu()
        choice = input("Masukkan pilihan Anda (1/2/3/4/5): ").strip()
        if choice == "1":
            run_analysis()
        elif choice == "2":
            update_skills()
        elif choice == "3":
            tampilkan_semua_data()
        elif choice == "4":
            tampilkan_data_nim()
        elif choice == "5":
            print("👋 Terima kasih telah menggunakan aplikasi ini. Sampai jumpa!")
            break
        else:
            print("❗ Pilihan tidak valid. Silakan coba lagi.\n")

if __name__ == "__main__":
    main()
