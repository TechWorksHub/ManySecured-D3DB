from pathlib import Path
from glob import glob
file = Path(__file__).absolute()
yaml_store = Path(file / ".."/ ".."/ ".." / "manufacturers").resolve()
print(file)
print(yaml_store)
print(glob(str(yaml_store), recursive=True))
print(map(str, yaml_store.glob("**/*")))
