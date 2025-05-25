# Baca isi teks dari PDF
        full_text = read_pdf_text(dest_path)  # pastikan fungsi ini sudah di-import
        # Dapatkan nama depan dari teks PDF
        nama = extract_first_name(full_text)
        # Update label dengan nama depan
        tk.Label(frame, text=f"Apakah {nama} sudah mengetahui MBTI Anda?", font=("Arial", 14)).pack(pady=20)
        btn_yes = tk.Button(frame, text="Ya", width=10, command=self.mbti_ya)
        btn_yes.pack(pady=5)
        btn_no = tk.Button(frame, text="Tidak", width=10, command=self.mbti_tidak)
        btn_no.pack(pady=5)
        btn_gantiNim = tk.Button(frame, text="Ganti NIM", width=10, command=lambda: self.show_frame(self.frame_input_nim))
        btn_gantiNim.pack(pady=5)

        return frame
        
    
        # Lanjut proses lain kalau perlu, misal baca transcript_data
        self.transcript_data = extract_transcript_data(dest_path)
        messagebox.showinfo("Sukses", "File PDF berhasil diupload dan dibaca.")
