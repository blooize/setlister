from icecream import ic
import sys
import mutagen
import serato_markers2 as sm2

def readMp3Data(path):
    tagfile = mutagen.File(path)
    data = tagfile['GEOB:Serato Markers2'].data

    entries = list(sm2.parse(data))
    cues = list()
    for cue in entries:
        if cue.NAME == 'CUE':
            cues.append({cue.index, cue.position})
    
    return cues

def main():
    cues = list()
    cues.append(readMp3Data('/Users/simon/Music/NeuroFunk/Agressor Bunx - Tornado.mp3'))
    ic(cues)
    
    return 0
if __name__ == '__main__':
    sys.exit(main())
