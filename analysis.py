import pandas as pd
import re
import argparse
import os.path as osp
import itertools
from collections import Counter
from nltk.tokenize import RegexpTokenizer
import json

def verb_calc(df, line_count):

    series_occurence = df.pony.value_counts()

    verbosity = series_occurence.apply(lambda x: x / line_count).to_dict()

    return verbosity

def mention_counter(df, ponies, pony_dict):

    mentions = {'twilight': {'twilight': 0,'applejack': 0, 'rarity': 0, 'pinkie': 0,'rainbow': 0,'fluttershy': 0, 'total': 0},
                'applejack': {'twilight': 0,'applejack': 0, 'rarity': 0, 'pinkie': 0,'rainbow': 0,'fluttershy': 0, 'total': 0},
                'rarity': {'twilight': 0,'applejack': 0, 'rarity': 0, 'pinkie': 0,'rainbow': 0,'fluttershy': 0, 'total': 0},
                'pinkie': {'twilight': 0,'applejack': 0, 'rarity': 0, 'pinkie': 0,'rainbow': 0,'fluttershy': 0, 'total': 0},
                'rainbow': {'twilight': 0,'applejack': 0, 'rarity': 0, 'pinkie': 0,'rainbow': 0,'fluttershy': 0, 'total': 0},
                'fluttershy': {'twilight': 0,'applejack': 0, 'rarity': 0, 'pinkie': 0,'rainbow': 0,'fluttershy': 0, 'total': 0}}

    for pony in ponies:
        tw_df = df[df['pony'] == pony]
        for index, row in tw_df.iterrows():
            repeated = -1
            for k, v in pony_dict.items():
                 if v in row['dialog']:
                    mentions[pony][k] += 1
                    mentions[pony]['total'] +=1
                    repeated +=1
        mentions[pony].pop(pony, None)
        if repeated > 0:
            mentions[pony]['total'] -= repeated


        if (mentions[pony]['total']) > 0:
            for k, v in mentions[pony].items():
                mentions[pony][k] = mentions[pony][k]/mentions[pony]['total']


        mentions[pony].pop('total', None)

    return mentions


def follow_on_comments_calculator(df, pony_dict):
    pony_dict['other'] = None
    follow_on_comments = dict.fromkeys(pony_dict.keys())
    for follow in follow_on_comments:
        follow_on_comments[follow] = {key:0 for key in pony_dict if (key != follow)}
        follow_on_comments[follow]['total_begin'] = 0

    previous = None

    for index, row in df.iterrows():
        current = row['pony']
        if (current != 'other') & (previous != current) & (previous != None):
            follow_on_comments[current][previous] += 1
            follow_on_comments[current]['total_begin'] += 1
        previous = current

    for following, prev_dict in follow_on_comments.items():
        if follow_on_comments[following]['total_begin'] == 0:
            continue
        else:
            for pony in pony_dict:
                if pony != following:
                    prev_dict[pony] = prev_dict[pony] / prev_dict['total_begin']
        follow_on_comments[following].pop('total_begin', None)

    follow_on_comments.pop('other', None)
    return follow_on_comments

def calc_non_dict (df, ponies, eng_list):
    non_dictionary_words = {}

    for pony in ponies:
        dialog_sentences = df[df['pony'] == pony]
        token_dialog = [word.lower() for word in col_tokenizer(dialog_sentences, 'dialog')]
        non_english_words_in_dialog = set(token_dialog) & set(eng_list)
        words_to_count = [word for word in token_dialog if word not in non_english_words_in_dialog]
        most_common_words = [word for word, word_count in Counter(words_to_count).most_common(5)]
        non_dictionary_words[pony] = most_common_words


    return non_dictionary_words

def col_tokenizer(df, col_name):
    tokenizer = RegexpTokenizer(r'\w+')
    words = []
    for index, row in df.iterrows():
        words.append(tokenizer.tokenize(row[col_name]))

    words = list(itertools.chain.from_iterable(words))
    return words

def __main__():

    parser = argparse.ArgumentParser(description='Read and analyse my Little Pony dialog')
    parser.add_argument('path_src_file', help='this the path to the dialog')
    parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'), default='out.json',
                        help='output file, in JSON format', required=True)

    args = parser.parse_args()


    path_src_file = args.path_src_file

    df = pd.read_csv(f'{path_src_file}clean_dialog.csv')


    ponies = ['twilight', 'applejack', 'rarity', 'pinkie', 'rainbow', 'fluttershy']
    ponynames = ['Twilight Sparkle', 'Applejack', 'Pinkie Pie', 'Rainbow Dash', 'Fluttershy', 'Rarity']

    df["pony"] = df["pony"].map(lambda x: "twilight" if re.search('^Twilight Sparkle$',x) else "applejack" if re.search('^Applejack$',x)
                                                else "fluttershy" if re.search('^Fluttershy$',x) else "rainbow" if re.search('^Rainbow Dash$',x)
                                                else "pinkie" if re.search('^Pinkie Pie$',x) else "rarity" if re.search('^Rarity$',x) else "other")


    dict_final = {"verbosity": {}, "mentions": {}, "follow_on_comments": {}, "non_dictionary_words": {}}

    pony_dict = {'twilight': 'Twilight',
                 'applejack': 'Applejack',
                 'rarity': 'Rarity',
                 'pinkie': 'Pinkie',
                 'rainbow': 'Rainbow',
                 'fluttershy': 'Fluttershy', }

    df_just_pony = df[df['pony'].str.match('twilight|fluttershy|applejack|rarity|pinkie|rainbow')]

    with open(osp.join(f'{path_src_file}', 'data', 'words_alpha.txt')) as f:
        eng_list = [line.rstrip('\n') for line in f]

    dict_final = {}
    line_count = len(df.index)
    dict_final['verbosity'] = verb_calc(df_just_pony, line_count)
    dict_final['mentions'] = mention_counter(df_just_pony, ponies, pony_dict)
    dict_final['follow_on_comments'] = follow_on_comments_calculator(df, pony_dict)
    df = df.replace(to_replace=r'<U\+[0-9]{4}>', value=' ', regex=True)
    dict_final['non_dictionary_words'] = calc_non_dict(df, ponies, eng_list)

    out = args.outfile if not (args.outfile is None) else 'json.out'
    json.dump(dict_final, out)
    out.write('\n')

if __name__ == '__main__':
    __main__()