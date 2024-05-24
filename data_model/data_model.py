from typing import Optional, Union

from httpcore import stream
from numpy import str_
from pydantic import BaseModel, Field

from data_model.types import *


def get_data_models():
    return [BasicFields, Lokalisation, Befundtext, Seite, Hormonrezeptor]


class BasicFields(BaseModel):
    Vorname: str
    Nachname: str
    Geburtsdatum: str
    Geschlecht: GeschlechtType = Field(description="Immer 'weiblich'")
    HistologieDatum: str = Field(description="Probeneingangsdatum")
    Ort: OrtType = Field(description="Immer 'Meine Einrichtung'")
    PathologischesInstitut1: PathologischesInstitut1Type = Field(
        description="Immer 'Uniklinikum RWTH Aachen'"
    )
    PathologischesInstitut2: PathologischesInstitut2Type = Field(
        description="Beginnt die Eingangsnummer mit 'E', dann 'Pathologie', beginnt sie mit 'M', dann 'Pathologie MVZ UKA'",
    )
    Einsendenummer: str = Field(description="Eingangsnummer")
    Praeparat: PraeparatType = Field(description="Art des untersuchten Präparats")
    Biopsieart: Optional[BiopsieartType] = Field(
        None,
        description="Art der Biospie, falls es sich um eine Biopsie handelt",
    )
    Entnahmestelle: EntnahmestelleType = Field(description="Entnahmestelle des Gewebes")
    Massgeblich: Ja_NeinType = Field(description="Immer 'Nein'")
    Tumornachweis: Ja_NeinType = Field(
        description="Falls ICD-O Code vorhanden, dann 'Ja', sonst 'Nein'"
    )
    ICDO3Histologie: ICDO3HistologieType = Field(
        description="""Extrahiere den Code, der im Bericht explizit steht.
        Wenn es mehrere Codes im Bericht gibt, dann nimm den, der als erstes kommt."""
    )
    Grading: Optional[GradingType] = Field(
        None, description="Das Grading des Tumors, wenn explizit angegeben"
    )
    TNM_nach: TNM_nachType = Field(
        description="Immer 'UICC', außer es handelt sich um Hauttumore, dann 'AJCC'",
    )
    HER2neu: Optional[HER2neuType] = Field(
        None,
        description="Bestimme den korrekten Wert, wenn HERneu explizit angegeben ist",
    )
    Ki67: Optional[int] = Field(
        None,
        description="""Als Dezimalzahl anzugeben ohne Prozentzeichen, falls Ki67 explizit angegeben ist.
        Falls eine range angegeben ist, nimm das Obere Ende davon. Also z.B. '30', wenn dort '20-30%' steht.""",
    )


class Lokalisation(BaseModel):
    Lokalisation: LokalisationType = Field(
        description="""Finde alle in Klammern angegebenen Lokalisationsangaben im Abschnitt 'Gutachten'.
        Selektiere davon jetzt nur diejenigen, die im nachfolgenden Text das Wort 'Karzinom' (oder eine Abwandlung wie 'Adenokarzinom') erwähnen.
        
        Auf Basis der Lokalisationsangaben, die jetzt noch übrig sind, bestimme die Lokalisation des Karzinoms/der Karzinome wie folgt:
        
        - Es darf auf keinen Fall eine Klammer zur Lokalisationsbestimmung benutzt werden, für die im nachfolgenden Text nicht ein einziges mal
        das Teilwort 'karzinom' vorkommt! Solche Klammern gelten nicht als 'relevante Klammer' und sind zu ignorieren!
        
        - Betrachte wirklich nur, was in Klammern steht, also wenn z.B. außerhalb der Klammer etwas von 'Brustgewebe' steht, hat das nichts mit der Lokalisation zu tun.
        
        - Ist z.B. '(Mamma links oben innen)' die einzige relevante Klammer, führt dies zum Wert 'Oberer innerer Quadrant der Brust'.
        Manchmal werden Abkürzungen wie 'o/a' benutzt, was in diesem Fall oben außen bedeutet. Analog für (u)nten und (i)nnen. 
        
        - Manchmal sind auch Uhrzeiten angegeben, diese sind wie folgt zu übersetzen:
        Linke Mamma 1-2 Uhr = 'Oberer äußerer Quadrant der Brust'
        Linke Mamma 3 Uhr = 'Brust, mehrere Teilbereiche überlappend'
        Linke Mamma 4-5 Uhr = 'Unterer äußerer Quadrant der Brust'
        Linke Mamma 6 Uhr = 'Brust, mehrere Teilbereiche überlappend'
        Linke Mamma 7-8 Uhr = 'Unterer innerer Quadrant der Brust'
        Linke Mamma 9 Uhr = 'Brust, mehrere Teilbereiche überlappend'
        Linke Mamma 10-11 Uhr = 'Oberer innerer Quadrant der Brust'
        Linke Mamma 12 Uhr = 'Brust, mehrere Teilbereiche überlappend'
        Rechte Mamma 1-2 Uhr = 'Oberer innerer Quadrant der Brust'
        Rechte Mamma 3 Uhr = 'Brust, mehrere Teilbereiche überlappend'
        Rechte Mamma 4-5 Uhr = 'Unterer innerer Quadrant der Brust'
        Rechte Mamma 6 Uhr = 'Brust, mehrere Teilbereiche überlappend'
        Rechte Mamma 7-8 Uhr = 'Unterer äußerer Quadrant der Brust'
        Rechte Mamma 9 Uhr = 'Brust, mehrere Teilbereiche überlappend'
        Rechte Mamma 10-11 Uhr = 'Oberer äußerer Quadrant der Brust'
        Rechte Mamma 12 Uhr = 'Brust, mehrere Teilbereiche überlappend'
        
        - Immer wenn es mehrere Quadranten betrifft oder die Lokalisation nicht genau angegeben/dir unbekannt ist, dann ist
        'Brust, mehrere Teilbereiche überlappend' anzugeben. Z.B. ist dies der Fall, wenn dort nur '(Mamma rechts)'
        oder nur '(Mamma rechts außen)' oder nur '(Mamma unten)' steht oder wenn sowohl '(Mamma rechts oben außen)' als auch '(Mamma links oben innen)' relevante Klammern sind.
        
        - 'Mamille', also Brustwarze/Nippel, oder 'Zentraler Drüsenkörper der Brust' oder 'Recessus axillaris der Brust', also Achsel, ist es nur, wenn es eindeutig in
        der relevanten Klammer so steht.""",
    )


class Seite(BaseModel):
    Seite: SeiteType = Field(
        description="""Finde alle in Klammern angegebenen Lokalisationsangaben im Abschnitt 'Gutachten'.
        Selektiere davon jetzt nur diejenigen, die im nachfolgenden Text das Wort 'Karzinom' (oder eine Abwandlung wie 'Adenokarzinom') erwähnen.
        Auf Basis der Lokalisationsangaben, die jetzt noch übrig sind, bestimme die Seite des Tumors.
        Dies ist entweder 'Links', 'Rechts' oder 'Beidseitig'."""
    )


class Befundtext(BaseModel):
    Befundtext: str = Field(
        description="""Finde im ersten Dokument den Abschnitt 'Gutachten', nicht zu verwechseln mit Mikroskopischer/Makroskopischer Befundung. In diesem stehen ein
        oder mehrere Klammern mit der Lokalisation von entnommenem Gewebe und dahinter jeweils beschreibende Sätze über die Art des Gewebes.
        Selektiere davon nur die Klammern, die das Wort 'Karzinom' (oder eine Abwandlung wie 'Adenokarzinom') im nachfolgenden Text erwähnen.
        Für alle Klammern, die jetzt noch übrig geblieben sind, tue folgendes:
        Kopiere einfach die Klammer(n), zusammen mit dem Text danach, aber schneide alles nach dem ersten Satz ab.
        So, dass das Ergebnis ein oder mehrere Klammern sind, hinter denen jeweils ein Satz steht.
        Meistens ist dies das korrekte Ergebnis, was du zurückgeben sollst.

        Finde trotzdem noch zu den Klammern in deinem Ergebnis die analogen Klammern in den nachfolgenden Dokumenten.
        Wenn es hier noch zusätzliche Informationen gibt, die das Gewebe beschreiben, dann hänge diese noch an den Satz nach der Klammer an.
        Allerdings sind zusätzliche Informationen, die in Form von Zahlen angegeben sind (z.B. Hormonrezeptoren oder ICD Codes) nicht relevant!
        Nur wenn es im Fließtext noch eine weitere wichtige Angabe über die Art des Gewebes gibt, dann sollte diese auch in deiner Antwort enthalten sein. Es sollen aber zusammen
        mit dem Satz aus dem ersten Dokument kein inhaltlichen Punkte doppelt genannt werden und wenn möglich sollten die Informationen zu einem Satz 
        zusammengefasst werden, inklusive dem Satz aus dem ersten Dokument). Dabei darf die Formulierung des ersten Satzes auch leicht verändert werden. 
        
        Wenn es mehrere Klammern mit nachfolgendem Text gibt, füge vor der zweiten und jeder weiteren Klammer eine Leerzeile ein.
        """,
    )


class Hormonrezeptor(BaseModel):
    OestrogenPositiveZellkerne: Optional[int] = Field(
        None,
        description="""Ist für den Östrogen-Rezeptor (ER) eine Prozentzahl angegeben, dann extrahiere diese, allerdings nur den 
        Dezimalwert ohne Prozentzeichen""",
    )
    OestrogenFaerbeintensitaet: Optional[OestrogenFaerbeintensitaetType] = Field(
        None,
        description="""Ist für den Östrogen-Rezeptor (ER) explizit eine Stärke der Farbreaktion angegeben 
        (damit ist keine Zahl gemeint, sondern eine Beschreibung wie 'stark'), dann wähle
        auf Basis dieser Angabe einen der folgenden Werte aus: ['keine', 'schwach', 'mäßig stark', 'stark'].
        Es muss immer ein Wert aus dieser Liste sein. Ansonsten lass dieses Feld weg.""",
    )
    OestrogenIRSScore: Optional[int] = Field(
        None,
        description="""Ist für den Östrogen-Rezeptor (ER) irgendetwas angegeben, dann steht hier manchmal explizit ein IRS Wert zwischen 0 und 12 dabei.
        Dies erkennst du daran, dass das Wort 'IRS' oder 'Remmele' vorkommt und danach eine Zahl zwischen 0 und 12 steht.
        Bestimme in diesem Fall den Wert zwischen 0 und 12""",
    )
    ProgesteronPositiveZellkerne: Optional[int] = Field(
        None,
        description="""Ist für den Progesteron-Rezeptor (PR) eine Prozentzahl angegeben, dann extrahiere diese, allerdings nur den 
        Dezimalwert ohne Prozentzeichen""",
    )

    ProgesteronFaerbeintensitaet: Optional[ProgesteronFaerbeintensitaetType] = Field(
        None,
        description="""Ist für den Progesteron-Rezeptor (PR) explizit eine Stärke der Farbreaktion angegeben 
        (damit ist keine Zahl gemeint, sondern eine Beschreibung wie 'stark'), dann wähle
        auf Basis dieser Angabe einen der folgenden Werte aus: ['keine', 'schwach', 'mäßig stark', 'stark'].
        Es muss immer ein Wert aus dieser Liste sein. Ansonsten lass dieses Feld weg.""",
    )
    ProgesteronIRSScore: Optional[int] = Field(
        None,
        description="""Ist für den Progesteron-Rezeptor (PR) irgendetwas angegeben, dann steht hier manchmal explizit ein IRS Wert zwischen 0 und 12 dabei.
        Dies erkennst du daran, dass das Wort 'IRS' oder 'Remmele' vorkommt und danach eine Zahl zwischen 0 und 12 steht.
        Bestimme in diesem Fall den Wert zwischen 0 und 12""",
    )


class AllFields(BasicFields, Lokalisation, Befundtext, Seite, Hormonrezeptor):
    def __init__(self, *args):
        super().__init__(**{k: v for arg in args for k, v in arg.dict().items()})
