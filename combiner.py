from icecream import ic
import sys
import mutagen
import serato_markers2 as sm2
import base64

def readMp3Data(path):
    name = path.split('/')[-1]

    tagfile = mutagen.File(path)
    data = tagfile['GEOB:Serato Markers2'].data

    entries = list(sm2.parse(data))
    cues = list()
    for cue in entries:
        if cue.NAME == 'CUE':
            cues.append(
                {
                    "index": cue.index,
                    "milliseconds": cue.position,
                    "name": name
                })
                
    return cues

# for some reason Flacs store the data diffrently inside the vorbis comment block compared to OGG????
def readFlacData(path):
    
    name = path.split('/')[-1]

    tagfile = mutagen.File(path)
    data = tagfile['serato_markers_v2']

    b64data = data[0].replace('\n', '')


    decoded = base64.b64decode(b64data + findPadding(b64data))
    decoded = decoded.removeprefix(b'application/octet-stream\x00\x00Serato Markers2\x00')
    entries = list(sm2.parse(decoded))
    cues = list()
    for cue in entries:
        if cue.NAME == 'CUE':
            #why tf is the object flipped
            cues.append(
                {
                    "index": cue.index, 
                    "milliseconds": cue.position,
                    "name": name
                })
                                    
    return cues


def findPadding(data):
    
    padding = 'A==' if len(data) % 4 == 1 else ('=' * (-len(data) % 4))

    return padding

def main():
    cues = list()
    cues.append(readMp3Data('/Users/simon/Music/NeuroFunk/Agressor Bunx - Tornado.mp3'))
    cues.append(readFlacData('/Users/simon/Music/midtempo/Alix Perez - Acid Jam (Original Mix).flac'))
    ic(cues)
    
    return 0
if __name__ == '__main__':
    sys.exit(main())
