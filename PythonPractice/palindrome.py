def is_palindrome(word):
    # Your code here: Check if the word is a palindrome
    i=0
    while i<len(word) // 2:
        if word[i] != word[-(i + 1)]:
            return False
        i += 1
    return True

# Test the function
input_word = input("Enter a word to check if it's a palindrome: ")
if is_palindrome(input_word):
    print(f"{input_word} is a palindrome.")
else:
    print(f"{input_word} is not a palindrome.")
