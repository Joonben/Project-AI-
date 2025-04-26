from pdfread import *
from TestMBTI import *
def main():
    try:
        # Step 1: Extract from PDF
        transcript_data = extract_transcript_data(Config.INPUT_PDF)

        # Step 2: Format for JSON output
        output_data = [{
            "NIM" : transcript_data["nim"],
            "Nama": transcript_data["nama"] or "Unknown",
            "MBTI": " ",
            "IPK": transcript_data["ipk"],
            "Prodi" : transcript_data["program_studi"],
            # "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Profil Lulusan": " ",
            "Nilai Mata Kuliah": {
                mk["nama"]: mk["nilai"]
                for mk in transcript_data["mata_kuliah"]
            }
        }]

        # Step 3: Save to JSON
        with open(Config.OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)

        # Step 4: Generate PDF output

        print(f"✅ Berhasil! File JSON disimpan di '{Config.OUTPUT_JSON}'")

    except Exception as e:
        print(f"❌ Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    main()