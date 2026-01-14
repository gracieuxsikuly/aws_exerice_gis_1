from pathlib import Path
p=Path("data/routess.geojson")
q = Path('eggs')
if(p.exists()):
    print("ca existe")
    size=p.stat().st_size
    mtime=p.stat().st_mtime
    print(f"la taille est {size}")
    print(mtime)
else:
    print("pas vraiment")
# test si c'est un fichier
if(p.is_file):
    print("c'est un fichier vraiment")
else:
    print("pas un fichier kabisa")
if(p.is_mount):
    print("ok")
