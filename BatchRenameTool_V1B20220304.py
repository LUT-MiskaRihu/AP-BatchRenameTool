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
APP = "BatchRenameTool"
VER = 1
BUILD = 20220304
DEV = "Miska Rihu"


# Error messages
ERR_NONE_SELECTED = "Yhtään tiedostoa ei ole valittu."
ERR_UNKNOWN_SELECTION = "Tuntematon valinta."
ERR_BAD_ID = "Virheellinen id: {0}"
DELIMITER = ","
DIRSEP = "\\"


# Classes
class FILE:
    prefix = 0
    filename = ""
    old_filename = ""
    new_filename = ""    


# Subprograms, functions, etc.
def menu(path):
    print("Valikko:")
    print("1) Aseta hakemiston polku (nykyinen: '{0}')".format(path))
    print("2) Valitse uudelleennimettävät tiedostot")
    print("3) Lisää alkunollat")
    print("4) Tallenna tiedostojen nimet tiedostoon")
    print("0) Lopeta")
    i = input("Valintasi: ")
    print()
    return i


def setPath(): # 1
    path = input("Anna hakemiston polku: ")
    while (True):
        if not os.path.exists(path):
            path = input("Annettua polkua ei ole, yritä uudestaan: ")
        else:
            break
    return path    


def renameFiles(files, path): # 3
    names = []
    
    for file in files:
        if (0 <= file.prefix <= 9):
            file.prefix = "00" + str(file.prefix)
        elif (10 <= file.prefix <= 99):
            file.prefix = "0" + str(file.prefix)
        else :
            file.prefix = str(file.prefix)
        
        file.new_filename = file.prefix + "_" + file.filename
        print(file.old_filename)
        print("-->", file.new_filename)
        print()
    
    print()
    print("Tiedostojen nimeämistä EI VOIDA PERUA.")
    while (True):
        answer = input("Haluatko varmasti nimetä em. tiedostot uudelleen (k/e): ")
        if (answer == "k"):
            for file in files:
                names.append(file.new_filename)
                os.rename(path + DIRSEP + file.old_filename, path + DIRSEP + file.new_filename)
            print("Tiedostot nimettiin uudelleen.")
            break
        elif (answer == "e"):
            for file in files:
                names.append(file.old_filename)
            print("Tiedostojen uudelleennimeäminen peruutettiin.")
            break
        else:
            print(ERR_UNKNOWN_SELECTION)

    return names


def selectFiles(path): # 2
    all_files = []
    selected = []
    
    extension = ""  # Tämä rivi alustaa päätteen tyhjäksi, jolloin seuraavan rivin
                    # kommentoiminen pois saa ohjelman valitsemaan aina pdf-tiedostot
                    # ilman promptia.
    extension = input("Anna haettavien tiedostojen tyyppi (oletus: pdf): ")
    if (extension == ""):
        extension = ".pdf"
    else:
        extension = "." + extension
    
    all_files = os.listdir(path)
    for f in all_files:
        if (extension in f):
            try:
                file = FILE()
                file.old_filename = f
                properties = f.split("_")
                file.prefix = int(properties[0])
                for i in range(1, len(properties)):
                    file.filename += properties[i]
                    if (i < len(properties)-1):
                        file.filename += "_"    
                selected.append(file)
                print("Löydettiin tiedosto:", file.filename)
            except Exception as e:
                print("Odottamaton virhe:", e)
    print()
    
    while (True):
        if (selected == []):
            print("Hakukriteereitä vastaavia tiedostoja ei löytynyt.")
            break
        else:
            print("Valitut tiedostot:")
            for i in range(len(selected)):
                print("{0}.\t{1}".format(i, selected[i].old_filename))
            print()
            buffer = input("Muokkaa valintaa (k/e): ")
            if (buffer == "k"):
                selected = modifySelection(selected)
            elif (buffer == "e"):
                break
            else:
                print(ERR_UNKNOWN_SELECTION)
    
    return selected


def modifySelection(selected):
    print("Poista tiedostoja valinnasta antamalla niiden id:t pilkulla erotettuna.")
    while (True):
        argv = []
        buffer = input("Anna id(:t) (x palaa edelliseen valikkoon): ")
        
        if (buffer == "x"):
            break
        elif (DELIMITER in buffer):
            argv = buffer.split(DELIMITER)
            argv.sort()
        elif (buffer.isdigit()):
            argv = [buffer]
        else:
            print(ERR_UNKNOWN_SELECTION)
            break
        
        j = 0
        for i in argv:
            if not (i.isdigit()):
                print(ERR_BAD_ID.format(i))
            else:
                i = int(i) - j
                if (0 <= i <= len(selected)):
                    #print("'{0}' poistettiin valinnasta".format(selected[i].old_filename))
                    selected.pop(i)
                    j += 1
                else:
                    print(ERR_BAD_ID.format(i))
        print()
        break
    return selected


def saveToFile(names, path): # 4
    names.sort()
    try:
        print("Kirjoitetaan tieodostojen nimet tiedostoon.")
        file = open(path + DIRSEP + "names.txt", "w")
        for name in names:
            file.write(name + "\n")
            print(name)
    except Exception as e:
        print("Tapahtui virhe:", e)
    print("Valmis.")
    return None


# Main program
def main():
    path = "."
    files = []
    filenames = []
    
    print(APP)
    print("Version/Build: {0}/{1}".format(VER, BUILD))
    print("Author:", DEV)
    print()
    
    while (True):
        selection = menu(os.path.abspath(path))
        if (selection == "0"):
            break
        elif (selection == "1"):
            path = setPath()
        elif (selection == "2"):
            files = selectFiles(path)
        elif (selection == "3"):
            if (files == []):
                print(ERR_NONE_SELECTED)
            else:
                filenames = renameFiles(files, path)
        elif (selection == "4"):
            if (files == []):
                print(ERR_NONE_SELECTED)
            else:
                saveToFile(filenames, path)
        else:
            print(ERR_UNKNOWN_SELECTION)
        print()
    print("Kiitos ohjelman käytöstä.")
    return None


main()
