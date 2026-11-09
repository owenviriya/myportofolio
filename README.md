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

Buka http://localhost:8000/ pada browser. Untuk menjalankan seluruh test (termasuk test API DRF):

```bash
python manage.py test main
```

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


### Tugas 3

1. Alasan menggunakan ModelForm dan CSRF token

Saya menggunakan ModelForm karena field-field pada Modelform bisa dibuat berdasarkan model Django, sehingga tidak perlu untuk menghubungkan setiap input ke model-model secara manual (Kalau pakai HTML biasa). Saya juga bisa mengatur label dan widget field melalui form, Django juga bisa membantu memeriksa apakah data yang diisi oleh pengguna sudah sesuai spesifikasi (tidak boleh kosong ataupun harus format tertentu) sebelum disimpan. Setelah form valid, form.save() dipakai untuk membuat data baru atau memperbarui data yang sudah ada. Saya menambahkan {% csrf_token %} agar Django dapat memeriksa token pada request POST dan membantu mencegah situs lain mengirim request palsu melalui browser pengguna.

2. Alasan JSON banyak digunakan dibandingkan XML

Menurut saya, JSON lebih sering digunakan karena bentuknya ringkas dan cukup mudah dibaca, terutama karena strukturnya mirip object dan array yang biasa dipakai JavaScript. Browser dan banyak bahasa pemrograman juga menyediakan cara yang mudah untuk membaca JSON, sehingga format ini lebih baik untuk bertukar data melalui API. XML tetap bisa digunakan untuk menyimpan data, tetapi tag pembuka dan penutupnya biasanya membuat data menjadi lebih panjang. Untuk kebutuhan aplikasi web seperti portofolio saya, JSON lebih sederhana untuk dikirim dan diproses.

3. Alur pengiriman data portofolio dalam JSON

Pada bagian Education, pertama browser meminta halaman /education/, lalu view show_education memanggil get_education_json untuk mengambil data dari database. View JSON tersebut dapat menyaring data berdasarkan nama institusi, kemudian serializers.serialize("json", education) mengubah queryset Django menjadi JSON yang dikirim dengan content type application/json. Serialization diperlukan karena queryset dan object Django adalah object Python yang tidak bisa langsung dikirim sebagai JSON. Setelah menerima response, show_education membaca isinya dan memakai serializers.deserialize untuk mengubah JSON kembali menjadi object Django. Object tersebut dimasukkan ke context dan digunakan oleh template education.html untuk menampilkan data pendidikan.


### Tugas 5

1. Fungsi debouncing pada pencarian AJAX

Debouncing adalah teknik untuk menunda pemanggilan suatu fungsi sampai tidak ada input baru selama durasi waktu tertentu. Pada fitur pencarian, setiap kali pengguna mengetik, timer sebelumnya dibatalkan dan timer baru dimulai. Request pencarian baru dikirim setelah pengguna berhenti mengetik, misalnya selama 300 milidetik. Dengan begitu, browser tidak mengirim request untuk setiap huruf yang diketik, sehingga jumlah request dan beban server dapat dikurangi.

2. Fungsi 'await' ketika menggunakan 'fetch()'

'fetch()' mengembalikan Promise karena browser perlu menunggu proses komunikasi dengan server. 'await' membuat eksekusi di dalam fungsi 'async' menunggu Promise tersebut selesai sebelum melanjutkan ke baris berikutnya. Setelah response diterima, saya bisa memeriksa statusnya dan membaca data JSON dengan 'await response.json()'. Tanpa 'await', kode langsung berjalan sementara hasil 'fetch()' masih berupa Promise, sehingga response atau data JSON belum siap digunakan.

3. XSS pada data yang ditampilkan melalui JavaScript

XSS (Cross-Site Scripting) adalah serangan ketika data berbahaya dari pengguna diperlakukan sebagai kode dan dijalankan di browser pengunjung. Pada halaman yang membuat HTML dengan JavaScript, nilai dari server bisa menjadi berbahaya jika langsung dimasukkan ke 'innerHTML', karena browser akan menafsirkannya sebagai markup. Template Django biasanya melakukan autoescape pada nilai yang dirender, sedangkan HTML yang dirakit sendiri melalui JavaScript perlu diamankan secara eksplisit. Karena itu, nilai teks di-escape sebelum dimasukkan ke HTML, dan input teks juga dibersihkan di server menggunakan 'strip_tags' pada form.

### Tugas 6

1. REST dan perbedaan PUT dengan PATCH

REST (Representational State Transfer) adalah gaya untuk merancang web API. Data diperlakukan sebagai resource yang ditunjuk URL, sedangkan HTTP method menyatakan tindakannya. Contohnya, `/api/v1/education/` menunjuk kumpulan data Education; `GET` membaca, `POST` membuat, `PUT` atau `PATCH` mengubah, dan `DELETE` menghapus data. JSON hanya format pertukaran data, jadi API yang mengembalikan JSON belum tentu RESTful. API juga perlu memakai resource URL, method, dan status HTTP secara konsisten. Misalnya, tindakan hapus lebih tepat dikirim sebagai `DELETE /api/v1/education/<uuid>/` daripada `POST /education/delete/<uuid>/`.

PUT mengirim representasi lengkap untuk mengganti data, sehingga semua field wajib harus disertakan. PATCH mengirim hanya field yang ingin diubah. PUT cocok untuk mengganti seluruh isi entri Education, sedangkan PATCH cocok untuk memperbarui periodenya saja. Pada proyek ini, form edit menggunakan PATCH.

2. Peran serializer pada Django REST Framework

Serializer bekerja dua arah. Saat membaca data, serializer mengubah objek model menjadi data yang dapat dirender sebagai JSON. Saat menerima input, serializer memvalidasi dan membersihkan data sebelum menyimpannya ke model. Dibandingkan merakit dictionary secara manual dengan `JsonResponse` seperti pada Tutorial 05, serializer membuat struktur data dan validasi berada di satu tempat. Field yang dikirim dapat ditulis eksplisit, field hasil perhitungan dapat dibuat read-only, dan error validasi dapat dikirim per field dengan status 400. `ModelSerializer` juga menyediakan pola pembuatan dan pembaruan model, sehingga kode view lebih ringkas dan tidak perlu merakit response satu per satu.

3. Perbedaan autentikasi dan otorisasi

Autentikasi menjawab siapa yang mengirim request, sedangkan otorisasi menentukan tindakan apa yang boleh dilakukan pengguna tersebut. Pada proyek ini, `SessionAuthentication` mengenali pengguna dari sesi login Django dan mengisi `request.user`. Permission class seperti `IsPortfolioOwnerOrEditorOrReadOnly` kemudian memeriksa hak aksesnya. Pemeriksaan ini harus dilakukan di server karena menyembunyikan tombol di template hanya mengubah tampilan; pengguna masih dapat mengirim request langsung ke API. Karena itu, test juga memastikan request yang ditolak tidak mengubah data di database.

4. CSRF pada SessionAuthentication dan keterbatasan `force_authenticate`

Pada `SessionAuthentication`, browser mengirim cookie sesi secara otomatis. Jika request tulis tidak memakai token CSRF, situs lain dapat mencoba membuat browser pengguna yang sedang login mengirim perubahan atas nama pengguna tersebut. Karena itu, request `POST`, `PUT`, `PATCH`, dan `DELETE` dari halaman mengirim token melalui header `X-CSRFToken`.

`force_authenticate` langsung menetapkan pengguna pada request dan melewati alur login sesi serta pemeriksaan CSRF. Tes yang memakai cara ini cocok untuk menguji permission, tetapi tidak membuktikan perlindungan CSRF. Untuk mengujinya, saya menggunakan `APIClient(enforce_csrf_checks=True)` dan `.login()`, lalu memeriksa bahwa request tanpa token ditolak dan request dengan token berhasil.


## AI Disclosure

Dalam pengembangan website ini, saya menggunakan Gemini 3.6 Flash sebagai alat bantu belajar, brainstorming, dan debugging. Saya memberikan potongan HTML/CSS, screenshot, serta pesan error untuk memperoleh penjelasan dan alternatif solusi. Gemini membantu saya memahami elemen semantik HTML5, timeline, pseudo-element `::before`, responsive layout, media query, sticky navbar, smooth scrolling, Experience, Skills, efek hover, serta Conventional Commits. Saya tidak menyalin jawabannya secara langsung, tetapi menyesuaikan setiap saran dengan struktur proyek dan desain yang saya inginkan. Hasil akhir saya verifikasi melalui browser, DevTools, perangkat seluler, dan `python manage.py check`. Karena beberapa saran AI dapat bersifat umum atau kurang sesuai dengan kondisi repository, keputusan desain saya, implementasi, pengujian, dan perbaikan akhir tetap saya lakukan sendiri.

Pada Tugas 2, saya juga menggunakan ChatGPT Luna 5.6 sebagai tutor untuk memahami penerapan arsitektur MVT, pembuatan model, URL, view, template dinamis, migration, pengisian data melalui database, dan pembuatan test case Django. Saya menggunakan AI untuk mendapatkan penjelasan bertahap, memeriksa kemungkinan kesalahan, serta membantu mengecek hasil implementasi. Saya tetap menyesuaikan kode dengan desain dan struktur project saya sendiri, melakukan verifikasi, serta bertanggung jawab memahami dan memeriksa hasil akhirnya.

Pada Tugas 3, saya menggunakan ChatGPT Luna 5.6 sebagai tutor untuk memahami ModelForm, CSRF, serialization dan deserialization JSON, serta alur CRUD dalam Django. Saya menggunakan AI untuk mendapatkan penjelasan bertahap, memeriksa kemungkinan kesalahan, serta membantu mengecek hasil implementasi. Saya tetap bertanggung jawab memahami kode dan melakukan verifikasi terhadap hasil akhir.

Pada Tugas 4, saya menggunakan ChatGPT Luna 6 sebagai tutor interaktif untuk memahami autentikasi, otorisasi, session, cookie, dan CSRF, serta merencanakan penerapan peran Editor melalui Django Group. Saya meminta panduan bertahap, lalu mengimplementasikan sendiri pemeriksaan hak akses CRUD, relasi ManyToMany User pada Experience, migrasi database, dan komponen star yang dapat digunakan ulang. ChatGPT membantu meninjau perubahan pada view, template, migrasi, dan serialisasi JSON, serta menjelaskan kesalahan logika yang saya perbaiki. ChatGPT juga membantu memeriksa status migrasi, menjalankan pemeriksaan Django, dan memastikan development server dapat dimulai. Saya tetap bertanggung jawab memahami saran AI, menentukan implementasi akhir, dan melakukan verifikasi akhir terhadap alur aplikasi.

Pada Tugas 5, saya menggunakan ChatGPT Luna 6 sebagai tutor untuk memahami Fetch API, Promise dan 'await', debouncing, CSRF, serta perlindungan XSS. Saya meminta penjelasan secara bertahap, lalu menggunakan pola Experience sebagai referensi untuk menerapkannya pada Education dan Skills. ChatGPT membantu meninjau kode pada template, view, URL, dan ModelForm, termasuk endpoint JSON manual, pencarian, modal tambah data, toast, dan sanitasi input. Saya tetap bertanggung jawab memahami saran AI, menentukan implementasi akhir, dan melakukan verifikasi akhir terhadap alur aplikasi.

Pada Tugas 6, saya menggunakan ChatGPT melalui Codex (GPT-6) sebagai tutor dan reviewer untuk memahami REST, serializer, permission, session, dan CSRF, lalu menerapkan pola DRF pada bagian Experience, Education, Skills, dan Language. Saya meminta penjelasan Tutorial 7 secara bertahap sambil mencocokkan contoh kode dengan struktur proyek, kemudian meminta review saat membangun serializer, API view, URL, dan interaksi Fetch di halaman. AI juga membantu menyusun test API Education dan menyesuaikan test halaman Education yang sebelumnya masih mengharapkan endpoint JSON manual. Saya meninjau dan menyesuaikan kode dengan model serta alur proyek, lalu menjalankan `python manage.py test main`; 95 test lulus pada verifikasi terbaru. Saya menggunakan AI sebagai tutor dan pemeriksa, tetapi tetap bertanggung jawab memahami, memilih, dan memeriksa perubahan yang digunakan.



Log chat AI:
- Tugas 1 : https://share.gemini.google/j5HEMG8OMOUF
- Tugas 2 : https://chatgpt.com/s/cx_6aa807d7051c81918c56e334cabc3eed
- Tugas 3 : https://chatgpt.com/s/cx_6ab14304123c8191a77b0f9ac4bf6fa6
- Tugas 4 : https://chatgpt.com/s/cx_6aba610172e081919fe2ffda23259e65
- Tugas 5 : https://chatgpt.com/s/cx_6ac397aacbc88191bcde9421e737c582
- Tugas 6 : https://chatgpt.com/s/cx_6af190cb74bc8191a76af885996b4f78
