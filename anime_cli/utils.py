import subprocess

def play_video(url, player="vlc"):
    try:
        subprocess.run([player, url])
    except FileNotFoundError:
        print(f"Le lecteur {player} n'est pas installé ou introuvable dans le PATH.")