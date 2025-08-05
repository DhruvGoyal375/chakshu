# Captioner
IMAGE_CAPTIONING_PROMPT = """
[User]: Forget all previous messages and context. Focus **only** on the provided image.

You are an AI specialized in generating **highly descriptive yet concise captions** for images,
designed to help **visually impaired individuals** understand the scene with clarity.

### **Key Instructions:**
1. **Use Provided Context for Identification (If Certain):**
   - If the **Title, Caption, or Description** mentions a **specific person, object, or place**, use the name **instead of generic terms**.
   - If uncertain, describe the object or person as seen without assumption.
2. **Describe Actions and Positions Clearly:**
   - Identify what each person is doing.
   - Specify relative positioning (who is sitting, standing, or interacting how).
3. **Include Background Elements Only If Relevant:**
   - Mention key visible details but avoid adding details that are not evident.
4. **Concise Yet Detailed:** Use structured, vivid descriptions while keeping it short and natural.

### **Context Provided (Use Only If It Matches What Is Seen):**
- **Title:** {Title}
- **Caption:** {Caption}
- **Description:** {Description}

### **Your Task:**
Generate a **short but structured paragraph** that accurately describes:
- **The main subjects and their actions.**
- **Their spatial arrangement (who is sitting, standing, or interacting how).**
- **Any relevant background elements.**
- **Ensure clarity while keeping it brief.**
"""

MODEL_NAME = "qwen2.5vl"

TABLE_SCREENSHOT_PATH = "screenshots/"

TABLE_ACCESSIBILITY_PROMPT = """
    Describe the table in the image in a way that is easily readable by a screen reader or text-to-speech application for a blind person.
    Clearly state the table's purpose, column headers, and each row's data.
    """

# List of valid element symbols from the periodic table
ELEMENTS = {
    "H",
    "He",
    "Li",
    "Be",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "Na",
    "Mg",
    "Al",
    "Si",
    "P",
    "S",
    "Cl",
    "Ar",
    "K",
    "Ca",
    "Sc",
    "Ti",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "Ga",
    "Ge",
    "As",
    "Se",
    "Br",
    "Kr",
    "Rb",
    "Sr",
    "Y",
    "Zr",
    "Nb",
    "Mo",
    "Tc",
    "Ru",
    "Rh",
    "Pd",
    "Ag",
    "Cd",
    "In",
    "Sn",
    "Sb",
    "Te",
    "I",
    "Xe",
    "Cs",
    "Ba",
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
    "Hf",
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Pt",
    "Au",
    "Hg",
    "Tl",
    "Pb",
    "Bi",
    "Po",
    "At",
    "Rn",
    "Fr",
    "Ra",
    "Ac",
    "Th",
    "Pa",
    "U",
    "Np",
    "Pu",
    "Am",
    "Cm",
    "Bk",
    "Cf",
    "Es",
    "Fm",
    "Md",
    "No",
    "Lr",
    "Rf",
    "Db",
    "Sg",
    "Bh",
    "Hs",
    "Mt",
    "Ds",
    "Rg",
    "Cn",
    "Nh",
    "Fl",
    "Mc",
    "Lv",
    "Ts",
    "Og",
}
