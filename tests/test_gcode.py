from wirecode import gcode
from wirecode import GCode

COMMAND = r"G01 (comment1) X 00 y-0.1 ;comment2"
GCODE = GCode(["G01", "X00", "Y-0.1"], [], ["(comment1)", ";comment2"])


def test_extract_comments():
    g = GCode()
    remainder = g._extract_comments(COMMAND)
    assert g.comments == ["(comment1)", ";comment2"]
    assert remainder == "G01  X 00 y-0.1 "


def test_extract_words():
    g = GCode()
    remainder = g._extract_words("G01X00Y-0.1")
    assert g.words == ["G01", "X00", "Y-0.1"]
    assert remainder == ""


def test_gcode_parse():
    g = GCode.from_string(COMMAND)
    assert g == GCODE


def test_get_word():
    g = GCode.from_string(COMMAND)
    result = g.get_code_word("X")
    assert result == ("X", 0.0)
    result = g.get_code_word("Z")
    assert result is None


def test_get_position():
    g = GCode.from_string(COMMAND)
    position = g.get_position()
    assert position == {"X": 0, "Y": -0.1}


def test_repr():
    g = GCode.from_string(COMMAND)
    assert str(g) == "G01 X00 Y-0.1 (comment1) ;comment2"


def test_split_line():
    g = GCode(["G01", "X00", "Y-0.1"])
    p = {"X": 0, "Y": 0.1}
    (gm,) = gcode.split_line(p, g)
    assert gm.get_position() == {"X": 0, "Y": 0}