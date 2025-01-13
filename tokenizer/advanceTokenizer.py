from baseTokenizer import BaseTokenizer
from helper import getPairStats, merge

import regex as re

PATTERN = r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""

class AdvanceTokenizer(BaseTokenizer):
    """
    An advanced tokenizer class implementing Byte Pair Encoding (BPE) 
    with custom tokenization based on a regex pattern.

    This tokenizer extends the BaseTokenizer and provides methods for training, 
    encoding, and decoding, using BPE for subword-level tokenization.

    Attributes:
        pattern (str): Regular expression pattern for spliting the text into subtexts.
        compiled_pattern (regex.Pattern): Compiled regex pattern for efficient spliting.
    """

    def __init__(self):
        super().__init__()
        self.pattern = PATTERN
        self.compiled_pattern = re.compile(self.pattern)

    
    def train(self, text, vocab_size):
        """
        Trains the tokenizer to learn subword merges using Byte Pair Encoding (BPE).

        Args:
            text (str): Input text to train the tokenizer on.
            vocab_size (int): Desired vocabulary size (must be >= 256 to include byte-level tokens).
        """
        assert vocab_size >= 256

        num_of_merges = vocab_size - 256

        # split input text into subwords based on the regex pattern
        text_list = re.findall(self.compiled_pattern, text)
        # Convert each subword into its byte representation
        bytes_list = [list(text.encode('utf-8')) for text in text_list]
        
        for i in range(num_of_merges):
            # Compute frequency of byte pairs across all subwords
            pairStats = {}
            for subword in bytes_list:
                pairStats = getPairStats(subword, pairStats)
            
            # Select the most frequent pair for merging
            pair = max(pairStats, key = lambda x : pairStats[x])
            # Merge the selected pair in all subwords
            bytes_list = [merge(subword, pair, 256 + i) for subword in bytes_list]

            # Update merge and vocabulary dictionaries
            self.merge_dict[pair] = 256 + i
            self.vocab_dict[256 + i] = self.vocab_dict[pair[0]] + self.vocab_dict[pair[1]]

        
    def encode(self, text):
        """
        Encodes the input text into a sequence of token IDs using the learned BPE merges.

        Args:
            text (str): Input text to encode.

        Returns:
            list: A list of token IDs representing the encoded text.
        """
        # split input text into subwords based on the regex pattern
        text_list = re.findall(self.compiled_pattern, text)
        bytes_list = [list(text.encode('utf-8')) for text in text_list]

        encoded_text = []
        for subword in bytes_list:
            # Apply BPE merges to reduce subword sequences
            while len(subword) >= 2:
                pairStat = getPairStats(subword)
                pair = min(pairStat, key = lambda x : self.merge_dict.get(x, float('inf')))
                if pair not in self.merge_dict:
                    break
                subword = merge(subword, pair, self.merge_dict[pair])
            encoded_text.extend(subword)

        return encoded_text
        
    

    def decode(self, tokenIds):
        """
        Decodes a sequence of token IDs back into the original text.

        Args:
            tokenIds (list): A list of token IDs to decode.

        Returns:
            str: The decoded text string.
        """
        text_bytes = b"".join(self.vocab_dict[t] for t in tokenIds)
        return text_bytes.decode("utf-8", errors='replace')



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


    tokenizer = AdvanceTokenizer()
    tokenizer.train(original_text, 512)

    text = tokenizer.decode(tokenizer.encode(original_text))
    print(text == original_text)

    #tokenizer.save("text")
    #tokenizer.load("text.model")
    print(tokenizer.encode(" supplementary right world"))
    print(tokenizer.decode([124, 32, 104, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100, 33, 32, 240, 159, 152, 132]))
    #print(tokenizer.vocab_dict)