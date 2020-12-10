from wirecode.gcode import GCode

COMMAND = r"G01 (comment1) X 00 y-0.1 ;comment2"
GCODE = GCode(["G01", "X00", "Y-0.1"], [], ["(comment1)", ";comment2"])


def test_extract_comments():
    gcode = GCode()
    remainder = gcode._extract_comments(COMMAND)
    assert gcode.comments == ["(comment1)", ";comment2"]
    assert remainder == "G01  X 00 y-0.1 "


def test_extract_words():
    gcode = GCode()
    remainder = gcode._extract_words("G01X00Y-0.1")
    assert gcode.words == ["G01", "X00", "Y-0.1"]
    assert remainder == ""


def test_gcode_parse():
    gcode = GCode.from_string(COMMAND)
    assert gcode == GCODE


def test_get_word():
    gcode = GCode.from_string(COMMAND)
    result = gcode.get_code_word("X")
    assert result == ("X", 0.0)
    result = gcode.get_code_word("Z")
    assert result is None


def test_get_position():
    gcode = GCode.from_string(COMMAND)
    position = gcode.get_position()
    assert position == {"X": 0, "Y": -0.1}
