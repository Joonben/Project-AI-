import os
import json

def update_skills():
    path = "Json/hasil_nilai_mahasiswa.json"
    if not os.path.exists(path):
        print("❗ File hasil analisis belum tersedia. Jalankan analisis terlebih dahulu.")
        return

    with open("Json/hasil_nilai_mahasiswa.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Cetak data utama
    for key in data:
        if key == "Nilai Mata Kuliah":
            print("\n📘 Nilai Mata Kuliah:")
            for nama_mk, nilai in data[key].items():
                print(f"  - {nama_mk}: {nilai}")
        elif key == "Skill":
            print("\n💼 Hard Skills:")
            for idx, skill in enumerate(data[key]["Hard Skill"], 1):
                print(f"  {idx}. {skill}")

            print("\n🤝 Soft Skills:")
            for idx, skill in enumerate(data[key]["Soft Skill"], 1):
                print(f"  {idx}. {skill}")
        else:
            print(f"{key}: {data[key]}")

    print("🛠️  Perbarui Data Skill")
    print("1. Edit Hard Skill")
    print("2. Tambah Soft Skill")
    print("3. Selesai")

    while True:
        choice = input("Masukkan pilihan (1/2/3): ").strip()
        if choice == "1":
            new_skill = input("Masukkan hard skill baru: ").strip()
            if new_skill:
                data["Skill"]["Hard Skill"].append(new_skill)
                print("✅ Hard skill ditambahkan.")
        elif choice == "2":
            new_skill = input("Masukkan soft skill baru: ").strip()
            if new_skill:
                data["Skill"]["Soft Skill"].append(new_skill)
                print("✅ Soft skill ditambahkan.")
        elif choice == "3":
            break
        else:
            print("❗ Pilihan tidak valid.")

    simpan_data(data)