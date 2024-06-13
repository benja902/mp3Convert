from flask import Flask, request, send_file, render_template
from pytube import YouTube
from pydub import AudioSegment
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/download', methods=['GET'])
def download_youtube_video_as_mp3():
    url = request.args.get('url')
    output_path = "./mp3"

    # Descargar el video de YouTube
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    video_file = video.download(output_path=output_path)
    
    # Convertir el archivo de video a MP3
    base, ext = os.path.splitext(video_file)
    mp3_file = base + '.mp3'
    
    audio = AudioSegment.from_file(video_file)
    audio.export(mp3_file, format='mp3')
    
    # Eliminar el archivo de video original
    os.remove(video_file)
    
    return send_file(mp3_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
