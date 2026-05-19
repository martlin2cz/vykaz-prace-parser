import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
import typing


@dataclass(frozen=True)
class SimpleToken:
    """ The simple lexer token (a start and end index, and the text) """
    start_char_index: int
    end_char_index: int
    text: str

    def __str__(self):
        return f"[{self.text}]"


@dataclass(frozen=True)
class ClassifiedCharacters:
    """ The mapping to the input characters and thier corresponding classes. """

    characters: str
    char_classes: str

    def __post_init__(self):
        if len(self.characters) != len(self.char_classes):
            raise ValueError("The character classes mismatch")

    def __iter__(self):
        return range(self.characters)

    def __len__(self):
        return len(self.characters)

    def chars_substr(self, start_index: int, end_index: str) -> str:
        """ Returns the substring of the characters of a given range. """
        return self.characters[start_index:end_index]

    def char_classes_substr(self, start_index: int) -> str:
        """ Returns the substring of the character classes starting by the given index. """
        return self.char_classes[start_index:]


class AbstractCharacterClassifier(ABC):
    """ The classifier. A part of the lexer, which computes class of a given input text character. """

    def classify(self, text: str) -> ClassifiedCharacters:
        """ Classifies the text. """

        char_classes = []

        for i in range(len(text)):
            char = text[i]

            class_ = self.class_of_char(i, char, text)
            if class_ is None or len(class_) != 1:
                raise ValueError("The class of the character has to be exactly one char long")

            char_classes.append(class_)

        return ClassifiedCharacters(text, "".join(char_classes))

    @abstractmethod
    def class_of_char(self, i: int, char: str, text: str) -> str:
        """ Classifies particular character of the text. Returns the character repesenting the class of the character. """
        pass


class AbstractTokeniser(ABC):
    """ The tokeniser. Takes the classified characters nad groups them into the tokens. """

    def tokenise(self, classes: ClassifiedCharacters) -> List[SimpleToken]:
        """ Tokenises the already classified characters. Returns the tokens. """

        result = []
        i = 0

        while i < len(classes):
            classes_substr = classes.char_classes_substr(i)
            match = self.find_matching_token(classes_substr)
            if match:
                relative_match_start, relative_match_end = (match.span()[0], match.span()[1]) \
                                        if isinstance(match, re.Match) else \
                                        (match[0], match[1])

                match_start, match_end = i + relative_match_start, i + relative_match_end
                text = classes.chars_substr(match_start, match_end)

                token = SimpleToken(match_start, match_end, text)
                result.append(token)

                i = match_end
            else:
                # TODO: yield unrecognised character or something
                i += 1

        return result

    @abstractmethod
    def find_matching_token(self, char_classes_substr: str) -> re.Match | typing.Tuple[int, int] | None:
        """ Finds the start and end of the following token from the start of the given classes substr. """
        pass


class SimpleLexer:
    """ The lexer. By using the particular classifier and tokeniser implementation tokens the specified input test. """

    def __init__(self, classifier: AbstractCharacterClassifier, tokeniser: AbstractTokeniser):
        self.classifier = classifier
        self.tokeniser = tokeniser

    def parse(self, text: str) -> List[SimpleToken]:
        """ Parses the given text into the tokens list. """

        classes = self.classifier.classify(text)
        return self.tokeniser.tokenise(classes)
