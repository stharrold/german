"""Generate printable PDFs from B1 exam exercise JSON files.

Usage:
    uv run python scripts/make_pdfs.py

Output:
    build/pdfs/b1-{skill}-{teil|aufgabe}-{N}.pdf  (one PDF per part, one exercise per page)
"""

import sys
from pathlib import Path

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

# macOS system font paths (Arial supports full Unicode including German characters)
_FONT_PATHS = {
    "": "/System/Library/Fonts/Supplemental/Arial.ttf",
    "B": "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "I": "/System/Library/Fonts/Supplemental/Arial Italic.ttf",
    "BI": "/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf",
}


def _find_fonts() -> dict[str, str]:
    """Return available font style → path mapping, raising if none found."""
    available = {style: path for style, path in _FONT_PATHS.items() if Path(path).exists()}
    if not available:
        raise FileNotFoundError(
            "No Arial TTF fonts found. Expected fonts at:\n"
            + "\n".join(f"  {p}" for p in _FONT_PATHS.values())
        )
    return available


class ExamPDF(FPDF):
    """PDF with consistent header/footer for exam exercises."""

    def __init__(self, skill: str, part_label: str) -> None:
        super().__init__()
        self.skill_name = skill
        self.part_label = part_label
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
        pdf.cell(pdf.get_string_width(speaker_text))
        pdf.set_font(FONT, "", 10)
        pdf.multi_cell(CONTENT_W - pdf.get_string_width(speaker_text), 5.5, f"{speaker_text}{line.text_de}")
        pdf.ln(1)
    pdf.ln(2)

    pdf.section_subtitle("Fragen")
    for q in ex.questions:
        pdf.set_font(FONT, "B", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(CONTENT_W, 5.5, f"{q.number}. {q.text_de}")
        if q.options:
            pdf.set_font(FONT, "", 10)
            for j, opt in enumerate(q.options):
                label = chr(ord("a") + j)
                pdf.cell(10)
                pdf.multi_cell(CONTENT_W - 10, 5.5, f"{label})  {opt}")
        elif q.type == "true_false":
            pdf.set_font(FONT, "", 10)
            pdf.cell(10)
            pdf.cell(30, 5.5, "\u25a1  richtig")
            pdf.cell(30, 5.5, "\u25a1  falsch")
            pdf.ln(6)
        pdf.ln(2)


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
    for q in ex.questions:
        pdf.set_font(FONT, "B", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(CONTENT_W, 5.5, f"{q.number}. {q.text_de}")
        if q.options:
            pdf.set_font(FONT, "", 10)
            for j, opt in enumerate(q.options):
                label = chr(ord("a") + j)
                pdf.cell(10)
                pdf.multi_cell(CONTENT_W - 10, 5.5, f"{label})  {opt}")
        elif q.type == "true_false":
            pdf.set_font(FONT, "", 10)
            pdf.cell(10)
            pdf.cell(30, 5.5, "\u25a1  richtig")
            pdf.cell(30, 5.5, "\u25a1  falsch")
            pdf.ln(6)
        pdf.ln(2)


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


def build_pdfs() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    count = 0

    # Hören
    for teil in range(1, 5):
        teil_dir = RESOURCES / "hoeren" / f"teil-{teil}"
        exercises = load_exercises(teil_dir, ListeningExercise)
        if not exercises:
            continue
        pdf = ExamPDF("Hören", f"Teil {teil}")
        for ex in exercises:
            render_listening(pdf, ex)
        out = OUTPUT / f"b1-hoeren-teil-{teil}.pdf"
        pdf.output(str(out))
        count += len(exercises)
        print(f"  {out.name}: {len(exercises)} exercises")

    # Lesen
    for teil in range(1, 6):
        teil_dir = RESOURCES / "lesen" / f"teil-{teil}"
        exercises = load_exercises(teil_dir, ReadingExercise)
        if not exercises:
            continue
        pdf = ExamPDF("Lesen", f"Teil {teil}")
        for ex in exercises:
            render_reading(pdf, ex)
        out = OUTPUT / f"b1-lesen-teil-{teil}.pdf"
        pdf.output(str(out))
        count += len(exercises)
        print(f"  {out.name}: {len(exercises)} exercises")

    # Schreiben
    for aufgabe in range(1, 4):
        aufgabe_dir = RESOURCES / "schreiben" / f"aufgabe-{aufgabe}"
        exercises = load_exercises(aufgabe_dir, WritingExercise)
        if not exercises:
            continue
        pdf = ExamPDF("Schreiben", f"Aufgabe {aufgabe}")
        for ex in exercises:
            render_writing(pdf, ex)
        out = OUTPUT / f"b1-schreiben-aufgabe-{aufgabe}.pdf"
        pdf.output(str(out))
        count += len(exercises)
        print(f"  {out.name}: {len(exercises)} exercises")

    # Sprechen
    for teil in range(1, 4):
        teil_dir = RESOURCES / "sprechen" / f"teil-{teil}"
        exercises = load_exercises(teil_dir, SpeakingExercise)
        if not exercises:
            continue
        pdf = ExamPDF("Sprechen", f"Teil {teil}")
        for ex in exercises:
            render_speaking(pdf, ex)
        out = OUTPUT / f"b1-sprechen-teil-{teil}.pdf"
        pdf.output(str(out))
        count += len(exercises)
        print(f"  {out.name}: {len(exercises)} exercises")

    print(f"\nGenerated {count} exercises across {len(list(OUTPUT.glob('*.pdf')))} PDFs in {OUTPUT}/")


if __name__ == "__main__":
    print("Generating B1 exam practice PDFs...\n")
    build_pdfs()
