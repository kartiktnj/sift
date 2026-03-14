import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, "cache")


def get_cache_path(video_id, length):
    return os.path.join(CACHE_DIR, f"{video_id}_{length}.json")


def load_from_cache(video_id, length):
    path = get_cache_path(video_id, length)

    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)

    return None


def save_to_cache(video_id, length, data):
    path = get_cache_path(video_id, length)

    os.makedirs(CACHE_DIR, exist_ok=True)

    with open(path, "w") as f:
        json.dump(data, f)