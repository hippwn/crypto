# -*- coding: utf-8 -*-

import re, csv, string, copy
from math import gcd

# ===== general functions =====
FREQ = {}
with open('letters.csv', 'r') as f:
    r = csv.DictReader(f)
    for row in r:
        for k, v in row.items():
            k = k.lower()
            v = float(v)
            if k in FREQ.keys():
                FREQ[k].append(v)
            else:
                FREQ[k] = [v]
for k, v in FREQ.items():
    FREQ[k] = dict(zip(string.ascii_lowercase, v))


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
    --------

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
    :return float: the index of coincidence
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
