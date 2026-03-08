import os
import requests

images = [
    "https://content.jdmagicbox.com/v2/comp/hyderabad/n1/040pxx40.xx40.260129152547.v6n1/catalogue/shubhotsav-soul-of-celebrations-jupiter-colony-hyderabad-photographers-e2o22ncj7i.jpg",
    "https://content.jdmagicbox.com/v2/comp/hyderabad/n1/040pxx40.xx40.260129152547.v6n1/catalogue/shubhotsav-soul-of-celebrations-jupiter-colony-hyderabad-photographers-wwfky5x7x0.jpg",
    "https://content.jdmagicbox.com/v2/comp/hyderabad/n1/040pxx40.xx40.260129152547.v6n1/catalogue/shubhotsav-soul-of-celebrations-jupiter-colony-hyderabad-photographers-kzaa0pkus1.jpg",
    "https://content.jdmagicbox.com/v2/comp/hyderabad/n1/040pxx40.xx40.260129152547.v6n1/catalogue/shubhotsav-soul-of-celebrations-jupiter-colony-hyderabad-photographers-li42vvwe4y.jpg",
    "https://content.jdmagicbox.com/v2/comp/hyderabad/n1/040pxx40.xx40.260129152547.v6n1/catalogue/shubhotsav-soul-of-celebrations-jupiter-colony-hyderabad-photographers-twiwcmuloz.jpg",
    "https://content.jdmagicbox.com/v2/comp/hyderabad/n1/040pxx40.xx40.260129152547.v6n1/catalogue/shubhotsav-soul-of-celebrations-jupiter-colony-hyderabad-photographers-ydzpjkcwo3.jpg"
]

os.makedirs('static/images', exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

for url in images:
    filename = url.split('/')[-1]
    filepath = os.path.join('static/images', filename)
    print(f"Downloading {filename}...")
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(r.content)
        print(f"Saved to {filepath}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
