import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
import datetime
import os

app = Flask(__name__)
app.secret_key = "studyhub"

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

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        return render_template("chat.html", username=session["username"])
    return render_template("login.html")

@socketio.on("send_message")
def chat(data):
    emit("receive_message", data, broadcast=True)

    text = data["message"].lower()
    if "@bot" not in text:
        return

    msg = text.replace("@bot", "").strip()
    hari_list = ["senin","selasa","rabu","kamis","jumat","sabtu","minggu"]
    hari_ini = hari_list[datetime.datetime.today().weekday()]

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
            "📅 *Menu Jadwal Kuliah*\n\n"
            "Ketik:\n"
            "@bot jadwal hari ini\n"
            "@bot jadwal senin\n"
            "@bot dosen sistem operasi"
        )

    elif "jadwal hari ini" in msg:
        if hari_ini in jadwal_kuliah:
            reply = f"📅 Jadwal hari ini ({hari_ini.capitalize()}):\n"
            for m in jadwal_kuliah[hari_ini]:
                reply += f"- {m['matkul']} ({m['jam']}, Ruang {m['ruang']})\n"
        else:
            reply = "Tidak ada jadwal hari ini."

    elif "jadwal" in msg:
        hari = msg.replace("jadwal", "").strip()
        if hari in jadwal_kuliah:
            reply = f"📅 Jadwal {hari.capitalize()}:\n"
            for m in jadwal_kuliah[hari]:
                reply += f"- {m['matkul']} ({m['jam']}, Ruang {m['ruang']})\n"
        else:
            reply = "Tidak ada jadwal di hari tersebut."

    elif msg == "motivasi":
        reply = "✨ Jangan menyerah. Sedikit demi sedikit tetap kemajuan 💜"

    else:
        reply = "Maaf aku belum paham 😅 ketik @bot"

    emit("receive_message", {
        "username": "🤖 Study Hub Bot",
        "message": reply
    }, broadcast=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    socketio.run(app, host="0.0.0.0", port=port)
