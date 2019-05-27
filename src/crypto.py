# -*- coding: utf-8 -*-

import re, csv, string, copy
from math import gcd

# ===== general functions =====
FREQ = {
    'english': {'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702, 'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153, 'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507, 'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056, 'u': 2.758, 'v': 0.978, 'w': 2.36, 'x': 0.15, 'y': 1.974, 'z': 0.074},
    'french': {'a': 7.636, 'b': 0.901, 'c': 3.26, 'd': 3.669, 'e': 14.715, 'f': 1.066, 'g': 0.866, 'h': 0.737, 'i': 7.529, 'j': 0.613, 'k': 0.074, 'l': 5.456, 'm': 2.968, 'n': 7.095, 'o': 5.796, 'p': 2.521, 'q': 1.362, 'r': 6.693, 's': 7.948, 't': 7.244, 'u': 6.311, 'v': 1.838, 'w': 0.049, 'x': 0.427, 'y': 0.128, 'z': 0.326},
    'german': {'a': 6.516, 'b': 1.886, 'c': 2.732, 'd': 5.076, 'e': 16.396, 'f': 1.656, 'g': 3.009, 'h': 4.577, 'i': 6.55, 'j': 0.268, 'k': 1.417, 'l': 3.437, 'm': 2.534, 'n': 9.776, 'o': 2.594, 'p': 0.67, 'q': 0.018, 'r': 7.003, 's': 7.27, 't': 6.154, 'u': 4.166, 'v': 0.846, 'w': 1.921, 'x': 0.034, 'y': 0.039, 'z': 1.134},
    'spanish': {'a': 11.525, 'b': 2.215, 'c': 4.019, 'd': 5.01, 'e': 12.181, 'f': 0.692, 'g': 1.768, 'h': 0.703, 'i': 6.247, 'j': 0.493, 'k': 0.011, 'l': 4.967, 'm': 3.157, 'n': 6.712, 'o': 8.683, 'p': 2.51, 'q': 0.877, 'r': 6.871, 's': 7.977, 't': 4.632, 'u': 2.927, 'v': 1.138, 'w': 0.017, 'x': 0.215, 'y': 1.008, 'z': 0.467},
    'portuguese': {'a': 14.634, 'b': 1.043, 'c': 3.882, 'd': 4.992, 'e': 12.57, 'f': 1.023, 'g': 1.303, 'h': 0.781, 'i': 6.186, 'j': 0.397, 'k': 0.015, 'l': 2.779, 'm': 4.738, 'n': 4.446, 'o': 9.735, 'p': 2.523, 'q': 1.204, 'r': 6.53, 's': 6.805, 't': 4.336, 'u': 3.639, 'v': 1.575, 'w': 0.037, 'x': 0.253, 'y': 0.006, 'z': 0.47},
    'esperanto': {'a': 12.117, 'b': 0.98, 'c': 0.776, 'd': 3.044, 'e': 8.995, 'f': 1.037, 'g': 1.171, 'h': 0.384, 'i': 10.012, 'j': 3.501, 'k': 4.163, 'l': 6.104, 'm': 2.994, 'n': 7.955, 'o': 8.779, 'p': 2.755, 'q': 0.0, 'r': 5.914, 's': 6.092, 't': 5.276, 'u': 3.183, 'v': 1.904, 'w': 0.0, 'x': 0.0, 'y': 0.0, 'z': 0.494},
    'italian': {'a': 11.745, 'b': 0.927, 'c': 4.501, 'd': 3.736, 'e': 11.792, 'f': 1.153, 'g': 1.644, 'h': 0.636, 'i': 10.143, 'j': 0.011, 'k': 0.009, 'l': 6.51, 'm': 2.512, 'n': 6.883, 'o': 9.832, 'p': 3.056, 'q': 0.505, 'r': 6.367, 's': 4.981, 't': 5.623, 'u': 3.011, 'v': 2.097, 'w': 0.033, 'x': 0.003, 'y': 0.02, 'z': 1.181},
    'turkish': {'a': 11.92, 'b': 2.844, 'c': 0.963, 'd': 4.706, 'e': 8.912, 'f': 0.461, 'g': 1.253, 'h': 1.212, 'i': 0.0086, 'j': 0.034, 'k': 4.683, 'l': 5.922, 'm': 3.752, 'n': 7.487, 'o': 2.476, 'p': 0.886, 'q': 0.0, 'r': 6.722, 's': 3.014, 't': 3.314, 'u': 3.235, 'v': 0.959, 'w': 0.0, 'x': 0.0, 'y': 3.336, 'z': 1.5},
    'swedish': {'a': 9.383, 'b': 1.535, 'c': 1.486, 'd': 4.702, 'e': 10.149, 'f': 2.027, 'g': 2.862, 'h': 2.09, 'i': 5.817, 'j': 0.614, 'k': 3.14, 'l': 5.275, 'm': 3.471, 'n': 8.542, 'o': 4.482, 'p': 1.839, 'q': 0.02, 'r': 8.431, 's': 6.59, 't': 7.691, 'u': 1.919, 'v': 2.415, 'w': 0.142, 'x': 0.159, 'y': 0.708, 'z': 0.07},
    'polish': {'a': 10.503, 'b': 1.74, 'c': 3.895, 'd': 3.725, 'e': 7.352, 'f': 0.143, 'g': 1.731, 'h': 1.015, 'i': 8.328, 'j': 1.836, 'k': 2.753, 'l': 2.564, 'm': 2.515, 'n': 6.237, 'o': 6.667, 'p': 2.445, 'q': 0.0, 'r': 5.243, 's': 5.224, 't': 2.475, 'u': 2.062, 'v': 0.012, 'w': 5.813, 'x': 0.004, 'y': 3.206, 'z': 4.852},
    'dutch': {'a': 7.486, 'b': 1.584, 'c': 1.242, 'd': 5.933, 'e': 0.01891, 'f': 0.805, 'g': 3.403, 'h': 2.38, 'i': 6.499, 'j': 0.00146, 'k': 2.248, 'l': 3.568, 'm': 2.213, 'n': 10.032, 'o': 6.063, 'p': 0.00157, 'q': 0.009, 'r': 6.411, 's': 0.00373, 't': 0.00679, 'u': 0.00199, 'v': 0.00285, 'w': 0.00152, 'x': 0.036, 'y': 0.035, 'z': 0.00139},
    'danish': {'a': 6.025, 'b': 2.0, 'c': 0.565, 'd': 5.858, 'e': 15.453, 'f': 2.406, 'g': 4.077, 'h': 1.621, 'i': 6.0, 'j': 0.73, 'k': 3.395, 'l': 5.229, 'm': 3.237, 'n': 7.24, 'o': 4.636, 'p': 1.756, 'q': 0.007, 'r': 8.956, 's': 5.805, 't': 6.862, 'u': 1.979, 'v': 2.332, 'w': 0.069, 'x': 0.028, 'y': 0.698, 'z': 0.034},
    'icelandic': {'a': 10.11, 'b': 1.043, 'c': 0.0, 'd': 1.575, 'e': 6.418, 'f': 3.013, 'g': 4.241, 'h': 1.871, 'i': 7.578, 'j': 1.144, 'k': 3.314, 'l': 4.532, 'm': 4.041, 'n': 7.711, 'o': 2.166, 'p': 0.789, 'q': 0.0, 'r': 8.581, 's': 5.63, 't': 4.953, 'u': 4.562, 'v': 2.437, 'w': 0.0, 'x': 0.046, 'y': 0.9, 'z': 0.0},
    'finnish': {'a': 12.217, 'b': 0.281, 'c': 0.281, 'd': 1.043, 'e': 7.968, 'f': 0.194, 'g': 0.392, 'h': 1.851, 'i': 10.817, 'j': 2.042, 'k': 4.973, 'l': 5.761, 'm': 3.202, 'n': 8.826, 'o': 5.614, 'p': 1.842, 'q': 0.013, 'r': 2.872, 's': 7.862, 't': 8.75, 'u': 5.008, 'v': 2.25, 'w': 0.094, 'x': 0.031, 'y': 1.745, 'z': 0.051},
    'czech': {'a': 8.421, 'b': 0.822, 'c': 0.74, 'd': 3.475, 'e': 7.562, 'f': 0.084, 'g': 0.092, 'h': 1.356, 'i': 6.073, 'j': 1.433, 'k': 2.894, 'l': 3.802, 'm': 2.446, 'n': 6.468, 'o': 6.695, 'p': 1.906, 'q': 0.001, 'r': 4.799, 's': 5.212, 't': 5.727, 'u': 2.16, 'v': 5.344, 'w': 0.016, 'x': 0.027, 'y': 1.043, 'z': 1.503}
}


def rot(text, n):
    return ''.join([string.ascii_lowercase[(string.ascii_lowercase.index(c) + n) % 26] for c in text])

def get_offset(text, lang):
    o = [0, 100]
    for i in range(26):
        diff = sum(abs(f - FREQ[lang][string.ascii_lowercase[i]]) for i, f in
                   enumerate([100 * l / len(text) for l in map(text.count, string.ascii_lowercase)]))
        if diff < o[1]:
            o = i, diff
        text = rot(text, 1)
    return o[0]

def vigenere(text, key_size, lang='french'):
    ciphers = ([], [], [], [])
    plains = ([], [], [], [])

    for i in range(len(text)):
        ciphers[i % key_size].append(text[i])
    for i in range(len(ciphers)):
        offset = get_offset(ciphers[i], lang)
        plains[i].extend([rot(t, offset) for t in ciphers[i]])

    plaintexts = tuple([''.join(p) for p in plains])
    plain = ""
    try:
        for i in range(len(plaintexts[0])):
            for c in plaintexts:
                plain += c[i]
    except:
        pass
    return plain

# ===== Kasiski's method =====

def repetitions(s):
    r = {}
    for m in re.compile(r'(?=(.{3,}).*(\1))').finditer(s):
        if m.group(1) in r:
            r[m.group(1)] |= {m.start(1), m.start(2)}
        else:
            r[m.group(1)] = {m.start(1), m.start(2)}
    return r

def get_dist_gcd(r):
    distances, cd = [], []
    for v in copy.deepcopy(r).values():
        mi = min(v)
        v.remove(mi)
        distances.extend([i - mi for i in v])
    for i in range(len(distances)-1):
        for j in range(len(distances)-1):
            if i != j:
                cd.append(gcd(distances[i], distances[j]))
    cd = list(filter(lambda x: x != 1, cd))
    if not len(cd):
        raise RuntimeError("unable to find distance")
    return max(cd, key=cd.count)

def get_most_seen(text):
    return max(text, key=text.count)


def vigenere_Kasiski(text, lang):
    """Cracks a Vigenere's encryption using Kasiski's method.
    
    It is based on the fact that if twos polygrams are found in a ciphertext,
    they are probably the two same polygrams in the plaintext. Therefor, the
    distance between these two sequences is likely to be a multiple of the
    key. If several duplicates are found, their GCD (Greatest Common Divider)
    should be the size of the key.

    :param text: the ciphertext to decrypt
    :param lang: the original lang of the text; the following are supported:
        English, French, German, Spanish, Portuguese, Esperanto, Italian,
        Turkish, Swedish, Polish, Dutch, Danish, Icelandic, Finnish, Czech

    Exemple:
        Consider the following::
            plain:      .....DES...........DES.......DES.........DES....DES.....
            key:        ABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCD
            chipher:    .....EGV.....................EGV.........EGV............
            distance:         <--------- 24 --------> <--- 12 -->

        Since GCD(24, 12) = 4, the length of the key is probably 4. 

    """
    lang = lang.lower()
    if lang not in list(map(str.lower, FREQ.keys())):
        raise ValueError("lang not recognized")
    text = text.replace(' ', '').lower()
    key_size = get_dist_gcd(repetitions(text))

    return vigenere(text, key_size, lang=lang)

# ===== IC method =====
IC = {
    'french': 0.074,
    'english': 0.065,
    'german': 0.072,
    'spanish': 0.074,
    'italian': 0.075
}

def get_IC(text):
    """Compute the index of coincidence of a text

    :param text: a lowercase text
    """
    nb = list(map(text.count, string.ascii_lowercase))
    s = sum(n*(n-1) for n in nb)
    total = sum(nb)
    return s / (total*(total-1))    

def vigenere_IC(text, lang, error=0.01):
    """Cracks Vigenere's encryption using the Index of Coincidence. 

    It is the probability of drawing two identical letters from a text. This index
    depends mostly on the langage of the text but a randomly arranged one will 
    have a IC of approximately 0.038. When spliting the ciphertext into pieces based
    on a key size (let's say 4), if the IC of these pieces is close to the one of the
    langage of the plaintext, then the key used to cipher was probably of length 4.
    
    :param text: the ciphertext to decrypt
    :param lang: the original lang of the text; the following are supported:
        English, French, German, Spanish, Italian
    """

    # check if the lang is supported
    lang = lang.lower()
    if lang not in list(map(str.lower, IC.keys())):
        raise ValueError("lang not recognized")

    key_size = 1
    ic = 0
    while ic < IC[lang] - error:
        # compute the index of coincidence for each key size
        key_size += 1
        if key_size > len(text):
            # if the size of the key is more than the text length,
            # the error threshold may need to be ajusted.
            raise RuntimeError("key size cannot be computed. Try to increase the error threshold")
        
        ciphers = [""] * key_size
        for i in range(len(text)):
            ciphers[i % key_size] += text[i]
        # get the IC of each subtext before taking the mean value
        icl = [get_IC(txt) for txt in ciphers]
        ic = sum(icl) / len(icl)

    return vigenere(text, key_size, lang=lang)

# test
if __name__ == "__main__":
    # Exercice 1: crack the following ciphertext using Kasiski's method.
    txt_kasiski = "zbpuevpuqsdlzgllksousvpasfpddggaqwptdgptzweemqzrdjtddefekeferdprrcyndgluaowcnbptzzzrbvpssfpashpncotemhaeqrferdlrlwwertlussfikgoeuswotfdgqsyasrlnrzppdhtticfrciwurhcezrpmhtpuwiyenamrdbzyzwelzucamrptzqseqcfgdrfrhrpatsepzgfnaffisbpvdblisrplzgnemswaqoxpdseehbeeksdptdttqsdddgxurwnidbdddplncsdddplncsd"
    print(vigenere_Kasiski(txt_kasiski, "french"))

    # Exercice 2: crack the following ciphertext using th CI method.
    txt_ic = "uzssgbufmdymbfykciyfrockmbnsxovanzcgfvyigslgkofwpsmjqqbwdqbwedimdaiftwmlawlwpsfggwmpujdwfcgtmwjsdvukmfxkgffweayeawlweryepollmuhszwghdwgweqieysfsbzoksfufpsjsdhcwpsmggjlsssmvqqylfsyhaeowaifweoolqilkfshsushlmrcjqzunqfclqgufeofdqfzsufymzhimddfmecoeawhkxchymzutmgnaxzysmamlqfxsyqbwldcwdfyjaiawxsnaffyeqgyvgwmafxydqgyebcllmwwzqngguopwozuhqfgaegcgzryexswgzgyjhonwgfvaqbyffshvgxydqgxwhclsu"
    print(vigenere_IC(txt_ic, "french"))
