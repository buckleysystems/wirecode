__version__ = "0.1.0"
from dataclasses import dataclass, field
from typing import Tuple, List, Union, Dict
import re

bracketed_comment_pattern = re.compile(r"(\(.*?\))")
word_pattern = re.compile(r"([A-Z][+,-]?\d*[\.]?\d*)")
whitespace_pattern = re.compile(r"\s+")


def remove_all_whitespace(string: str) -> str:
    return re.sub(whitespace_pattern, "", string)


@dataclass
class GCode:
    words: List[str] = field(default_factory=list)
    params: List[str] = field(default_factory=list)
    comments: List[str] = field(default_factory=list)

    def _extract_comments(self, command: str) -> str:
        """Extract comments from a gcode string"""
        idx = command.find(";")  # Find first semicolon
        if idx < 0:
            # No semicolon means no comment, whole line is command
            remainder = command
        else:
            # Split around the first semicolon
            remainder = command[:idx]
            line_comments = [command[idx:]]
        # Now split out bracketed comments
        parts = re.split(bracketed_comment_pattern, remainder)
        # This gives comments and remaining command interleaved (remainder first)
        remainder = "".join(parts[::2])
        bracket_comments = parts[1::2]
        # Add comments (in order)
        self.comments += bracket_comments
        self.comments += line_comments
        # Give back the rest
        return remainder

    def _extract_words(self, command: str) -> str:
        """extract words from a normalized, uncommented gcode string"""
        parts = re.split(word_pattern, command)
        # This gives words and remaining stuff interleaved (remainder starts at 0)
        remainder = "".join(parts[::2])
        self.words = parts[1::2]
        return remainder

    @classmethod
    def from_string(cls, gcode_string: str):
        """given a string, parse and update self"""
        gcode = cls()
        # Leading and trailing whitespace is not meaningful
        remainder = gcode_string.strip()
        # Pull out comments first, since they are whitespace/case sensitive
        remainder = gcode._extract_comments(remainder)
        # Once comments are removed, whitespace is meaningless, so lets get rid of it
        remainder = remove_all_whitespace(remainder)
        # Also uppercase it (as a normalization)
        remainder = remainder.upper()
        # Now get out words
        remainder = gcode._extract_words(remainder)
        print("+" * 80)
        print(remainder)
        # That should be everything
        assert remainder == ""
        # Pass back GCode object
        return gcode

    def get_code_word(self, code: str) -> Union[Tuple[str, float], None]:
        # Code should be a single character between A and Z
        code = code.upper()
        assert len(code) == 1
        assert "A" <= code <= "Z"

        # Look for code in words
        for w in self.words:
            if w.startswith(code):
                return (code, float(w[1:]))

        # If not found return None
        return None

    def get_position(self) -> Dict[str, float]:
        # Get code words that encode position
        words = [self.get_code_word(c) for c in ("X", "Y", "Z", "A", "B")]
        # Filter out "None"s from the list
        found_words = [w for w in words if w is not None]
        # Return as a dictionary
        return {code: value for (code, value) in found_words}
