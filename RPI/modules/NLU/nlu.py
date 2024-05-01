import io
import json
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_FR
from pathlib import Path

# SAMPLE_DATASET_PATH = Path(__file__).parent / "dataset/rdv_or_beverage_dataset.json"

# with SAMPLE_DATASET_PATH.open(encoding="utf8") as f:
#     sample_dataset = json.load(f)

# nlu_engine = SnipsNLUEngine(config=CONFIG_FR)
# nlu_engine.fit(sample_dataset)

# # text = "Est-ce que je peux avoir 10 cafes pour la soiree s'il te plait ?"
# text = "Je veux prendre un rendez-vous professionnel le 6 mai à 15h"
# parsing = nlu_engine.parse(text)
# print(json.dumps(parsing, indent=2))


class Nlu:
    def __init__(self):
        self.SAMPLE_DATASET_PATH = Path(
            __file__).parent / "dataset/rdv_or_beverage_dataset.json"
        with self.SAMPLE_DATASET_PATH.open(encoding="utf8") as f:
            self.sample_dataset = json.load(f)
        self.nlu_engine = SnipsNLUEngine(config=CONFIG_FR)
        self.nlu_engine.fit(self.sample_dataset)

    def run(self, input):
        self.text = input
        self.parsing = self.nlu_engine.parse(self.text)
        print(json.dumps(self.parsing, indent=2))
