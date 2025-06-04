import os
import json
from menu import *
from tabulate import tabulate  # pip install tabulate

def simpan_data(data, path="Json/hasil_nilai_mahasiswa.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("💾 Data mahasiswa berhasil disimpan.")

def simpan_skill_master(skill_master, path="Json/skill_master.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(skill_master, f, indent=4, ensure_ascii=False)
    print("💾 Skill master berhasil diperbarui.")

def tampilkan_skill_table(hard_skills, soft_skills, judul="SKILLS"):
    max_len = max(len(hard_skills), len(soft_skills))
    hard_skills += [""] * (max_len - len(hard_skills))
    soft_skills += [""] * (max_len - len(soft_skills))
    table = list(zip(range(1, max_len + 1), hard_skills, soft_skills))
    headers = ["No", "Hard Skill", "Soft Skill"]
    print(f"\n📋 {judul}")
    print(tabulate(table, headers=headers, tablefmt="grid"))

def update_skills(nim):
    tampilkan_data_nim(nim)

    mahasiswa_path = "Json/hasil_nilai_mahasiswa.json"
    master_path = "Json/skill.json"

    if not os.path.exists(mahasiswa_path) or not os.path.exists(master_path):
        print("❗ File data tidak lengkap.")
        return

    # Load data
    with open(mahasiswa_path, "r", encoding="utf-8") as f:
        semua_data = json.load(f)
    with open(master_path, "r", encoding="utf-8") as f:
        skill_master = json.load(f)

    indeks = next((i for i, m in enumerate(semua_data) if m.get("NIM") == nim), None)
    if indeks is None:
        print(f"❗ Data NIM {nim} tidak ditemukan.")
        return
    data = semua_data[indeks]

    while True:
        print("\n🛠️  Menu Update Skill")
        print("1. Tampilkan Semua Skill Dimiliki")
        print("2. Tambah Skill")
        print("3. Hapus Skill")
        print("4. Selesai")

        choice = input("Pilihan (1-4): ").strip()

        if choice == "1":
            tampilkan_skill_table(data["Skill"]["Hard Skill"], data["Skill"]["Soft Skill"], "SKILL DIMILIKI")

        elif choice == "2":
            owned_hard = set(data["Skill"]["Hard Skill"])
            owned_soft = set(data["Skill"]["Soft Skill"])

            available_hard = [s for s in skill_master["hard_skills"] if s not in owned_hard]
            available_soft = [s for s in skill_master["soft_skills"] if s not in owned_soft]

            tampilkan_skill_table(available_hard, available_soft, "TAMBAH SKILL (YANG BELUM DIMILIKI)")

            jenis = input("Tambah ke (hard/soft): ").strip().lower()
            if jenis not in ["hard", "soft"]:
                print("❗ Jenis tidak valid.")
                continue

            skill = input("Masukkan nama skill atau nomor dari tabel: ").strip()
            try:
                idx = int(skill) - 1
                selected = available_hard[idx] if jenis == "hard" else available_soft[idx]
            except:
                selected = skill.strip()

            if jenis == "hard":
                if selected not in skill_master["hard_skills"]:
                    konfirmasi = input(f"Skill baru '{selected}' belum di master. Tambahkan? (y/n): ").lower()
                    if konfirmasi == "y":
                        skill_master["hard_skills"].append(selected)
                        simpan_skill_master(skill_master)
                if selected not in owned_hard:
                    data["Skill"]["Hard Skill"].append(selected)
                    print("✅ Hard skill ditambahkan.")
                else:
                    print("⚠️ Sudah dimiliki.")
            else:
                if selected not in skill_master["soft_skills"]:
                    konfirmasi = input(f"Skill baru '{selected}' belum di master. Tambahkan? (y/n): ").lower()
                    if konfirmasi == "y":
                        skill_master["soft_skills"].append(selected)
                        simpan_skill_master(skill_master)
                if selected not in owned_soft:
                    data["Skill"]["Soft Skill"].append(selected)
                    print("✅ Soft skill ditambahkan.")
                else:
                    print("⚠️ Sudah dimiliki.")

        elif choice == "3":
            hard = data["Skill"]["Hard Skill"]
            soft = data["Skill"]["Soft Skill"]

            tampilkan_skill_table(hard, soft, "HAPUS SKILL")

            jenis = input("Hapus dari (hard/soft): ").strip().lower()
            if jenis not in ["hard", "soft"]:
                print("❗ Jenis tidak valid.")
                continue

            daftar = hard if jenis == "hard" else soft
            if not daftar:
                print(f"❗ Tidak ada {jenis} skill yang bisa dihapus.")
                continue

            no = input("Masukkan nomor skill yang ingin dihapus: ").strip()
            if not no.isdigit() or not (1 <= int(no) <= len(daftar)):
                print("❗ Nomor tidak valid.")
                continue

            removed = daftar.pop(int(no) - 1)
            print(f"🗑️ Skill '{removed}' berhasil dihapus.")

        elif choice == "4":
            break

        else:
            print("❗ Pilihan tidak valid.")

    semua_data[indeks] = data
    simpan_data(semua_data)
