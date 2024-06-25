# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## 1. Business Understanding

Jaya Jaya Maju merupakan sebuah perusahaan multinasional yang telah berdiri sejak tahun 2000. Perusahaan ini bergerak di bidang edutech dan memiliki 1000 karyawan yang tersebar di seluruh negeri.

Untuk memantau karyawannya, terdapat sistem profiling karyawan yang berisi status attrition (karyawan keluar), gaji, departemen, dll yang dikelola oleh HR. Namun, meski sudah berdiri lama, ternyata perusahaan masih memiliki attrition rate yang cukup besar, yaitu sekitar 10% dari total karyawan.

## 2. Permasalahan Bisnis


### 2.1. Masalah

Dengan total 1000 karyawan, attrition rate sebesar 10% berarti terdapat 100 karyawan yang meninggalkan perusahaan dalam jangka waktu tertentu.

Posisi yang ditinggalkan karyawan karena attrition tidak akan diisi sama sekali atau dalam waktu yang lama (berbeda dengan turnover).

### 2.2. Hipotesis/Dugaan

Terdapat penyebab internal dan eksternal yang dapat menyebabkan attrition. Namun, penyebab yang masih dapat dikontrol HR umumnya adalah penyebab internal. Beberapa penyebab internal yang mungkin antara lain [^1]:

1. Kurangnya besaran gaji/kenaikan gaji
2. Pekerjaan/lokasi yang tidak sesuai. Dapat terjadi karena paksaan (tuntutan kantor/atasan) ataupun sukarela (menghindari pengangguran)
3. Fasilitas tidak memadai/memuaskan (tidak higienis, internet bermasalah, dsb)
4. Masalah manajemen kerja atau tim (overtime, bad leadership, pekerjaan monoton, dsb)

### 2.3. Urgensi

Berdasarkan penelitian terkait:
1. Berdasarkan studi oleh Center for American Progress, biaya untuk menggantikan suatu karyawan yang pindah umumnya memakan sekitar 16% sampai 213% dari gaji tahunan karyawan tersebut [^2], dan bisa lebih besar (dari segi waktu, biaya, dan kerugian produktivitas) jika posisinya semakin penting
2. Attrition rate yang tinggi juga bisa disebabkan karena retirement (pensiun) atau restrukturisasi perusahaan [^3]. Jika karena faktor tersebut, maka diperlukan transfer knowledge secepatnya untuk menghindari masalah pada karyawan yang akan mengambil alih posisi tersebut
3. 60% karyawan (generasi milenial) umumnya terbuka untuk pekerjaan baru, namun hanya 26% jika mereka nyaman di tempat kerja saat ini [^4]. 54% dari mereka akan pergi bila mendapat gaji 20% lebih tinggi, namun turun ke 37% bila karyawan tersebut nyaman di tempat kerja saat ini [^5]. Oleh karena itu, faktor-faktor penyebab karyawan tidak nyaman juga perlu untuk ditelusuri

### 2.4. Rumusan dan Usulan Solusi

Diperlukan solusi atas masalah tingginya attrition rate tersebut, yang secara garis besar dapat menjawab beberapa pertanyaan berikut:

1. Berapa besar kemungkinan suatu karyawan akan keluar dari perusahaan?
2. Apa faktor-faktor utama yang menyebabkan karyawan keluar?
3. Apa yang bisa diterapkan untuk mengurangi jumlah karyawan yang akan keluar?

Untuk membantu mencapai solusi tersebut maka:

1. Diperlukan adanya dashboard bagi HR untuk memantau faktor-faktor yang menyebabkan karyawan keluar
2. Membuat model prediksi untuk mendeteksi potensi suatu karyawan akan keluar

## Cakupan Proyek

1. Mengubah bentuk data dari CSV ke database agar bisa diproses lebih lanjut dengan berbagai tools
2. Membuat dashboard (Metabase) untuk memantau attrition karyawan
3. Membuat model prediksi (TensorFlow) attrition karyawan

## Persiapan

**Sumber data:**

Database HR employee attrition pada server Supabase (lihat `database.txt`). File akan terbaca otomatis oleh notebook (bila diperlukan memperbarui data ke Supabase)

**Setup environment:**

Setup Metabase v0.49.6
1. Download `metabase.jar` di [sini](https://www.metabase.com/start/oss/jar) dan Java (JRE/JDK) di [sini](https://adoptium.net/temurin/archive/)
2. Letakkan `metabase.jar` pada folder `dashboard` (di root folder proyek ini)
3. Buka shell terminal (Zsh, Git Bash, dsb) dan jalankan `run_metabase.sh` (atau `java -jar metabase.jar`)
4. Akses Metabase dengan membuka URL `localhost:3000`

Setup Python v3.11.5
1. Download Python di [sini](https://www.python.org/downloads/)
2. Pastikan tambahkan Python ke `PATH` saat instalasi
3. Buka folder proyek ini lewat IDE/code editor (misal VS Code)
4. Buat virtual environment dan install dependensi proyek pada terminal di IDE: 
    ``` bash
    python -m venv .venv
    source .venv/Scripts/activate
    pip install -r requirements.txt
    ```
5. Jalankan notebook dengan kernel virtual environment pada IDE (bila diperlukan)
6. Untuk **menjalankan model prediksi**, bisa dijalankan lewat IDE langsung atau perintah `python predict.py` (tidak wajib menjalankan notebook). Hasil prediksi akan tersimpan pada `data/model_output.csv`
7. Bila terdapat error dependensi, pastikan virtual environment sudah diaktifkan pada terminal. Bila terminal diganti/ditutup, maka perlu diaktifkan kembali sesuai perintah step 4 baris 2

## Business Dashboard

Dashboard dibagi menjadi 4 bagian untuk memantau attrition dari sudut pandang yang berbeda:

- **Berdasarkan keragaman (diversity):** Berisi visualisasi dari segi umur, gender, departemen, jenis pekerjaan, latar belakang pendidikan, dll
- **Berdasarkan faktor umum yang dilihat karyawan:** Berisi visualisasi dari segi gaji, WLB, overtime, jarak rumah ke kantor, dll
- **Berdasarkan tahun/pengalaman:** Berisi visualisasi dari tahun mulai bekerja (total/hanya di perusahaan/hanya untuk role ini), jumlah perusahaan karyawan sebelumnya, dll
- **Berdasarkan hasil survei:** Berisi visualisasi dari hasil survei WLB, job involvement, job satisfaction, relationship satisfaction, dll

Catatan terkait dashboard:

- Untuk menghindari penumpukan visualisasi, dashboard hanya menampilkan hubungan langsung antara tiap variabel dengan attrition
- Hubungan tidak langsung (lebih dari 2 arah) bisa dilihat dengan menerapkan filter pada dashboard

## Conclusion

Berdasarkan grafik dashboard serta analisis lanjutan, didapat konklusi berupa:

1. Pada masing-masing variabel, attrition umumnya berkaitan erat dengan golongan terendah pada variabel/grafik tersebut, misalnya:
    - Pekerja dengan usia 18-20 tahun (57% attrition)
    - Pekerja yang bekerja di perusahaan setara/dibawah 2 tahun (35% attrition)
    - Pekerja dengan skor job involvement 1 (33% attrition)
    - Pekerja dengan skor WLB 1 (31% attrition)
    - Pekerja dengan gaji setara/dibawah $2000 (30% attrition)
    - Pekerja yang overtime (30% attrition)
    - Pekerja dengan job level 1 (26% attrition)
    - Dan seterusnya
2. Namun, bila dilihat dari korelasinya maka:
    - Attrition memiliki korelasi searah yang kuat dengan:
        - Overtime (24%)
        - Frekuensi travel bisnis (12%)
    - Attrition memiliki korelasi terbalik yang kuat dengan:
        - Total pengalaman kerja (17%)
        - Job level (17%)
        - Monthly income (16%)
        - Usia (16%)
        - Lama waktu bekerja dibawah manager (15%)

Bila dilihat secara lebih detail:

1. Pekerjaan yang paling banyak mengalami attrition adalah di bidang teknisi (24%) dan sales (18-40% tergantung role)
   - Karyawan yang memiliki background pendidikan teknik (9%) dan marketing (11%) juga jauh lebih sedikit daripada bidang lainnya
   - Meski begitu, departemen R&D memiliki jumlah karyawan terbanyak (65%) dan memiliki attrition rate relatif rendah (13%) dibandingkan departemen sales (20%) dan HR (19%)
2. Karyawan yang single memiliki attrition rate lebih tinggi (25%) dari married (12%) dan divorced (10%)
    - Karyawan single terbanyak berada dikisaran usia 26-40 tahun (19% dari total karyawan)
    - Karyawan yang single rata-rata berada di job level 1 dan 2 (25% dari total karyawan)
    - 27% dari karyawan yang single telah bekerja overtime, dengan 50% diantaranya (yang overtime) mengalami attrition
3. Attrition rate karyawan dengan monthly income direntang $1000 (54%), $2000 (26%) dan $10000 (20%) cenderung lebih besar dari yang lainnya
    - Meski sebaran monthly income semakin turun dengan tingginya pendapatan, sebaran monthly rate (gaji + bonus) cukup stabil dan terlihat kurang berpengaruh terhadap attrition
    - Karyawan dengan persentase kenaikan gaji terbesar (21-25%) memiliki attrition (16%) yang serupa dengan kenaikan gaji terkecil (11-15%), sehingga dampak perbedaan kenaikan gaji tidak terlalu signifikan
    - Karyawan yang memiliki stok/digaji dengan stok di level menengah (1 dan 2) memiliki attrition rate lebih rendah (7-9%) daripada yang tidak punya sama sekali (24%) dan yang punya opsi stok tertinggi (17%)
4. Karyawan yang telah bekerja dibanyak perusahaan sebelumnya (terutama lebih dari 4 perusahaan) berkemungkinan lebih besar mengalami attrition (x̄ = 22%)
    - Karyawan yang telah bekerja di lebih dari 4 perusahaan memiliki jumlah yang lebih sedikit pula (20%) daripada karyawan lainnya
    - Karyawan yang telah bekerja di lebih dari 4 perusahaan rata-rata memiliki job level 1 dan 2 (14% dari total karyawan), yang berarti hanya 6% berada di level 3+
5. Karyawan yang telah berpengalaman (baik secara total/hanya di perusahaan ini) tepat 1 tahun lebih mudah mengalami attrition (34-49%), dan akan turun relatif stabil di kisaran 9-15% untuk tahun-tahun setelahnya
    - Karyawan baru yang merasa tidak cocok dengan manager/pekerjaannya akan attrition (30%) sebelum 1 tahun. Angka ini turun ke 24% bila karyawan telah mempunyai experience sebelumnya minimal 2 tahun
6. Karyawan yang mengisi skor 1 pada WLB dan satisfaction survey (environment, relationship, dan job involvement) memiliki attrition yang lebih tinggi (20-30%) dari karyawan dengan skor lainnya
    - Meski begitu, semakin tinggi skor WLB dan satisfaction survey tidak menjamin turunnya attrition rate pada karyawan dengan skor tinggi tersebut, melainkan relatif merata di kisaran 9-15% untuk semua skor diatas 1
    - Semua karyawan memiliki skor performance rating di rentang 3 dan 4, yang berarti semua karyawan relatif kompeten meskipun skor survei lainnya bisa saja buruk

## Rekomendasi Action Items (Optional)

Berdasarkan konklusi di atas dan analisis lebih lanjut, maka sebaiknya:

1. Melarang overtime berlebih terutama untuk kalangan karyawan yang:
    - Berusia setara/dibawah 25 tahun (60% attrition)
        - Usia setelahnya tetap memiliki attrition >30% sampai usia 31-35 tahun
    - Memiliki gaji $4000 atau dibawahnya (58% attrition)
    - Memiliki job level 1 (52% attrition)
    - Berstatus single (50% attrition)
    - Bekerja di bidang sales representative (66% attrition) atau teknisi laboratorium (50% attrition)
    - Rumahnya berjarak 15+ km dari kantor atau sering melakukan travel bisnis (40% attrition)
2. Merevisi mekanisme insentif/bonus sehingga karyawan tidak bergantung sepenuhnya terhadap monthly rate (mencegah burnout dan overtime)
    - 60% karyawan memiliki monthly income yang 2x lebih kecil dari monthly rate (83% jika spesifik pada role sales representative)
        - Mereka yang bekerja overtime pada kondisi ini memiliki 37% attrition rate
        - Jika diperdalam, 42% karyawan memiliki monthly income 3x lebih kecil dari monthly rate, 30% untuk 4x, dan 21% untuk 5x. Attrition rate juga naik dengan semakin tingginya kesenjangan kedua variabel tersebut
    - Insentif berupa stok (level 1/2/3) cukup efektif menurunkan attrition (x̄ = 11%) dibandingkan dengan yang tidak memiliki stok sama sekali (24% attrition)
    - Mengkaji ulang monthly income/rate terutama untuk job level 1 (26% attrition) sesuai dengan beban dan waktu kerjanya, atau memberi insentif dalam bentuk lain (snack, dsb) untuk memberikan engagement
3. Memantau manager yang memiliki banyak bawahan dengan attrition rate tinggi dan/atau menempatkan karyawan baru ke manager yang lebih komunikatif
    - 20% karyawan akan attrition dalam jangka waktu 1 tahun bila tidak cocok dengan manager saat ini, meskipun telah bekerja lebih dari 1 tahun di perusahaan
        - Angka ini naik ke 30% bila merupakan karyawan baru (belum 1 tahun bekerja di perusahaan)
        - Mereview tingkat kepuasan karyawan setiap 1 tahun bekerja (misal apakah mereka mempunyai ambisi tidak tercapai dengan kondisi saat ini?), dan mengakomodasinya bila memungkinkan
            - Catatan: ambisi tidak selalu dalam bentuk uang, namun dapat juga dalam bentuk eksplorasi skill baru yang tidak ada dalam kultur perusahaan saat ini
    - Memberikan motivasi dan insentif terhadap manager yang memiliki attrition/turnover rate rendah (jurnal terkait [^6]). Bila secara tidak langsung misalnya dengan kompetisi "manager of the month", dsb
    - Melakukan post interview/memantau beberapa saat (0-3 bulan) setelah karyawan attrition
        - Apakah karyawan yang keluar sudah bekerja kembali (di perusahaan lain)? Bila belum mendapat pekerjaan maka ada faktor khusus (manager, dsb) yang menyebabkan karyawan tidak tahan/keluar sebelum memiliki backup pekerjaan lain 
    - Menjaga karyawan yang telah bekerja selama 5 tahun atau lebih (x̄ = 11% attrition)
4. Gunakan model machine learning untuk memprediksi attrition karyawan, namun tetap memperhatikan faktor-faktor lainnya pada konklusi karena model tidak sepenuhnya akurat (akurasi = 82%, skor F1 = 70%)


[^1]: G. Negi, “Employee attrition: Inevitable yet manageable,” International Monthly Refereed Journal of Research In Management & Technology, vol. 2, no. 1, 2013, Diakses: 30 April 2024. [Daring]. Tersedia pada: https://www.academia.edu/download/38728081/8.pdf

[^2]: H. Boushey dan S. Glynn, “There are significant costs to replacing business employees,” Center for American Progress, hlm. 1–9, 2012.

[^3]: A. Przystanski, “Turnover vs. Attrition: Decoding Two of HR’s Most Important Metrics.” Diakses: 30 April 2024. [Daring]. Tersedia pada: https://lattice.com/library/turnover-vs-attrition-decoding-two-of-hrs-most-important-metrics

[^4]: B. Rigoni dan B. Nelson, “For Millennials, Is Job-Hopping Inevitable?,” Gallup.com. Diakses: 4 Mei 2024. [Daring]. Tersedia pada: https://news.gallup.com/businessjournal/197234/millennials-job-hopping-inevitable.aspx

[^5]: B. Rigoni dan B. Nelson, “Retaining Employees: How Much Does Money Matter?,” Gallup.com. Diakses: 4 Mei 2024. [Daring]. Tersedia pada: https://news.gallup.com/businessjournal/188399/retaining-employees-money-matter.aspx

[^6]: M. Hoffman dan S. Tadelis, “People Management Skills, Employee Attrition, and Manager Rewards: An Empirical Analysis,” Journal of Political Economy, vol. 129, no. 1, hlm. 243–285, Jan 2021, doi: 10.1086/711409.
