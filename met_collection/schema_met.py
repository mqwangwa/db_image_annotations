from enum import Enum
import typing_extensions as typing
import pandas as pd

df = pd.read_excel("FilteredObjects.xlsx")


class Department(Enum):
    dept1 = "American Decorative Arts"
    # dept 2 missing
    dept3 = "Ancient Near Eastern Art"
    dept4 = "Arms and Armor"
    dept5 = "Arts of Africa, Oceania, and the Americas"
    dept6 = "Asian Art"
    dept7 = "The Cloisters"
    dept8 = "The Costume Institute"
    dept9 = "Drawings and Prints"
    dept10 = "Egyptian Art"
    dept11 = "European Paintings"
    dept12 = "European Sculpture and Decorative Arts"
    dept13 = "Greek and Roman Art"
    dept14 = "Islamic Art"
    dept15 = "The Robert Lehman Collection"
    dept16 = "The Libraries"
    dept17 = "Medieval Art"
    dept18 = "Musical Instruments"
    dept19 = "Photographs"
    dept21 = "Modern Art"


class Period(Enum):
    period1 = 'Edo period (1615–1868)'
    period2 = 'Meiji period (1868–1912)'
    period3 = 'Ming dynasty (1368–1644)'
    period4 = 'Qing dynasty (1644–1911)'
    period5 = 'Edo (1615–1868) or Meiji period (1868–1912)'
    period6 = 'Qing dynasty (1644–1911), Qianlong period (1736–95)'
    period7 = 'Qing dynasty (1644–1911), Kangxi period (1662–1722)'
    period8 = 'Hellenistic'
    period9 = 'Early Imperial'
    period10 = 'Archaic'
    period11 = 'Classical'
    period12 = 'Late Archaic'
    period13 = 'Late Classical'
    period14 = 'Archaic/Classical'
    period15 = 'Sasanian'
    period16 = 'Late Archaic/Early Classical'


class Classification(Enum):
    classification1 = 'Prints'
    classification2 = 'Metalwork'
    classification3 = 'Glass'
    classification4 = 'Sculpture'
    classification5 = 'Textiles-Embroidered'
    classification6 = 'Textiles-Woven'
    classification7 = 'Textiles'
    classification8 = 'Vases'
    classification9 = 'Ceramics'


class Culture(Enum):
    culture1 = 'Japan'
    culture2 = 'China'
    culture3 = 'Greek'
    culture4 = 'Roman'
    culture5 = 'Cypriot'
    culture6 = 'Greek, Attic'
    culture7 = 'Etruscan'
    culture8 = 'Sasanian'


class Medium(Enum):
    medium1 = 'Woodblock print; ink and color on paper'
    medium2 = 'Bronze'
    medium3 = 'Glass'
    medium4 = 'Silver'
    medium5 = 'Gold'
    medium6 = 'Stone'
    medium7 = 'Silk'
    medium8 = 'Terracotta'
    medium9 = 'Ceramic'


class Schema(typing.TypedDict):
    department: Department
    period: Period
    classification: Classification
    culture: Culture
    medium: Medium
