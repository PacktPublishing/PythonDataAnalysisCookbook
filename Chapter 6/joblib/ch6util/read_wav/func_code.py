# first line: 10
@memory.cache
def read_wav():
    wav = dl.data.get_smashing_baby()

    return wavfile.read(wav)
