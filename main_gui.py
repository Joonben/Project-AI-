import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import json
import os
import io
import sys

# Asumsikan semua tools Anda ada di folder Tools dan bisa diimpor
# Jika ada error import, pastikan struktur folder dan PYTHONPATH benar
try:
    from Tools.pdfread import *
    from Tools.TestMBTI import *
    from Tools.CariProfil import *
    from Tools.SkillsFinder import *
    from Tools.UpdateSkills import *
    from Tools.JobFinder import *
except ImportError as e:
    messagebox.showerror("Import Error", f"Gagal mengimpor modul Tools: {e}\nPastikan folder 'Tools' ada di direktori yang sama atau dalam PYTHONPATH.")
    sys.exit(1)

# --- Konfigurasi Path ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "Json")
DAFTAR_NILAI_DIR = os.path.join(BASE_DIR, "DaftarNilai")
HASIL_MAHASISWA_PATH = os.path.join(JSON_DIR, "hasil_nilai_mahasiswa.json")
JOB_DATA_PATH = os.path.join(JSON_DIR, "JobData.json") # Pastikan file ini ada

os.makedirs(JSON_DIR, exist_ok=True)
os.makedirs(DAFTAR_NILAI_DIR, exist_ok=True)


# --- Fungsi Helper untuk GUI ---
class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = ""

    def write(self, string):
        self.buffer += string
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END) # Auto-scroll

    def flush(self):
        pass # Tkinter Text widget handles its own flushing


def load_hasil_mahasiswa():
    if os.path.exists(HASIL_MAHASISWA_PATH):
        with open(HASIL_MAHASISWA_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                messagebox.showerror("JSON Error", "Gagal membaca data JSON mahasiswa.")
                return []
    return []

def save_hasil_mahasiswa(data):
    with open(HASIL_MAHASISWA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- Modifikasi Fungsi Backend untuk GUI ---

def tampilkan_data_nim_gui(nim, text_output_widget):
    """Menampilkan data NIM ke widget Text, menangkap print."""
    original_stdout = sys.stdout
    sys.stdout = StdoutRedirector(text_output_widget)
    try:
        # Panggil fungsi asli dari CariProfil.py
        # Asumsikan tampilkan_data_nim mengambil path file hasil_nilai_mahasiswa.json
        # atau kita load datanya di sini
        data_mahasiswa_all = load_hasil_mahasiswa()
        mahasiswa = next((m for m in data_mahasiswa_all if m.get("NIM") == nim), None)
        if mahasiswa:
            print(f"--- Profil Mahasiswa (NIM: {nim}) ---")
            print(f"Nama: {mahasiswa.get('Nama', 'N/A')}")
            print(f"NIM: {mahasiswa.get('NIM', 'N/A')}")
            print(f"Profil Lulusan: {mahasiswa.get('Profil Lulusan', 'N/A')}")
            print(f"MBTI: {mahasiswa.get('MBTI', {}).get('Tipe', 'N/A')}")
            
            mbti_details = mahasiswa.get('MBTI', {}).get('Deskripsi Singkat', 'Tidak ada deskripsi.')
            if isinstance(mbti_details, list): # Jika deskripsi adalah list
                print(f"Deskripsi MBTI:")
                for item in mbti_details:
                    print(f"  - {item}")
            else: # Jika string biasa
                print(f"Deskripsi MBTI: {mbti_details}")

            skills = mahasiswa.get('Skill', {})
            print("\n--- Skills ---")
            print("Hard Skills:")
            for skill in skills.get('Hard Skill', ['Tidak ada']):
                print(f"  - {skill}")
            print("Soft Skills:")
            for skill in skills.get('Soft Skill', ['Tidak ada']):
                print(f"  - {skill}")
        else:
            print(f"Data untuk NIM {nim} tidak ditemukan di {HASIL_MAHASISWA_PATH}.")

    except Exception as e:
        print(f"Error saat menampilkan data: {e}")
    finally:
        sys.stdout = original_stdout

def update_skills_gui_wrapper(nim, text_output_widget, app_instance):
    """Wrapper untuk update_skills yang menggunakan dialog Tkinter."""
    skill_type = simpledialog.askstring("Tipe Skill", "Masukkan tipe skill (Hard/Soft):", parent=app_instance.root)
    if not skill_type or skill_type.lower() not in ["hard", "soft"]:
        messagebox.showwarning("Input Tidak Valid", "Tipe skill harus 'Hard' atau 'Soft'.")
        return

    action = simpledialog.askstring("Aksi", "Tambah atau Hapus skill? (tambah/hapus):", parent=app_instance.root)
    if not action or action.lower() not in ["tambah", "hapus"]:
        messagebox.showwarning("Input Tidak Valid", "Aksi harus 'tambah' atau 'hapus'.")
        return

    skill_name = simpledialog.askstring("Nama Skill", "Masukkan nama skill:", parent=app_instance.root)
    if not skill_name:
        messagebox.showwarning("Input Tidak Valid", "Nama skill tidak boleh kosong.")
        return

    # Panggil fungsi update yang sudah dimodifikasi (atau buat yang baru)
    # update_skill_data_for_nim harus menerima parameter ini dan path file
    try:
        success, message = update_skill_data_for_nim(
            nim, 
            skill_type.capitalize() + " Skill", # "Hard Skill" atau "Soft Skill"
            action.lower(), 
            skill_name,
            hasil_mahasiswa_path=HASIL_MAHASISWA_PATH
        )
        if success:
            messagebox.showinfo("Sukses", message)
            text_output_widget.insert(tk.END, f"INFO: {message}\n")
            app_instance.current_user_data = next((m for m in load_hasil_mahasiswa() if m["NIM"] == nim), None) # Reload data
        else:
            messagebox.showerror("Gagal", message)
            text_output_widget.insert(tk.END, f"ERROR: {message}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan saat update skill: {e}")
        text_output_widget.insert(tk.END, f"ERROR: Terjadi kesalahan: {e}\n")


def rekomendasi_pekerjaan_by_nim_fc_gui(nim, text_output_widget):
    """Menampilkan rekomendasi pekerjaan ke widget Text, menangkap print."""
    original_stdout = sys.stdout
    sys.stdout = StdoutRedirector(text_output_widget)
    try:
        # Panggil fungsi asli dari JobFinder.py
        # Pastikan path ke JobData.json dan hasil_nilai_mahasiswa.json benar
        rekomendasi_pekerjaan_by_nim_fc(
            nim,
            mahasiswa_data_path=HASIL_MAHASISWA_PATH,
            jobdata_path=JOB_DATA_PATH
        )
    except FileNotFoundError as e:
        print(f"ERROR: File yang dibutuhkan tidak ditemukan: {e.filename}")
    except Exception as e:
        print(f"Error saat mencari rekomendasi: {e}")
    finally:
        sys.stdout = original_stdout

# --- Kelas Aplikasi Utama ---
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analisis Profil Mahasiswa")
        self.root.geometry("800x600")

        self.current_nim = None
        self.current_user_data = None

        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam') # atau 'alt', 'default', 'classic'

        self.setup_nim_input_frame()
        self.setup_output_area() # Output area selalu ada

    def clear_output(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)

    def add_to_output(self, message):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)

    def setup_nim_input_frame(self):
        self.nim_input_frame = ttk.Frame(self.root, padding="20")
        self.nim_input_frame.pack(fill=tk.X, pady=10)

        ttk.Label(self.nim_input_frame, text="Selamat Datang! Pastikan file PDF nilai ada di folder 'DaftarNilai/'.", font=("Arial", 12)).pack(pady=5)
        ttk.Label(self.nim_input_frame, text="Masukkan NIM Anda:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.nim_entry = ttk.Entry(self.nim_input_frame, width=20, font=("Arial", 10))
        self.nim_entry.pack(side=tk.LEFT, padx=5)
        self.nim_entry.bind("<Return>", self.process_nim_event) # Bind Enter key

        self.nim_button = ttk.Button(self.nim_input_frame, text="Proses", command=self.process_nim)
        self.nim_button.pack(side=tk.LEFT, padx=5)

    def setup_main_menu_frame(self):
        if hasattr(self, 'main_menu_frame') and self.main_menu_frame.winfo_exists():
            self.main_menu_frame.destroy()

        self.main_menu_frame = ttk.Frame(self.root, padding="10")
        self.main_menu_frame.pack(fill=tk.X)

        nama = self.current_user_data.get('Nama', 'Mahasiswa')
        ttk.Label(self.main_menu_frame, text=f"Selamat datang, {nama} (NIM: {self.current_nim})!", font=("Arial", 12, "bold")).pack(pady=10)

        options = [
            ("Lihat Profil, MBTI, dan Skill", self.show_profile_data),
            ("Update Skill (Hard/Soft Skill)", self.trigger_update_skills),
            ("Cari Pekerjaan (Cocok/Tidak Cocok)", self.find_jobs),
            ("Ganti NIM / Logout", self.logout),
            ("Keluar Aplikasi", self.root.quit)
        ]

        for text, command in options:
            ttk.Button(self.main_menu_frame, text=text, command=command, width=40).pack(pady=5, fill=tk.X, padx=20)

    def setup_output_area(self):
        self.output_frame = ttk.Frame(self.root, padding="10")
        self.output_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(self.output_frame, wrap=tk.WORD, state=tk.DISABLED, height=15, font=("Courier New", 9))
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Tambahkan tombol Clear Output
        self.clear_button = ttk.Button(self.output_frame, text="Clear Output", command=self.clear_output)
        self.clear_button.pack(pady=5, side=tk.BOTTOM)


    def process_nim_event(self, event): # Handler untuk Enter key
        self.process_nim()

    def process_nim(self):
        self.clear_output()
        nim_input = self.nim_entry.get().strip()
        if not nim_input:
            messagebox.showerror("Input Kosong", "NIM tidak boleh kosong.")
            self.add_to_output("ERROR: NIM tidak boleh kosong.")
            return

        self.current_nim = nim_input
        path_data_pdf = os.path.join(DAFTAR_NILAI_DIR, f"daftarnilai{self.current_nim}.pdf")

        if not os.path.exists(path_data_pdf):
            messagebox.showerror("File Tidak Ditemukan", f"File {os.path.basename(path_data_pdf)} tidak ditemukan di folder 'DaftarNilai/'.")
            self.add_to_output(f"ERROR: File PDF untuk NIM {self.current_nim} tidak ditemukan.")
            self.current_nim = None
            return

        semua_data = load_hasil_mahasiswa()
        self.current_user_data = next((m for m in semua_data if m.get("NIM") == self.current_nim), None)

        if not self.current_user_data:
            self.add_to_output(f"INFO: Data NIM {self.current_nim} belum dianalisis. Memulai analisis otomatis...")
            try:
                # Panggil run_analysis dari pdfread.py
                # Asumsikan run_analysis menerima nim dan path ke folder pdf
                # serta mengupdate/membuat file hasil_nilai_mahasiswa.json
                run_analysis(self.current_nim) # Fungsi ini harus ada di Tools.pdfread
                self.add_to_output(f"INFO: Analisis untuk NIM {self.current_nim} selesai.")
                
                semua_data = load_hasil_mahasiswa() # Reload data
                self.current_user_data = next((m for m in semua_data if m.get("NIM") == self.current_nim), None)

                if not self.current_user_data:
                    messagebox.showerror("Analisis Gagal", "Gagal menganalisis dan memuat data mahasiswa setelah analisis.")
                    self.add_to_output(f"ERROR: Gagal memuat data setelah analisis untuk NIM {self.current_nim}.")
                    self.current_nim = None
                    return
            except Exception as e:
                messagebox.showerror("Error Analisis", f"Terjadi kesalahan saat analisis: {e}")
                self.add_to_output(f"ERROR saat analisis: {e}")
                self.current_nim = None
                return
        
        self.add_to_output(f"INFO: Data untuk NIM {self.current_nim} berhasil dimuat.")
        self.nim_input_frame.pack_forget() # Sembunyikan frame input NIM
        self.setup_main_menu_frame() # Tampilkan menu utama


    def show_profile_data(self):
        self.clear_output()
        if self.current_nim and self.current_user_data:
            self.add_to_output(f"Menampilkan data untuk NIM: {self.current_nim}...\n")
            tampilkan_data_nim_gui(self.current_nim, self.output_text)
        else:
            messagebox.showwarning("Data Tidak Ada", "Silakan proses NIM terlebih dahulu.")
            self.add_to_output("WARNING: Tidak ada data NIM yang aktif.")

    def trigger_update_skills(self):
        self.clear_output()
        if self.current_nim and self.current_user_data:
            self.add_to_output(f"Update skill untuk NIM: {self.current_nim}...\n")
            update_skills_gui_wrapper(self.current_nim, self.output_text, self)
        else:
            messagebox.showwarning("Data Tidak Ada", "Silakan proses NIM terlebih dahulu.")
            self.add_to_output("WARNING: Tidak ada data NIM yang aktif.")

    def find_jobs(self):
        self.clear_output()
        if self.current_nim and self.current_user_data:
            self.add_to_output(f"Mencari rekomendasi pekerjaan untuk NIM: {self.current_nim}...\n")
            rekomendasi_pekerjaan_by_nim_fc_gui(self.current_nim, self.output_text)
        else:
            messagebox.showwarning("Data Tidak Ada", "Silakan proses NIM terlebih dahulu.")
            self.add_to_output("WARNING: Tidak ada data NIM yang aktif.")

    def logout(self):
        self.clear_output()
        self.add_to_output("INFO: Anda telah logout. Silakan masukkan NIM baru.")
        self.current_nim = None
        self.current_user_data = None
        if hasattr(self, 'main_menu_frame') and self.main_menu_frame.winfo_exists():
            self.main_menu_frame.pack_forget()
        self.nim_entry.delete(0, tk.END) # Bersihkan entry NIM
        self.nim_input_frame.pack(fill=tk.X, pady=10) # Tampilkan kembali frame input NIM


if __name__ == "__main__":
    # Pastikan file JobData.json ada dan berisi data yang valid
    # Contoh isi minimal JobData.json:
    # { "categories": [ { "category_name": "Contoh Kategori", "roles": [] } ] }
    if not os.path.exists(JOB_DATA_PATH):
        with open(JOB_DATA_PATH, "w") as f:
            json.dump({"categories": []}, f) # Buat file kosong jika tidak ada
        print(f"INFO: File {JOB_DATA_PATH} tidak ditemukan, file kosong telah dibuat.")
    
    # Pastikan file hasil_nilai_mahasiswa.json ada (bisa kosong awalnya)
    if not os.path.exists(HASIL_MAHASISWA_PATH):
        with open(HASIL_MAHASISWA_PATH, "w") as f:
            json.dump([], f)
        print(f"INFO: File {HASIL_MAHASISWA_PATH} tidak ditemukan, file kosong telah dibuat.")


    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()