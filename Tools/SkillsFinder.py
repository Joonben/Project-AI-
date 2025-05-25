import json

def tentukan_hard_skill(mata_kuliah):
    with open("Json/Matkul.json", "r") as f:
        mapping = json.load(f)["mata_kuliah"]
        ambang = ["A", "A-"]
        hard_skills = set()

        for matkul, nilai in mata_kuliah.items():
            if nilai in ambang:
                skills = mapping.get(matkul, [])
                hard_skills.update(skills)

    return sorted(hard_skills)

def tentukan_soft_skill(mbti):
    try:
        with open("Json/MBTI.json", "r", encoding="utf-8") as f:
            mapping = json.load(f).get("mbti", {})
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ Gagal membuka atau membaca file MBTI.json")
        return []

    soft_skills = mapping.get(mbti.upper(), [])
    return sorted(soft_skills)
