import csv
import os
import re
from typing import Any


def compute_OestrogenPositiveZellkerne(data_model):
    if data_model.OestrogenPositiveZellkerne:
        pos_zellkerne = data_model.OestrogenPositiveZellkerne
        if pos_zellkerne == 0:
            return "0"
        elif pos_zellkerne > 0 and pos_zellkerne < 10:
            return "1"
        elif pos_zellkerne >= 10 and pos_zellkerne <= 50:
            return "2"
        elif pos_zellkerne > 50 and pos_zellkerne <= 80:
            return "3"
        elif pos_zellkerne > 80:
            return "4"
    else:
        return ""


def compute_ProgesteronPositiveZellkerne(data_model):
    if data_model.ProgesteronPositiveZellkerne:
        pos_zellkerne = data_model.ProgesteronPositiveZellkerne
        if pos_zellkerne == 0:
            return "0"
        elif pos_zellkerne > 0 and pos_zellkerne < 10:
            return "1"
        elif pos_zellkerne >= 10 and pos_zellkerne <= 50:
            return "2"
        elif pos_zellkerne > 50 and pos_zellkerne <= 80:
            return "3"
        elif pos_zellkerne > 80:
            return "4"
    else:
        return ""


def compute_OestrogenIRSScore(data_model):
    if data_model.OestrogenIRSScore:
        return data_model.OestrogenIRSScore
    elif (
        data_model.OestrogenPositiveZellkerne and data_model.OestrogenFaerbeintensitaet
    ):
        return int(compute_OestrogenPositiveZellkerne(data_model)) * int(
            data_model.OestrogenFaerbeintensitaet.name[-1]
        )
    else:
        return ""


def compute_ProgesteronIRSScore(data_model):
    if data_model.ProgesteronIRSScore:
        return data_model.ProgesteronIRSScore
    elif (
        data_model.ProgesteronPositiveZellkerne
        and data_model.ProgesteronFaerbeintensitaet
    ):
        return int(compute_ProgesteronPositiveZellkerne(data_model)) * int(
            data_model.ProgesteronFaerbeintensitaet.name[-1]
        )
    else:
        return ""


def convert_to_onkostar_csv(
    data_model: Any, file_path: str, model_name: str, pat_id: int
):

    with open(
        os.path.join(file_path, f"{model_name}_diagnosis.csv"),
        "w",
        newline="",
        encoding="windows-1252",
    ) as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["Test"])
        writer.writerow(["OS.Diagnose"])
        writer.writerow(
            [
                "PatientenId",
                "Vorname",
                "Nachname",
                "Geburtsdatum",
                "Geschlecht",
                "TumorId",
                "DokumentierendeEinrichtung",
                "DokumentierendeFachabteilung",
                "Diagnosedatum",
                "Diagnosesicherung",
                "Diagnosestatus",
                "ICD10",
                "ICDO3Histologie",
                "ICDO3Lokalisation",
                "InternExtern",
                "Primaerfall",
                "Seite",
                "StatusDerZuordnung",
                "ZentrumsfallDZ",
            ]
        )
        writer.writerow(
            [
                pat_id,
                data_model.Vorname,
                data_model.Nachname,
                data_model.Geburtsdatum,
                data_model.Geschlecht.name,
                "1",
                "UKA",
                "TuDo",
                data_model.HistologieDatum,
                "7",
                "B",
                (
                    f"C50.{data_model.Lokalisation.name[-1]}"
                    if data_model.ICDO3Histologie.value[-1] == "3"
                    else "D05.1" if data_model.ICDO3Histologie.value[-1] == "2" else ""
                ),
                (data_model.ICDO3Histologie.value),
                f"C50.{data_model.Lokalisation.name[-1]}",
                data_model.Ort.name,
                "1",
                data_model.Seite.name,
                "geprüft",
                "1",
            ]
        )

    with open(
        os.path.join(file_path, f"{model_name}_patho.csv"),
        "w",
        newline="",
        encoding="windows-1252",
    ) as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["Test"])
        writer.writerow(["OS.Pathologiebefund"])
        writer.writerow(
            [
                "PatientenId",
                "Vorname",
                "Nachname",
                "Geburtsdatum",
                "Geschlecht",
                "TumorId",
                "DokumentierendeEinrichtung",
                "DokumentierendeFachabteilung",
                "Befundtext",
                "Biopsieart",
                "DurchfuehrendeOE",
                "DurchfuehrendeOE_fachabteilung",
                "Einsendenummer",
                "EntnahmestellederBiopsie",
                "Grading",
                "HER2neu",
                "HistologieDatum",
                "ICDO3Histologie",
                "InternExtern",
                "Ki67",
                "ICDO3Lokalisation",
                "Massgeblich",
                "OestrogenMethode",
                "OestrogenIRSPosZellkerne",
                "OestrogenFaerbeintens",
                "OestrogenScore",
                "Praeparat",
                "ProgesteronMethode",
                "ProgestIRSPosZellk",
                "ProgestFaerbeintensitaet",
                "ProgesteronScore",
                "TNMOrg",
                "Tumornachweis",
            ]
        )
        writer.writerow(
            [
                pat_id,
                data_model.Vorname,
                data_model.Nachname,
                data_model.Geburtsdatum,
                data_model.Geschlecht.name,
                "1",
                "UKA",
                "TuDo",
                data_model.Befundtext,
                "" if not data_model.Biopsieart else data_model.Biopsieart.name,
                data_model.PathologischesInstitut1.name,
                re.sub("_", " ", data_model.PathologischesInstitut2.name),
                data_model.Einsendenummer,
                data_model.Entnahmestelle.name,
                "" if not data_model.Grading else data_model.Grading.name[-1],
                "" if not data_model.HER2neu else data_model.HER2neu.name[-1],
                data_model.HistologieDatum,
                data_model.ICDO3Histologie.value,
                data_model.Ort.name,
                "" if not data_model.Ki67 else data_model.Ki67,
                f"C50.{data_model.Lokalisation.name[-1]}",
                data_model.Massgeblich.name[-1],
                (
                    ""
                    if not data_model.OestrogenPositiveZellkerne
                    and not data_model.OestrogenFaerbeintensitaet
                    and not data_model.OestrogenIRSScore
                    else "IRS"
                ),
                compute_OestrogenPositiveZellkerne(data_model),
                (
                    ""
                    if not data_model.OestrogenFaerbeintensitaet
                    else data_model.OestrogenFaerbeintensitaet.name[-1]
                ),
                compute_OestrogenIRSScore(data_model),
                data_model.Praeparat.name,
                (
                    ""
                    if not data_model.ProgesteronPositiveZellkerne
                    and not data_model.ProgesteronFaerbeintensitaet
                    and not data_model.ProgesteronIRSScore
                    else "IRS"
                ),
                compute_ProgesteronPositiveZellkerne(data_model),
                (
                    ""
                    if not data_model.ProgesteronFaerbeintensitaet
                    else data_model.ProgesteronFaerbeintensitaet.name[-1]
                ),
                compute_ProgesteronIRSScore(data_model),
                data_model.TNM_nach.name,
                data_model.Tumornachweis.name[-1],
            ]
        )
