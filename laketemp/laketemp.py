import random
import urllib.request
import xml.etree.ElementTree as ET

LAKE_ID_MAPPING = {
    "Afritzer See": "lake1",
    "Brennsee": "lake2",
    "Faaker See": "lake3",
    "Gösselsdorfer See": "lake4",
    "Keutschacher See": "lake5",
    "Klopeiner See": "lake6",
    "Längsee": "lake7",
    "Maltschacher See": "lake8",
    "Millstätter See": "lake9",
    "Ossiacher See": "lake10",
    "Pressegger See": "lake11",
    "Weißensee": "lake12",
    "Wörthersee": "lake13",
}

ICONS = [22838, 31377, 10497, 19772, 24115, 24116, 24117]


def run(lake_ids):
    lakes = {LAKE_ID_MAPPING[lake.name]: lake for lake in Lake.get_lakes() if lake.name in LAKE_ID_MAPPING}
    frames = []
    for lake_id in lake_ids:
        if lake_id not in lakes:
            continue

        frames.append(
            {
                "text": f"{lakes[lake_id].name} {lakes[lake_id].temp}",
                "icon": random.choice(ICONS),
            }
        )
    if not frames:
        frames.append(
            {
                "text": "No lake selected",
                "icon": random.choice(ICONS),
            }
        )
    return {"frames": frames}


class Lake:
    def __init__(self, name: str = "", temp: str = "", waterheight: str = "", date_of_meassurment: str = ""):
        self.name = name
        self.temp = temp
        self.waterheight = waterheight
        self.date_of_meassurment = date_of_meassurment

    def __repr__(self) -> str:
        return f"{self.name}: {self.temp}"

    @classmethod
    def get_lakes(cls):
        try:
            feed = urllib.request.urlopen("https://info.ktn.gv.at/asp/hydro/hydro_stationen_see_rss_mit_Werte.asp")
        except Exception as e:
            print(e)
            return []

        tree = ET.parse(feed)
        root = tree.getroot()
        lake_entries = root.findall("channel/item")

        lakes = []
        try:
            for lake_entry in lake_entries:
                title = lake_entry.find("title")
                desc = lake_entry.find("description")

                desc_data = desc.text.replace("<p>", "").replace("</p>", "").replace("\n", "").split("<br />")

                lake = cls(name=title.text.split("-")[0].strip())
                for line in desc_data:
                    line = line.strip()
                    if line.startswith("Datum"):
                        lake.date_of_meassurment = line.split(" : ")[1]
                    elif line.startswith("Wasserstand"):
                        lake.waterheight = line.split(":")[1].strip() + " cm"
                    elif line.startswith("Wassertemperatur"):
                        lake.temp = line.split(":")[1].strip() + " °C"

                lakes.append(lake)
        except Exception as e:
            print(e)
        return lakes
