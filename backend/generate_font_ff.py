# generate_font_ff.py
# Run: fontforge -script generate_font_ff.py svg_folder out.ttf "Font Name"
import fontforge
import sys
import os

CHARS = [chr(ord('a') + i) for i in range(26)]

if len(sys.argv) < 4:
    print("Usage: fontforge -script generate_font_ff.py svg_dir out.ttf 'Font Name'")
    sys.exit(1)

svg_dir = sys.argv[1]
out_ttf = sys.argv[2]
font_name = sys.argv[3]

font = fontforge.font()
font.encoding = 'UnicodeFull'
font.fontname = font_name.replace(" ", "")
font.fullname = font_name
font.familyname = font_name

# set a default em size and ascent/descent
EM = 1000
font.ascent = 800
font.descent = 200

for ch in CHARS:
    svg_path = os.path.join(svg_dir, f"{ch}.svg")
    if not os.path.exists(svg_path):
        print("Missing", svg_path, "-- skipping", ch)
        continue
    codepoint = ord(ch)
    glyph = font.createChar(codepoint, ch)
    print("Importing", svg_path, "into glyph", ch)
    glyph.importOutlines(svg_path)
    # optional: scale glyph to fit em size
   #glyph.transform(psMat.scale(1, -1))  # flip as needed (sometimes SVGs invert)
    # set width
    glyph.width = 600

# generate font
font.generate(out_ttf)
print("Generated font:", out_ttf)
