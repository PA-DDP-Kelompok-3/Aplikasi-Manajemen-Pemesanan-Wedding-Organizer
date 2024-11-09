import csv
import pwinput
from prettytable import PrettyTable
import os
from datetime import datetime


print("Selamat Datang Di BrideStory!")

FILE_USER = 'user.csv'
FILE_PRODUK = 'produk.csv'
FILE_TRANSAKSI = 'transaksi.csv'

def penyimpanan_data(nama_file):
    data = {}
    try:
        with open(nama_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data[row[0]] = row[1:]  
    except FileNotFoundError:
        pass
    return data

def simpan_data(data, nama_file):
    with open(nama_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for key, values in data.items():
            writer.writerow([key] + values)

user = penyimpanan_data(FILE_USER)
produk = penyimpanan_data(FILE_PRODUK)
transaksi = penyimpanan_data(FILE_TRANSAKSI)

def inisialisasi_layanan():
    if os.path.exists(FILE_PRODUK) and os.path.getsize(FILE_PRODUK) > 0:
        return 

layanan_awal = [
    ["1", "Paket Pernikahan Basic", "300000", "Foto pre-wedding, Dekorasi sederhana, Penyewaan tenda, Kursi dan meja, Konsultasi pernikahan"],
    ["2", "Paket Pernikahan Silver", "400000", "Foto pre-wedding dan on the day, Dekorasi dengan tema pilihan, Catering untuk 100 orang, Sound system, MC profesional"],
    ["3", "Paket Pernikahan Gold", "500000", "Foto pre-wedding dan on the day, Dekorasi mewah dengan bunga segar, Catering untuk 150 orang, Sound system dan lighting, Penyewaan gaun pengantin, Paket spa untuk pengantin"],
    ["4", "Paket Pernikahan Platinum", "750000", "Foto pre-wedding dan on the day, Dekorasi lengkap dengan tema, Catering untuk 200 orang, Live music, Penyewaan gaun dan tuxedo, Paket honeymoon, Dokumentasi video"],
    ["5", "Paket Pernikahan Diamond", "1000000", "Foto pre-wedding dan on the day dengan fotografer terkenal, Dekorasi premium, Catering untuk 300 orang dengan menu pilihan, Sound system dan lighting canggih, Live band, Paket spa dan kecantikan untuk pengantin, Penyewaan mobil mewah"],
]

with open(FILE_PRODUK, mode='w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['id', 'nama', 'harga', 'fasilitas'])  
    csv_writer.writerows(layanan_awal)
    
inisialisasi_layanan()

def register():
    try:
        username = input("Masukkan username: ")
        if username in user:
            print("Username sudah ada.")
            return
        password = pwinput.pwinput("Masukkan password: ")
        role = input("Masukkan role (user/admin): ")
        if role not in ["user", "admin"]:
            print("Role tidak valid.")
            return
        emoney = "0" if role == "user" else "0"
        user[username] = [password, role, emoney]
        simpan_data(user, FILE_USER)
        print(f"Akun {username} berhasil dibuat dengan role {role}.")
    except(KeyboardInterrupt,ValueError):
        print("\nPendaftaran dibatalkan.")

def login():
    try:
        username = input("Masukkan Username:")
        password = pwinput.pwinput("Masukkan password: ")
        role = input("Masukkan role (user/admin): ")
        if username in user:
            pw, sesuai_role, emoney = user[username]
            if pw == password and role == sesuai_role:
                return username, role
            elif pw == password and role != sesuai_role:
                print(f"Role {role} tidak valid untuk pengguna ini.")
            else:
                print("Password salah.")
        else:
            print("Username tidak ditemukan.")
    except (KeyboardInterrupt,ValueError):
        print("\nLogin dibatalkan.")
    return None, None

def menu_utama():
    try:
        print("=== Aplikasi Wedding Organizer ===")
        menu = True
        while menu:
            print("\n1. Register")
            print("2. Login")
            print("3. Keluar")
            opsi = input("Pilih opsi: ")
            if opsi == "1":
                register()
            elif opsi == "2":
                username, role = login()
                if username: 
                    if role == "admin":
                        menu_admin()  
                    elif role == "user":
                        menu_user(username)
            elif opsi == "3":
                print("Terima kasih telah berkunjung!")
                menu = False
            else:
                print("Pilihan anda tidak ada!")
    except(KeyboardInterrupt,ValueError):
        print("Menu login dibatalkan")

def tambah_layanan():
    try:
        id = input("Masukkan ID baru ")

        if not id or any(c not in "0123456789" for c in id) or int(id) <= 0:
            print("ID harus berupa angka positif!.")
            return
        
        with open(FILE_PRODUK, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader) 
            if any(row[0] == id for row in csv_reader):
                print("ID sudah ada. Gunakan ID lain.")
                return

        nama = input("Masukkan nama layanan baru: ")

        try:
            harga = int(input("Masukkan harga layanan: "))
            if harga < 0:
                print("Harga tidak boleh kurang dari 0.")
                return
        except ValueError:
            print("Harga harus berupa angka.")
            return

        fasilitas = input("Masukkan fasilitas layanan (pisahkan dengan koma jika lebih dari satu): ")

        with open(FILE_PRODUK, mode='a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([id, nama, harga, fasilitas])
        print(f"Layanan '{nama}' berhasil ditambahkan dengan fasilitas: {fasilitas}!")
    except (KeyboardInterrupt, ValueError):
        print("\nPenambahan layanan dibatalkan.")

def lihat_layanan():
    try:
        print("========= Ini layanan yang tersedia ========")
        table = PrettyTable()
        table.field_names = ["ID", "Nama Layanan", "Harga"]

        with open(FILE_PRODUK, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                table.add_row([row['id'], row['nama'], row['harga']])   
        print(table)
        print("===========================================")
    except(KeyboardInterrupt,ValueError):
        print("\nLihat layanan dibatalkan.")

def hapus_layanan():
    try:
        id = input("Masukkan ID layanan yang ingin dihapus: ")
        updated_rows = []
        found = False

        with open(FILE_PRODUK, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] != id:
                    updated_rows.append(row)  
                else:
                    found = True  

        if found:
            print(f"Layanan dengan ID {id} berhasil dihapus.")
            with open(FILE_PRODUK, mode='w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(updated_rows)
        else:
            print(f"Layanan tidak ditemukan.")
    except (KeyboardInterrupt,ValueError):
        print("\nPenghapusan layanan dibatalkan.")

def update_layanan():
    try:
        id = input("Masukkan ID layanan yang ingin diperbarui: ")
        
        with open(FILE_PRODUK, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  
            if not any(row[0] == id for row in csv_reader):
                print("ID tidak ditemukan.")
                return

        nama_baru = input("Masukkan nama layanan baru (biarkan kosong jika tidak ingin mengubah): ")

        try:
            harga_baru_input = input("Masukkan harga layanan baru (biarkan kosong jika tidak ingin mengubah): ")
            if harga_baru_input:
                harga_baru = int(harga_baru_input)
                if harga_baru < 0:
                    print("Harga tidak boleh kurang dari 0.")
                    return
        except ValueError:
            print("Harga harus berupa angka.")
            return

        fasilitas_baru = input("Masukkan fasilitas baru (pisahkan dengan koma jika lebih dari satu, biarkan kosong jika tidak ingin mengubah): ")

        updated_rows = []
        found = False

        with open(FILE_PRODUK, mode='r') as file:
            csv_reader = csv.DictReader(file)
            headers = csv_reader.fieldnames  

            for row in csv_reader:
                if row['id'] == id:
                    row['nama'] = nama_baru if nama_baru else row['nama']
                    row['harga'] = harga_baru if harga_baru_input else row['harga']
                    row['fasilitas'] = fasilitas_baru if fasilitas_baru else row['fasilitas']
                    found = True
                    print(f"Layanan dengan ID {id} berhasil diperbarui.")
                
                updated_rows.append(row)

        if found:
            with open(FILE_PRODUK, mode='w', newline='') as file:
                csv_writer = csv.DictWriter(file, fieldnames=headers)
                csv_writer.writeheader()
                csv_writer.writerows(updated_rows)
    except(KeyboardInterrupt,ValueError):
        print("\nPembaruan layanan dibatalkan.")

def cari_layanan():
    try:
        kata_kunci = input("Masukkan kata kunci layanan yang ingin dicari: ").strip()
        layanan_ditemukan = False

        with open(FILE_PRODUK, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if kata_kunci.lower() in row['nama'].lower():  
                    layanan_ditemukan = True
                    print("\nLayanan ditemukan!")
                    print(f"ID           : {row['id']}")
                    print(f"Nama Layanan : {row['nama']}")
                    print(f"Harga        : Rp{int(row['harga']):,}")
                    print(f"Fasilitas    : {row['fasilitas']}")
                    print("=" * 40)

        if not layanan_ditemukan:
            print("Layanan tidak ditemukan dengan kata kunci tersebut.")
    except (KeyboardInterrupt, ValueError):
        print("\nPencarian layanan dibatalkan.")


def beli_layanan(username):
    try:
        print("=== Beli Layanan ===")
        lihat_layanan() 
        id_layanan = input("Masukkan ID layanan yang ingin dibeli: ")

        # Membaca data layanan
        with open(FILE_PRODUK, mode='r') as file:
            csv_reader = csv.DictReader(file)
            layanan_ditemukan = False
            harga_layanan = 0
            nama_layanan = ""
            fasilitas = ""
            for row in csv_reader:
                if row['id'] == id_layanan:
                    layanan_ditemukan = True
                    nama_layanan = row['nama']
                    harga_layanan = int(row['harga'])
                    fasilitas = row['fasilitas']
                    break

        if not layanan_ditemukan:
            print("Layanan tidak ditemukan.")
            return

        # Memasukkan tanggal acara pernikahan
        tanggal_acara = input("Masukkan tanggal acara pernikahan (format: YYYY-MM-DD): ")
        try:
            tanggal_acara_dt = datetime.strptime(tanggal_acara, "%Y-%m-%d")
        except ValueError:
            print("Format tanggal tidak valid.")
            return

        # Mengecek saldo pengguna
        password, role, saldo = user[username]
        if int(saldo) < harga_layanan:
            print("Saldo Anda tidak mencukupi untuk membeli layanan ini.")
            return

        # Mengurangi saldo setelah pembelian
        saldo = int(saldo) - harga_layanan
        user[username] = [password, role, str(saldo)]
        simpan_data(user, FILE_USER)  

        # Mencatat transaksi
        with open(FILE_TRANSAKSI, mode='a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([username, id_layanan, harga_layanan, tanggal_acara])

        # Menampilkan invoice di output
        print("\n=== INVOICE ===")
        print(f"Username       : {username}")
        print(f"Layanan Dibeli : {nama_layanan}")
        print(f"ID Layanan     : {id_layanan}")
        print(f"Fasilitas      : {fasilitas}")
        print(f"Tanggal Acara  : {tanggal_acara_dt.strftime('%d %B %Y')}")
        print(f"Harga          : Rp{harga_layanan:,}")
        print(f"Sisa Saldo     : Rp{saldo:,}")
        print("Transaksi berhasil dicatat.")
        print("=" * 30)
    except (KeyboardInterrupt, ValueError):
        print("\nBeli Layanan Dibatalkan.")

def cek_saldo(username):
    if username in user:
        pw, role, emoney = user[username]
        print(f"Saldo Anda: Rp{int(emoney):,}")
    else:
        print("Pengguna tidak ditemukan.")

def isi_saldo(username):
    try:
        print("=== Isi Saldo ===")
        try:
            jumlah = int(input("Masukkan jumlah saldo yang ingin ditambahkan: Rp"))
            if jumlah <= 0:
                print("Jumlah saldo harus lebih dari 0.")
                return
        except ValueError:
            print("Input tidak valid. Harap masukkan angka.")
            return

        password, role, saldo = user[username]
        saldo = int(saldo) + jumlah

        if saldo > 10000000:
            print("Saldo tidak dapat melebihi Rp 10.000.000.")
            return
        
        user[username] = [password, role, str(saldo)] 
        simpan_data(user, FILE_USER)  

        print(f"Saldo Anda berhasil diisi! Saldo baru: Rp{saldo:,}")
    except(KeyboardInterrupt,ValueError):
        print("\nIsi Saldo Dibatalkan")

def urutkan_layanan():
    try:
        print("=== Layanan yang Diurutkan Berdasarkan Harga ===")
        layanan = []
        with open(FILE_PRODUK, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                layanan.append(row)
        
        layanan.sort(key=lambda x: int(x['harga']))
        table = PrettyTable()
        table.field_names = ["ID", "Nama Layanan", "Harga"]
        
        for row in layanan:
            table.add_row([row['id'], row['nama'], f"Rp{int(row['harga']):,}"])
        
        print(table)
        print("===========================================")
    except (KeyboardInterrupt, ValueError):
        print("\nUrutkan layanan dibatalkan.")

def menu_admin():
    try:
        menu = True
        while menu:
            print("\n=== Menu Admin ===")
            print("1. Tambah Layanan")
            print("2. Lihat Layanan")
            print("3. Hapus Layanan")
            print("4. Update Layanan")
            print("5. Keluar")
            opsi = (input("Pilih opsi: "))
            if opsi == "1":
                tambah_layanan()
            elif opsi == "2":
                lihat_layanan()
            elif opsi == "3":
                hapus_layanan()
            elif opsi == "4":
                update_layanan()
            elif opsi == "5":
                print("Terima kasih telah berkunjung")
                menu = False
            else: 
                print("Pilihan tidak ada!")
    except(KeyboardInterrupt,ValueError):
        print("\nMenu Admin Dibatalkan")

def menu_user(username):
    try:
        menu = True
        while menu:
            print("\n=== Menu User ===")
            print("1. Lihat Layanan")
            print("2. Cari Layanan")
            print("3.Urutkan layanan")
            print("4. Beli Layanan")
            print("5. Cek Saldo")
            print("6. Isi Saldo")
            print("7. Keluar")
            opsi = input("Masukkan pilihan: ")
            if opsi == "1":
                lihat_layanan()
            elif opsi == "2":
                cari_layanan()
            elif opsi == "3":
                urutkan_layanan()
            elif opsi == "4":
                beli_layanan(username)
            elif opsi == "5":
                cek_saldo(username)
            elif opsi == "6":
                isi_saldo(username)
            elif opsi == "7":
                print("Terima kasih sudah berkunjung!")
                menu = False
            else:
                print("Pilihan anda tidak ada!")
    except (KeyboardInterrupt,ValueError):
        print("\nMenu User Dibatalkan")

menu_utama()
