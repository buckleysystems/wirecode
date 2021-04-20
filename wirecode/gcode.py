from dataclasses import dataclass, field, asdict
from typing import Tuple, List, Union, Dict
import re
from .geometry import p_to_z, z_to_p, midpoint

bracketed_comment_pattern = re.compile(r"(\(.*?\))")
word_pattern = re.compile(r"([A-Z][+,-]?\d*[\.]?\d*)")
whitespace_pattern = re.compile(r"\s+")
_pfmt = "+014.8f"


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
            line_comments = []
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
        self.words += parts[1::2]
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

    def delete_code(self, code: str):
        code = code.upper()
        self.words = [w for w in self.words if not w.startswith(code)]

    def set_position(self, p: Dict[str, float]):
        for axis, value in p.items():
            self.delete_code(axis)
            self.words += [f"{axis}{value:{_pfmt}}"]
        return self

    def copy(self):
        return type(self)(**asdict(self))

    def __repr__(self):
        return " ".join(self.words + self.comments)


def _word_to_tuple(string: str) -> Tuple[str, float]:
    code = string[0].upper()
    value = float(string[1:])
    assert "A" <= code <= "Z"
    return (code, value)


def split_line(start_position, gcode):
    end_position = start_position.copy()
    end_position.update(gcode.get_position())
    m = midpoint(p_to_z(start_position), p_to_z(end_position))
    gm = gcode.copy()
    gm.set_position(z_to_p(m))
    return (gm,)


def load_gcode(file):
    """Read gcode from file-like object, return list of GCodes"""
    file_lines = file.readlines()
    gcode_lines = [remove_all_whitespace(l) for l in file_lines]
    return [GCode.from_string(l) for l in gcode_lines if l is not None]
