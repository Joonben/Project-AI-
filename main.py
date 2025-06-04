from Tools.pdfread import *
from Tools.TestMBTI import *
from Tools.CariProfil import *
from Tools.SkillsFinder import *
from Tools.UpdateSkills import *
from Tools.JobFinder import *
from menu import *

import json
import os

def main():
    print("=" * 50)
    print("SELAMAT DATANG DI APLIKASI ANALISIS PROFIL MAHASISWA")
    print("=" * 50)
    print("")
    print("Pastikan Anda sudah memasukkan file daftar nilai ke folder `DaftarNilai/` terlebih dahulu.")
    nim = input("Silakan masukkan NIM Anda terlebih dahulu: ").strip()

    path_data = f"DaftarNilai/daftarnilai{nim}.pdf"

    # Cek apakah file PDF ada
    if not os.path.exists(path_data):
        print("❗ File data mahasiswa tidak ditemukan.")
        return

    # Load data mahasiswa yang sudah dianalisis
    semua_data = []
    if os.path.exists("Json/hasil_nilai_mahasiswa.json"):
        with open("Json/hasil_nilai_mahasiswa.json", "r", encoding="utf-8") as f:
            try:
                semua_data = json.load(f)
            except json.JSONDecodeError:
                print("❗ Gagal membaca data JSON.")
                return

    # Cek apakah NIM sudah dianalisis
    data_mahasiswa = next((m for m in semua_data if m["NIM"] == nim), None)
    if not data_mahasiswa:
        print("\n🔍 Data mahasiswa belum dianalisis. Memulai analisis otomatis...")
        run_analysis(nim)

        # Reload data setelah dianalisis
        with open("Json/hasil_nilai_mahasiswa.json", "r", encoding="utf-8") as f:
            semua_data = json.load(f)
            data_mahasiswa = next((m for m in semua_data if m["NIM"] == nim), None)

        if not data_mahasiswa:
            print("❗ Gagal menganalisis dan menyimpan data mahasiswa.")
            return

    clear_screen()
    print(f"✅ Selamat datang, {data_mahasiswa['Nama']} (NIM: {nim})!")

    while True:
        print("Silakan pilih opsi berikut:")
        print("1. Lihat Profil, MBTI, dan Skill berdasarkan Daftar Nilai")
        print("2. Update Skill (Hard/Soft Skill) Secara Manual")
        print("3. Cari Pekerjaan yang Cocok dan Tidak Cocok")
        print("4. Keluar")
        print("=" * 50)
        choice = input("Masukkan pilihan Anda (1/2/3/4): ").strip()

        if choice == "1":
            clear_screen()
            tampilkan_data_nim(nim)
        elif choice == "2":
            clear_screen()
            update_skills(nim)
        elif choice == "3":
            clear_screen()
            rekomendasi_pekerjaan_by_nim_fc(nim)
        elif choice == "4":
            print("👋 Terima kasih telah menggunakan aplikasi ini. Sampai jumpa!")
            break
        else:
            print("❗ Pilihan tidak valid. Silakan coba lagi.\n")

if __name__ == "__main__":
    clear_screen()
    main()