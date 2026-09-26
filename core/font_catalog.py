"""Additional Google Fonts families verified for Turkish glyph coverage."""

ADDITIONAL_FONT_FAMILIES = {
    'serif': ('Literata', 'Alegreya', 'Andada Pro', 'Bitter', 'Gentium Book Plus',
              'Brygada 1918', 'Domine', 'Faustina', 'Hepta Slab', 'IBM Plex Serif',
              'Newsreader', 'Petrona', 'Roboto Serif', 'STIX Two Text'),
    'sans': ('Atkinson Hyperlegible Next', 'Barlow', 'Cabin', 'Figtree', 'Geologica',
             'IBM Plex Sans', 'Manrope', 'Mulish', 'Outfit', 'Public Sans', 'Sora',
             'Space Grotesk', 'Ubuntu', 'Urbanist'),
    'mono': ('IBM Plex Mono', 'Inconsolata', 'Recursive', 'Roboto Mono', 'Space Mono'),
    'display': ('Bodoni Moda', 'Cinzel', 'Fraunces', 'Unbounded'),
    'handwriting': ('Bad Script', 'Marck Script', 'Pangolin'),
}


def additional_font_options():
    return {category: [(name.replace(' ', '+'), name) for name in names]
            for category, names in ADDITIONAL_FONT_FAMILIES.items()}
