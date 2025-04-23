import json
import pdfplumber

def information_parser(text):
    possible_scores = [
        "A", "A-",
        "B+", "B", "B-",
        "C+","C" ,"C-",
        "D", "E"
    ]

    possible_matkul = {}
    with open("Matkul.json", "r") as f:
        possible_matkul = json.load(f)["mata_kuliah"]

    splittan = text.split()
    end_indices = []

    for i in range(len(splittan)):
        possibly_sks = splittan[i]
        if possibly_sks not in "1234567890":
            continue
        possibly_score = splittan[i+1]
        if possibly_score in possible_scores:
            end_indices.append(i+1)

    informations = []
    start_index = 0
    for i in end_indices:
        information = splittan[start_index:i+1]
        nama = " ".join(splittan[2+start_index:i+1-2])
        norm_info = {
            "no": information[0],
            "kode": information[1],
            "nama": nama,
            "nilai": information[-1],
            "sks": information[-2],
        }
        start_index = i + 1
        if (not norm_info["no"].isnumeric()):
            continue
        informations.append(norm_info)


    return informations

def parse_krs(text):
    informations = []
    texts = text.split("\n")
    for text in texts:
        try:
            info = information_parser(text)
            informations += info
        except:
            continue
    informations = sorted(informations, key=lambda x : int(x['no']))
    return informations

