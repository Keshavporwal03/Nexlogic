import os
import requests

icons = {
    "location-pin": "mdi:map-marker",
    "shield": "mdi:shield-check",
    "briefcase": "mdi:briefcase",
    "person": "mdi:account",
    "checkmark": "mdi:check-circle",
    "globe": "mdi:earth",
    "mail": "mdi:email",
    "megaphone": "mdi:bullhorn"
}

output_dir = os.path.join(os.path.dirname(__file__), "app", "static", "icons")
os.makedirs(output_dir, exist_ok=True)

for name, icon_id in icons.items():
    url = f"https://api.iconify.design/{icon_id.split(':')[0]}/{icon_id.split(':')[1]}.png?color=%231F1F1F&width=64"
    print(f"Downloading {name} from {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        path = os.path.join(output_dir, f"{name}.png")
        with open(path, "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to download {name}: {response.status_code}")

# White versions for colored cards
for name, icon_id in icons.items():
    url = f"https://api.iconify.design/{icon_id.split(':')[0]}/{icon_id.split(':')[1]}.png?color=white&width=64"
    print(f"Downloading {name} (white) from {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        path = os.path.join(output_dir, f"{name}_white.png")
        with open(path, "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to download {name} (white): {response.status_code}")
