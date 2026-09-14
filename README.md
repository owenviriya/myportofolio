# MyPortofolio

**Nama:** Owen Viriya Chandra  
**NPM:** 2506539196  
**Kelas:** PBP B  

## Deskripsi

MyPortofolio adalah website portofolio pribadi yang dibuat menggunakan Django.
Website ini menampilkan profil, pendidikan, pengalaman, keterampilan teknis,
dan kemampuan bahasa.

## Menjalankan Secara Lokal

```bash
git clone https://github.com/owenviriya/myportofolio.git
cd myportofolio

python -m venv env
env\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Buka http://localhost:8000/ pada browser.

## Deployment

Website yang sudah di-deploy dapat diakses melalui [PWS](https://owen-viriya-myportofolio.pws.cs.ui.ac.id/).

### Tugas 1

1. Penggunaan Elemen Semantik HTML5

Ya, saya menggunakan beberapa elemen semantik HTML5 seperti section dan article. Elemen section saya gunakan untuk memisahkan antara bagian Profile, Education, Experience, dan Skills. Elemen article juga saya gunakan untuk membuat setiap subbagian Education dan juga Experience karena masing-masing merupakan konten yang berdiri sendiri. Penggunaan elemen-elemen semantik juga berfungsi untuk membuat struktur kode HTML menjadi lebih rapi dan readable untuk saya, yang membuat pengembangan selanjutnya bisa lebih mudah.

2. Tantangan Responsive Layout

Tantangan yang saya temukan adalah ketika mencoba menyesuaikan navbar, kartu Experience, logo, dan skill tags agar tetap rapi pada layar kecil. Navbar di mobile awalnya menggunakan layout 1 baris seperti di dekstop, namun ternyata tulisan 'Skills' itu kepotong saat membuka tampilan mobile dan teks Experience yang panjang membuat kartu melebar keluar dari layar. Saya mengatasinya dengan mengatur ulang navbar menggunakan Grid, mengecilkan logo dan padding pada kartu, serta menggunakan overflow-wrap agar teks yang panjang dapat turun ke baris berikutnya. Saya mengevaluasi hasilnya melalui responsive mode di DevTools dengan mencoba beberapa ukuran layar dan memperbaiki bagian yang terlihat kurang enak dilihat.

3. Keterbatasan Static Web

Karena website ini masih bersifat static web, sebagian besar informasi masih ditulis langsung di dalam file HTML. Kalau saya ingin mengubah pengalaman, pendidikan, atau skills, saya harus mengedit file, melakukan commit, dan melakukan deployment ulang. Website ini belum ada sistem untuk mengelola konten secara dinamis.
Pada iterasi berikutnya, saya ingin coba menambahkan model Django untuk Project, Experience, dan Education. Saya juga ingin membuat halaman admin agar konten portofolio dapat diperbarui tanpa mengubah HTML secara manual.


### Tugas 2

1. Alur ketika halaman portofolio dibuka

Ketika pengguna membuka halaman seperti /education/, pertama browser mengirimkan request ke server Django lalu request tersebut pertama kali diterima oleh urls.py pada level proyek, yaitu portofolio/urls.py. File ini menggunakan include("main.urls") untuk meneruskan pencarian URL ke urls.py punya aplikasi main. Kemudian di dalam main/urls.py, URL /education/ dicocokkan dengan route yang terhubung ke view show_education. View tersebut mengambil data pendidikan dari database melalui model Education dengan Education.objects.all().

Setelah data diperoleh, view memasukkannya ke dalam context dengan nama education_list, kemudian memanggil render untuk menggabungkan context tersebut dengan template education.html. Template lalu melakukan perulangan terhadap education_list dan menghasilkan HTML berdasarkan setiap object pendidikan. HTML hasil render dikirim sebagai response kepada browser, lalu browser menampilkan halaman portofolio kepada pengguna. Alur yang sama juga digunakan untuk halaman Experience dan Skills dengan model, view, serta template masing-masing.

2. Alasan data disimpan pada model

Data portofolio sebaiknya disimpan pada model, karena model memisahkan data dari tampilan HTML. Template cukup bertanggung jawab hanya untuk mengatur struktur dan presentasi halaman, sedangkan model menyimpan data yang sewaktu-waktu bisa berubah seperti pengalaman, pendidikan, dan skills. Dengan cara ini, data dapat ditambah, diubah, atau dihapus melalui database dan halaman admin tanpa mengedit template. Hal tersebut membuat pemeliharaan lebih mudah, mengurangi pengulangan data di HTML, serta memungkinkan data yang sama digunakan oleh beberapa halaman atau fitur lain. Struktur ini juga memudahkan aplikasi untuk dikembangkan ketika jumlah data semakin banyak.

3. Perbedaan makemigrations dan migrate

makemigrations digunakan untuk membuat file migration berdasarkan perubahan yang dilakukan pada model. File tersebut berisi instruksi perubahan schema database, tetapi belum langsung mengubah database. Sementara itu, migrate digunakan untuk menjalankan file migration tersebut sehingga perubahan schema benar-benar diterapkan pada database. Contohnya, ketika saya menambahkan model Education atau menambahkan field location pada model Experience, saya perlu menjalankan python manage.py makemigrations untuk membuat file migration baru. Setelah itu, saya menjalankan python manage.py migrate agar tabel atau kolom yang baru tersebut dibuat di database.


## AI Disclosure

Dalam pengembangan website ini, saya menggunakan Gemini 3.6 Flash sebagai alat bantu belajar, brainstorming, dan debugging. Saya memberikan potongan HTML/CSS, screenshot, serta pesan error untuk memperoleh penjelasan dan alternatif solusi. Gemini membantu saya memahami elemen semantik HTML5, timeline, pseudo-element `::before`, responsive layout, media query, sticky navbar, smooth scrolling, Experience, Skills, efek hover, serta Conventional Commits. Saya tidak menyalin jawabannya secara langsung, tetapi menyesuaikan setiap saran dengan struktur proyek dan desain yang saya inginkan. Hasil akhir saya verifikasi melalui browser, DevTools, perangkat seluler, dan `python manage.py check`. Karena beberapa saran AI dapat bersifat umum atau kurang sesuai dengan kondisi repository, keputusan desain saya, implementasi, pengujian, dan perbaikan akhir tetap saya lakukan sendiri.

Pada Tugas 2, saya juga menggunakan ChatGPT Luna 5.6 sebagai tutor untuk memahami penerapan arsitektur MVT, pembuatan model, URL, view, template dinamis, migration, pengisian data melalui database, dan pembuatan test case Django. Saya menggunakan AI untuk mendapatkan penjelasan bertahap, memeriksa kemungkinan kesalahan, serta membantu mengecek hasil implementasi. Saya tetap menyesuaikan kode dengan desain dan struktur project saya sendiri, melakukan verifikasi, serta bertanggung jawab memahami dan memeriksa hasil akhirnya.

Log chat AI:
- Tugas 1 : https://share.gemini.google/j5HEMG8OMOUF
- Tugas 2 : https://chatgpt.com/s/cx_6aa807d7051c81918c56e334cabc3eed
