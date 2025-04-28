import pickle
import os
from anime_sama_api import AnimeSama
import inspect

SEARCH_CACHE = "anime_search_cache.pkl"

class AnimeSamaAPI:
    def __init__(self, site_url="https://anime-sama.fr/"):
        self.api = AnimeSama(site_url)
        self.last_search = self.load_cache()
        self._last_results = None  # Sera rempli après un search

    async def search(self, query):
        results = await self.api.search(query)
        self._last_results = results
        self.last_search = [{"name": a.name, "url": a.url} for a in results]
        self.save_cache(self.last_search)
        return self.last_search

    def get_anime(self, idx):
        return self.last_search[idx]

    def get_anime_obj(self, idx):
        if self._last_results is None:
            raise Exception("Lance d'abord la commande 'search' dans la même session.")
        return self._last_results[idx]

    async def get_episodes_from_catalogue(self, catalogue):
        episodes = []
        seasons = await catalogue.seasons()
        for season in seasons:
            eps = await season.episodes()
            for ep in eps:
                url_info = ep.best(["vostfr", "vf"])
                episodes.append({"name": ep.name, "url": url_info})
        return episodes

    async def get_episodes(self, anime_idx):
        if self._last_results is None:
            raise Exception("Lance d'abord la commande 'search' dans la même session.")
        catalogue = self._last_results[anime_idx]
        return await self.get_episodes_from_catalogue(catalogue)

    def save_cache(self, data):
        with open(SEARCH_CACHE, "wb") as f:
            pickle.dump(data, f)

    def load_cache(self):
        if os.path.exists(SEARCH_CACHE):
            with open(SEARCH_CACHE, "rb") as f:
                try:
                    return pickle.load(f)
                except EOFError:
                    return []
        return []