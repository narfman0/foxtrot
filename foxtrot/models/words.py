import string

vowels = list("aeiou")


def generate(random):
    return gen_word(random, 2, 4)


def gen_word(random, min, max):
    word = ""
    syllables = min + int(random.random() * (max - min))
    for i in range(0, syllables):
        word += gen_syllable(random)
    return word.capitalize()


def gen_syllable(random):
    ran = random.random()
    if ran < 0.333:
        return word_part(random, "v") + word_part(random, "c")
    if ran < 0.666:
        return word_part(random, "c") + word_part(random, "v")
    return word_part(random, "c") + word_part(random, "v") + word_part(random, "c")


def word_part(random, type):
    if type is "c":
        return random.sample(
            [ch for ch in list(string.ascii_lowercase) if ch not in vowels], 1
        )[0]
    if type is "v":
        return random.sample(vowels, 1)[0]
