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

### Tugas 1

1. Penggunaan Elemen Semantik HTML5

Ya, saya menggunakan beberapa elemen semantik HTML5 seperti section dan article. Elemen section saya gunakan untuk memisahkan antara bagian Profile, Education, Experience, dan Skills. Elemen article juga saya gunakan untuk membuat setiap subbagian Education dan juga Experience karena masing-masing merupakan konten yang berdiri sendiri. Penggunaan elemen-elemen semantik juga berfungsi untuk membuat struktur kode HTML menjadi lebih rapi dan readable untuk saya, yang membuat pengembangan selanjutnya bisa lebih mudah.

2. Tantangan Responsive Layout

Tantangan yang saya temukan adalah ketika mencoba menyesuaikan navbar, kartu Experience, logo, dan skill tags agar tetap rapi pada layar kecil. Navbar di mobile awalnya menggunakan layout 1 baris seperti di dekstop, namun ternyata tulisan 'Skills' itu kepotong saat membuka tampilan mobile dan teks Experience yang panjang membuat kartu melebar keluar dari layar. Saya mengatasinya dengan mengatur ulang navbar menggunakan Grid, mengecilkan logo dan padding pada kartu, serta menggunakan overflow-wrap agar teks yang panjang dapat turun ke baris berikutnya. Saya mengevaluasi hasilnya melalui responsive mode di DevTools dengan mencoba beberapa ukuran layar dan memperbaiki bagian yang terlihat kurang enak dilihat.

3. Keterbatasan Static Web

Karena website ini masih bersifat static web, sebagian besar informasi masih ditulis langsung di dalam file HTML. Kalau saya ingin mengubah pengalaman, pendidikan, atau skills, saya harus mengedit file, melakukan commit, dan melakukan deployment ulang. Website ini belum ada sistem untuk mengelola konten secara dinamis.
Pada iterasi berikutnya, saya ingin coba menambahkan model Django untuk Project, Experience, dan Education. Saya juga ingin membuat halaman admin agar konten portofolio dapat diperbarui tanpa mengubah HTML secara manual.


## AI Disclosure

Dalam pengembangan website ini, saya menggunakan Gemini 3.6 Flash sebagai alat bantu belajar, brainstorming, dan debugging. Saya memberikan potongan HTML/CSS, screenshot, serta pesan error untuk memperoleh penjelasan dan alternatif solusi. Gemini membantu saya memahami elemen semantik HTML5, timeline, pseudo-element `::before`, responsive layout, media query, sticky navbar, smooth scrolling, Experience, Skills, efek hover, serta Conventional Commits. Saya tidak menyalin jawabannya secara langsung, tetapi menyesuaikan setiap saran dengan struktur proyek dan desain yang saya inginkan. Hasil akhir saya verifikasi melalui browser, DevTools, perangkat seluler, dan `python manage.py check`. Karena beberapa saran AI dapat bersifat umum atau kurang sesuai dengan kondisi repository, keputusan desain saya, implementasi, pengujian, dan perbaikan akhir tetap saya lakukan sendiri.

Log chat Gemini:
- Tugas 1 : https://share.gemini.google/j5HEMG8OMOUF
