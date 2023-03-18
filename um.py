import yt_dlp
import ffmpeg
import PySimpleGUI as sg

def download_audio(url):
    options = {
    'outtmpl': '%(title)s.%(ext)s',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'ffmpeg_location': 'C:/ffmpeg/ffmpeg-master-latest-win64-gpl/bin',
}

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            audio_url = info_dict['url']
            title = info_dict['title']
            
            (
                ffmpeg
                .input(audio_url)
                .output(f"{title}.mp3", 
                        codec='libmp3lame', 
                        audio_bitrate='192k',
                        ac=2)
                .run()
            )
        sg.Popup(f'{title} convertido com sucesso!')
    except yt_dlp.utils.DownloadError:
        sg.Popup('Erro ao converter o vídeo. Verifique a URL e sua conexão com a internet.')
    except AttributeError as e:
        if "'module' object has no attribute 'input'" in str(e):
            sg.Popup('Erro ao converter o vídeo. Verifique se o FFmpeg está instalado corretamente.')
        else:
            raise e
        
sg.theme('DefaultNoMoreNagging')  # Define a aparência dos elementos da interface

layout = [[sg.Text('Insira a URL do vídeo do YouTube que deseja converter para MP3')],
          [sg.Input(key='-URL-')],
          [sg.Button('Converter'), sg.Button('Cancelar')]]  # Define a interface gráfica

window = sg.Window('Conversor de Vídeo para MP3', layout)  # Cria a janela da interface

while True:
    event, values = window.read()  # Lê os eventos da interface
    
    if event == sg.WINDOW_CLOSED or event == 'Cancelar':  # Fecha a janela se clicar em Cancelar ou no 'X'
        break
    
    if event == 'Converter':  # Executa o código de conversão quando clicar em Converter
        url = values['-URL-']
        download_audio(url)
        
window.close()  # Fecha a janela da interface ao final do programa
