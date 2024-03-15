import string
import argparse
import pickle
import sys

LETTERS = string.ascii_letters
LOWALPHA = string.ascii_lowercase
UPALPHA = string.ascii_uppercase


def get_read(inp: str) -> str:
    if inp is not None:
        with open(inp, 'r') as file:
            input_str = file.read()
    else:
        input_str = input()
    return input_str


def get_write(output_str: str, outp: str) -> None:
    if outp is not None:
        with open(outp, 'w') as file:
            file.write(output_str)
    else:
        print(output_str)


def encode_caesar(key: str, inp_str: str) -> str:
    key = int(key)
    list_caes = list()
    for i in inp_str:
        if i in LOWALPHA:
            list_caes.append(LOWALPHA[(LOWALPHA.index(i, 0, 26) + key) % 26])
        elif i in UPALPHA:
            list_caes.append(UPALPHA[(UPALPHA.index(i, 0, 26) + key) % 26])
        else:
            list_caes.append(i)
    return ''.join(list_caes)


def encode_vigenere(vig_str: str, key: str) -> str:
    list_vig = list()
    period = 0
    key = key.upper()
    for i in range(len(vig_str)):
        if vig_str[i] in LOWALPHA:
            list_vig.append(LOWALPHA[(UPALPHA.index(key[(i - period) % len(key)], 0, 26) +
                                      LOWALPHA.index(vig_str[i], 0, 26)) % 26])
        elif vig_str[i] in UPALPHA:
            list_vig.append(UPALPHA[(UPALPHA.index(key[(i - period) % len(key)], 0, 26) +
                                     UPALPHA.index(vig_str[i], 0, 26)) % 26])
        else:
            list_vig.append(vig_str[i])
            period += 1
    return ''.join(list_vig)


def encode_vernam(text: str, key: str):
    answer = ""
    p = 0  # pointer for the key
    for char in text:
        answer += chr(ord(char) ^ ord(key[p]))
        p += 1
        if p == len(key):
            p = 0
    return answer


def check_correctness(cipher: str, key: str):
    if cipher == 'caesar':
        try:
            key = int(key)
        except:
            sys.exit("NOOO! ,Caesar key can be only digit")
    if cipher == 'vigenere':
        if not key.isalpha():
            sys.exit("NOOOO!!, Key should contain only latin letters")


def en_de_code(key: str, inputt: str, output: str, cipher: str) -> None:
    input_str = get_read(inputt)
    if cipher == 'caesar':
        out_str = encode_caesar(key, input_str)
        get_write(out_str, output)
    elif cipher == 'vigenere':
        out_str = encode_vigenere(input_str, key)
        get_write(out_str, output)
    elif cipher == 'vernam':
        out_str = encode_vernam(input_str, key)
        get_write(out_str, output)
    else:
        sys.exit("There is no such cipher")


def vigenere_hack(model_dict, input_str):
    alpha_count = 0
    for symbol in input_str:
        if symbol.isalpha():
            alpha_count += 1
    max_len = int(alpha_count/10)
    key_len = 0
    max_ind = 0
    for cur_len in range(max_len, 1, -1):
        s = list()
        for i in range(cur_len):
            s.append(input_str[i::cur_len])
        cur_ind_of_coinc = float()
        cur_ind = 0
        for i in range(cur_len):
            dc = getit_model(s[i])
            cur_ind_of_coinc = 0
            for alpha in UPALPHA:
                fi = dc[alpha]
                cur_ind_of_coinc += fi * (fi - 1)
            cur_ind += cur_ind_of_coinc/((len(s[i])) * (len(s[i]) - 1))
        cur_ind = cur_ind/cur_len
        print(cur_ind)
        if max_ind <= cur_ind * 1.067:
            max_ind = cur_ind
            key_len = cur_len
    key = ''
    s = list()
    for ind in range(key_len):
        s.append(get_hack(model_dict, input_str[ind::key_len]))
    out = list()
    for ind in range(len(input_str)):
        out.append(s[ind % key_len][int(ind / key_len)])
    return ''.join(out)


def getit_model(train_str: str) -> dict:
    model_dict = dict()
    for alpha in UPALPHA:
        model_dict[alpha] = 0
    alpha_count = 0
    for alpha in train_str:
        if alpha in LETTERS:
            alpha_count += 1
            model_dict[alpha.upper()] += 1
    if alpha_count == 0:
        return model_dict
    return model_dict


def get_hack(model_dict: dict, input_str: str) -> str:
    min_dis = 26
    min_key = 0
    _key_model = _model(input_str)
    my_dc = dict()
    for ind in range(26):
        for j in range(26):
            my_dc[UPALPHA[j]] = _key_model[UPALPHA[(j - ind) % 26]]
        dis = 0
        for alpha in UPALPHA:
            dis += (model_dict[alpha] - my_dc[alpha]) ** 4
        if dis < min_dis:
            min_dis = dis
            min_key = ind
    return encode_caesar(min_key, input_str)


def get_args():
    parser = argparse.ArgumentParser(description='This is a python program')
    subs = parser.add_subparsers(dest='action', help='action to encode, decode, train or hack')
    encode = subs.add_parser('encode', help='Encode')
    encode.add_argument('--cipher', help='Cipher')
    encode.add_argument('--key', dest='key', help='Key')
    encode.add_argument('--input-file', dest='input', help='Input file')
    encode.add_argument('--output-file', dest='output', help='Ouput file')
    decode = subs.add_parser('decode', help='Decode')
    decode.add_argument('--cipher', help='Cipher')
    decode.add_argument('--key', dest='key', help='Key')
    decode.add_argument('--input-file', dest='input', help='Input file')
    decode.add_argument('--output-file', dest='output', help='Ouput file')
    train = subs.add_parser('train', help='Train')
    train.add_argument('--text-file', dest='text', help='Text file')
    train.add_argument('--model-file', dest='model', help='Model file')
    hack = subs.add_parser('hack', help='Hack')
    hack.add_argument('--input-file', dest='input', help='Input file')
    hack.add_argument('--output-file', dest='output', help='Ouput file')
    hack.add_argument('--model-file', dest='model', help='Model file')
    args = parser.parse_args()
    return args


def _model(train_str: str) -> dict:
    model_dict = dict()
    for alpha in UPALPHA:
        model_dict[alpha] = 0
    alpha_count = 0
    for alpha in train_str:
        if alpha in LETTERS:
            alpha_count += 1
            model_dict[alpha.upper()] += 1
    if alpha_count == 0:
        return model_dict
    for alpha in UPALPHA:
        model_dict[alpha] /= alpha_count
    return model_dict


def read_model(inp: str) -> dict:
    with open(inp, 'rb') as file:
        return pickle.load(file)


def write_model(model_dict: dict, outp: str) -> None:
    if outp is not None:
        with open(outp, 'wb') as file:
            pickle.dump(model_dict, file)
    else:
        print(model_dict)


def main():
    args = get_args()
    if args.action == 'encode':
        check_correctness(args.cipher, args.key)
        en_de_code(args.key, args.input, args.output, args.cipher)
    if args.action == 'decode':
        check_correctness(args.cipher, args.key)
        if args.cipher == 'caesar':
            en_de_code((26 - args.key) % 26, args.input, args.output, args.cipher)
        elif args.cipher == 'vigenere':
            _key = ''
            key = args.key.upper()
            for i in key:
                _key += LOWALPHA[(-UPALPHA.index(i) + 26) % 26]
            en_de_code(_key, args.input, args.output, args.cipher)
        elif args.cipher == 'vernam':
            en_de_code(args.key, args.input, args.output, args.cipher)
    if args.action == 'train':
        text_str = get_read(args.text)
        model_dict = _model(text_str)
        write_model(model_dict, args.model)
    if args.action == 'hack':
        input_str = get_read(args.input)
        model_dict = read_model(args.model)
        out_str = get_hack(model_dict, input_str)
        get_write(out_str, args.output)


if __name__ == '__main__':
    main()
