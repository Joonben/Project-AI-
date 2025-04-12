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

def main():
    print("Tes Kepribadian MBTI Sederhana")
    print("Pilih salah satu jawaban yang paling sesuai dengan Anda.\n")

    # Dimensi
    EI = 0  # +1 untuk E, -1 untuk I
    SN = 0  # +1 untuk N, -1 untuk S
    TF = 0  # +1 untuk F, -1 untuk T
    JP = 0  # +1 untuk P, -1 untuk J

    # Pertanyaan per dimensi (2 per dimensi agar simpel)
    EI += 1 if ask_question("Saya mendapatkan energi dari:", "Berinteraksi dengan banyak orang", "Menyendiri dan refleksi pribadi") == 'A' else -1
    EI += 1 if ask_question("Saya lebih suka:", "Diskusi kelompok", "Menulis dan merenung sendiri") == 'A' else -1

    SN += 1 if ask_question("Saya lebih percaya pada:", "Pengalaman nyata dan fakta", "Ide dan kemungkinan masa depan") == 'B' else -1
    SN += 1 if ask_question("Saya memproses informasi dengan:", "Langsung dan praktis", "Intuitif dan konseptual") == 'B' else -1

    TF += 1 if ask_question("Saya mengambil keputusan berdasarkan:", "Perasaan dan hubungan", "Logika dan analisis") == 'A' else -1
    TF += 1 if ask_question("Yang penting bagi saya:", "Keadilan dan logika", "Empati dan kasih sayang") == 'B' else -1

    JP += 1 if ask_question("Saya lebih suka gaya hidup yang:", "Terjadwal dan teratur", "Fleksibel dan spontan") == 'B' else -1
    JP += 1 if ask_question("Saya nyaman dengan:", "Keputusan yang sudah dibuat", "Pilihan yang masih terbuka") == 'B' else -1

    # Menentukan tipe MBTI
    tipe = ""
    tipe += "E" if EI > 0 else "I"
    tipe += "N" if SN > 0 else "S"
    tipe += "F" if TF > 0 else "T"
    tipe += "P" if JP > 0 else "J"

    print(f"\nTipe Kepribadian Anda berdasarkan tes ini adalah: {tipe}")

if __name__ == "__main__":
    main()
