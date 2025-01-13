class BaseTokenizer:
    """
    A base class for building and training custom tokenizers.

    This class provides a framework for encoding and decoding text as byte sequences
    and allows for extending tokenizer functionality through subclassing. By default,
    it supports basic encoding and decoding operations for Unicode text using UTF-8 encoding.

    Attributes:
        vocab_dict (dict): A dictionary mapping byte values (0-255) to their corresponding byte representations.
        merge_dict (dict): An empty dictionary intended for use by subclasses to store merge operations or rules.
        pattern (str): An empty string, provided as a placeholder for tokenization patterns in subclasses.

    Methods:
        train(text, vocab_size):
            Placeholder method to be implemented in subclasses for training a tokenizer.
        encode(text):
            Encodes a given text into a sequence of byte values.
        decode(tokenIds):
            Decodes a sequence of byte values back into the original text.
        _build_vocab_dict():
            Constructs the initial vocabulary dictionary mapping byte values to byte representations.
    """

    def __init__(self):
        """
        Initializes the BaseTokenizer with a default vocabulary dictionary, an empty merge dictionary,
        and a placeholder for tokenization patterns.
        """
        self.merge_dict = {}
        self.pattern = ""
        self.vocab_dict = self._build_vocab_dict()

    def train(self, text, vocab_size):
        """
        Placeholder method for training a tokenizer.

        Args:
            text (str): The text to train the tokenizer on.
            vocab_size (int): The target vocabulary size for the tokenizer.

        Raises:
            NotImplementedError: This method is meant to be implemented in subclasses.
        """
        raise NotImplementedError

    def encode(self, text):
        """
        Encodes the input text into a sequence of byte values.

        Args:
            text (str): The input text to encode.

        Returns:
            list: A list of byte values representing the encoded text.
        """
        text_bytes = text.encode("utf-8")
        byte_ids = list(text_bytes)
        return byte_ids

    def decode(self, tokenIds):
        """
        Decodes a sequence of byte values back into text.

        Args:
            tokenIds (list): A list of byte values to decode.

        Returns:
            str: The decoded text string.
        """
        text_bytes = b"".join(self.vocab_dict[t] for t in tokenIds)
        decoded_text = text_bytes.decode("utf-8", errors='replace')
        return decoded_text

    def _build_vocab_dict(self):
        """
        Constructs the vocabulary dictionary mapping byte values to their byte representations.

        This method initializes the vocabulary with byte values (0-255) and updates it based on
        merge rules stored in `merge_dict`. Each entry in `merge_dict` represents a pair of bytes
        to be merged into a new token.

        Returns:
            dict: A dictionary where:
                - Keys are byte values or merged token indices.
                - Values are the corresponding byte representations as `bytes` objects.
        """

        # Initialize vocabulary with basic byte values
        vocab_dict = {i: bytes([i]) for i in range(256)}

        # Extend vocabulary using merge rules
        for key, val in self.merge_dict.items():
            vocab_dict[val] = vocab_dict[key[0]] + vocab_dict[key[1]]

        return vocab_dict


    def save(self, file_name):
        """
        Saves the tokenizer's merge rules and vocabulary to files.

        Args:
            file_name (str): Base name for the files to save the tokenizer data.
                            Two files will be created:
                            - `file_name.model`: Contains the merge rules.
                            - `file_name.vocab`: Contains the vocabulary.
        """

        # Save merge rules
        model_file = file_name + ".model"
        with open(model_file, "w") as file:   
            for key, value in self.merge_dict.items():
                p0, p1 = key
                file.write(f"{p0} {p1} {value}\n")

        # Save vocabulary
        vocab_file = file_name + ".vocab"
        with open(vocab_file, "w") as file:
            for key, value in self.vocab_dict.items():
                file.write(f"{key} {value}\n")

    def load(self, model_file_name):
        """
        Loads the tokenizer's merge rules from a file and rebuilds the vocabulary.

        Args:
            model_file_name (str): Name of the file containing merge rules.
        """

        with open(model_file_name, "r", encoding='utf-8') as file:
            for line in file:
                p0, p1, idx = line.split()
                self.merge_dict[(int(p0), int(p1))] = int(idx)

        self.vocab_dict = self._build_vocab_dict()
       

            



if __name__ == "__main__":
    original_text = """Ｕｎｉｃｏｄｅ! 🅤🅝🅘🅒🅞🅓🅔‽ 🇺‌🇳‌🇮‌🇨‌🇴‌🇩‌🇪! 😄 The very name strikes fear 
    and awe into the hearts of programmers worldwide. 
    We all know we ought to “support Unicode” in our software
    (whatever that means—like using wchar_t for all the strings, 
    right?). But Unicode can be abstruse, and diving into the
    thousand-page Unicode Standard plus its dozens of supplementary annexes,
    reports, and notes can be more than a little intimidating. 
    I don’t blame programmers for still finding the whole thing mysterious, 
    even 30 years after Unicode’s inception."""

    tokenizer = BaseTokenizer()

    text = tokenizer.decode(tokenizer.encode(original_text))
    print(text == original_text)

    print(tokenizer.encode("| hello world! 😄"))
    print(tokenizer.decode([124, 32, 104, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100, 33, 32, 240, 159, 152, 132]))

    # Uncomment the following line to inspect the vocabulary dictionary
    # print(tokenizer.vocab_dict)




