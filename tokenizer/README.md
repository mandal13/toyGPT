# Tokenizer Module

This folder contains a modular implementation of a tokenizer, inspired by Andrej Karpathy's lecture *"Let's build the GPT Tokenizer"* on YouTube.

It provides tools to
- train a tokenizer with the given text to build a vocabulary dictionary and merges dictionary
- encode a given text to tokens
- decode a given token lists to text

## Files and Structure

- **`helper.py`**  
  Contains utility functions that assist in various operations required by the tokenizer module.

- **`baseTokenizer.py`**  
  Defines the `BaseTokenizer` class, which provides foundational methods for tokenization, including byte-level encoding and decoding.

- **`basicTokenizer.py`**  
  Implements a basic tokenizer built on top of `BaseTokenizer`, introducing simple tokenization with the help of Byte Pair Encoding (BPE) algorithm.

- **`advanceTokenizer.py`**  
  Contains an advanced tokenizer implementation using Byte Pair Encoding (BPE) algorithm which splits the text according to `regex` pattern to avoid merges between letters, numbers and punctuations etc.

## Acknowledgment

This project is heavily inspired by Andrej Karpathy's excellent lecture on building a GPT tokenizer. You can find his lecture and accompanying resources here:  
- **YouTube Lecture:** [Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE&t=1983s&ab_channel=AndrejKarpathy)  
- **GitHub Repository:** [Andrej Karpathy's minbpe](https://github.com/karpathy/minbpe)

## Usage

To use any of the tokenizers, simply import the required module and create an instance of the tokenizer. For example:

```python
from tokenizer import BaseTokenizer

tokenizer = BaseTokenizer()
encoded = tokenizer.encode("Hello, World!")
decoded = tokenizer.decode(encoded)

print(encoded)  # Byte-level token IDs
print(decoded)  # Original text

