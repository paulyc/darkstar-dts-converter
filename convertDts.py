
import sys
import json

import readDts
import mapObjects
import writeObj
import volinfo

with open('structures.json') as f:
    structures = json.load(f)

importFilenames = sys.argv[1:]

for importFilename in importFilenames:
    if importFilename.endswith("vol") or importFilename.endswith("VOL"):
        with open(importFilename, "rb") as volFile:
            rawVolFile = volFile.read()

        file_info = archive_module.get_file_metadata(raw_data)
    else:
        exportFilename = importFilename.replace(".dts", ".obj").replace(".DTS", ".obj")
        exportFilenameWithoutExtension = exportFilename.split(".obj")[0]
        print("reading " + importFilename)
        try:
            with open(importFilename, "rb") as input_fd:
                # first get the parsed shape datastructures
                rawData = input_fd.read()
                shape = readDts.readDtsData(structures, rawData)
            # then map them for conversation later
            mappedDetails = mapObjects.mapObjects(shape, False)

            for detail in mappedDetails:
                try:
                    exportFilename.split("0")
                    newFilename = exportFilenameWithoutExtension + "_" + detail.rootNode.name.decode("utf-8") + ".obj"
                    print("writing " + newFilename)
                    # save a new file
                    with open(newFilename,"w") as shapeFile:
                        #TODO move the normal table out of the obj writer into the object mapper
                        writeObj.writeObj(detail.rootNode, structures["normalTable"], shapeFile)
                    print("completed " + newFilename)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
