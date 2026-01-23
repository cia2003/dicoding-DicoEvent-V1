# dicoding-DicoEvent-V1 & V2 (Rating Project: 5 Stars)
Repositori ini merupakan pengerjaan tugas proyek tahap pertama dan kedua fundamental back-end

# Studi Kasus 
## (tahap 1)
Sebagai seorang Back-End Developer yang berpengalaman, Anda baru saja bergabung dengan startup yang ambisius, DicoTech. Startup ini berencana meluncurkan DicoEvent, sebuah aplikasi manajemen event yang inovatif dan Anda baru saja ditugaskan untuk pengembangan DicoEvent.

Dalam fase pengembangan awal, tugas Anda adalah membangun RESTful API dasar yang akan menjadi tahap pertama dari pengembangan DicoEvent. RESTful API ini akan menangani segala aspek terkait dengan event, seperti menambah, menghapus, dan memodifikasi informasi event di dalam database. Fase ini kritikal dalam memastikan fondasi yang kuat untuk pengembangan fitur lebih lanjut.

## (tahap 2)
Setelah sukses dalam pengembangan dan peluncuran DicoEvent versi 1, platform ini telah menjadi salah satu favorit bagi penyelenggara event untuk mengelola dan menjalankan acara mereka dengan lebih efisien. DicoTech berambisi untuk mengembangkan DicoEvent lebih lanjut.

Saat ini, DicoTech sedang bersiap untuk peluncuran DicoEvent versi 2. Berdasarkan feedback dari pengguna, ada beberapa fitur yang sangat diharapkan, termasuk kemampuan untuk mengirimkan email reminder ke peserta event dan mengunggah gambar kustom untuk setiap acara yang dapat digunakan sebagai materi promosi atau identitas visual acara. Selain itu, perlu untuk meningkatkan performa RESTful API DicoEvent agar meningkatkan pengalaman pengguna.

------------
# Hasil Gambar ERD
<img src="https://github.com/cia2003/dicoding-DicoEvent-V1/blob/main/ERD-DicoEvent-versi-1.png" alt="ERD-DicoEvent-versi-1" width="700" height="500">

------------
# Cara menjalankan
1. Setelah clone atau unduh file, bisa masuk ke environment-nya dulu
   ```
   env\Scripts\activate # khusus windows
   ```
2. Kemudian, jalankan server
   ```
   python manage.py runserver
   ```
3. Kalau mau hapus semua data (termasuk superuser), bisa seperti ini
   ```
   python manage.py flush
   ```

   Setelah dihapus semua data, bisa buat dulu untuk superusernya dengan cara
   ```
   python manage.py createsuperuser
   ```
   Di situlah Anda memasukkan nama, email, dan password
