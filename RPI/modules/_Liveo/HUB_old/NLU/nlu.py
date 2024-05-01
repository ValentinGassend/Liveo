import io
import json
import locale
import datetime
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
        self.SAMPLE_DATASET_RDV_PATH = Path(
            __file__).parent / "dataset/new_rdv_dataset.json"
        with self.SAMPLE_DATASET_RDV_PATH.open(encoding="utf8") as f:
            self.sample_dataset_rdv = json.load(f)
        self.nlu_engine_rdv = SnipsNLUEngine(config=CONFIG_FR)

        self.SAMPLE_DATASET_CHOICE_PATH = Path(
            __file__).parent / "dataset/choice_dataset.json"
        with self.SAMPLE_DATASET_CHOICE_PATH.open(encoding="utf8") as f:
            self.sample_dataset_choice = json.load(f)
        self.nlu_engine_choice = SnipsNLUEngine(config=CONFIG_FR)

        self.SAMPLE_DATASET_BOOL_PATH = Path(
            __file__).parent / "dataset/bool_dataset.json"
        with self.SAMPLE_DATASET_BOOL_PATH.open(encoding="utf8") as f:
            self.sample_dataset_bool = json.load(f)
        self.nlu_engine_bool = SnipsNLUEngine(config=CONFIG_FR)
        self.SAMPLE_DATASET_REMIND_PATH = Path(
            __file__).parent / "dataset/remind_dataset.json"
        with self.SAMPLE_DATASET_REMIND_PATH.open(encoding="utf8") as f:
            self.sample_dataset_remind = json.load(f)
        self.nlu_engine_remind = SnipsNLUEngine(config=CONFIG_FR)

    def fit_rdv(self):
        self.nlu_engine_rdv.fit(self.sample_dataset_rdv)

    def fit_choice(self):
        self.nlu_engine_choice.fit(self.sample_dataset_choice)

    def fit_bool(self):
        self.nlu_engine_bool.fit(self.sample_dataset_bool)

    def fit_remind(self):
        self.nlu_engine_remind.fit(self.sample_dataset_remind)

    def run_rdv(self, file=None, text=None):
        if file:
            with open(file) as f:
                self.text = f.read()
        elif text:
            self.text = text
        print(self.text)
        self.parsing = self.nlu_engine_rdv.parse(self.text)
        print(self.parsing)
        print(json.dumps(self.parsing, indent=4))
        # print(output)
        return self.parsing

    def run_choice(self, file=None, text=None):
        if file:
            with open(file) as f:
                self.text = f.read()
        elif text:
            self.text = text
        print(self.text)
        self.parsing = self.nlu_engine_choice.parse(self.text)
        print(self.parsing)
        print(json.dumps(self.parsing, indent=4))
        # print(output)
        return self.parsing

    def run_bool(self, file=None, text=None):
        if file:
            with open(file) as f:
                self.text = f.read()
        elif text:
            self.text = text
        print(self.text)
        self.parsing = self.nlu_engine_bool.parse(self.text)
        print(self.parsing)
        print(json.dumps(self.parsing, indent=4))
        # print(output)
        return self.parsing
    def run_remind(self, file=None, text=None):
        if file:
            with open(file) as f:
                self.text = f.read()
        elif text:
            self.text = text
        print(self.text)
        self.parsing = self.nlu_engine_remind.parse(self.text)
        print(self.parsing)
        print(json.dumps(self.parsing, indent=4))
        # print(output)
        return self.parsing


# # myNlu = Nlu()
# # # data = myNlu.run('Whisper_and_NLU/text_live.txt')
# # data = {'input': 'Je souhaite prendre un rendez-vous chez le médecin pour le 20 juin à 15h', 'intent': {'intentName': 'scheduleMeeting', 'probability': 0.6148814566204538}, 'slots': [{'range': {'start': 23, 'end': 34}, 'rawValue': 'rendez-vous', 'value': {
# # 'kind': 'Custom', 'value': 'réunion'}, 'entity': 'meeting_type', 'slotName': 'meeting_type'}, {'range': {'start': 56, 'end': 72}, 'rawValue': 'le 20 juin à 15h', 'value': {'kind': 'InstantTime', 'value': '2023-06-20 15:00:00 +02:00', 'grain': 'Hour', 'precision': 'Exact'}, 'entity': 'snips/datetime', 'slotName': 'meeting_time'}]}
# # output = json.load(data)

# locale.setlocale(locale.LC_TIME, '')  # date en français
# Type = [False, "le type de rendez-vous"]
# date = [False, "la date"]
# heure = [False, "l'heure"]
# lieu = [False, "le lieu"]
# details = [False, "les détails du rendez-vous"]

# # data = {'input': "Je veux prendre un rendez-vous d'affaires avec le responsable des ventes le 28 juin à 14h00 au bureau de l'entreprise.", 'intent': {'intentName': 'prendreRendezVousProfessionnel', 'probability': 0.5798443978978777}, 'slots': [{'range': {'start': 19, 'end': 41}, 'rawValue': "rendez-vous d'affaires", 'value': {'kind': 'Custom', 'value': 'rendez-vous professionnel'}, 'entity': 'type_rendez_vous', 'slotName': 'type_rendez_vous'}, {'range': {'start': 47, 'end': 72}, 'rawValue': 'le responsable des ventes', 'value': {'kind': 'Custom', 'value': 'le responsable des ventes'}, 'entity': 'details_rendez_vous', 'slotName': 'details_rendez_vous'}, {
# #     'range': {'start': 76, 'end': 83}, 'rawValue': '28 juin', 'value': {'kind': 'InstantTime', 'value': '2023-06-28 00:00:00 +02:00', 'grain': 'Day', 'precision': 'Exact'}, 'entity': 'snips/date', 'slotName': 'date'}, {'range': {'start': 86, 'end': 91}, 'rawValue': '14h00', 'value': {'kind': 'InstantTime', 'value': '2023-05-11 14:00:00 +02:00', 'grain': 'Minute', 'precision': 'Exact'}, 'entity': 'snips/time', 'slotName': 'heure'}, {'range': {'start': 95, 'end': 117}, 'rawValue': "bureau de l'entreprise", 'value': {'kind': 'Custom', 'value': "siège social de l'entreprise"}, 'entity': 'lieu', 'slotName': 'lieu'}]}
# data = {'input': 'Je voudrais prendre un rendez-vous médical avec le Dr. Martin le 4 juillet prochain.', 'intent': {'intentName': 'prendreRendezVousMedical', 'probability': 0.5753630750519433}, 'slots': [{'range': {'start': 23, 'end': 42}, 'rawValue': 'rendez-vous médical', 'value': {'kind': 'Custom', 'value': 'rendez-vous médical'}, 'entity': 'type_rendez_vous', 'slotName': 'type_rendez_vous'}, {
#     'range': {'start': 51, 'end': 61}, 'rawValue': 'Dr. Martin', 'value': {'kind': 'Custom', 'value': 'Dr. Martin'}, 'entity': 'details_rendez_vous', 'slotName': 'details_rendez_vous'}, {'range': {'start': 65, 'end': 83}, 'rawValue': '4 juillet prochain', 'value': {'kind': 'InstantTime', 'value': '2023-07-04 00:00:00 +02:00', 'grain': 'Day', 'precision': 'Exact'}, 'entity': 'snips/date', 'slotName': 'date'}]}

# print("Phrase d'origine : " + data["input"])
# for slot in data["slots"]:
#     if slot["slotName"] == "type_rendez_vous":
#         print("Le type de rendez-vous est : " + slot["value"]["value"])
#         Type = [True, "le type de rendez-vous"]
#     if slot["slotName"] == "details_rendez_vous":
#         print("Le détail du rendez-vous est : " + slot["value"]["value"])
#         details = [True, "les détails du rendez-vous"]
#     if slot["slotName"] == "date":
#         if slot["value"]["grain"] == "Day":
#             unformatedDate = datetime.datetime.strptime(
#                 slot["value"]["value"], "%Y-%m-%d %H:%M:%S %z")
#             new_format_date = "%A %d %B %Y"
#             formatedDate = unformatedDate.strftime(new_format_date)
#             print("La date du rendez-vous est : " + formatedDate)
#             date = [True, "la date"]
#     if slot["slotName"] == "heure":
#         unformatedHour = datetime.datetime.strptime(
#             slot["value"]["value"], "%Y-%m-%d %H:%M:%S %z")
#         new_format_hours = "%H:%M"
#         formatedHour = unformatedHour.strftime(new_format_hours)
#         print("L'heure du rendez-vous est : " + formatedHour)
#         heure = [True, "l'heure"]
#     if slot["slotName"] == "lieu":
#         print("Le lieu du rendez-vous est : " + slot["value"]["value"])
#         lieu = [True, "le lieu"]

# whatIWant = [heure, date, Type]
# whatIsNotRequired = [details, lieu]
# for item in whatIWant:
#     if not item[0]:
#         print("\n\nil manque "+item[1] +
#               " c'est essentiel pour le rappel ATTENTION")
# for item in whatIsNotRequired:
#     if not item[0]:
#         print("il manque "+item[1] +
#               " ce n'est pas essentiel pour le rappel ceci dit \n")
