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
    for m_data in semua_data_mahasiswa:
        if m_data.get("NIM") == nim:
            mahasiswa_found = m_data
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
        print(f"⚠️ Tidak ditemukan pekerjaan yang cocok untuk {mahasiswa_found.get('Nama', 'Mahasiswa')} (NIM {nim}) dengan profil '{user_profile}'.")
    else:
        print(f"\n💼 Rekomendasi Pekerjaan untuk {mahasiswa_found.get('Nama', 'Mahasiswa')} (NIM {nim}) berdasarkan profil '{user_profile}':\n")
        for i, item in enumerate(hasil_rekomendasi):
            print(f"{i+1}. Role: {item['role_name']}")
            print(f"   Total Match: {item['total_match']}%")
            print(f"   Hard Skill Match: {item['hard_skill_match']}%")
            print(f"   Soft Skill Match: {item['soft_skill_match']}%")
            
            matched_hard = item.get('matched_hard_skills', [])
            print(f"   Matched Hard Skills: {', '.join(matched_hard) if matched_hard else '-'}")
                
            matched_soft = item.get('matched_soft_skills', [])
            print(f"   Matched Soft Skills: {', '.join(matched_soft) if matched_soft else '-'}")
            print()

    return hasil_rekomendasi

if __name__ == "__main__":
    print("--- Contoh Rekomendasi Langsung ---")
    my_profile = "Artificial Intelligence"
    my_hard_skills = ["Python", "Machine Learning", "SQL", "AWS", "Docker"]
    my_soft_skills = ["Problem Solving", "Analytical Thinking", "Team Collaboration", "Curiosity & Willingness to Learn"]
    
    recommendations = rekomendasi_pekerjaan_forward_chaining(my_profile, my_hard_skills, my_soft_skills, job_data_filepath="Json/JobData.json")
    
    if recommendations:
        print(f"\nTop Rekomendasi untuk profil '{my_profile}':\n")
        for i, rec in enumerate(recommendations[:5]): 
            print(f"{i+1}. {rec['role_name']} - Total Match: {rec['total_match']}%")
            print(f"   Hard Skills Matched: {', '.join(rec['matched_hard_skills']) if rec['matched_hard_skills'] else '-'}")
            print(f"   Soft Skills Matched: {', '.join(rec['matched_soft_skills']) if rec['matched_soft_skills'] else '-'}")
            print("-" * 20)
    else:
        print("Tidak ada rekomendasi yang ditemukan.")

    print("\n" + "="*50 + "\n")

    # contoh_mahasiswa_data = [
    #     {
    #         "NIM": "12345",
    #         "Nama": "Budi Santoso",
    #         "Profil Lulusan": "Artificial Intelligence",
    #         "Skill": {
    #             "Hard Skill": ["Python", "TensorFlow", "SQL", "Data Analysis", "Git"],
    #             "Soft Skill": ["Critical Thinking", "Problem Solving", "Adaptability"]
    #         }
    #     },
    #     {
    #         "NIM": "67890",
    #         "Nama": "Citra Lestari",
    #         "Profil Lulusan": "UI/UX",
    #         "Skill": {
    #             "Hard Skill": ["HTML", "CSS", "Data Visualization"],
    #             "Soft Skill": ["Communication Skills", "Attention to Detail", "Team Collaboration"]
    #         }
    #     },
    #     {
    #         "NIM": "11223", 
    #         "Nama": "Eka Putra",
    #         "Profil Lulusan": "Database",
    #         "Skill": {
    #             "Hard Skill": ["SQL", "MySQL", "Troubleshooting", "Python"]
    #         }
    #     }
    # ]
    # with open("Json/hasil_nilai_mahasiswa.json", "w") as f:
    #    json.dump(contoh_mahasiswa_data, f, indent=2)

    print("--- Contoh Rekomendasi by NIM ---")
    rekomendasi_pekerjaan_by_nim_fc("71210683", jobdata_path="Json/JobData.json", mahasiswa_data_path="Json/hasil_nilai_mahasiswa.json")
    print("\n" + "-"*50 + "\n")
    rekomendasi_pekerjaan_by_nim_fc("712", jobdata_path="Json/JobData.json", mahasiswa_data_path="Json/hasil_nilai_mahasiswa.json")
    print("\n" + "-"*50 + "\n")
    rekomendasi_pekerjaan_by_nim_fc("11223", jobdata_path="Json/JobData.json", mahasiswa_data_path="Json/hasil_nilai_mahasiswa.json") 
    print("\n" + "-"*50 + "\n")
    rekomendasi_pekerjaan_by_nim_fc("00000", jobdata_path="Json/JobData.json", mahasiswa_data_path="Json/hasil_nilai_mahasiswa.json")