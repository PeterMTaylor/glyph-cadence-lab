from datetime import datetime

class Glyph:
    def __init__(self, name, reversed=False):
        self.name = name
        self.reversed = reversed
        self.timestamp = datetime.now()

    def pulse(self):
        return f"{self.name} {'(reversed)' if self.reversed else '(normal)'} @ {self.timestamp}"

# Example glyph cycle
glyphs = [
    Glyph("The Lantern Drawer"),
    Glyph("The Sidle Signal", reversed=True),
    Glyph("Fork Whisper")
]

for g in glyphs:
    print(g.pulse())
