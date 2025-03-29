import os
from flask import Flask, request, render_template, send_file
import whisper

app = Flask(__name__)
model = whisper.load_model("base")

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

        result = model.transcribe(filepath, language="ur")

        def format_timestamp(seconds):
            h = int(seconds // 3600)
            m = int((seconds % 3600) // 60)
            s = int(seconds % 60)
            ms = int((seconds - int(seconds)) * 1000)
            return f"{h:02}:{m:02}:{s:02},{ms:03}"

        srt = ""
        for i, segment in enumerate(result["segments"], 1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()
            srt += f"{i}\n{start} --> {end}\n{text}\n\n"

        srt_path = filepath.rsplit(".", 1)[0] + ".srt"
        with open(srt_path, "w") as f:
            f.write(srt)

        return send_file(srt_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(debug=True)
