import io
import json
import locale
import datetime
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_FR
from pathlib import Path


class Nlu:
    def __init__(self):
        self.SAMPLE_DATASET_RDV_PATH = Path(__file__).parent / "dataset/new_rdv_dataset.json"
        with self.SAMPLE_DATASET_RDV_PATH.open(encoding="utf8") as f:
            self.sample_dataset_rdv = json.load(f)
        self.nlu_engine_rdv = SnipsNLUEngine(config=CONFIG_FR)

        self.SAMPLE_DATASET_CHOICE_PATH = Path(__file__).parent / "dataset/choice_dataset.json"
        with self.SAMPLE_DATASET_CHOICE_PATH.open(encoding="utf8") as f:
            self.sample_dataset_choice = json.load(f)
        self.nlu_engine_choice = SnipsNLUEngine(config=CONFIG_FR)

        self.SAMPLE_DATASET_BOOL_PATH = Path(__file__).parent / "dataset/bool_dataset.json"
        with self.SAMPLE_DATASET_BOOL_PATH.open(encoding="utf8") as f:
            self.sample_dataset_bool = json.load(f)
        self.nlu_engine_bool = SnipsNLUEngine(config=CONFIG_FR)

        self.SAMPLE_DATASET_REMIND_PATH = Path(__file__).parent / "dataset/remind_dataset.json"
        with self.SAMPLE_DATASET_REMIND_PATH.open(encoding="utf8") as f:
            self.sample_dataset_remind = json.load(f)
        self.nlu_engine_remind = SnipsNLUEngine(config=CONFIG_FR)

    def fit(self):
        self.nlu_engine_rdv.fit(self.sample_dataset_rdv)
        self.nlu_engine_choice.fit(self.sample_dataset_choice)
        self.nlu_engine_bool.fit(self.sample_dataset_bool)
        self.nlu_engine_remind.fit(self.sample_dataset_remind)

    def run(self, file=None, text=None, intent="rdv"):
        if file:
            with open(file) as f:
                self.text = f.read()
        elif text:
            self.text = text
        print(self.text)
        
        if intent == "rdv":
            self.parsing = self.nlu_engine_rdv.parse(self.text)
        elif intent == "choice":
            self.parsing = self.nlu_engine_choice.parse(self.text)
        elif intent == "bool":
            self.parsing = self.nlu_engine_bool.parse(self.text)
        elif intent == "remind":
            self.parsing = self.nlu_engine_remind.parse(self.text)
            
        print(self.parsing)
        print(json.dumps(self.parsing, indent=4))
        return self.parsing
