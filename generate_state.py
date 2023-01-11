import json
import pathlib
import main
import os
from functools import wraps


def write_wrapper(path: str):
    def decorator(func):
        print(f"Writing to path: {path}")
        path_obj = pathlib.Path(path)
        parents = list(path_obj.parents)
        parents.reverse()
        for parent in parents:
            if parent.exists():
                pass
            else:
                parent.mkdir()
        with open(path, 'w') as write_handle:
            write_handle.write(func())
    return decorator


@write_wrapper('./api/public/people/index.json')
def generate_product_index():
    build = list()
    people = main.collections['people']
    for person in people:
        build.append(f"{person['doc_id']}.json")
    return json.dumps(build)


for entity in main.collections['people']:
    write_wrapper(f'./api/public/people/{entity["doc_id"]}.json')(lambda: json.dumps(entity))

