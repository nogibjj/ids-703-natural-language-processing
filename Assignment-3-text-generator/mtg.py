"""
Natural Language Processing - Assignment 2
Text Generation using N-gram Markov Text Generators
"""
from collections import defaultdict, Counter
import string
import random

def most_frequent(List):
    """
    Function to get the most common element of the list
    """  
    punctuation_list = list(string.punctuation)
    List = [x for x in List if x not in punctuation_list]
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]

def finish_sentence(sentence, n, corpus, deterministic=False):
    """
    Based on the corpus, and given 'n', construct all lower n-gram models.
    Using the words in the sentence, use the n-gram model to predict the next words
    (upto 10 or till the first '.', '?', '!')
    """
    if n < 1:
        print("n must be greater than or equal to 1. ")
        return []

    if n > len(sentence):
        print("Input word list is lesser than the N-grams model. Input atleast N words")
        return []

    corpus = [
        word.strip()
        for word in corpus
        if word not in ("'", '"', '""', "''", "``", "`", "--", "-", "[", "]", "(", ")")
    ]
    n_gram_dict = defaultdict(defaultdict)
    uni_gram_deterministic = most_frequent(corpus)
    
    # Initialise the n-gram transition table
    current_n_gram = n
    while current_n_gram >= 1:
        current_n_gram = current_n_gram - 1
        n_gram_dict[current_n_gram] = {}
        
        for index in range(current_n_gram, len(corpus) - current_n_gram):
            # Increment or initialze the count of next word
            prev_words = "".join(corpus[index - current_n_gram : index])
            current_word = corpus[index]

            if not prev_words in n_gram_dict[current_n_gram].keys():
                n_gram_dict[current_n_gram][prev_words] = {}

            if not current_word in n_gram_dict[current_n_gram][prev_words].keys():
                n_gram_dict[current_n_gram][prev_words][current_word] = 0

            n_gram_dict[current_n_gram][prev_words][current_word] += 1


    current_n = n - 1
    while True:
        try:
            # Break condition
            if any(x in sentence for x in [".", "?", "!"]) or (len(sentence) >= 10):
                break

            # Depending on the value of the "deterministic" flag
            # Append the next predicted word to the list
            prediction_string = "".join(sentence[-current_n:])
            next_word_list = n_gram_dict[current_n][prediction_string]
            if deterministic:
                next_word = max(next_word_list, key=next_word_list.get)
                sentence.append(next_word)
            else:
                next_word = random.choices(list(next_word_list.keys()), list(next_word_list.values()), k=1)
                sentence.append(next_word[0])
            current_n = n - 1
        except (ValueError, KeyError):
            current_n -= 1
            if current_n < 1:
                if deterministic:
                    sentence.append(uni_gram_deterministic)
                else:
                    sentence.append(random.choice(corpus))
            continue

    return sentence
