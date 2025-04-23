import json

def tentukan_profil(mata_kuliah):
    # Hitung skor untuk setiap profil
    skor = {
        "ISD": 0,  # Artificial Intelligence
        "UI": 0,   # UI/UX
        "NSS": 0,   # Infrastruktur
        "DB": 0,   # Database
    }

    # Rule untuk Artificial Intelligence
    isd_mk = [
        "Internet of Things",
        "Machine Learning",
        "Jaringan Syaraf Tiruan",
        "Knowledge-Based System",
        "Pemrosesan Bahasa Natural",
        "Pemrosesan Citra Digital",
        "Pemrosesan Sinyal Digital",
        "Game Engine",
        "Deep Learning"
    ]

    skor["ISD"] = sum(mata_kuliah.get(mk, 0) for mk in isd_mk) / len(isd_mk) if isd_mk else 0

    # Rule untuk UI/UX
    ui_mk = [
        "Pola Desain Antarmuka Pengguna",
        "Desain Eksperimental",
        "Desain dan Evaluasi Antarmuka",
        "Pemodelan Proses Bisnis",
        "Test Engineering",
        "Visualisasi Data"
    ]
    skor["UI"] = sum(mata_kuliah.get(mk, 0) for mk in ui_mk) / len(ui_mk) if ui_mk else 0

    # Rule untuk Infrastruktur Jaringan
    nss_mk = [
        "Cloud Infrastructure",
        "Enterprise Network",
        "Pengantar Keamanan Jaringan",
        "Jaringan Nir Kabel",
        "Otomasi Jaringan",
        "Teknologi WAN",
        "Keamanan Jaringan",
        "Internet of Things"
    ]
    skor["NSS"] = sum(mata_kuliah.get(mk, 0) for mk in nss_mk) / len(nss_mk) if nss_mk else 0

    # Rule untuk Database
    db_mk = [
        "Administrasi Basis Data",
        "Data Warehouse",
        "Basis Data Terdistribusi",
        "Keamanan Basis Data",
        "Administrasi Basis Data Non Relasional",
    ]
    skor["DB"] = sum(mata_kuliah.get(mk, 0) for mk in db_mk) / len(db_mk) if db_mk else 0

    # Filter out profiles with score 0 and get the highest
    valid_profiles = {k: v for k, v in skor.items() if v > 0}
    if not valid_profiles:
        return "General IT"
    
    profil = max(valid_profiles, key=valid_profiles.get)
    
    # Add threshold (minimum average score of 70)
    if valid_profiles[profil] < 70:
        return "General IT"
    
    return profil

def tambah_profil_ke_json(filepath="Project-AI-/Data.json"):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("File tidak ditemukan.")
        return

    for item in data:
        mata_kuliah = item.get("mata_kuliah", {})  # Ambil nilai mata kuliah
        profil = tentukan_profil(mata_kuliah)
        item["profil_lulusan"] = profil

    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    print("✅ Profil lulusan berhasil ditambahkan ke semua data.")

tambah_profil_ke_json()