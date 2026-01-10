from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
import datetime

app = Flask(__name__)
app.secret_key = "studyhub"

# WAJIB pakai async_mode eventlet untuk Render
socketio = SocketIO(app, async_mode="eventlet")

# ===== DATA JADWAL =====
jadwal_kuliah = {
    "senin": [
        {"matkul": "Bahasa Indonesia", "jam": "07.30 - 09.00", "ruang": "303", "dosen": "Nurul Hidayah Azmi, M.Hum"},
        {"matkul": "Sejarah Peradaban Islam", "jam": "10.30 - 12.00", "ruang": "303", "dosen": "Imam Adlin Sinaga, ST, M.Ars"},
        {"matkul": "Interaksi Manusia dan Komputer", "jam": "12.00 - 13.30", "ruang": "305", "dosen": "Heri Santoso, M.Kom"},
        {"matkul": "E-Commerce", "jam": "13.30 - 15.00", "ruang": "305", "dosen": "Adnan Buyung Nasution, M.Kom"}
    ],
    "selasa": [
        {"matkul": "Mitigasi Bencana", "jam": "10.30 - 12.00", "ruang": "305", "dosen": "Imam Adlin Sinaga, ST, M.Ars"},
        {"matkul": "Manajemen Organisasi Bisnis", "jam": "13.30 - 15.00", "ruang": "305", "dosen": "Fathiya Hasyifah, M.Kom"},
        {"matkul": "Sistem Operasi", "jam": "15.00 - 16.30", "ruang": "COMP-D", "dosen": "Rahmat Syuhada, M.Kom"}
    ],
    "rabu": [
        {"matkul": "Bahasa Arab", "jam": "09.00 - 10.30", "ruang": "306", "dosen": "Hendrifal"},
        {"matkul": "Analisis Proses Bisnis", "jam": "10.30 - 12.00", "ruang": "305", "dosen": "Adnan Buyung Nasution, M.Kom"}
    ],
    "jumat": [
        {"matkul": "Sistem Manajemen Basis Data", "jam": "07.30 - 09.00", "ruang": "Lab 2", "dosen": "Raissa Amanda Putri, S.Kom, M.TI"}
    ]
}

# ===== LOGIN =====
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        return render_template("chat.html", username=session["username"])
    return render_template("login.html")

# ===== CHAT =====
@socketio.on("send_message")
def chat(data):
    emit("receive_message", data, broadcast=True)

    text = data["message"].lower()

    if "@bot" not in text:
        return

    msg = text.replace("@bot", "").strip()

    hari_list = ["senin", "selasa", "rabu", "kamis", "jumat", "sabtu", "minggu"]
    hari_ini = hari_list[datetime.datetime.today().weekday()]

    # ===== MENU =====
    if msg == "":
        reply = (
            "Hai 👋 Aku Study Hub Bot 🤖\n\n"
            "Aku bisa bantu kamu dengan:\n"
            "1️⃣ Jadwal Kuliah\n"
            "2️⃣ Motivasi Belajar\n\n"
            "Ketik:\n"
            "@bot jadwal\n"
            "@bot motivasi"
        )

    elif msg == "jadwal":
        reply = (
            "📅 Menu Jadwal Kuliah\n\n"
            "Contoh perintah:\n"
            "@bot jadwal hari ini\n"
            "@bot jadwal senin\n"
            "@bot dosen sistem operasi\n"
            "@bot ruang e-commerce"
        )

    elif "jadwal hari ini" in msg:
        if hari_ini in jadwal_kuliah:
            reply = f"📅 Jadwal hari ini ({hari_ini.capitalize()}):\n"
            for m in jadwal_kuliah[hari_ini]:
                reply += f"- {m['matkul']} ({m['jam']} | Ruang {m['ruang']})\n"
        else:
            reply = "Tidak ada jadwal hari ini."

    elif "jadwal" in msg:
        hari = msg.replace("jadwal", "").strip()
        if hari in jadwal_kuliah:
            reply = f"📅 Jadwal {hari.capitalize()}:\n"
            for m in jadwal_kuliah[hari]:
                reply += f"- {m['matkul']} ({m['jam']} | Ruang {m['ruang']})\n"
        else:
            reply = "Jadwal tidak ditemukan."

    elif "dosen" in msg:
        nama = msg.replace("dosen", "").strip()
        reply = "Data dosen tidak ditemukan."
        for hari in jadwal_kuliah.values():
            for m in hari:
                if nama in m["matkul"].lower():
                    reply = f"Dosen {m['matkul']} adalah {m['dosen']}"

    elif "ruang" in msg:
        nama = msg.replace("ruang", "").strip()
        reply = "Data ruang tidak ditemukan."
        for hari in jadwal_kuliah.values():
            for m in hari:
                if nama in m["matkul"].lower():
                    reply = f"{m['matkul']} berada di Ruang {m['ruang']}"

    elif msg == "motivasi":
        reply = "✨ Jangan menyerah yaa, sedikit demi sedikit itu tetap kemajuan 💜"

    else:
        reply = "Aku belum paham 😅 ketik @bot untuk lihat menu."

    emit("receive_message", {
        "username": "🤖 Study Hub Bot",
        "message": reply
    }, broadcast=True)

# ===== RUN SERVER (RENDER READY) =====
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)
