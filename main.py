import os

import torch

from embedding import embed, compare
from feeds import create_favorites, get_new_entries, get_entry_url

if not os.path.exists("urls"):
    raise SystemExit()

# if not os.path.exists("rssmate"):
#     print("Creating rssmate file")
#     try:
#         os.mknod("rssmate")
#     except PermissionError:
#         print("Permision denied!")
#     except Exception as e:
#         print(e)
#     finally:
#         print("Created")

if not os.path.exists("embeddings.pth"):
    print("Looks like you don't have favorite file. Let's make one")
    favorites = create_favorites()
    favorites_embeddings = embed(favorites)
    torch.save(favorites_embeddings, "embeddings.pth")

favorites_embeddings = torch.load("embeddings.pth")

new_entries = get_new_entries()
embeded_entries = embed(new_entries, bar_description="Embedding new entries")

compared = sorted(
    compare(favorites_embeddings, embeded_entries), key=lambda x: x[2], reverse=True
)
entries_to_show = compared[: int(input("How many entries you want to discover? "))]

for n, i in enumerate(entries_to_show):
    url = get_entry_url(i[0])
    print("{}.\n{}\n{}\n{}\n{}\n".format(n + 1, i[0], i[1], i[2].item(), url))

entries_to_show = list(
    map(
        lambda x: x[1],
        entries_to_show
    )
)
entries_to_convert = []

while (user_in := input("Do you like any of these? 0 - no: ")) != "0" and user_in != "":
    user_in = int(user_in)
    entries_to_convert.append(entries_to_show[user_in - 1])

favorites_embeddings.update(embed(entries_to_convert))
torch.save(favorites_embeddings, "embeddings.pth")
