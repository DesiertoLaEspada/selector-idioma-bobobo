import os
import subprocess
import json
import webbrowser
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

def cambiar_flags(idioma, progress, status):
    archivos = [archivo for archivo in os.listdir('.') if archivo.endswith('.mkv')]
    for i, archivo in enumerate(archivos, start=1):
        status['text'] = f"Analizando el archivo: {archivo}"

        # Obtener información de las pistas del archivo .mkv
        info = subprocess.run(['mkvmerge', '-J', archivo], capture_output=True, text=True)
        pistas = json.loads(info.stdout)['tracks']

        # Desactivar todas las flags "default" y "forzadas"
        for pista in pistas:
            if pista['type'] == 'audio':
                subprocess.run(['mkvpropedit', archivo, '--edit', f'track:{pista["id"]+1}', '--set', 'flag-default=0', '--set', 'flag-forced=0'], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif pista['type'] == 'subtitles':
                subprocess.run(['mkvpropedit', archivo, '--edit', f'track:{pista["id"]+1}', '--set', 'flag-default=0', '--set', 'flag-forced=0'], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Activar las flags según la selección
        if idioma == 'spa':
            # Establecer audio en español y subtítulos forzados
            for pista in pistas:
                if pista['type'] == 'audio' and pista['properties'].get('language') == 'spa':
                    subprocess.run(['mkvpropedit', archivo, '--edit', f'track:{pista["id"]+1}', '--set', 'flag-default=1'], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if pista['type'] == 'subtitles' and ('Forzados' in pista['properties'].get('name', '') or pista['properties'].get('language') == 'spa'):
                    subprocess.run(['mkvpropedit', archivo, '--edit', f'track:{pista["id"]+1}', '--set', 'flag-forced=1'], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    break  # Solo activar la primera pista forzada

        elif idioma == 'cat':
            # Establecer audio en catalán y subtítulos forzados
            for pista in pistas:
                if pista['type'] == 'audio' and pista['properties'].get('language') == 'cat':
                    subprocess.run(['mkvpropedit', archivo, '--edit', f'track:{pista["id"]+1}', '--set', 'flag-default=1'], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if pista['type'] == 'subtitles' and ('Forçats' in pista['properties'].get('name', '') or pista['properties'].get('language') == 'cat'):
                    subprocess.run(['mkvpropedit', archivo, '--edit', f'track:{pista["id"]+1}', '--set', 'flag-forced=1'], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    break  # Solo activar la primera pista forzada

        elif idioma == 'jpn_spa':
            # Establecer audio en japonés y subtítulos en español
            for pista in pistas:
                if pista['type'] == 'audio' and pista['properties'].get('language') == 'jpn':
                    subprocess.run(['mkvpropedit', archivo, '--edit', f'track:{pista["id"]+1}', '--set', 'flag-default=1'], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Activar la segunda pista de subtítulos en español o la que contenga "Completos"
            spanish_subtitles = [pista for pista in pistas if pista['type'] == 'subtitles' and pista['properties'].get('language') == 'spa']
            if len(spanish_subtitles) > 1:
                subprocess.run(['mkvpropedit', archivo, '--edit', f'track:{spanish_subtitles[1]["id"]+1}', '--set', 'flag-default=1'], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                for pista in spanish_subtitles:
                    if 'Completos' in pista['properties'].get('name', ''):
                        subprocess.run(['mkvpropedit', archivo, '--edit', f'track:{pista["id"]+1}', '--set', 'flag-default=1'], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        break  # Solo activa la pista que contenga "Completos"

        elif idioma == 'jpn_eng':
            # Establecer audio en japonés y subtítulos en inglés
            for pista in pistas:
                if pista['type'] == 'audio' and pista['properties'].get('language') == 'jpn':
                    subprocess.run(['mkvpropedit', archivo, '--edit', f'track:{pista["id"]+1}', '--set', 'flag-default=1'], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if pista['type'] == 'subtitles' and pista['properties'].get('language') == 'eng':
                    subprocess.run(['mkvpropedit', archivo, '--edit', f'track:{pista["id"]+1}', '--set', 'flag-default=1'], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    break  # Solo activar la primera pista forzada

        # Actualiza la barra de progreso
        progress['value'] = (i / len(archivos)) * 100
        progress.update_idletasks()

    status['text'] = "El programa ha terminado."

def open_link(url):
    webbrowser.open(url)

def main():
    window = Tk()
    window.title("Selector de idioma de Bobobo v1.0")
    window.geometry("800x450")
    window.configure(bg='#ADD8E6')

    Label(window, text="Bobobo: Bienvenido al selector de idioma", font=("Helvetica", 15, 'bold'), bg='#ADD8E6', fg='red').pack(pady=20)
    Button(window, text="Castellano", command=lambda: cambiar_flags('spa', progress, status), font=("Helvetica", 12, 'bold'), bg='yellow').pack(fill=X, padx=70, pady=5)
    Button(window, text="Catalán", command=lambda: cambiar_flags('cat', progress, status), font=("Helvetica", 12, 'bold'), bg='yellow').pack(fill=X, padx=70, pady=5)
    Button(window, text="Japonés (Sub. Español)", command=lambda: cambiar_flags('jpn_spa', progress, status), font=("Helvetica", 12, 'bold'), bg='yellow').pack(fill=X, padx=70, pady=5)
    Button(window, text="Japonés (Sub. Inglés)", command=lambda: cambiar_flags('jpn_eng', progress, status), font=("Helvetica", 12, 'bold'), bg='yellow').pack(fill=X, padx=70, pady=5)

    progress = ttk.Progressbar(window, length=500, mode='determinate')
    progress.pack(pady=20)

    status = Label(window, text="", font=("Helvetica", 10), bg='#ADD8E6', fg='blue')
    status.pack(pady=10)

    # Obtiene el directorio actual del script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Carga los iconos de las redes sociales desde el directorio actual
    twitter_icon_path = os.path.join(current_dir, 'icons', 'twitter_icon.png')
    instagram_icon_path = os.path.join(current_dir, 'icons', 'instagram_icon.png')
    youtube_icon_path = os.path.join(current_dir, 'icons', 'youtube_icon.png')
    tiktok_icon_path = os.path.join(current_dir, 'icons', 'tiktok_icon.png')

    # Redimensiona y carga las imágenes
    twitter_icon = ImageTk.PhotoImage(Image.open(twitter_icon_path).resize((20, 20)))
    instagram_icon = ImageTk.PhotoImage(Image.open(instagram_icon_path).resize((20, 20)))
    youtube_icon = ImageTk.PhotoImage(Image.open(youtube_icon_path).resize((20, 20)))
    tiktok_icon = ImageTk.PhotoImage(Image.open(tiktok_icon_path).resize((20, 20)))

    # Crea botones con los iconos de las redes sociales
    Button(window, image=twitter_icon, command=lambda: open_link('https://x.com/desiertoespada')).pack(side=RIGHT, padx=5)
    Button(window, image=youtube_icon, command=lambda: open_link('https://youtube.com/@desiertolaespada')).pack(side=RIGHT, padx=5)
    Button(window, image=instagram_icon, command=lambda: open_link('https://instagram.com/desiertolaespada')).pack(side=RIGHT, padx=5)
    Button(window, image=tiktok_icon, command=lambda: open_link('https://www.tiktok.com/@desiertoespada')).pack(side=RIGHT, padx=5)
    
    Label(window, text="", font=("Helvetica", 10, 'bold'), bg='#ADD8E6', fg='blue').pack(side=RIGHT, padx=0)
    link = Label(window, text="por Desierto La Espada", font=("Helvetica", 10, 'bold'), bg='#ADD8E6', fg='blue')
    link.pack(side=RIGHT, padx=0)
    
    window.mainloop()

if __name__ == "__main__":
    main()