# **Dompetin - Personal Finance App**

Aplikasi **Dompetin** adalah software personal finance yang membantu pengguna mengatur keuangan pribadi dengan berbagai fitur seperti transaksi, laporan saldo, dan grafik pendapatan-pengeluaran.

## **Cara Menjalankan Aplikasi**

bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
source venv/bin/activate       # untuk Linux/macOS
venv\Scripts\activate         # untuk Windows

# Instal library dari requirements.txt
pip install -r requirements.txt

# Jalankan aplikasi
flet run dompetin_app

## **Daftar Modul**

Berikut adalah daftar modul yang diimplementasikan dalam aplikasi:

- anggaran.py  
- balance.py  
- carousel.py  
- charts.py  
- dashboard.py  
- inputform.py  
- transaksi.py  
- updateform.py  
- util.py  

## **Pembagian Tugas**

### **Muhammad Farrel Wibowo (13523153):**
- Dashboard page
- transaksi.py
- CRUD transaksi
- balance.py
- Styling halaman Dashboard dan Transaksi
- Navigation sidebar

### **Jonathan Kenan Budianto (13523139):**
- inputform.py
- Sistem kategori transaksi
- Sistem tipe transaksi

### **Mahesa Fadhillah Andre (13523140):**
- anggaran.py
- Anggaran page
- charts.py
- carousel.py
- Grafik pendapatan (line chart, pie chart, bar chart)

### **Sebastian Enrico Nathanael (13523134):**
- Desain aplikasi (Figma)
- Testing program

## **Database**

### **Tabel: `transaksi`**  
| Kolom             | Tipe Data  |  
|--------------------|-----------|  
| title             | VARCHAR   |  
| date              | DATE      |  
| category          | VARCHAR   |  
| amount            | FLOAT     |  
| transaction_type  | VARCHAR   |  

### **Tabel: `balance`**  
| Kolom       | Tipe Data  |  
|-------------|-----------|  
| amount     | FLOAT      |  