import asyncio
from anime_cli.api import AnimeSamaAPI
import subprocess
import yt_dlp
from colorama import Fore, Style, init
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.shortcuts import radiolist_dialog
import re
import pyperclip
api = AnimeSamaAPI()

init(autoreset=True)

def extract_direct_url(embed_url):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "format": "best",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(embed_url, download=False)
        return info["url"]  # Lien direct vers la vidéo


class AnimeCompleter(Completer):
    def __init__(self, api):
        self.api = api
        self.last_query = ""
        self.last_results = []

    def get_completions(self, document, complete_event):
        # Nécessaire pour l'API de prompt_toolkit, mais inutilisé ici
        return iter([])

    async def get_completions_async(self, document, complete_event):
        text = document.text
        if len(text) < 2:
            return
        if text.lower() != self.last_query.lower():
            self.last_results = await self.api.search(text)
            self.last_query = text
        # Filtrage local très strict : la séquence tapée doit apparaître dans le titre (insensible à la casse)
        filtered = [
            anime for anime in self.last_results
            if text.lower() in anime['name'].lower()
        ]
        for anime in filtered[:10]:
            yield Completion(anime['name'], start_position=-len(text))

async def interactive_search(api):
    session = PromptSession()
    completer = AnimeCompleter(api)
    print(Fore.YELLOW + "Recherche anime :" + Style.RESET_ALL)
    anime_name = await session.prompt_async(
        "> ",
        completer=completer,
        complete_while_typing=True
    )
    return anime_name

async def choose_from_list(prompt_text, items):
    for idx, item in enumerate(items):
        print(f"{idx+1}. {item}")
    while True:
        choice = input(prompt_text)
        if choice.isdigit() and 1 <= int(choice) <= len(items):
            return int(choice) - 1
        print("Choix invalide.")

async def choose_from_list_interactive(title, items):
    print(Fore.YELLOW + f"\n{title}" + Style.RESET_ALL)
    for idx, item in enumerate(items):
        print(f"{idx+1}. {item}")
    print()
    while True:
        choix = input(Fore.YELLOW + "Numéro : " + Style.RESET_ALL)
        if choix.isdigit():
            choix = int(choix)
            if 1 <= choix <= len(items):
                return choix - 1
        print(Fore.RED + "Choix invalide." + Style.RESET_ALL)

def print_logo():
    print(Fore.RED + Style.BRIGHT + r"""
 _                         ____ _     ___ 
| |    __ _ _ __ ___  ____/ ___| |   |_ _|
| |   / _` | '_ ` _ \|_  / |   | |    | | 
| |__| (_| | | | | | |/ /| |___| |___ | | 
|_____\__,_|_| |_| |_/___|\____|_____|___|
                                            
""" + Style.RESET_ALL)
    print(Fore.YELLOW + Style.BRIGHT + "           Bienvenue sur lamz-cli !\n" + Style.RESET_ALL)
    print(Fore.YELLOW + "="*50 + Style.RESET_ALL)

async def main():
    print_logo()
    while True:
        # 1. Recherche interactive
        anime_name = await interactive_search(api)
        results = await api.search(anime_name)
        if not results:
            print("Aucun résultat.")
            continue
        anime_names = [a['name'] for a in results] + ["Quitter / Nouvelle recherche"]
        anime_idx = await choose_from_list_interactive("Choisis un anime", anime_names)
        if anime_idx is None or anime_idx == len(anime_names) - 1:
            continue

        anime_obj = api.get_anime_obj(anime_idx)

        # 2. Choix de la saison
        while True:
            seasons = await anime_obj.seasons()
            season_names = [s.name for s in seasons] + ["Retour / Quitter"]
            season_idx = await choose_from_list_interactive("Choisis une saison", season_names)
            if season_idx is None or season_idx == len(season_names) - 1:
                break  # Retour à la recherche d'anime

            season = seasons[season_idx]

            # 3. Choix de l'épisode
            while True:
                eps = await season.episodes()
                ep_names = [e.name for e in eps] + ["Retour / Quitter"]
                ep_idx = await choose_from_list_interactive("Choisis un épisode", ep_names)
                if ep_idx is None or ep_idx == len(ep_names) - 1:
                    break  # Retour au choix de la saison

                ep = eps[ep_idx]
                # 4. Lecture directe dans VLC
                embed_url = ep.best(["vostfr", "vf"])
                print("Extraction du lien direct...")
                direct_url = extract_direct_url(embed_url)
                print("Lecture dans VLC...")
                subprocess.run([
                    r"C:\Program Files\VideoLAN\VLC\vlc.exe",
                    "--no-sub-autodetect-file",
                    "--sub-track=-1",
                    "--no-osd",
                    direct_url
                ])
                # Après la lecture, on revient au choix d'épisode

if __name__ == "__main__":
    asyncio.run(main())