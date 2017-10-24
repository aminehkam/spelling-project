import csv
import distance
import pprint
import matplotlib.pyplot as plt

def count_vowels(word):
    """ Count the number of English Vowels in the given word
    """
    vowels = ['a', 'e', 'i', 'o', 'u']
    num_vowels = 0
    for c in word:
        if c in vowels:
            num_vowels += 1
    return num_vowels


def compute_frequencies(input_file):
    """ Computes the frequency of misspelled words based
    on their length and also based on the number of vowels
    in each word. The latter roughly represents the number
    of syllable in the word.

    The input file should be in tsv format.

    The Levenshtein distances in the misspelled corpus were either
    1 or 2. Therefore, the absolute distance values did not bear any
    significant meaning.
    """
    # word length to misspelling count
    word_length_to_misspelling = {}

    # vowels to misspelling count
    vowels_to_misspelling = {}

    with open(input_file, 'r') as csvfile:
        state_reader = csv.reader(csvfile, delimiter='\t', dialect=csv.excel_tab)
        # Each row is two words. The second one should be the correct one that we use
        for row in state_reader:
            if len(row) == 2:
                wrong_word, correct_word = row
                cur_distance = distance.levenshtein(wrong_word, correct_word)

                if cur_distance > 0 :
                    cur_len = len(correct_word)
                    word_length_to_misspelling[cur_len] = word_length_to_misspelling.get(cur_len, 0) + 1

                    num_vowels = count_vowels(correct_word)
                    vowels_to_misspelling[num_vowels] = vowels_to_misspelling.get(num_vowels, 0) + 1
    return word_length_to_misspelling, vowels_to_misspelling

def plot_me(a_dict, title, xlabel, ylabel):
    """ Create a bar chart from the given dictionary.
    The dictionary is assumed to have counts of each key and
    the keys are assumed to be numbers. The missing keys are
    inserted before plotting.
    """
    max_val = max(a_dict.keys())
    for i in range(max_val+1):
        if i not in a_dict:
            a_dict[i] = 0
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    values = a_dict.values()
    plt.bar(range(len(values)), values, align='center')
    plt.xticks(range(len(values)), a_dict.keys())
    plt.show()

def main():
    input_file = '/Users/amineh/Downloads/spelling/en_keystroke_pairs.sorted.txt'
    word_length_count, vowels_count = compute_frequencies(input_file)
    plot_me(title = 'Frequency of Misspelled Words Based on Their Vowels Count',
            xlabel = 'Vowel Count',
            ylabel = 'Frequency',
            a_dict = vowels_count)

    plot_me(title = 'Frequency of Misspelled Words Based on Their Length',
            xlabel = 'Word Length',
            ylabel = 'Frequency',
            a_dict = word_length_count)

if __name__ == "__main__":
    main()
