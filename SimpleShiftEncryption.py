"""
Class to encrypt and decrypt using simple censor shift using
simple poly alphabetic substitution
Name: MNA Ahimbisibwe
SN: 217005435
Model: UJ Mobile Phone Firmware Hacking Tool
"""
import string


class Encryption:
    # Initialize the class with a list of shifts
    def __init__(self, shifts):
        # Define the standard English alphabet for plaintext
        alpha = list(string.ascii_uppercase)
        self.plaintext_alphabet = ''.join(alpha)  # results "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # Initialize an empty list for cipher alphabets
        self.cipher_alphabets = []
        # Initialize an empty list for row numbers
        self.row_numbers = []

        # For each shift in the given list...
        for shift in shifts:
            # Generate a cipher alphabet and corresponding row number
            substitution_alphabet, row_number = self.generate_substitution_alphabet(shift)
            # Append the cipher alphabet to the list of cipher alphabets
            self.cipher_alphabets.append(substitution_alphabet)
            # Append the row number to the list of row numbers
            self.row_numbers.append(row_number)

    # Define a method to encrypt plaintext into ciphertext
    def encrypt(self, word: str) -> str:
        # Convert the plaintext to uppercase
        word = word.upper()
        # Initialize an empty string for the ciphertext
        ciphertext = ""

        # For each character in the plaintext...
        for i in range(len(word)):
            # Get the current character
            char = word[i]
            # Find its index in the plaintext alphabet
            plaintext_index = self.plaintext_alphabet.find(char)

            # If the character isn't in the alphabet, just add it to the ciphertext as is
            if plaintext_index == -1:
                ciphertext += char
                continue

            # Get the cipher alphabet for this character's position
            substitution_alphabet = self.cipher_alphabets[i % len(self.cipher_alphabets)]
            # Substitute the character and add it to the ciphertext
            substituted_char = substitution_alphabet[plaintext_index]
            ciphertext += substituted_char

        # Return the final ciphertext
        return ciphertext

    # Define a method to decrypt ciphertext into plaintext
    def decrypt(self, ciphertext: str) -> str:
        # Initialize an empty string for the plaintext
        plaintext = ""

        # For each character in the ciphertext...
        for i in range(len(ciphertext)):
            # Get the current character
            char = ciphertext[i]
            # Find its index in the cipher alphabet
            cipher_index = self.cipher_alphabets[i % len(self.cipher_alphabets)].find(char)

            # If the character isn't in the cipher alphabet, just add it to the plaintext as is
            if cipher_index == -1:
                plaintext += char
                continue

            # Find the corresponding character in the plaintext alphabet
            original_char = self.plaintext_alphabet[cipher_index]
            # Add the original character to the plaintext
            plaintext += original_char

        # Return the final plaintext
        return plaintext

    # Define a method to generate a cipher alphabet and row number from a shift
    def generate_substitution_alphabet(self, shift):
        # Shift the plaintext alphabet by the given amount to get the cipher alphabet
        shifted_alphabet = self.plaintext_alphabet[shift:] + self.plaintext_alphabet[:shift]
        # Define the row number as the shift plus one
        row_number = shift + 1
        # Return the cipher alphabet and row number
        return shifted_alphabet, row_number

# # Define the list of shifts
# shifts = [4, 3, 1, 6, 7]
# # Create an instance of the Encryption class with these shifts
# encryption = Encryption(shifts)
# # Define the plaintext to be encrypted
# word = "JOHANNESBURG"
# # Encrypt the plaintext into ciphertext
# encrypted_word = encryption.encrypt(word)
# print(f"Plaintext: {word}")
# print(f"Ciphertext: {encrypted_word}")
#
# # Decrypt the ciphertext back into plaintext
# decrypted_word = encryption.decrypt(encrypted_word)
# print(f"Decrypted: {decrypted_word}")
