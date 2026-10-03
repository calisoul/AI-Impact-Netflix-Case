"""Erzeugt docs/data.js (schlanker Datensatz fuer das Dashboard) aus Clean-Data/."""
import csv, json, collections as C

D = "Clean-Data/"
multi = {}
for k in ("country", "listed_in"):
    m = C.defaultdict(list)
    for r in csv.DictReader(open(f"{D}titles_{k}.csv", encoding="utf-8")):
        m[r["show_id"]].append(r[k])
    multi[k] = m

rows = []
for r in csv.DictReader(open(f"{D}netflix_titles_clean.csv", encoding="utf-8")):
    i = r["show_id"]
    rows.append([
        0 if r["type"] == "Movie" else 1,
        int(r["release_year"]),
        int(r["year_added"]) if r["year_added"] else None,
        r["rating_group"],
        multi["country"][i],
        multi["listed_in"][i],
    ])
open("docs/data.js", "w", encoding="utf-8").write(
    "// [typ(0=Film,1=Serie), release_year, year_added, rating_group, laender, genres]\n"
    "const DATA = " + json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + ";\n")
print(len(rows), "Titel")
