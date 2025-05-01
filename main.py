from pdfread import *
from TestMBTI import *
from CariProfil import *

def main():
    print("hai selamat datang")
    print("apakah tau mbti anda?")
    print("masukan daftar nilai ke folder DaftarNilai")
    nim = input("masukan nim anda\n")
    try:
        transcript_data = extract_transcript_data(f"DaftarNilai/daftarnilai{nim}.pdf")

        output_data = {
            "NIM" : transcript_data["nim"],
            "Nama": transcript_data["nama"] or "Unknown",
            "MBTI": " ",
            "IPK": transcript_data["ipk"],
            "Prodi" : transcript_data["program_studi"],
            "Profil Lulusan": " ",
            "Nilai Mata Kuliah": {
                mk["nama"]: mk["nilai"]
                for mk in transcript_data["mata_kuliah"]
            }
        }

        mata_kuliah = output_data.get("Nilai Mata Kuliah", {})
        profil = tentukan_profil(mata_kuliah)
        output_data["Profil Lulusan"] = profil
        output_data["MBTI"] = mbti_test()

        with open("Json/hasil_nilai_mahasiswa.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
        
        

        print(f"✅ Berhasil! File JSON disimpan di Json/hasil_nilai_mahasiswa.json")

    except Exception as e:
        print(f"❌ Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    main()