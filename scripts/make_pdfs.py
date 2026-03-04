"""Generate printable PDFs from B1 exam exercise JSON files.

Usage:
    uv pip install -e ".[pdf]"
    uv run python scripts/make_pdfs.py

Output:
    build/pdfs/b1-{skill}-{teil|aufgabe}-{N}.pdf  (one PDF per part, one exercise per page)
"""

import os
import platform
import sys
from pathlib import Path
from typing import Callable

from fpdf import FPDF

# Ensure src/ is importable
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from german.exams.loader import load_exercises
from german.exams.models import ListeningExercise, ReadingExercise, SpeakingExercise, WritingExercise

RESOURCES = Path(__file__).parent.parent / "resources" / "exams" / "b1"
OUTPUT = Path(__file__).parent.parent / "build" / "pdfs"

# Page layout constants
PAGE_W = 210  # A4 width mm
MARGIN = 15
CONTENT_W = PAGE_W - 2 * MARGIN

# Font name used throughout (registered as Unicode TTF)
FONT = "Arial"

# Cross-platform font search paths (Arial or fallback sans-serif)
_WIN_FONTS = Path(os.environ.get("SystemRoot", "C:/Windows")) / "Fonts"
_FONT_CANDIDATES: dict[str, list[str]] = {
    "": [
        "/System/Library/Fonts/Supplemental/Arial.ttf",  # macOS
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",  # Linux (Debian/Ubuntu)
        "/usr/share/fonts/liberation-sans/LiberationSans-Regular.ttf",  # Linux (Fedora)
        str(_WIN_FONTS / "arial.ttf"),  # Windows
    ],
    "B": [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/liberation-sans/LiberationSans-Bold.ttf",
        str(_WIN_FONTS / "arialbd.ttf"),
    ],
    "I": [
        "/System/Library/Fonts/Supplemental/Arial Italic.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
        "/usr/share/fonts/liberation-sans/LiberationSans-Italic.ttf",
        str(_WIN_FONTS / "ariali.ttf"),
    ],
    "BI": [
        "/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf",
        "/usr/share/fonts/liberation-sans/LiberationSans-BoldItalic.ttf",
        str(_WIN_FONTS / "arialbi.ttf"),
    ],
}


def _find_fonts() -> dict[str, str]:
    """Return font style -> path mapping, searching cross-platform locations.

    Falls back to the regular font for missing bold/italic variants.
    Raises FileNotFoundError if no regular font is found.
    """
    found: dict[str, str] = {}
    for style, candidates in _FONT_CANDIDATES.items():
        for path in candidates:
            if Path(path).exists():
                found[style] = path
                break
    if "" not in found:
        raise FileNotFoundError(
            f"No Arial/Liberation Sans TTF font found ({platform.system()}).\n"
            "Install liberation-sans (Linux) or ensure Arial is available."
        )
    # Fall back to regular for missing variants
    for style in ("B", "I", "BI"):
        if style not in found:
            found[style] = found[""]
    return found


class ExamPDF(FPDF):
    """PDF with consistent header/footer for exam exercises."""

    def __init__(self, skill: str, part_label: str) -> None:
        super().__init__()
        self.skill_name = skill
        self.part_label = part_label
        self.set_margins(MARGIN, MARGIN, MARGIN)
        self.set_auto_page_break(auto=True, margin=20)
        # Register Unicode TTF fonts
        for style, path in _find_fonts().items():
            self.add_font(FONT, style, path)

    def header(self) -> None:
        self.set_font(FONT, "B", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 6, f"Goethe-Zertifikat B1  |  {self.skill_name}  |  {self.part_label}", align="C")
        self.ln(8)
        self.set_draw_color(200, 200, 200)
        self.line(MARGIN, self.get_y(), PAGE_W - MARGIN, self.get_y())
        self.ln(4)

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font(FONT, "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Seite {self.page_no()}", align="C")

    def section_title(self, text: str) -> None:
        self.set_font(FONT, "B", 13)
        self.set_text_color(0, 0, 0)
        self.multi_cell(CONTENT_W, 7, text)
        self.ln(2)

    def section_subtitle(self, text: str) -> None:
        self.set_font(FONT, "B", 10)
        self.set_text_color(60, 60, 60)
        self.multi_cell(CONTENT_W, 6, text)
        self.ln(2)

    def body_text(self, text: str) -> None:
        self.set_font(FONT, "", 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(CONTENT_W, 5.5, text)
        self.ln(2)

    def italic_text(self, text: str) -> None:
        self.set_font(FONT, "I", 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(CONTENT_W, 5.5, text)
        self.ln(1)

    def bullet_list(self, items: list[str]) -> None:
        self.set_font(FONT, "", 10)
        self.set_text_color(0, 0, 0)
        for item in items:
            self.cell(5)
            self.multi_cell(CONTENT_W - 5, 5.5, f"\u2022  {item}")
            self.ln(1)
        self.ln(1)

    def numbered_list(self, items: list[str], start: int = 1) -> None:
        self.set_font(FONT, "", 10)
        self.set_text_color(0, 0, 0)
        for i, item in enumerate(items, start=start):
            self.cell(8)
            self.multi_cell(CONTENT_W - 8, 5.5, f"{i}.  {item}")
            self.ln(1)
        self.ln(1)

    def separator(self) -> None:
        self.set_draw_color(200, 200, 200)
        y = self.get_y()
        self.line(MARGIN, y, PAGE_W - MARGIN, y)
        self.ln(4)

    def answer_lines(self, count: int = 8) -> None:
        self.set_draw_color(200, 200, 200)
        for _ in range(count):
            y = self.get_y()
            self.line(MARGIN, y, PAGE_W - MARGIN, y)
            self.ln(8)


def _render_questions(pdf: ExamPDF, questions: list) -> None:
    """Render questions with options or true/false checkboxes."""
    for q in questions:
        pdf.set_font(FONT, "B", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(CONTENT_W, 5.5, f"{q.number}. {q.text_de}")
        if q.options:
            pdf.set_font(FONT, "", 10)
            for opt in q.options:
                pdf.cell(10)
                pdf.multi_cell(CONTENT_W - 10, 5.5, opt)
        elif q.type == "true_false":
            pdf.set_font(FONT, "", 10)
            pdf.cell(10)
            pdf.cell(30, 5.5, "\u25a1  richtig")
            pdf.cell(30, 5.5, "\u25a1  falsch")
            pdf.ln(6)
        pdf.ln(2)


def render_listening(pdf: ExamPDF, ex: ListeningExercise) -> None:
    pdf.add_page()
    pdf.section_title(ex.title)
    pdf.italic_text(ex.instructions)
    pdf.body_text(f"Zeit: {ex.time_minutes} Minuten")
    pdf.separator()

    pdf.section_subtitle("Transkript")
    for line in ex.transcript:
        pdf.set_font(FONT, "B", 10)
        pdf.set_text_color(0, 0, 0)
        speaker_text = f"{line.speaker}: "
        speaker_w = pdf.get_string_width(speaker_text)
        pdf.cell(speaker_w, 5.5, text=speaker_text)
        pdf.set_font(FONT, "", 10)
        # Temporarily adjust left margin so wrapped lines align under dialogue text
        old_l_margin = pdf.l_margin
        pdf.set_left_margin(MARGIN + speaker_w)
        pdf.multi_cell(CONTENT_W - speaker_w, 5.5, line.text_de)
        pdf.set_left_margin(old_l_margin)
        pdf.ln(1)
    pdf.ln(2)

    pdf.section_subtitle("Fragen")
    _render_questions(pdf, ex.questions)


def render_reading(pdf: ExamPDF, ex: ReadingExercise) -> None:
    pdf.add_page()
    pdf.section_title(ex.title)
    pdf.italic_text(ex.instructions)
    pdf.body_text(f"Zeit: {ex.time_minutes} Minuten")
    pdf.separator()

    pdf.section_subtitle(f"Text ({ex.passage.source})")
    pdf.body_text(ex.passage.text_de)
    pdf.separator()

    pdf.section_subtitle("Fragen")
    _render_questions(pdf, ex.questions)


def render_writing(pdf: ExamPDF, ex: WritingExercise) -> None:
    pdf.add_page()
    pdf.section_title(ex.title)
    pdf.italic_text(ex.instructions)
    pdf.separator()

    pdf.section_subtitle("Situation")
    pdf.body_text(ex.situation_de)

    pdf.section_subtitle("Inhaltspunkte")
    pdf.bullet_list(ex.required_points)

    pdf.body_text(f"Schreiben Sie circa {ex.target_word_count} Wörter.")
    pdf.separator()
    pdf.answer_lines(10)


def render_speaking(pdf: ExamPDF, ex: SpeakingExercise) -> None:
    pdf.add_page()
    pdf.section_title(ex.title)
    pdf.italic_text(ex.instructions)
    pdf.separator()

    pdf.section_subtitle("Situation")
    pdf.body_text(ex.situation_de)

    pdf.section_subtitle("Diskussionspunkte")
    pdf.bullet_list(ex.discussion_points)


# Skill configuration: each entry drives PDF generation for one exam section
_SKILL_CONFIG: list[dict] = [
    {"name_de": "Hören", "dir_name": "hoeren", "part_prefix": "teil", "part_label": "Teil", "model": ListeningExercise, "renderer": render_listening},
    {"name_de": "Lesen", "dir_name": "lesen", "part_prefix": "teil", "part_label": "Teil", "model": ReadingExercise, "renderer": render_reading},
    {"name_de": "Schreiben", "dir_name": "schreiben", "part_prefix": "aufgabe", "part_label": "Aufgabe", "model": WritingExercise, "renderer": render_writing},
    {"name_de": "Sprechen", "dir_name": "sprechen", "part_prefix": "teil", "part_label": "Teil", "model": SpeakingExercise, "renderer": render_speaking},
]


def build_pdfs() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    exercise_count = 0
    pdf_count = 0

    for config in _SKILL_CONFIG:
        skill_dir = RESOURCES / config["dir_name"]
        if not skill_dir.exists():
            continue
        renderer: Callable = config["renderer"]
        for part_dir in sorted(skill_dir.glob(f"{config['part_prefix']}-*")):
            part_num = part_dir.name.split("-")[-1]
            exercises = load_exercises(part_dir, config["model"])
            if not exercises:
                continue
            pdf = ExamPDF(config["name_de"], f"{config['part_label']} {part_num}")
            for ex in exercises:
                renderer(pdf, ex)
            out = OUTPUT / f"b1-{config['dir_name']}-{config['part_prefix']}-{part_num}.pdf"
            pdf.output(str(out))
            exercise_count += len(exercises)
            pdf_count += 1
            print(f"  {out.name}: {len(exercises)} exercises")

    print(f"\nGenerated {exercise_count} exercises across {pdf_count} PDFs in {OUTPUT}/")


if __name__ == "__main__":
    print("Generating B1 exam practice PDFs...\n")
    build_pdfs()
