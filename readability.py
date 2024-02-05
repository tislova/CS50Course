# Determines grade level of inputted text
def main():
    # Prompt the user for some text
    text = input("Text: ")

    # Count the number of letters, words, and sentences in the text
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # Compute the Coleman-Liau index
    L = (letters / words) * 100
    S = (sentences / words) * 100
    index = 0.0588 * L - 0.296 * S - 15.8

    index1 = round(index)
    index2 = int(index1)

    # Print the grade level
    if index2 < 16 and index2 >= 1:
        print(f"Grade {index2}")
    elif index2 >= 16:
        print("Grade 16+")
    else:
        print("Before Grade 1")


def count_letters(text):
    # Return the number of letters in text
    j = 0
    for char in text:
        if char.isalpha():
            j += 1
    return j


def count_words(text):
    # Return the number of words in text
    words_list = text.split()
    return len(words_list)


def count_sentences(text):
    # Return the number of sentences in text
    j = 0
    for char in text:
        if char in ['.', '!', '?']:
            j += 1
    return j


main()
