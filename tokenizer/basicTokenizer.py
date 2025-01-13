from baseTokenizer import BaseTokenizer
from helper import getPairStats, merge

class BasicTokenizer(BaseTokenizer):
    """
    A basic implementation of a Byte Pair Encoding (BPE) tokenizer.

    This tokenizer extends the BaseTokenizer to support Byte Pair Encoding (BPE) for
    training, encoding, and decoding text. It incrementally merges the most frequent
    pairs of bytes to create new tokens, building an extended vocabulary.

    Attributes:
        vocab_dict (dict): Inherited from BaseTokenizer, it maps byte and token IDs to their corresponding byte sequences.
        merge_dict (dict): A dictionary storing pairs of tokens and their corresponding new token IDs.

    Methods:
        train(text, vocab_size):
            Trains the tokenizer on the given text to generate a vocabulary of the specified size using BPE.
        encode(text):
            Encodes the input text into a sequence of token IDs using the trained vocabulary.
        decode(tokenIds):
            Decodes a sequence of token IDs back into the original text.
    """

    def __init__(self):
        """
        Initializes the BasicTokenizer by calling the BaseTokenizer initializer.
        """
        super().__init__()

    def train(self, text, vocab_size):
        """
        Trains the tokenizer to generate a vocabulary using Byte Pair Encoding.

        Args:
            text (str): Input text to train the tokenizer.
            vocab_size (int): Desired vocabulary size, which must be at least 256 (initial byte values).

        Raises:
            AssertionError: If the vocab_size is less than 256.

        Updates:
            vocab_dict: Extends the vocabulary with merged tokens.
            merge_dict: Stores pairs of tokens and their new token IDs.
        """
        assert vocab_size >= 256, "Vocab size must be at least 256"

        # Calculate the number of merges needed to reach the desired vocabulary size
        num_of_merges = vocab_size - 256

        # Convert the input text to a list of byte values
        byte_ids = list(text.encode("utf-8"))

        for i in range(num_of_merges):
            # Compute the frequency of all consecutive byte pairs
            pairStats = getPairStats(byte_ids)

            # Find the most frequent byte pair
            pair = max(pairStats, key=lambda x: pairStats[x])

            # Replace all occurrences of this pair with a new token
            byte_ids = merge(byte_ids, pair, 256 + i)

            # Update the merge dictionary to track this new token
            self.merge_dict[pair] = 256 + i

            # Update the vocabulary dictionary with the new token and its corresponding bytes
            self.vocab_dict[256 + i] = self.vocab_dict[pair[0]] + self.vocab_dict[pair[1]]

    def encode(self, text):
        """
        Encodes the input text into a sequence of token IDs using the trained vocabulary.

        Args:
            text (str): Input text to encode.

        Returns:
            list: A list of token IDs representing the encoded text.

        Note:
            The encoding stops when no further pairs can be merged.
        """
        # Convert the input text to a list of byte values
        text_bytes = text.encode("utf-8")
        byte_ids = list(text_bytes)

        while len(byte_ids) >= 2:
            # Compute the frequency of all consecutive byte pairs in the current byte list
            pairStats = getPairStats(byte_ids)

            # Find the first pair that exists in the merge dictionary (smallest token ID)
            pair = min(pairStats, key=lambda x: self.merge_dict.get(x, float('inf')))

            # If the pair is not in the merge dictionary, stop the encoding process
            if pair not in self.merge_dict:
                break

            # Replace the found pair with its corresponding token ID
            byte_ids = merge(byte_ids, pair, self.merge_dict[pair])

        return byte_ids

    def decode(self, tokenIds):
        """
        Decodes a sequence of token IDs back into the original text.

        Args:
            tokenIds (list): A list of token IDs to decode.

        Returns:
            str: The decoded text string.
        """
        # Reconstruct the byte sequence from the token IDs using the vocabulary dictionary
        text_bytes = b"".join(self.vocab_dict[t] for t in tokenIds)

        # Decode the byte sequence into a UTF-8 string, replacing invalid characters if necessary
        decoded_text = text_bytes.decode("utf-8", errors='replace')
        return decoded_text


if __name__ == "__main__":
    # Example usage of the BasicTokenizer

    # A sample text for training
    original_text = """Ｕｎｉｃｏｄｅ! 🅤🅝🅘🅒🅞🅓🅔‽ 🇺‌🇳‌🇮‌🇨‌🇴‌🇩‌🇪! 😄 The very name strikes fear 
    and awe into the hearts of programmers worldwide. 
    We all know we ought to “support Unicode” in our software
    (whatever that means—like using wchar_t for all the strings, 
    right?). But Unicode can be abstruse, and diving into the
    thousand-page Unicode Standard plus its dozens of supplementary annexes,
    reports, and notes can be more than a little intimidating. 
    I don’t blame programmers for still finding the whole thing mysterious, 
    even 30 years after Unicode’s inception."""

    # Create an instance of BasicTokenizer
    tokenizer = BasicTokenizer()

    # Train the tokenizer to generate a vocabulary with a size of 512 tokens
    tokenizer.train(original_text, 512)

    # Verify that encoding and decoding are consistent
    text = tokenizer.decode(tokenizer.encode(original_text))
    print("Encoding-Decoding Consistency:", text == original_text)

    # Encode and decode a sample string
    encoded = tokenizer.encode("| hello world! 😄")
    print("Encoded:", encoded)
    decoded = tokenizer.decode(encoded)
    print("Decoded:", decoded)





