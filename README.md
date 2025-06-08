Project-AI: Sistem Rekomendasi Pekerjaan untuk Alumni

Proyek ini dikembangkan sebagai bagian dari tugas mata kuliah **Kecerdasan Buatan**. Sistem ini menganalisis data mahasiswa dan memberikan **saran pekerjaan yang relevan** berdasarkan pengetahuan yang telah dimodelkan menggunakan teknik **representasi pengetahuan** dan algoritma **forward chaining**.

---

## 📌 Deskripsi Singkat

Sistem ini bertujuan untuk membantu **alumni atau mahasiswa akhir** dalam menemukan pekerjaan yang sesuai berdasarkan nilai, keterampilan, dan sifat mereka. Pendekatan yang digunakan berbasis *rule-based system*.

---

## 🧠 Komponen AI

- **Representasi Pengetahuan**: Menggunakan file `hasil_nilai_mahasiswa.json`, yang berisi informasi nilai, keterampilan, dan profil mahasiswa.
- **Inferensi (Penalaran)**: Menggunakan metode **Forward Chaining** untuk mencocokkan data mahasiswa dengan aturan pekerjaan.
- **Analisis Output**: Sistem akan memberikan rekomendasi pekerjaan yang cocok, disimpan atau ditampilkan melalui *console* atau antarmuka sederhana.

---

## 🗂 Struktur Proyek



Project-AI/
│
├── main.py                      # Script utama sistem inferensi
├── hasil\_nilai\_mahasiswa.json  # Basis data pengetahuan (profil mahasiswa)
├── jobfinder/                  # Direktori pengujian sistem (data kasus uji)
│   ├── mahasiswa1.json
│   ├── mahasiswa2.json
│   └── ...
├── rules/                      # (Opsional) Aturan inference bisa dipisahkan
│   └── rules.json
├── README.md                   # Dokumentasi proyek

`

---

## ⚙ Cara Menjalankan

1. **Clone repository ini** atau buka folder proyek di IDE.
2. Pastikan sudah terinstall Python 3.x.
3. Jalankan program utama:

bash
python main.py
`

4. Sistem akan membaca data dari `hasil_nilai_mahasiswa.json` dan menampilkan hasil rekomendasi.

---

## 🧪 Data Pengujian

Data pengujian terdiri dari **6–8 mahasiswa** yang masing-masing memiliki profil:

* Nilai akhir
* Hard skill & soft skill
* Minat karier

Contoh data mahasiswa:

json
{
  "nama": "Budi",
  "nilai": 85,
  "hard_skills": ["Python", "Data Analysis"],
  "soft_skills": ["Komunikasi", "Problem Solving"],
  "minat": ["Data Scientist"]
}


---

## ✅ Output Sistem

Setelah sistem diproses, contoh output:


Mahasiswa: Budi
Saran Pekerjaan: Data Analyst, Junior Data Scientist
Alasan: Cocok dengan skill Python dan minat pada bidang Data


---

## 📚 Teknologi yang Digunakan

* Python 3.x
* Representasi Pengetahuan: JSON
* Algoritma Inferensi: Forward Chaining
* Editor: VS Code

---

## 🙋‍♂ Tim Pengembang

* Samuel Natanael
* Revaldo Hohary
* Jona Ruben Manalu

---

## 🏁 Status

✅ Versi awal telah selesai dan dapat dijalankan untuk analisis berbasis rule.

---

## 📌 Catatan Tambahan

* Sistem bisa dikembangkan lebih lanjut menggunakan antarmuka web/GUI.
* Data dan aturan bisa diperluas untuk mendukung lebih banyak jenis pekerjaan.



---

Kalau kamu ingin saya bantu membuat file rules.json atau main.py dengan forward chaining juga, tinggal beri tahu saja!
```
