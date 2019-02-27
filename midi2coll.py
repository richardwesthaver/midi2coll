from mido import MidiFile, second2tick
from os import listdir
from os.path import isdir, isfile, splitext

# seq, start, dur, pitch, velocity


def midi_parse(arg):

    def write(arg):
        seq = 1
        t = 0.
        coll = []
        for msg in MidiFile(str(arg)):
            print(msg)
            tpb = 480
            if msg.dict().get('type') == 'set_tempo':
                tempo = msg.dict().get('tempo')
            if msg.dict().get('type') == 'note_on':
                msg = msg.dict()
                t += float(second2tick(msg.get('time'), ticks_per_beat=tpb, tempo=int(tempo)))
                if not msg.get('velocity') == 0:
                    n = msg.get('note')
                    v = msg.get('velocity')
                    coll.append([seq, t, 0, n, v])
                elif msg.get('velocity') == 0:
                    n = msg.get('note')
                    key = max(k for k, v in enumerate(coll) if (v[3] == n))
                    coll[key][2] = t-coll[key][1]
        with open(splitext(arg)[0]+'.txt', 'w+') as file:
            for i in range(len(coll)):
                file.write('{0}, {1};\n'.format(i, "".join(x for x in str(coll[i]) if x not in '[],')))
            file.close()

    if isdir(arg):
        d_files = [f for f in listdir(arg) if isfile(f)]
        for f in d_files:
            write(f)
    elif isfile(arg):
        write(arg)


midi=input('midi file or directory: ')
midi_parse(midi)
