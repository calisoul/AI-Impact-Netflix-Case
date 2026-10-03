"""Bereinigt Raw-Data/netflix_titles.csv -> Clean-Data/ (Rohdatei bleibt unveraendert)."""
import csv, re
from datetime import datetime

SRC, OUT = "Raw-Data/netflix_titles.csv", "Clean-Data"
GROUP = {
    "G": "Kinder/Familie", "TV-Y": "Kinder/Familie", "TV-G": "Kinder/Familie", "TV-Y7": "Kinder/Familie",
    "TV-Y7-FV": "Kinder/Familie", "PG": "Kinder/Familie", "TV-PG": "Kinder/Familie",
    "PG-13": "Jugendliche", "TV-14": "Jugendliche",
    "R": "Erwachsene", "TV-MA": "Erwachsene", "NC-17": "Erwachsene",
    "NR": "Unbewertet", "UR": "Unbewertet",
}
rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
log = {"verschobene Zeilen korrigiert": 0}
long = {k: [] for k in ("country", "listed_in", "cast", "director")}
clean = []
for r in rows:
    r = {k: (v or "").strip() for k, v in r.items()}
    if re.fullmatch(r"\d+ min", r["rating"]) and not r["duration"]:  # verrutschte Spalten
        r["duration"], r["rating"] = r["rating"], ""
        log["verschobene Zeilen korrigiert"] += 1
    try:
        d = datetime.strptime(r["date_added"], "%B %d, %Y"); r["date_added"] = d.date().isoformat()
        r["year_added"] = d.year
    except ValueError:
        r["date_added"], r["year_added"] = "", ""
    m = re.fullmatch(r"(\d+)\s+(min|Seasons?)", r["duration"])
    r["duration_value"] = m.group(1) if m else ""
    r["duration_unit"] = {"min": "min", "Season": "Seasons", "Seasons": "Seasons"}[m.group(2)] if m else ""
    r["rating_group"] = GROUP.get(r["rating"], "Unbekannt")
    for k in long:
        items = [x.strip() for x in r[k].split(",") if x.strip()]
        r[k + "_count"] = len(items)
        long[k] += [(r["show_id"], x) for x in items]
    del r["duration"]
    clean.append(r)

def write(name, header, data):
    with open(f"{OUT}/{name}", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(data)

cols = list(clean[0].keys())
write("netflix_titles_clean.csv", cols, [[r[c] for c in cols] for r in clean])
for k, v in long.items():
    write(f"titles_{k}.csv", ["show_id", k], v)
print(len(clean), "Zeilen;", log, {k: len(v) for k, v in long.items()})
