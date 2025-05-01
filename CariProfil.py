import json

def konversi_nilai_huruf(nilai_huruf):
    """Mengkonversi nilai huruf menjadi nilai numerik"""
    konversi = {
        'A': 85,
        'A-': 80,
        'B+': 75,
        'B': 70,
        'B-': 65,
        'C+': 60,
        'C': 55,
        'D': 50,
        'E': 40
    }
    return konversi.get(nilai_huruf, 0)

def hitung_skor_profil(mata_kuliah, daftar_mk):
    total = 0
    jumlah = 0
    mk_lower = {mk.lower(): nilai for mk, nilai in mata_kuliah.items()}
    
    for mk in daftar_mk:
        mk_key = mk.lower()
        nilai = mk_lower.get(mk_key) or mk_lower.get(mk_key + " mbkm")
        if nilai:
            total += konversi_nilai_huruf(nilai)
            jumlah += 1
    
    return total / max(jumlah, 1)  # Hindari division by zero



def tentukan_profil(mata_kuliah):
    """Menentukan profil berdasarkan nilai mata kuliah"""
    # Daftar mata kuliah untuk setiap profil
    profil_mk = {
        "ISD": [  # Artificial Intelligence
            "Internet of Things",
            "Machine Learning",
            "Jaringan Syaraf Tiruan",
            "Knowledge-Based System",
            "Pemrosesan Bahasa Natural",
            "Pemrosesan Citra Digital",
            "Pemrosesan Sinyal Digital",
            "Game Engine",
            "Deep Learning"
        ],
        "UI": [  # UI/UX
            "Pola Desain Antarmuka Pengguna",
            "Desain Eksperimental",
            "Desain dan Evaluasi Antarmuka",
            "Pemodelan Proses Bisnis",
            "Test Engineering",
            "Visualisasi Data"
        ],
        "NSS": [  # Infrastruktur Jaringan
            "Cloud Infrastructure",
            "Cloud Infrastructure MBKM",
            "Enterprise Network",
            "Pengantar Keamanan Jaringan",
            "Pengantar Keamanan Jaringan MBKM",
            "Jaringan Nir Kabel",
            "Otomasi Jaringan",
            "Teknologi WAN",
            "Keamanan Jaringan",
            "Internet of Things"
        ],
        "DB": [  # Database
            "Administrasi Basis Data",
            "Data Warehouse",
            "Basis Data Terdistribusi",
            "Keamanan Basis Data",
            "Administrasi Basis Data Non Relasional"
        ]
    }
    mk_input = {mk.lower(): nilai for mk, nilai in mata_kuliah.items()}

    # Hitung skor untuk setiap profil
    skor = {}
    for profil, daftar_mk in profil_mk.items():
        skor[profil] = hitung_skor_profil(mata_kuliah, daftar_mk)

    # Filter profil dengan skor di atas 0 dan cari yang tertinggi
    profil_terbaik = None
    skor_tertinggi = 0
    
    for profil, nilai in skor.items():
        if nilai > skor_tertinggi:
            skor_tertinggi = nilai
            profil_terbaik = profil
    
    if skor_tertinggi < 75:  # sebelumnya 70
        return "General IT"
    
    return profil_terbaik