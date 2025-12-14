# 🎮 WARRIOR RUSH  
Game 2D Berbasis Python (Pygame) – UAS Pemrograman Berorientasi Objek

---

## 📌 Deskripsi Aplikasi
Warrior Rush adalah game 2D action berbasis Python yang dikembangkan menggunakan library Pygame. Pemain mengendalikan karakter warrior untuk bertahan hidup dari serangan musuh (enemy) yang muncul secara terus-menerus dari berbagai arah. Game ini dikembangkan sebagai tugas Ujian Akhir Semester (UAS) mata kuliah Pemrograman Berorientasi Objek dengan tujuan menerapkan konsep Object-Oriented Programming (OOP) secara nyata.

---

## 🎯 Tujuan Pengembangan
1. Menerapkan konsep Pemrograman Berorientasi Objek (OOP)
2. Mengimplementasikan sistem interaksi pengguna yang sederhana dan intuitif
3. Membangun game 2D dengan fitur pergerakan, serangan, musuh, dan skor
4. Menyusun struktur program yang rapi dan mudah dikembangkan

---

## 🧩 Penerapan Konsep OOP

### 1. Encapsulation
Encapsulation diterapkan dengan membungkus atribut dan metode ke dalam class. Atribut seperti posisi, ukuran, dan HP tidak dimanipulasi secara langsung, melainkan melalui method tertentu.

Contoh penerapan:
- Class `GameObject`
- Method `take_damage()` untuk mengurangi HP secara terkontrol

### 2. Inheritance
Inheritance digunakan untuk menghindari duplikasi kode dan membangun struktur class yang rapi. Class `Player` dan `Enemy` merupakan turunan dari class `GameObject`.

Contoh penerapan:
- `class Player(GameObject)`
- `class Enemy(GameObject)`

### 3. Polymorphism
Polymorphism diterapkan melalui penggunaan method dengan nama yang sama namun memiliki perilaku yang berbeda pada class yang berbeda.

Contoh penerapan:
- Method `move()` pada Player dan Enemy
- Method `draw()` pada Player dan Enemy

### 4. Abstraction
Abstraction diterapkan dengan menyederhanakan kompleksitas sistem. Class `GameManager` hanya berinteraksi dengan method umum seperti `update()` dan `draw()` tanpa mengetahui detail implementasi setiap objek.

---

## 🎮 Fitur Utama Game
- Pergerakan player menggunakan tombol W, A, S, dan D
- Sistem serangan menggunakan tombol SPASI
- Enemy mengejar player secara otomatis
- Sistem skor dan kill count
- Menu awal, gameplay, dan game over
- Tombol Retry dan Menu
- Efek suara dan background music

---

## 🕹️ Kontrol Game

| Tombol | Fungsi |
|------|-------|
| W | Bergerak ke atas |
| A | Bergerak ke kiri |
| S | Bergerak ke bawah |
| D | Bergerak ke kanan |
| SPACE | Menyerang |
| Mouse | Navigasi menu |

---

## 🗂️ Struktur File
WarriorRush/
│
├── UAS
│   ├── main.py
│   ├── mywarrior.png
│   ├── enemy.png
│   ├── menu_bg.png
│   ├── game_bg.png
│   ├── gameover_bg.png
│   ├── bgm.wav
│   ├── attack.wav
└── README.md


---

## 👨‍💻 Pengembang
Nama  : Syawailie Syaf Anhar
NIM   : 24091397053
Mata Kuliah : Pemrograman Berorientasi Objek  
Tahun : 2025  

---
