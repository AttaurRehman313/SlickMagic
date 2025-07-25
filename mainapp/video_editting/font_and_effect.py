# subtitle options
def video_aspect_ratio(value):
    if value == "portrait":
        height = 1280
        width = 720
    elif value == "landscape":
        height = 720
        width = 1280
    else:
        height = 1280
        width = 720
    return height, width


def select_aspect_ratio(value):
    if not value:
        return "1024x1792"
    elif value.lower() == "landscape":
        return "1792x1024"
    elif value.lower() == "portrait":
        return "1024x1792"
    else:
        return value


effects_options = [
    "color",
    "karaoke",
    "highlight",
    "fade",
    "bounce",
    "slide",
    "enlarge",
]
font_family_options = [
    "Roboto",
    "Open Sans",
    "Lato",
    "Montserrat",
    "Oswald",
    "Source Sans Pro",
    "Slabo 27px",
    "Raleway",
    "PT Sans",
    "Merriweather",
    "Nunito",
    "Ubuntu",
    "Playfair Display",
    "Roboto Condensed",
    "Poppins",
    "Noto Sans",
    "Comfortaa",
    "Fira Sans",
    "Oxygen",
    "Quicksand",
    "Cabin",
    "Indie Flower",
    "Lobster",
    "Anton",
    "Bitter",
    "Dancing Script",
    "Arimo",
    "Josefin Sans",
    "Abril Fatface",
    "Pacifico",
    "Titillium Web",
    "Rubik",
    "Karla",
    "Bebas Neue",
    "Work Sans",
    "Hind",
    "Varela Round",
    "Fjalla One",
    "Inconsolata",
    "Yanone Kaffeesatz",
    "Zilla Slab",
    "Asap",
    "Teko",
    "Catamaran",
    "Libre Baskerville",
    "Lora",
    "Crimson Text",
    "Barlow",
    "Cairo",
    "Muli",
    "Rokkitt",
    "Signika",
    "Monda",
    "PT Serif",
    "Nanum Gothic",
    "Amatic SC",
    "Architects Daughter",
    "Questrial",
    "Exo 2",
    "Lobster Two",
    "Shadows Into Light",
    "Courgette",
    "Kanit",
    "Mukta",
    "Crete Round",
    "Bree Serif",
    "Alegreya",
    "Tajawal",
    "Abril Display",
    "Caveat",
    "Bowlby One",
    "Khand",
    "Sacramento",
    "Marck Script",
    "Satisfy",
    "Yellowtail",
    "Cookie",
    "Overpass",
    "Acme",
    "Archivo Narrow",
    "Cinzel",
    "Spectral",
    "Righteous",
    "Domine",
    "Lemonada",
    "Bree Serif",
    "Fira Code",
    "EB Garamond",
    "Rajdhani",
    "Fira Sans Condensed",
    "DM Serif Display",
    "Fira Sans Extra Condensed",
    "Arial",
    "Helvetica",
    "Georgia",
    "Times New Roman",
    "Trebuchet MS",
    "Verdana",
    "Courier New",
    "Lucida Console",
    "Tahoma",
    "Impact",
]

# Theme options
themes = [
    "Realistic",
    "Animated",
    "Cartoonish",
    "Abstract",
    "Vintage",
    "Minimalist",
    "Fantasy",
    "Sci-Fi",
    "Pop Art",
    "Sketch",
]
