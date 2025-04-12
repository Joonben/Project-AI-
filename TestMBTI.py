import json
import os
from datetime import datetime

MBTI_TYPES = {
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
}

def ask_question(question, option1, option2):
    print(f"\n{question}")
    print(f"A. {option1}")
    print(f"B. {option2}")
    while True:
        answer = input("Jawaban Anda (A/B): ").strip().upper()
        if answer in ['A', 'B']:
            return answer
        else:
            print("Masukkan hanya A atau B.")

def save_result(name, mbti_type):
    # Pastikan folder ada
    os.makedirs("Project", exist_ok=True)

    filename = "Project/Data.json"
    result = {
        "nama": name,
        "mbti": mbti_type,
        "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # Overwrite jika nama sama
    data = [item for item in data if item["nama"].lower() != name.lower()]
    data.append(result)

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print("\n💾 Data Anda berhasil disimpan (overwrite jika ada).")

def main():
    print("=== Tes Kepribadian MBTI Sederhana ===")
    name = input("Masukkan nama Anda: ").strip()

    tahu_mbti = input("Apakah Anda sudah mengetahui tipe MBTI Anda? (y/n): ").strip().lower()

    if tahu_mbti == "y":
        while True:
            mbti = input("Masukkan tipe MBTI Anda (contoh: INFP, ESTJ): ").strip().upper()
            if mbti in MBTI_TYPES:
                break
            print("❌ Tipe MBTI tidak valid. Coba lagi.")
        print(f"\n🧠 Tipe Kepribadian Anda adalah: {mbti}")
        save_result(name, mbti)
        return

    print("\nSilakan jawab beberapa pertanyaan berikut untuk menentukan MBTI Anda.\n")

    # Skor dimensi
    EI = SN = TF = JP = 0

    # Pertanyaan EI
    EI += 1 if ask_question("Saya mendapatkan energi dari:", "Berinteraksi dengan banyak orang", "Menyendiri dan refleksi pribadi") == 'A' else -1
    EI += 1 if ask_question("Saya lebih suka:", "Diskusi kelompok", "Menulis dan merenung sendiri") == 'A' else -1

    # Pertanyaan SN
    SN += 1 if ask_question("Saya lebih percaya pada:", "Pengalaman nyata dan fakta", "Ide dan kemungkinan masa depan") == 'B' else -1
    SN += 1 if ask_question("Saya memproses informasi dengan:", "Langsung dan praktis", "Intuitif dan konseptual") == 'B' else -1

    # Pertanyaan TF
    TF += 1 if ask_question("Saya mengambil keputusan berdasarkan:", "Perasaan dan hubungan", "Logika dan analisis") == 'A' else -1
    TF += 1 if ask_question("Yang penting bagi saya:", "Keadilan dan logika", "Empati dan kasih sayang") == 'B' else -1

    # Pertanyaan JP
    JP += 1 if ask_question("Saya lebih suka gaya hidup yang:", "Terjadwal dan teratur", "Fleksibel dan spontan") == 'B' else -1
    JP += 1 if ask_question("Saya nyaman dengan:", "Keputusan yang sudah dibuat", "Pilihan yang masih terbuka") == 'B' else -1

    # Menentukan MBTI
    mbti = ("E" if EI > 0 else "I") + \
           ("N" if SN > 0 else "S") + \
           ("F" if TF > 0 else "T") + \
           ("P" if JP > 0 else "J")

    print(f"\n🧠 Tipe Kepribadian Anda berdasarkan tes ini adalah: {mbti}")
    save_result(name, mbti)

if __name__ == "__main__":
    main()
