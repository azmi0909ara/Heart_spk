## 🧠 Analisis dan Penjelasan Logika Fuzzy dalam Pengambilan Keputusan

Proyek ini menggunakan **algoritma Logika Fuzzy (Fuzzy Logic)** sebagai dasar pengambilan keputusan untuk mendiagnosis tingkat risiko penyakit jantung.  
Fuzzy Logic dipilih karena mampu menangani **ketidakpastian** dan **nilai-nilai yang bersifat tidak pasti** dalam data kesehatan — seperti tekanan darah, kolesterol, dan detak jantung — yang tidak selalu bisa dikategorikan secara tegas (misalnya “tinggi” atau “rendah”).

Pada sistem ini, setiap variabel kesehatan seperti **usia**, **tekanan darah (trestbps)**, **kolesterol (chol)**, **detak jantung maksimum (thalach)**, dan **oldpeak** diubah menjadi nilai keanggotaan fuzzy menggunakan fungsi *membership* seperti `rendah`, `normal`, atau `tinggi`.  
Nilai-nilai ini kemudian diproses melalui **aturan IF–THEN**, contohnya:

> *IF usia tua AND tekanan darah tinggi AND kolesterol tinggi THEN risiko tinggi*

Melalui kombinasi aturan-aturan tersebut, sistem menghasilkan **nilai risiko akhir** dalam rentang 0–100. Proses akhir disebut **defuzzifikasi**, yang mengubah hasil fuzzy menjadi nilai numerik pasti agar dapat diklasifikasikan menjadi tiga kategori:
- **0–39:** Risiko Rendah  
- **40–69:** Risiko Sedang  
- **70–100:** Risiko Tinggi

---

## 🧩 Analisis Logika Sistem

Sistem ini bekerja seperti cara berpikir manusia ketika menilai kondisi kesehatan jantung seseorang.  
hanya dengan melihat satu angka (misalnya tekanan darah tinggi = berbahaya), sistem fuzzy mencoba **memahami konteks keseluruhan** dari beberapa faktor seperti usia, kolesterol, tekanan darah, detak jantung, dan nilai oldpeak.

Setiap faktor tersebut tidak dinilai dengan batas tegas seperti “tinggi” atau “rendah”, tetapi dalam **tingkat keabu-abuan** — misalnya “agak tinggi”, “cukup normal”, atau “sedikit rendah”.  
Inilah yang membuat logika fuzzy mirip dengan cara dokter menilai pasien: **tidak hitam putih, tapi berdasarkan tingkat kemungkinan**.

Contohnya:
- Jika seseorang **masih muda** dan **detak jantungnya bagus**, meskipun kolesterolnya agak tinggi, sistem akan menilai risikonya masih **rendah atau sedang**.  
- Tapi kalau seseorang **sudah tua** dan **tekanan darah serta kolesterolnya tinggi**, sistem akan memberikan keputusan **risiko tinggi**, karena gabungan faktor tersebut memperkuat kemungkinan adanya gangguan jantung.

Setelah semua faktor dievaluasi menggunakan aturan fuzzy (aturan IF–THEN seperti “Jika usia tua DAN kolesterol tinggi maka risiko tinggi”), sistem akan menghasilkan **skor risiko antara 0–100**.  
Semakin besar nilainya, semakin besar juga kemungkinan seseorang mengalami masalah jantung.

Dengan cara ini, sistem tidak hanya menghitung angka secara kaku, tapi juga **meniru intuisi manusia dalam pengambilan keputusan medis** — mempertimbangkan berbagai aspek secara bersamaan untuk memberikan hasil yang **lebih adil, fleksibel, dan realistis**.

---

📘 *Dibangun menggunakan Python, Streamlit, dan scikit-fuzzy — bagian dari proyek SPK (Sistem Penunjang Keputusan) oleh Azmi .A, 2025.*

