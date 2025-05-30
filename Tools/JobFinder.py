def tentukan_job(mbti, skill):
    with open("Json/JobData.json", "r") as f:
        data = json.load(f)

    for job in data:
        percentage_skill = 0
        for skill in job["skills"]:
            if skill in skill:
                percentage_skill += 1
            if Soft
        if percentage_skill >= 50:
            return job["job"]

    return None

