import json

def load_job_data(filepath="Json/JobData.json"):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"❗ File {filepath} tidak ditemukan.")
        return None
    except json.JSONDecodeError as e:
        print(f"❗ Format JSON salah di {filepath}: {e}")
        return None

def rekomendasi_pekerjaan(user_profile, hard_skills_user, soft_skills_user=None, filepath="Json/JobData.json"):
    data = load_job_data(filepath)
    if not data:
        return []

    hasil_rekomendasi = []

    for profil in data.get("job_data", []):
        if profil["profil"].lower() != user_profile.lower():
            continue

        for role in profil.get("roles", []):
            role_name = role.get("role_name", "")
            hard_skills_role = set(role.get("hard_skills", []))
            soft_skills_role = set(role.get("soft_skills", []))

            matched_hard = set(hard_skills_user).intersection(hard_skills_role)
            matched_soft = set(soft_skills_user or []).intersection(soft_skills_role)

            hard_match = (len(matched_hard) / len(hard_skills_role)) * 100 if hard_skills_role else 0
            soft_match = (len(matched_soft) / len(soft_skills_role)) * 100 if soft_skills_role else 0

            total_match = (hard_match + soft_match) / 2 if soft_skills_role else hard_match

            hasil_rekomendasi.append({
                "role_name": role_name,
                "hard_skill_match": round(hard_match, 2),
                "soft_skill_match": round(soft_match, 2),
                "total_match": round(total_match, 2),
                "matched_hard_skills": list(matched_hard),
                "matched_soft_skills": list(matched_soft)
            })

    hasil_rekomendasi.sort(key=lambda x: x["total_match"], reverse=True)
    return hasil_rekomendasi

def rekomendasi_pekerjaan_by_nim(nim, mahasiswa_data_path="Json/hasil_nilai_mahasiswa.json", jobdata_path="Json/JobData.json"):
    try:
        with open(mahasiswa_data_path, "r", encoding="utf-8") as f:
            semua_data = json.load(f)
            
    except FileNotFoundError:
        print(f"❗ File {mahasiswa_data_path} tidak ditemukan.")
        return []
    except json.JSONDecodeError:
        print(f"❗ File {mahasiswa_data_path} mengandung format JSON tidak valid.")
        return []

    mahasiswa = next((m for m in semua_data if m["NIM"] == nim), None)

    if not mahasiswa:
        print(f"❗ Data untuk NIM {nim} tidak ditemukan.")
        return []

    profil = mahasiswa.get("Profil Lulusan", "")
    hard_skills = mahasiswa.get("Skill", {}).get("Hard Skill", [])
    soft_skills = mahasiswa.get("Skill", {}).get("Soft Skill", [])

    hasil = rekomendasi_pekerjaan(profil, hard_skills, soft_skills, filepath=jobdata_path)

    if not hasil:
        print("⚠️ Tidak ditemukan pekerjaan yang cocok.")
    else:
        print(f"\n💼 Rekomendasi Pekerjaan untuk {mahasiswa['Nama']} (NIM {nim}):\n")
        for i, item in enumerate(hasil, 1):
            print(f"{i}. Role: {item['role_name']}")
            print(f"   Total Match: {item['total_match']}%")
            print(f"   Hard Skill Match: {item['hard_skill_match']}%")
            print(f"   Soft Skill Match: {item['soft_skill_match']}%")
            print(f"   Matched Hard Skills: {', '.join(item['matched_hard_skills']) or '-'}")
            print(f"   Matched Soft Skills: {', '.join(item['matched_soft_skills']) or '-'}")
            print()

    return hasil
