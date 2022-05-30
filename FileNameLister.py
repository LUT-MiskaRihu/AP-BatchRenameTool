###############################################################################
# BatchRenameTool
# Author: Mis
# Last Modified: 4.3.2022
# License: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0)
###############################################################################

# Imports
import os
import sys


# App info
APP = "FileNameFetcher"
VER = 1
BUILD = 20220322
DEV = "Miska Rihu"


# Error messages
ERR_NONE_SELECTED = "Yhtään tiedostoa ei ole valittu."
ERR_UNKNOWN_SELECTION = "Tuntematon valinta."
ERR_BAD_ID = "Virheellinen id: {0}"
DELIMITER = ","
DIRSEP = "\\"


# Subprograms, functions, etc.
def setPath(): # 1
    path = input("Anna hakemiston polku: ")
    while (True):
        if not os.path.exists(path):
            path = input("Annettua polkua ei ole, yritä uudestaan: ")
        else:
            break
    return path


def selectFiles(path): # 2
    all_files = []
    selected = []
    
    extension = ""  # Tämä rivi alustaa päätteen tyhjäksi, jolloin seuraavan rivin
                    # kommentoiminen pois saa ohjelman valitsemaan aina pdf-tiedostot
                    # ilman promptia.
    extension = input("Anna haettavien tiedostojen tyyppi (esim. txt): ")
    lkm = 0
    all_files = os.listdir(path)
    for name in all_files:
        if (extension in name):
            try:
                lkm += 1
                selected.append(name)
                print("{0}.\t{1}".format(lkm, name))
                with open("names.txt", "a", encoding="utf-8") as f:
                    f.write(name + "\n")
            except Exception as e:
                print("Tapahtui virhe:", e)
    print()

    if (selected == []):
        print("Hakukriteereitä vastaavia tiedostoja ei löytynyt.")
    else:
        print("Löydetyt tiedostot: {0} kpl".format(lkm))
    
    return selected


def saveToFile(names, path): # 4
    names.sort()
    try:
        print("Kirjoitetaan tieodostojen nimet tiedostoon.")
        file = open(path + DIRSEP + "names.txt", "a", encoding="utf-8")
        for name in names:
            file.write(name + "\n")
            print(name)
    except Exception as e:
        print("Tapahtui virhe:", e)
    print("Valmis.")
    return None


# Main program
def main():
    path = setPath()
    filenames = selectFiles(path)
    saveToFile(filenames, path)


main()
