from enum import Enum

from attr import field


class GeschlechtType(Enum):
    w = "weiblich"
    m = "männlich"
    d = "divers"


class OrtType(Enum):
    M = "Meine Einrichtung"
    A = "Andere Einrichtung"
    N = "N.n.b. andere Einrichtung"


class PathologischesInstitut1Type(Enum):
    UKA = "Uniklinikum RWTH Aachen"
    Andere_Einrichtung = "Andere Einrichtung"


class PathologischesInstitut2Type(Enum):
    PA = "Pathologie"
    PA_MVZ = "Pathologie MVZ UKA"


class PraeparatType(Enum):
    B = "Biopsie"
    R = "Resektat"
    S = "Sonstiges"
    U = "Unbekannt"


class BiopsieartType(Enum):
    S = "Stanzbiopsie"
    CT = "CT-Stanze"
    F = "Fusionsbiopsie"
    TUR = "TUR (Tumorspäne)"
    V = "Vakuumbiopsie"
    SV = "Stereotaktische Vakuumbiopsie"
    FNP = "FNP (Feinnadelpunktion)"
    Z = "Zangenbiopsie"
    O = "Offene Biospie"
    K = "Knochenmarkbiopsie"
    SCH = "Schlingenbiopsie"
    A = "Andere Biospie"
    U = "Unbekannt"


class EntnahmestelleType(Enum):
    P = "Primärtumor"
    R = "Rezidiv"
    L = "Lymphknoten"
    M = "Metastase"


class ICDO3HistologieType(Enum):
    nicht_invasiv_0 = "8500/2"
    nicht_invasiv_1 = "8520/2"
    nicht_invasiv_2 = "8522/2"
    nicht_invasiv_3 = "8540/3"
    nicht_invasiv_4 = "8543/3"

    invasiv_0 = "8211/3"
    invasiv_1 = "8480/3"
    invasiv_2 = "8500/3"
    invasiv_3 = "8510/3"
    invasiv_4 = "8520/3"
    invasiv_5 = "8522/3"

    inflammatorisch_0 = "8530/3"

    selten_0 = "8020/3"
    selten_1 = "8022/3"
    selten_2 = "8200/3"
    selten_3 = "8314/3"
    selten_4 = "8315/3"
    selten_5 = "8502/3"
    selten_6 = "8503/3"
    selten_7 = "8504/3"
    selten_8 = "8523/3"
    selten_9 = "8524/3"
    selten_10 = "8541/3"


class LokalisationType(Enum):
    field_0 = "Mamille"
    field_1 = "Zentraler Drüsenkörper der Brust"
    field_2 = "Oberer innerer Quadrant der Brust"
    field_3 = "Unterer innerer Quadrant der Brust"
    field_4 = "Oberer äußerer Quadrant der Brust"
    field_5 = "Unterer äußerer Quadrant der Brust"
    field_6 = "Recessus axillaris der Brust"
    field_8 = "Brust, mehrere Teilbereiche überlappend"


class Ja_NeinType(Enum):
    field_1 = "Ja"
    field_0 = "Nein"


class GradingType(Enum):
    field_1 = "G1"
    field_2 = "G2"
    field_3 = "G3"
    field_4 = "G4"
    field_X = "GX"


class TNM_nachType(Enum):
    UICC = "UICC"
    AJCC = "AJCC"


class OestrogenFaerbeintensitaetType(Enum):
    field_0 = "keine"
    field_1 = "schwach"
    field_2 = "mäßig stark"
    field_3 = "stark"


class ProgesteronFaerbeintensitaetType(Enum):
    field_0 = "keine"
    field_1 = "schwach"
    field_2 = "mäßig stark"
    field_3 = "stark"


class HER2neuType(Enum):
    field_0 = "0"
    field_1 = "1+"
    field_2 = "2+"
    field_3 = "3+"


class SeiteType(Enum):
    L = "Links"
    R = "Rechts"
    B = "Beidseitig"
    M = "Mittellinie"
    T = "Trifft nicht zu"
    U = "Unbekannt"
