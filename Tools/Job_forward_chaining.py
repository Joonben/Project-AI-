import json

def load_JobData(file_path="Json/job.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"❗ File {file_path} tidak ditemukan.")
        return None
    except json.JSONDecodeError as e:
        print(f"❗ Kesalahan format JSON di file {file_path}: {e}")
        return None

def forward_chaining_rekomendasi(user_skills):
    user_skills = set(skill.lower() for skill in user_skills)
    JobData = load_JobData()

    bidang_keywords = get_bidang_keywords()
    bidang_to_jobs = JobData.get("Bidang", {})

    hasil = {}
    for bidang, keywords in bidang_keywords.items():
        matched_skills = user_skills.intersection(keywords)
        percentage = (len(matched_skills) / len(keywords) * 100) if keywords else 0
        if percentage > 0:
            hasil[bidang] = {
                "percentage": percentage,
                "recommended_jobs": bidang_to_jobs.get(bidang, [])
            }
    # Urutkan berdasarkan percentage tertinggi
    return sorted(hasil.items(), key=lambda x: x[1]["percentage"], reverse=True)
