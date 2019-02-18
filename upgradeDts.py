
import sys
import json
import glob

import readDts
import mapObjects
import writeObj

from collections import namedtuple

def upgradeObject(oldObject):
    newObject = {}
    newObject["nameIndex"] = oldObject.fName
    # objects/meshes are 1:1 in the old format
    newObject["numMeshes"] = 1
    newObject["startMeshIndex"] = oldObject.fMeshIndex
    # figure out what this is
    # probably either the index of the next item
    # or the index of the next object of this object's node
    # which should be the next object
    newObject["nextSibling"] = 0
    newObject["nodeIndex"] = oldObject.fNodeIndex
    # need to find out what this should be
    # and if 0 is okay
    newObject["firstDecal"] = 0

    return newObject

def upgradeNode(oldNode):
    newNode = {}
    newNode["nameIndex"] = oldNode.fName
    newNode["parentIndex"] = oldNode.fParent
    # need to iterate through
    # the objects to get this
    newNode["firstObject"] = 0
    # just to give us more work
    newNode["firstChild"] = 0
    newNode["nextSibling"] = 0
    return newNode

def upgradeTransform(oldTransform):
    magicValue = 32767
    newRotation = {}
    newTranslation = {}
    newRotation["x"] = oldTransform.fRotateX / magicValue
    newRotation["y"] = oldTransform.fRotateY / magicValue
    newRotation["z"] = oldTransform.fRotateZ / magicValue
    newRotation["Z"] = oldTransform.fRotateW / magicValue
    newTranslation["x"] = oldTransform.fTranslateX
    newTranslation["y"] = oldTransform.fTranslateY
    newTranslation["z"] = oldTransform.fTranslateZ
    return (newRotation, newTranslation)

def upgradeMesh(oldMesh):
    newMesh = {}
    # whoah, hold on there
    # need to figure this one out
    newMesh["type"] = 0
    # number of key frames
    # not frames used to unpack
    # verts
    newMesh["numFrames"] = 0
    newMesh["numMatFrames"] = 0
    # has to be calculated
    newMesh["parentMesh"] = 0
    # should be the first verts
    # need to verify
    newMesh["bounds"] = 0
    # might be shared with the rest of the shape
    newMesh["center"] = 0
    newMesh["radius"] = oldMesh.radius
    newMesh["numVerts"] = oldMesh.numVerts
    oldMesh = someMesh.frames[0]
    scaleX = firstFrame.scaleX
    scaleY = firstFrame.scaleY
    scaleZ = firstFrame.scaleZ

    originX = firstFrame.originX
    originY = firstFrame.originY
    originZ = firstFrame.originZ
    expandedVertices = []
    newMesh["verts"] = expandedVertices
    for vert in oldMesh.verts:
        newVert = (vert.x * scaleX + originX, vert.y * scaleY + originY, vert.z * scaleZ + originZ)
        expandedVertices.append(newVert)
    newMesh["numTVerts"] = oldVert.numTexVerts
    # figure out this one
    newMesh["tverts"] = []
    # is this the same?
    newMesh["norms"] = []
    newMesh["encodedNormals"] = []
    newMesh["numPrimitives"] = oldVert.numFaces
    primitives = []
    indices = []
    newMesh["primitives"] = primitives
    newMesh["numIndices"] = len(oldVert.faces) * 3
    newMesh["indices"] = primitives
    newMesh["numMergeIndices"] = 0
    newMesh["mergeIndices"] = []
    newMesh["mVertsPerFrame"] = oldVert.mVertsPerFrame
    # oi, what's this?
    newMesh["flags"] = 0
    for face in oldVert.faces:
        newPrimitive = {}
        newPrimitive["start"] = len(indices)
        newPrimitive["numElements"] = 3
        newPrimitive["matIndex"] = face.material
        indices.append(face.vi1)
        indices.append(face.vi2)
        indices.append(face.vi3)
        primitives.append(newPrimitive)


def upgradeSequence(oldSequence, oldSubSequence, oldKeyframe):
    newSequence = {}
    newSequence["nameIndex"] = oldSequence.fName
    # hey, figure me out please
    newSequence["flags"] = 0
    newSequence["numKeyFrames"] = oldSubSequence.fnKeyframes
    newSequence["duration"] = oldSequence.fDuration
    newSequence["priority"] = oldSequence.fPriority
    newSequence["firstGroundFrame"] = 0
    newSequence["numGroundFrames"] = 0
    # this comes from the node
    # or from the first key frame
    # which usually are the same
    newSequence["baseRotation"] = oldKeyframe.fKeyValue
    newSequence["baseTranslation"] = oldKeyframe.fKeyValue
    newSequence["baseScale"] = oldKeyframe.fKeyValue
    # need to understand object state first
    newSequence["baseObjectState"] = 0
    newSequence["baseDecalState"] = 0
    newSequence["firstTrigger"] = oldSequence.fFirstFrameTrigger
    newSequence["numTriggers"] = oldSubSequence.fNumFrameTriggers
    newSequence["toolBegin"] = 0
    # the fun stuff
    newSequence["rotationMatters"] = {}
    newSequence["translationMatters"] = {}
    newSequence["scaleMatters"] = {}
    newSequence["decalMatters"] = {}
    newSequence["iflMatters"] = {}
    newSequence["visMatters"] = {}
    newSequence["frameMatters"] = {}
    newSequence["matFrameMatters"] = {}

def upgradeTrigger(oldTrigger):

def upgradeName(oldName):
    return nodeName = oldName.name.split("\0")[0] + "\0"


with open('structures.json') as f:
    structures = json.load(f)

importFilenames = sys.argv[1:]

for importFilename in importFilenames:
    exportFilename = importFilename.replace(importFilename, "upgraded/" + importFilename )

    print "reading " + importFilename
    try:
        with open(importFilename, "rb") as input_fd:
            # first get the parsed shape datastructures
            rawData = input_fd.read()
            shape = readDts.readDtsData(structures, rawData)

        # save a new file
#        with open(exportFilename,"w") as shapeFile:

    except Exception as e:
        print e
