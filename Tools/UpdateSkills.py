import os
import json
from menu import *

def update_skills(nim):
    tampilkan_data_nim(nim)
    path = "Json/hasil_nilai_mahasiswa.json"
    if not os.path.exists(path):
        print("❗ File hasil analisis belum tersedia. Jalankan analisis terlebih dahulu.")
        return

    # Load seluruh data mahasiswa
    with open(path, "r", encoding="utf-8") as f:
        try:
            semua_data = json.load(f)
            if not isinstance(semua_data, list):
                print("❗ Format data tidak valid.")
                return
        except json.JSONDecodeError:
            print("❗ File JSON rusak atau kosong.")
            return

    # Cari mahasiswa dengan NIM yang sesuai
    indeks = None
    for i, mahasiswa in enumerate(semua_data):
        if mahasiswa.get("NIM") == nim:
            indeks = i
            break

    if indeks is None:
        print(f"❗ Data dengan NIM {nim} tidak ditemukan.")
        return

    data = semua_data[indeks]

    # Menu update
    print("\n🛠️  Perbarui Data Skill")
    print("1. Edit Hard Skill")
    print("2. Edit Soft Skill")
    print("3. Selesai")

    while True:
        choice = input("Masukkan pilihan (1/2/3): ").strip()
        if choice == "1":
            new_skill = input("Masukkan hard skill baru: ").strip()
            if new_skill and new_skill not in data["Skill"]["Hard Skill"]:
                data["Skill"]["Hard Skill"].append(new_skill)
                print("✅ Hard skill ditambahkan.")
        elif choice == "2":
            new_skill = input("Masukkan soft skill baru: ").strip()
            if new_skill and new_skill not in data["Skill"]["Soft Skill"]:
                data["Skill"]["Soft Skill"].append(new_skill)
                print("✅ Soft skill ditambahkan.")
        elif choice == "3":
            break
        else:
            print("❗ Pilihan tidak valid.")

    # Simpan kembali ke semua_data dan file
    semua_data[indeks] = data
    simpan_data(semua_data)

def simpan_data(data, path="Json/hasil_nilai_mahasiswa.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("💾 Data berhasil disimpan ke file.")
