import json

def tentukan_job(mbti, user_skills, user_soft_skills=None, filepath='Json/JobData.json'):
    # Muat data dari JSON
    data = load_JobData(filepath)

    # Pastikan kunci job_data ada
    JobData = data.get("JobData", [])
    if not JobData:
        raise ValueError("Kunci 'JobData' tidak ditemukan di dalam file JSON!")

    for profile in JobData:
        for role in profile.get("roles", []):
            hard_skills = role.get("hard_skills", [])
            soft_skills = role.get("soft_skills", [])

            # Hitung kecocokan hard skills
            matching_hard_skills = [skill for skill in hard_skills if skill in user_skills]
            hard_skill_match = (len(matching_hard_skills) / len(hard_skills)) * 100 if hard_skills else 0

            # Hitung kecocokan soft skills jika diberikan
            soft_skill_match = 0
            if user_soft_skills:
                matching_soft_skills = [skill for skill in soft_skills if skill in user_soft_skills]
                soft_skill_match = (len(matching_soft_skills) / len(soft_skills)) * 100 if soft_skills else 0

            # Tentukan jika kecocokan hard skills dan soft skills >= 50%
            if hard_skill_match >= 50 and (not soft_skills or soft_skill_match >= 50):
                return {
                    "profile": profile["profil"],
                    "role": role["role_name"],
                    "hard_skill_match": hard_skill_match,
                    "soft_skill_match": soft_skill_match
                }

    return {"profile": None, "role": None, "hard_skill_match": 0, "soft_skill_match": 0}
