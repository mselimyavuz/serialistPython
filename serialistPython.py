#!pip install scamp scamp-extensions python-rtmidi pynput numpy

#from scamp import test_run
#test_run.play(show_xml=True)

from scamp import * # for sound
import numpy as np # randomness



C = 60 # middle C
noteCol = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
# whole note, half note, triplet, quarter, eighth, triplet eighth, sixteenth etc.
rCol = ['w', 'h', 't', 'q', '8', 't8', '16', 't16', '32']
rVal = {'w': 4, 'h': 2, 't': 1.33, 'q': 1, '8': 0.5, 't8': 0.33, '16': 0.25, 't16': 0.166, '32': 0.125, 4: 'w', 2: 'h', 1.33: 't', 1: 'q', 0.5: '8', 0.33: 't8', 0.25: '16', 0.166: 't16', 0.125: '32'}
switchR = {'w': 0, 'h': 1, 't': 2, 'q': 3, '8': 4, 't8': 5, '16': 6, 't16': 7, '32': 8, 0: 'w', 1: 'h', 2: 't', 3: 'q', 4: '8', 5: 't8', 6: '16', 7: 't16', 8: '32'}
# fff, ff, f, mf, mp, p, pp, ppp
dCol = ['fff', 'ff', 'f', 'mf', 'mp', 'p', 'pp', 'ppp', 'r']
dVal = {'fff': 1.0,'ff': 0.875,'f': 0.75,'mf': 0.625,'mp': 0.5,'p': 0.375, 'pp': 0.25, 'ppp': 0.125, 'r': 0, 1.0: 'fff', 0.875: 'ff', 0.75: 'f', 0.625: 'mf', 0.5: 'mp', 0.375: 'p', 0.25: 'pp', 0.125: 'ppp', 0: 'r'}
switchD = {'fff': 0,'ff': 1,'f': 2,'mf': 3,'mp': 4,'p': 5, 'pp': 6, 'ppp': 7, 'r': 8, 0: 'fff', 1: 'ff', 2: 'f', 3: 'mf', 4: 'mp', 5: 'p', 6: 'pp', 7: 'ppp', 8: 'r'}
# 1, 2, 3, 4, 5, 6, 7
oCol = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th']
oVal = {'1st': 1, '2nd': 2, '3rd': 3, '4th': 4, '5th': 5, '6th': 6, '7th': 7, 1: '1st', 2: '2nd', 3: '3rd', 4: '4th', 5: '5th', 6: '6th', 7: '7th'}
switchO = {'1st': 0, '2nd': 1, '3rd': 2, '4th': 3, '5th': 4, '6th': 5, '7th': 6, 0: '1st', 1: '2nd', 2: '3rd', 3: '4th', 4: '5th', 5: '6th', 6: '7th'}
switch = {
    'C': 0,
    'C#': 1,
    'D': 2,
    'D#': 3,
    'E': 4,
    'F': 5,
    'F#': 6,
    'G': 7,
    'G#': 8,
    'A': 9,
    'A#': 10,
    'B': 11,
    0: 'C',
    1: 'C#',
    2: 'D',
    3: 'D#',
    4: 'E',
    5: 'F',
    6: 'F#',
    7: 'G',
    8: 'G#',
    9: 'A',
    10: 'A#',
    11: 'B'
}
def getMIDINum(note, octave):
    return C+switch.get(note)+((octave-4)*12)
def reverseMIDINum(note, octave):
    return switch.get(note-C-((octave-4)*12))
def part(session, which_inst, amp, melody, rh, oc, instName):
    i = 0
    while i < 12:
        currentA = amp[i]
        currentR = rh[i]
        currentP = melody[i]
        currentO = oc[i]
        print(f"{instName} PLAYING {reverseMIDINum(currentP, currentO)}{currentO} PITCH WITH A RHYTHMIC VALUE OF {rVal.get(currentR)} AND THE DYNAMIC VALUE IS {dVal.get(currentA)}")
        if currentA == 0:
            which_inst.play_note(currentP, 0.000001, currentR)
        else:
            which_inst.play_note(currentP, currentA, currentR)
        i += 1

def createRow(col, sw):
    notes = col.copy()
    toneRow = []
    tones = 0
    mod = len(notes)
    while tones < 12:
        randomPop = np.random.randint(0,len(notes))
        note = notes.pop(randomPop)
        toneRow.append(note)
        tones += 1
        if len(col) < 12:
            notes = col.copy()

    tones = 0
    toneRowSemitone = []

    while tones < 12:
        toneRowSemitone.append(sw.get(toneRow[tones]))
        tones += 1

    tones = 1
    shift = [0]
    while tones < 12:
        shift.append((sw.get(toneRow[tones])-sw.get(toneRow[0]))%mod)
        tones += 1
    return toneRow, toneRowSemitone, shift

def createMatrix(rs, rsh, sw):
    mod = len(sw)//2
    matrix = []
    matrixNote = []
    inversion = []
    note = 0
    while note < 12:
        inversion.append(((rs[0]+(mod-rsh[note]))%mod))
        note += 1

    for prime in inversion:
        p = []
        pNote = []
        note = 0
        while note < 12:
            p.append((prime+rsh[note])%mod)
            pNote.append(sw.get((prime+rsh[note])%mod))
            note += 1
        matrix.append(p)
        matrixNote.append(pNote)

    return matrixNote, matrix

def printMatrix(matrix, sw):
    flag = 0
    if sw == switch:
        flag = 1
    if flag == 1:
        print("", end="\t")
        for note in matrix[0]:
            noteNum = sw.get(note)
            print("I" + str(noteNum), end="\t")
        print()

    for i in matrix:
        if flag == 1:
            print("P" + str(sw.get(i[0])), end="\t")
        for j in i:
            print(j, end="\t")
        if flag == 1:
            print("R" + str(sw.get(i[0])))
        else:
            print()
    if flag == 1:
        print("", end="\t")
        for note in matrix[0]:
            noteNum = sw.get(note)
            print("RI" + str(noteNum), end="\t")

    print()

def getDirection(matrix, ty, instNum):
    direction = [0, 1, 2, 3]
    randomNum = np.random.randint(0,12)
    flag = np.random.randint(0,4)
    if flag == 0:
        if ty == 1: print(f"Selecting P{randomNum} for inst {instNum+1}")
        return matrix[randomNum,:] # select a prime row
    elif flag == 1:
        if ty == 1: print(f"Selecting I{randomNum} for inst {instNum+1}")
        return matrix[:,randomNum] # select an inversion row
    elif flag == 2:
        if ty == 1: print(f"Selecting R{randomNum} for inst {instNum+1}")
        return matrix[randomNum,::-1] # select a retrograde row
    elif flag == 3:
        if ty == 1: print(f"Selecting RI{randomNum} for inst {instNum+1}")
        return matrix[::-1,randomNum] # select a retrograde inversion row

# tone row
tr, trs, s = createRow(noteCol, switch)
print("tone row done")
mn, m = createMatrix(trs, s, switch)
print("tone matrix done")
# dynamics row
dr, drs, ds = createRow(dCol, switchD)
print("dynamics row done")
dn, d = createMatrix(drs, ds, switchD)
print("dynamics matrix done")
# rhythmic row
rhr, rhrs, rhs = createRow(rCol, switchR)
print("rhytmic row done")
rhn, rh = createMatrix(rhrs, rhs, switchR)
print("rhytmic matrix done")
# octave row
ocr, ocrs, ocs = createRow(oCol, switchO)
print("octave row done")
ocn, oc = createMatrix(ocrs, ocs, switchO)
print("octave matrix done")

oMatrix = np.array(oc)
tMatrix = np.array(m) # for column ops
rMatrix = np.array(rh) # for column ops
dMatrix = np.array(d) # for column ops

print("\nOctave Matrix\n")
printMatrix(ocn, switchO)
print("\nRhythm Matrix\n")
printMatrix(rhn, switchR)
print("\nDynamics Matrix\n")
printMatrix(dn, switchD)
print("\nTone Matrix\n")
printMatrix(mn, switch)

voices = 4 # how many voices in the polyphony
MIN_ITERATION = 1
MAX_ITERATION = 2

iterations = np.random.randint(MIN_ITERATION, MAX_ITERATION) # how many rows to use
oEnsemble = []
tEnsemble = []
dEnsemble = []
rEnsemble = []
t = 0
while t < voices:
    oPerf = []
    tPerf = []
    dPerf = []
    rPerf = []

    j = 0
    while j < iterations:
        oPlay = []
        tPlay = []
        dPlay = []
        rPlay = []

        i = 0
        while i < 12:
            oPlay.append(oVal.get(switchO.get(getDirection(oMatrix,0, t)[i])))
            dPlay.append(dVal.get(switchD.get(getDirection(dMatrix,0, t)[i])))
            rPlay.append(rVal.get(switchR.get(getDirection(rMatrix,0, t)[i])))
            i += 1

        i = 0
        while i < 12:
            tPlay.append(getMIDINum(switch.get(getDirection(tMatrix, 1, t)[i]), oPlay[i]))
            i += 1
        #print(tPlay)

        oPerf.append(oPlay)
        tPerf.append(tPlay)
        dPerf.append(dPlay)
        rPerf.append(rPlay)

        j += 1
    oEnsemble.append(oPerf)
    tEnsemble.append(tPerf)
    dEnsemble.append(dPerf)
    rEnsemble.append(rPerf)
    t += 1

TEMPO_MIN = 80
TEMPO_MAX = 140
tempoRand = np.random.randint(TEMPO_MIN, TEMPO_MAX)
session = Session(tempo = tempoRand)
# session.print_default_soundfont_presets() # select instrument
# session.fast_forward_in_beats(1000)
piano1 = session.new_part("Piano Merlin") # piano sound
piano2 = session.new_part("Piano Merlin") # piano sound
piano3 = session.new_part("Piano Merlin") # piano sound
piano4 = session.new_part("Piano Merlin") # piano sound

print(f"\n\n\n\nTempo is {tempoRand}bpm, playing {iterations} rows.\n\n\n\n")
session.start_transcribing()
i = 0
while i < iterations:
    clock1 = session.fork(part, args=(session, piano1, dEnsemble[0][i], tEnsemble[0][i], rEnsemble[0][i], oEnsemble[0][i], "Piano #1"))
    clock2 = session.fork(part, args=(session, piano2, dEnsemble[1][i], tEnsemble[1][i], rEnsemble[1][i], oEnsemble[1][i], "Piano #2"))
    clock3 = session.fork(part, args=(session, piano3, dEnsemble[2][i], tEnsemble[2][i], rEnsemble[2][i], oEnsemble[2][i], "Piano #3"))
    clock4 = session.fork(part, args=(session, piano3, dEnsemble[3][i], tEnsemble[3][i], rEnsemble[3][i], oEnsemble[3][i], "Piano #4"))

    wait_for_children_to_finish()
    wait(5)

    i += 1
performance = session.stop_transcribing()
performance.to_score().show()
