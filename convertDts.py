
import os
import sys
import json
import glob

import readDts
import mapObjects
import writeObj
import volinfo



def exportDtsToObj(importFilename, rawData):
    exportFilename = importFilename.replace(".dts", ".obj").replace(".DTS", ".obj")
    exportFilenameWithoutExtension = exportFilename.split(".obj")[0]
    shape = readDts.readDtsData(structures, rawData)
    # then map them for conversation later
    mappedDetails = mapObjects.mapObjects(shape, False)

    for detail in mappedDetails:
        try:
            exportFilename.split("0")
            newFilename = exportFilenameWithoutExtension + "_" + detail.rootNode.name.decode("utf-8") + ".obj"
            print("writing " + newFilename)
            # save a new file
            with open(newFilename, "w") as shapeFile:
                # TODO move the normal table out of the obj writer into the object mapper
                writeObj.writeObj(detail.rootNode, structures["normalTable"], shapeFile)
            print("completed " + newFilename)
        except Exception as e:
            print(e)


with open('structures.json') as f:
    structures = json.load(f)

importFilenames = []

for importFilename in sys.argv[1:]:
    files = glob.glob(importFilename)
    importFilenames.extend(files)

for importFilename in importFilenames:
    if importFilename.endswith("vol") or importFilename.endswith("VOL"):
        with open(importFilename, "rb") as volFile:
            rawVolFile = volFile.read()

        destDir = importFilename.replace(".vol", "").replace(".VOL", "")

        if not os.path.exists(destDir):
            os.makedirs(destDir)
        file_info = volinfo.get_file_metadata(rawVolFile)
        for file in file_info:
            if file.filename.endswith(".dts") or file.filename.endswith(".DTS"):
                try:
                    exportDtsToObj(os.path.join(destDir, file.filename), rawVolFile[file.start_offset:file.end_offset])
                except Exception as e:
                    print(e)
    else:
        print("reading " + importFilename)
        try:
            with open(importFilename, "rb") as input_fd:
                # first get the parsed shape datastructures
                rawData = input_fd.read()
                exportDtsToObj(importFilename, rawData)
        except Exception as e:
            print(e)
