from tqdm import tqdm
import torch.nn.functional as F
import torch.nn as nn
import torch

from torch import Tensor
from transformers import AutoTokenizer, AutoModel


def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


def embed(text: list[str], bar_description: str = "Creating new vectors") -> dict:
    tokenizer = AutoTokenizer.from_pretrained("intfloat/multilingual-e5-large")
    model = AutoModel.from_pretrained("intfloat/multilingual-e5-large")

    output = {}
    for i in tqdm(text, desc=bar_description):
        if i == "":
            continue

        batch_dict = tokenizer(
            "query: " + i,
            max_length=512,
            padding=True,
            truncation=True,
            return_tensors="pt",
        )
        outputs = model(**batch_dict)
        embbeding = average_pool(
            outputs.last_hidden_state, batch_dict["attention_mask"]
        )
        embbeding = F.normalize(embbeding, p=2, dim=1)

        output[i] = embbeding

    return output


def compare(favorites, new_entries, bar_description: str = "Comparing"):
    results = []
    cos = nn.CosineSimilarity(dim=1, eps=1e-6)

    for entry in tqdm(new_entries.keys(), desc=bar_description):
        for favorite in favorites.keys():
            if entry == favorite:
                continue

            results.append(
                [favorite, entry, cos(favorites[favorite], new_entries[entry])]
            )

    return results
