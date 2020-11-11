from unittest import TestCase
import pandas as pd


class Test(TestCase):

    def test_verb_calc(self):
        from analysis import verb_calc
        df = pd.DataFrame({'pony': ["pinkie", "applejack", "twilight", "rainbow", "rarity", "fluttershy"],
                           'dialog': ['always Twilight never others',
                                      'Rainbow Dash, Rarity and Pinkie Pie are my best friends',
                                      'nice feather Rarity',
                                      'hello fluttershy?',
                                      'hi Fluttershy come!',
                                      'hallo hi super cool']})

        pony_dict = {'twilight': 'Twilight',
                     'applejack': 'Applejack',
                     'rarity': 'Rarity',
                     'pinkie': 'Pinkie',
                     'rainbow': 'Rainbow',
                     'fluttershy': 'Fluttershy', }

        ponies = ['twilight', 'applejack', 'rarity', 'pinkie', 'rainbow', 'fluttershy']
        verbosity = verb_calc(df, 6)

        dict = {1: 1 / 6, 2: 1 / 6, 3: 1 / 6, 4: 1 / 6, 5: 1 / 6, 6: 1 / 6}

        self.assertEqual(list(verbosity.values()), list(dict.values()))

    def test2_verb_calc(self):
        from analysis import verb_calc
        df = pd.DataFrame({'pony': ["pinkie", "pinkie", "pinkie", "twilight", "pinkie", "rarity", "fluttershy", "rainbow", "applejack"],
                           'dialog': ['always Twilight never others',
                                      'Rainbow Dash, Rarity and Pinkie Pie are my best friends',
                                      'nice feather Rarity',
                                      'hello fluttershy?',
                                      'hi Fluttershy come!',
                                      'hallo hi super cool',
                                      'hello fluttershy?',
                                      'hi Fluttershy come!',
                                      'hallo hi super cool']})

        # ponies = ['twilight', 'applejack', 'rarity', 'pinkie', 'rainbow', 'fluttershy']
        verbosity = verb_calc(df, 9)

        dict = {1: 4/9, 2: 1/9, 3: 1/9, 4: 1/9, 5: 1/9, 6: 1/9}

        self.assertEqual(list(verbosity.values()), list(dict.values()))

    def test_mention_counter(self):
        from analysis import mention_counter
        df = pd.DataFrame({'pony': ["applejack", "applejack", "twilight", "applejack", "applejack", "applejack"],
                           'dialog': ['always Twilight never others',
                                      'Rainbow Dash, Rarity and Pinkie Pie are my best friends',
                                      'nice feather Rarity',
                                      'hello fluttershy?',
                                      'hi Fluttershy come!',
                                      'hallo hi super cool']})

        pony_dict = {'twilight': 'Twilight',
                     'applejack': 'Applejack',
                     'rarity': 'Rarity',
                     'pinkie': 'Pinkie',
                     'rainbow': 'Rainbow',
                     'fluttershy': 'Fluttershy', }

        ponies = ['twilight', 'applejack', 'rarity', 'pinkie', 'rainbow', 'fluttershy']

        mentions = mention_counter(df, ponies, pony_dict)

        self.assertEqual(list(mentions['applejack'].values()), [1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 5])


    def test2_mention_counter(self):
        from analysis import mention_counter
        df = pd.DataFrame({'pony': ["applejack", "applejack", "twilight", "applejack", "applejack", "applejack"],
                           'dialog': ['always Twilight never others',
                                      'Rainbow Dash, Rarity, Rarity, Rarity Pinkie Pie are my best friends',
                                      'nice feather Rarity',
                                      'hello Rarity fluttershy?',
                                      'hi Fluttershy come!',
                                      'hallo hi super cool']})

        pony_dict = {'twilight': 'Twilight',
                     'applejack': 'Applejack',
                     'pinkie': 'Pinkie',
                     'rainbow': 'Rainbow',
                     'fluttershy': 'Fluttershy',
                     'rarity': 'Rarity'}

        ponies = ['twilight', 'applejack',  'pinkie', 'rainbow', 'fluttershy','rarity']

        mentions = mention_counter(df, ponies, pony_dict)

        self.assertNotEqual(list(mentions['applejack'].values()), [1 / 6, 2 / 6, 8 / 6, 1 / 6, 5 / 6])

    def test3_mention_counter(self):
        from analysis import mention_counter
        df = pd.DataFrame({'pony': ["applejack", "applejack", "twilight", "applejack", "applejack", "applejack"],
                           'dialog': ['always Twilight never others',
                                      'Rainbow Dash, Rarity, Rarity, Rarity Pinkie Pie are my best friends',
                                      'nice feather Rarity',
                                      'hello Rarity fluttershy?',
                                      'hi Fluttershy come!',
                                      'hallo hi super cool']})

        pony_dict = {'twilight': 'Twilight',
                     'applejack': 'Applejack',
                     'pinkie': 'Pinkie',
                     'rainbow': 'Rainbow',
                     'fluttershy': 'Fluttershy',
                     'rarity': 'Rarity'}

        ponies = ['twilight', 'applejack',  'pinkie', 'rainbow', 'fluttershy', 'rarity']

        mentions = mention_counter(df, ponies, pony_dict)

        self.assertEqual(list(mentions['applejack'].values()), [1 / 6, 2 / 6, 1 / 6, 1 / 6, 1 / 6])


    def test_follow_on_comments_calculator(self):
        from analysis import follow_on_comments_calculator
        df = pd.DataFrame({'pony': ["rarity", "twilight", "other", "twilight", "fluttershy", "twilight"],
                           'dialog': ['always Twilight never others',
                                      'Rainbow Dash, Rarity and Pinkie Pie are my best friends',
                                      'nice feather Rarity',
                                      'hello fluttershy?',
                                      'hi Fluttershy come!',
                                      'hallo hi super cool']})

        pony_dict = {'twilight': 'Twilight',
                     'applejack': 'Applejack',
                     'rarity': 'Rarity',
                     'pinkie': 'Pinkie',
                     'rainbow': 'Rainbow',
                     'fluttershy': 'Fluttershy', }

        foc = follow_on_comments_calculator(df, pony_dict)

        self.assertEqual(list(foc['twilight'].values()), [0, 1/3, 0, 0, 1/3, 1/3])

    def test2_follow_on_comments_calculator(self):
        from analysis import follow_on_comments_calculator
        df = pd.DataFrame({'pony': ["other", "rarity", "rarity", "other", "rarity", "other"],
                           'dialog': ['always Twilight never others',
                                      'Rainbow Dash, Rarity and Pinkie Pie are my best friends',
                                      'nice feather Rarity',
                                      'hello fluttershy?',
                                      'hi Fluttershy come!',
                                      'hallo hi super cool']})

        pony_dict = {'twilight': 'Twilight',
                     'applejack': 'Applejack',
                     'rarity': 'Rarity',
                     'pinkie': 'Pinkie',
                     'rainbow': 'Rainbow',
                     'fluttershy': 'Fluttershy', }

        foc = follow_on_comments_calculator(df, pony_dict)

        self.assertEqual(list(foc['rarity'].values()), [0, 0, 0, 0, 0, 2/2])

    def test_calc_non_dict(self):
        from analysis import calc_non_dict
        df = pd.DataFrame({'pony': ["twilight", "twilight", "applejack", "twilight", "twilight", "twilight"],
                           'dialog': ['hi hello dog huh huh huh huh',
                                      'argh',
                                      'pencil hi ok dog argh',
                                      'glass argh lol pencil dog',
                                      'hello hi hello yoohoo',
                                      'wazzup lol glass wazzup yeet']})

        ponies = ['twilight', 'applejack', 'rarity', 'pinkie', 'rainbow', 'fluttershy']

        eng_list = ['hi', 'hello', 'dog', 'glass', 'pencil']
        non_dict = calc_non_dict(df, ponies, eng_list)

        self.assertEqual(non_dict['twilight'], ["huh", "argh", "lol", "wazzup", "yoohoo"])

    def test2_calc_non_dict(self):
        from analysis import calc_non_dict
        df = pd.DataFrame({'pony': ["applejack", "twilight", "applejack", "twilight", "twilight", "twilight"],
                           'dialog': ['hi hello argh dog huh huh huh huh',
                                      'argh',
                                      'pencil hi ok dog argh',
                                      'glass argh lol pencil dog',
                                      'hello hi hello yoohoo',
                                      'wazzup lol glass wazzup yeet']})

        ponies = ['twilight', 'applejack', 'rarity', 'pinkie', 'rainbow', 'fluttershy']

        eng_list = ['hi', 'hello', 'dog', 'glass', 'pencil', 'yup']
        non_dict = calc_non_dict(df, ponies, eng_list)

        self.assertNotEqual(non_dict['applejack'], ["argh", "huh", "ok"])

    def test3_calc_non_dict(self):
        from analysis import calc_non_dict
        df = pd.DataFrame({'pony': ["pony"],
                            'dialog': ['hi cat cat cat cat glass uyh nui nui nui hello woop glass glass woop argh dog huh huh huh huh']})

        ponies = ['pony', 'rainbow']

        eng_list = ['hi', 'hello', 'dog', 'glass', 'pencil', 'yup']
        non_dict = calc_non_dict(df, ponies, eng_list)

        self.assertEqual(non_dict['pony'], ["cat", "huh", "nui", 'woop', 'uyh'])