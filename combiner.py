from icecream import ic
import sys
import mutagen
import serato_markers2 as sm2
import base64
import parse_crate as pc
import argparse
import json

def readMp3Data(path):
    name = path.split('/')[-1]

    tagfile = mutagen.File(path)
    data = tagfile['GEOB:Serato Markers2'].data
    # ic(data)
    entries = list(sm2.parse(data))
    cues = createCueList(entries)
    cues.append({"name": name})

    return cues

# for some reason Flacs store the data diffrently inside the vorbis comment block compared to OGG????
def readFlacData(path):
    
    name = path.split('/')[-1]

    tagfile = mutagen.File(path)
    data = tagfile['serato_markers_v2']

    #Flac base64 decoding
    b64data = data[0].replace('\n', '')
    decoded = base64.b64decode(b64data + findPadding(b64data))
    decoded = decoded.removeprefix(b'application/octet-stream\x00\x00Serato Markers2\x00')
    # ic(decoded)
    entries = list(sm2.parse(decoded))
    cues = createCueList(entries)       
    cues.append({"name": name})

    return cues

# def readOggData(path):
#     name = path.split('/')[-1]

#     tagfile = mutagen.File(path)
#     data = tagfile['serato_markers2']
#     data = data[0]
#     b64data = data.replace('\n', '')
#     foo = str.encode(b64data) + findPadding(b64data).encode()
#     decode = base64.b64decode(foo)




def createCueList(entries):
    cues = list()
    for cue in entries:
        if cue.NAME == 'CUE':
            #why tf is the object flipped, why isnt it when i do this
            cues.append(
                {
                    "index": cue.index, 
                    "milliseconds": cue.position,
                })
                                    
    return cues

def findPadding(data):
    
    padding = 'A==' if len(data) % 4 == 1 else ('=' * (-len(data) % 4))

    return padding

def calcSetLength(cues):
    length = 0
    for cue in cues:
        length += (cue[1]['milliseconds'] - cue[0]['milliseconds'])
    
    return length

def getSetlist(file):
    list = pc.loadcrate(file)
    trunked = list[9:]
    titles = []
    for t in trunked:
        name = t[1][0][1]
        filetype = name.split('.')[-1]
        titles.append({ "name": name, "type": filetype })

    fixed = []
    for title in titles:
        fixed.append(title)

    return fixed

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('crate', metavar='CRATE')

    args = parser.parse_args(argv)
    cues = list()

    for file in getSetlist(args.crate):
        if file['type'] == 'mp3':
            cues.append(readMp3Data("/" + file['name']))
        elif file['type'] == 'flac':
            cues.append(readFlacData("/" + file['name']))
        else:
            print(file["name"] + " is currently incompatible, or not a music file")
    length = round(calcSetLength(cues)/1000/60, 2)
    data = {"length": str(length) + " minutes", "setlist": cues}
    dump = json.dumps(data)

    return dump

if __name__ == '__main__':
    sys.exit(main())
