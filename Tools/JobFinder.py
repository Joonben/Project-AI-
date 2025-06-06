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

def rekomendasi_pekerjaan_forward_chaining(user_profile_category, user_hard_skills, user_soft_skills=None, job_data_filepath="Json/JobData.json"):
    job_knowledge_base = load_job_data(job_data_filepath)
    if not job_knowledge_base:
        return []

    potential_candidate_roles = []
    for profile_data in job_knowledge_base.get("job_data", []):
        if profile_data.get("profil", "").lower() == user_profile_category.lower():
            potential_candidate_roles.extend(profile_data.get("roles", []))
            break

    if not potential_candidate_roles:
        print(f"⚠️ Tidak ada kategori pekerjaan yang cocok dengan profil '{user_profile_category}'.")
        return []

    derived_recommendations = []

    for role_definition in potential_candidate_roles:
        role_name = role_definition.get("role_name", "Nama Peran Tidak Diketahui")
        required_hard_skills = set(role_definition.get("hard_skills", []))
        required_soft_skills = set(role_definition.get("soft_skills", []))

        user_hard_skills_set = set(user_hard_skills)
        matched_hard_skills_set = user_hard_skills_set.intersection(required_hard_skills)
        
        hard_skill_match_percentage = 0
        if required_hard_skills:
            hard_skill_match_percentage = (len(matched_hard_skills_set) / len(required_hard_skills)) * 100
        elif not required_hard_skills: 
             hard_skill_match_percentage = 100

        soft_skill_match_percentage = 0
        matched_soft_skills_set = set()
        if user_soft_skills:
            user_soft_skills_set = set(user_soft_skills)
            matched_soft_skills_set = user_soft_skills_set.intersection(required_soft_skills)
            if required_soft_skills:
                soft_skill_match_percentage = (len(matched_soft_skills_set) / len(required_soft_skills)) * 100
            elif not required_soft_skills:
                soft_skill_match_percentage = 100
        elif not user_soft_skills and not required_soft_skills:
            soft_skill_match_percentage = 100
        
        current_total_match_score = hard_skill_match_percentage
        if user_soft_skills and required_soft_skills:
             current_total_match_score = (hard_skill_match_percentage + soft_skill_match_percentage) / 2
        elif not user_soft_skills and required_soft_skills:
            current_total_match_score = (hard_skill_match_percentage + 0) / 2
        elif user_soft_skills and not required_soft_skills:
            current_total_match_score = (hard_skill_match_percentage + soft_skill_match_percentage) / 2


        derived_recommendations.append({
            "role_name": role_name,
            "hard_skill_match": round(hard_skill_match_percentage, 2),
            "soft_skill_match": round(soft_skill_match_percentage if user_soft_skills else 0.0, 2),
            "total_match": round(current_total_match_score, 2),
            "matched_hard_skills": list(matched_hard_skills_set),
            "matched_soft_skills": list(matched_soft_skills_set) if user_soft_skills else []
        })
    
    derived_recommendations.sort(key=lambda item: item["total_match"], reverse=True)
    
    return derived_recommendations

import json

def rekomendasi_pekerjaan_by_nim_fc(nim, mahasiswa_data_path="Json/hasil_nilai_mahasiswa.json", jobdata_path="Json/JobData.json"):
    try:
        with open(mahasiswa_data_path, "r", encoding="utf-8") as f:
            semua_data_mahasiswa = json.load(f)
    except FileNotFoundError:
        print(f"❗ File {mahasiswa_data_path} tidak ditemukan.")
        return []
    except json.JSONDecodeError:
        print(f"❗ File {mahasiswa_data_path} mengandung format JSON tidak valid.")
        return []

    mahasiswa_found = None
    idx_found = None
    for idx, m_data in enumerate(semua_data_mahasiswa):
        if m_data.get("NIM") == nim:
            mahasiswa_found = m_data
            idx_found = idx
            break

    if not mahasiswa_found:
        print(f"❗ Data untuk NIM {nim} tidak ditemukan.")
        return []

    user_profile = mahasiswa_found.get("Profil Lulusan", "")
    user_hard_skills = []
    user_soft_skills = []

    if "Skill" in mahasiswa_found:
        user_hard_skills = mahasiswa_found["Skill"].get("Hard Skill", [])
        user_soft_skills = mahasiswa_found["Skill"].get("Soft Skill", [])

    if not user_profile:
        print(f"⚠️ Profil lulusan untuk NIM {nim} tidak ditemukan. Tidak dapat memberikan rekomendasi.")
        return []

    hasil_rekomendasi = rekomendasi_pekerjaan_forward_chaining(
        user_profile,
        user_hard_skills,
        user_soft_skills if user_soft_skills else None,
        job_data_filepath=jobdata_path
    )

    if not hasil_rekomendasi:
        print(f"\n⚠️  Tidak ditemukan pekerjaan yang cocok untuk:")
        print(f"   Nama: {mahasiswa_found.get('Nama', 'Mahasiswa')}")
        print(f"   NIM: {nim}")
        print(f"   Profil: '{user_profile}'")
    else:
        print(f"\n✨ {' REKOMENDASI PEKERJAAN ':=^60} ✨")
        print(f"\n🎓 Profil Kandidat:")
        print(f"   ├─ Nama: {mahasiswa_found.get('Nama', 'Mahasiswa')}")
        print(f"   ├─ NIM: {nim}")
        print(f"   └─ Profil: '{user_profile}'\n")

        print("🔍 Hasil Rekomendasi:\n")
        for i, item in enumerate(hasil_rekomendasi):
            print(f"🏆 {i+1}. {item['role_name'].upper()}")
            print(f"   📊 Total Kecocokan: {item['total_match']}%")
            print(f"   ⚙️  Hard Skill Match: {item['hard_skill_match']}%")
            print(f"   💬 Soft Skill Match: {item['soft_skill_match']}%")

            matched_hard = item.get('matched_hard_skills', [])
            print(f"\n   🔧 Hard Skills yang Cocok:")
            print(f"      {', '.join(matched_hard) if matched_hard else 'Tidak ada'}")

            matched_soft = item.get('matched_soft_skills', [])
            print(f"\n   🌟 Soft Skills yang Cocok:")
            print(f"      {', '.join(matched_soft) if matched_soft else 'Tidak ada'}")

            print("\n" + "─" * 60 + "\n")

        # Ambil rekomendasi paling cocok (indeks 0 karena sudah diurutkan)
        rekom_terbaik = hasil_rekomendasi[0]
        job_info = {
            "Cocok": {
                "Role": rekom_terbaik.get("role_name", "Tidak Diketahui"),
                "Hard Skill Match (%)": rekom_terbaik.get("hard_skill_match", 0),
                "Soft Skill Match (%)": rekom_terbaik.get("soft_skill_match", 0)
            }
        }

        # Tambahkan ke data mahasiswa
        semua_data_mahasiswa[idx_found]["Job"] = job_info

        # Simpan kembali ke file
        try:
            with open(mahasiswa_data_path, "w", encoding="utf-8") as f:
                json.dump(semua_data_mahasiswa, f, indent=4, ensure_ascii=False)
            print(f"✅ Rekomendasi pekerjaan terbaik berhasil disimpan ke dalam data mahasiswa (NIM: {nim}).")
        except Exception as e:
            print(f"❗ Gagal menyimpan data rekomendasi ke file: {e}")

    return hasil_rekomendasi
