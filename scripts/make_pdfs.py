#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""Generate printable PDFs for exam practice exercises.

Produces one PDF per skill (Hören, Lesen, Schreiben, Sprechen) with
exercise pages and a separate answer key section at the end.

Usage:
    uv run --extra pdf python scripts/make_pdfs.py
    uv run --extra pdf python scripts/make_pdfs.py --level a2
    uv run --extra pdf python scripts/make_pdfs.py --level b1 --skill hoeren
    uv run --extra pdf python scripts/make_pdfs.py --level b2

Requirements:
    fpdf2 (install via: uv pip install fpdf2, or use --extra pdf)
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from fpdf import FPDF
except ImportError:
    print("Error: fpdf2 is required. Install with: uv pip install fpdf2", file=sys.stderr)
    sys.exit(1)

EXAMS_DIR = Path(__file__).resolve().parent.parent / "resources" / "exams"

# Unicode replacements for latin-1 compatible PDF output
UNICODE_REPLACEMENTS = {
    "\u2014": "-",  # em dash
    "\u2013": "-",  # en dash
    "\u2018": "'",  # left single quote
    "\u2019": "'",  # right single quote
    "\u201c": '"',  # left double quote
    "\u201d": '"',  # right double quote
    "\u2026": "...",  # ellipsis
    "\u00a0": " ",  # non-breaking space
    "\u2022": "-",  # bullet
    "\u2080": "0",  # subscript 0
    "\u2081": "1",  # subscript 1
    "\u2082": "2",  # subscript 2
    "\u2083": "3",  # subscript 3
    "\u2084": "4",  # subscript 4
    "\u2085": "5",  # subscript 5
    "\u2086": "6",  # subscript 6
    "\u2087": "7",  # subscript 7
    "\u2088": "8",  # subscript 8
    "\u2089": "9",  # subscript 9
}


def sanitize_text(text: str) -> str:
    """Replace Unicode characters unsupported by latin-1 PDF fonts."""
    for char, replacement in UNICODE_REPLACEMENTS.items():
        text = text.replace(char, replacement)
    # Replace any remaining non-latin-1 characters with '?'
    return text.encode("latin-1", errors="replace").decode("latin-1")


# Skill display names and directory mappings per level
LEVELS = {
    "a1": {
        "hoeren": {"name": "Hören", "part_label": "Teil", "parts": 3},
        "lesen": {"name": "Lesen", "part_label": "Teil", "parts": 4},
        "schreiben": {"name": "Schreiben", "part_label": "Aufgabe", "parts": 2},
        "sprechen": {"name": "Sprechen", "part_label": "Teil", "parts": 3},
    },
    "a2": {
        "hoeren": {"name": "Hören", "part_label": "Teil", "parts": 4},
        "lesen": {"name": "Lesen", "part_label": "Teil", "parts": 4},
        "schreiben": {"name": "Schreiben", "part_label": "Aufgabe", "parts": 2},
        "sprechen": {"name": "Sprechen", "part_label": "Teil", "parts": 3},
    },
    "b1": {
        "hoeren": {"name": "Hören", "part_label": "Teil", "parts": 4},
        "lesen": {"name": "Lesen", "part_label": "Teil", "parts": 5},
        "schreiben": {"name": "Schreiben", "part_label": "Aufgabe", "parts": 3},
        "sprechen": {"name": "Sprechen", "part_label": "Teil", "parts": 3},
    },
    "b2": {
        "hoeren": {"name": "Hören", "part_label": "Teil", "parts": 4},
        "lesen": {"name": "Lesen", "part_label": "Teil", "parts": 5},
        "schreiben": {"name": "Schreiben", "part_label": "Aufgabe", "parts": 2},
        "sprechen": {"name": "Sprechen", "part_label": "Teil", "parts": 2},
    },
}


class ExamPDF(FPDF):
    """PDF generator with German character support and consistent formatting."""

    def __init__(self, level: str, skill_name: str):
        super().__init__()
        self.level = level.upper()
        self.skill_name = skill_name
        self.set_auto_page_break(auto=True, margin=20)

    def cell(self, w=0, h=None, text="", *args, **kwargs):
        return super().cell(w, h, sanitize_text(str(text)), *args, **kwargs)

    def multi_cell(self, w=0, h=None, text="", *args, **kwargs):
        return super().multi_cell(w, h, sanitize_text(str(text)), *args, **kwargs)

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, f"Goethe-Zertifikat {self.level} - {self.skill_name}", align="L")
        self.ln(10)
        self.set_draw_color(200, 200, 200)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Seite {self.page_no()}", align="C")

    def add_title_page(self):
        self.add_page()
        self.ln(60)
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(0, 0, 0)
        self.cell(0, 15, f"Goethe-Zertifikat {self.level}", align="C")
        self.ln(20)
        self.set_font("Helvetica", "B", 22)
        self.cell(0, 12, self.skill_name, align="C")
        self.ln(20)
        self.set_font("Helvetica", "", 14)
        self.set_text_color(80, 80, 80)
        self.cell(0, 10, "Übungsmaterialien / Practice Materials", align="C")

    def add_section_header(self, text: str):
        self.add_page()
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 0, 0)
        self.cell(0, 12, text)
        self.ln(14)

    def add_exercise_header(self, exercise_id: str, title: str, instructions: str, time_minutes: int = 0):
        self.ln(4)
        self.set_draw_color(180, 180, 180)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, title)
        self.ln(8)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(100, 100, 100)
        if time_minutes:
            self.cell(0, 6, f"{exercise_id}  |  {time_minutes} Minuten")
        else:
            self.cell(0, 6, exercise_id)
        self.ln(8)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, instructions)
        self.ln(4)

    def add_text_block(self, label: str, text: str):
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 7, label)
        self.ln(7)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 6, text)
        self.ln(3)

    def add_questions(self, questions: list[dict], show_answers: bool = False):
        for q in questions:
            q_type = q.get("type", "")
            q_num = q.get("number", "")
            text = q.get("text_de", "")

            self.set_font("Helvetica", "B", 10)
            self.cell(8, 7, f"{q_num}.")
            self.set_font("Helvetica", "", 10)

            if q_type == "true_false":
                self.cell(0, 7, f"{text}")
                self.ln(7)
                if show_answers:
                    answer = "Richtig" if q["correct_answer"] else "Falsch"
                    self.set_font("Helvetica", "B", 9)
                    self.set_text_color(0, 100, 0)
                    explanation = q.get("explanation_de", "")
                    self.cell(8, 6, "")
                    self.multi_cell(0, 6, f"{answer} - {explanation}" if explanation else answer)
                    self.set_text_color(0, 0, 0)
                else:
                    self.set_font("Helvetica", "", 9)
                    self.cell(8, 6, "")
                    self.cell(20, 6, "[ ] Richtig")
                    self.cell(20, 6, "[ ] Falsch")
                    self.ln(6)

            elif q_type == "multiple_choice":
                self.cell(0, 7, text)
                self.ln(7)
                options = q.get("options", [])
                for i, opt in enumerate(options):
                    letter = chr(ord("a") + i)
                    self.set_font("Helvetica", "", 9)
                    self.cell(8, 6, "")
                    if show_answers and q.get("correct_answer") == letter:
                        self.set_font("Helvetica", "B", 9)
                        self.set_text_color(0, 100, 0)
                        self.cell(0, 6, f"[x] {opt}")
                        self.set_text_color(0, 0, 0)
                    else:
                        self.cell(0, 6, f"[ ] {opt}")
                    self.ln(6)
                if show_answers:
                    explanation = q.get("explanation_de", "")
                    if explanation:
                        self.set_font("Helvetica", "B", 9)
                        self.set_text_color(0, 100, 0)
                        self.cell(8, 6, "")
                        self.multi_cell(0, 6, explanation)
                        self.set_text_color(0, 0, 0)

            elif q_type == "matching":
                self.multi_cell(0, 7, text)
                if show_answers:
                    self.set_font("Helvetica", "B", 9)
                    self.set_text_color(0, 100, 0)
                    self.cell(8, 6, "")
                    self.cell(0, 6, f"Antwort: {q['correct_answer']}")
                    self.ln(6)
                    explanation = q.get("explanation_de", "")
                    if explanation:
                        self.cell(8, 6, "")
                        self.multi_cell(0, 6, explanation)
                    self.set_text_color(0, 0, 0)
                else:
                    self.cell(8, 6, "")
                    self.cell(0, 6, "Antwort: _______________")
                    self.ln(6)

            self.ln(2)

    def add_bullet_list(self, label: str, items: list[str]):
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 7, label)
        self.ln(7)
        self.set_font("Helvetica", "", 9)
        left_margin = self.l_margin
        for item in items:
            self.set_x(left_margin + 6)
            available_w = self.w - self.r_margin - self.get_x()
            self.multi_cell(available_w, 6, f"- {item}")
        self.ln(2)


def load_exercises(level: str, skill: str, part_num: int) -> list[dict]:
    """Load all exercises for a level/skill/part from JSON files."""
    skills = LEVELS[level]
    part_prefix = skills[skill]["part_label"].lower()
    part_dir = EXAMS_DIR / level / skill / f"{part_prefix}-{part_num}"
    if not part_dir.exists():
        return []
    exercises = []
    for f in sorted(part_dir.glob("uebung-*.json")):
        with open(f, "r", encoding="utf-8") as fh:
            exercises.append(json.load(fh))
    return exercises


def render_hoeren(pdf: ExamPDF, exercises: list[dict], show_answers: bool):
    """Render listening exercises."""
    for ex in exercises:
        time_min = ex.get("time_minutes", 8)
        pdf.add_exercise_header(ex["id"], ex["title"], ex["instructions"], time_min)

        if not show_answers:
            # Show transcript for practice
            pdf.add_text_block("Transkript:", "")
            pdf.set_font("Helvetica", "", 9)
            for line in ex.get("transcript", []):
                speaker = line.get("speaker", "")
                text = line.get("text_de", "")
                pdf.set_x(pdf.l_margin)
                available_w = pdf.w - pdf.l_margin - pdf.r_margin
                pdf.multi_cell(available_w, 6, f"  {speaker}: {text}")
            pdf.ln(4)

        pdf.add_questions(ex.get("questions", []), show_answers=show_answers)


def render_lesen(pdf: ExamPDF, exercises: list[dict], show_answers: bool):
    """Render reading exercises."""
    for ex in exercises:
        time_min = ex.get("time_minutes", 10)
        pdf.add_exercise_header(ex["id"], ex["title"], ex["instructions"], time_min)

        if not show_answers:
            passage = ex.get("passage", {})
            text_de = passage.get("text_de", "")
            source = passage.get("source", "")
            pdf.add_text_block(f"Text ({source}):", text_de)

        pdf.add_questions(ex.get("questions", []), show_answers=show_answers)


def render_schreiben(pdf: ExamPDF, exercises: list[dict], show_answers: bool):
    """Render writing exercises."""
    for ex in exercises:
        pdf.add_exercise_header(ex["id"], ex["title"], ex["instructions"])

        pdf.add_text_block("Situation:", ex.get("situation_de", ""))
        pdf.add_bullet_list("Inhaltspunkte:", ex.get("required_points", []))

        if show_answers:
            model = ex.get("model_answer", {})
            pdf.add_text_block("Musterantwort:", model.get("text_de", ""))
            pdf.add_bullet_list("Bewertungskriterien:", ex.get("scoring_criteria", []))
        else:
            # Writing space
            pdf.ln(4)
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(150, 150, 150)
            pdf.cell(0, 6, f"(Schreiben Sie ca. {ex.get('target_word_count', 80)} Wörter)")
            pdf.set_text_color(0, 0, 0)
            pdf.ln(8)
            for _ in range(10):
                pdf.set_draw_color(220, 220, 220)
                pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
                pdf.ln(8)


def render_sprechen(pdf: ExamPDF, exercises: list[dict], show_answers: bool):
    """Render speaking exercises."""
    for ex in exercises:
        pdf.add_exercise_header(ex["id"], ex["title"], ex["instructions"])

        pdf.add_text_block("Situation:", ex.get("situation_de", ""))
        pdf.add_bullet_list("Gesprächspunkte:", ex.get("discussion_points", []))

        if show_answers:
            pdf.add_text_block("Musterdialog:", "")
            pdf.set_font("Helvetica", "", 9)
            for line in ex.get("model_dialogue", []):
                speaker = line.get("speaker", "")
                text = line.get("text_de", "")
                pdf.set_x(pdf.l_margin)
                available_w = pdf.w - pdf.l_margin - pdf.r_margin
                pdf.multi_cell(available_w, 6, f"  {speaker}: {text}")
            pdf.ln(3)
            pdf.add_bullet_list("Bewertungskriterien:", ex.get("evaluation_criteria", []))


RENDERERS = {
    "hoeren": render_hoeren,
    "lesen": render_lesen,
    "schreiben": render_schreiben,
    "sprechen": render_sprechen,
}


def generate_skill_pdf(level: str, skill: str, output_dir: Path) -> Path:
    """Generate a PDF for one exam skill at a given level."""
    skills = LEVELS[level]
    info = skills[skill]
    pdf = ExamPDF(level, info["name"])

    # Title page
    pdf.add_title_page()

    # Load all exercises once
    renderer = RENDERERS[skill]
    all_exercises = {}
    for part_num in range(1, info["parts"] + 1):
        exercises = load_exercises(level, skill, part_num)
        if exercises:
            all_exercises[part_num] = exercises

    # Exercise pages
    for part_num, exercises in all_exercises.items():
        section_label = f"{info['part_label']} {part_num}"
        pdf.add_section_header(section_label)
        renderer(pdf, exercises, show_answers=False)

    # Answer key section
    pdf.add_section_header("Lösungen / Answer Key")
    for part_num, exercises in all_exercises.items():
        section_label = f"{info['part_label']} {part_num}"
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, section_label)
        pdf.ln(10)
        renderer(pdf, exercises, show_answers=True)

    output_path = output_dir / f"{level}_{skill}.pdf"
    pdf.output(str(output_path))
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate printable PDFs for exam exercises")
    parser.add_argument("--level", choices=list(LEVELS.keys()), default="b1", help="CEFR level")
    parser.add_argument("--output-dir", help="Output directory (default: resources/exams/{level}/pdfs)")
    parser.add_argument("--skill", help="Generate PDF for a single skill only")
    args = parser.parse_args()

    output_dir = Path(args.output_dir) if args.output_dir else Path(f"resources/exams/{args.level}/pdfs")
    output_dir.mkdir(parents=True, exist_ok=True)

    skills_config = LEVELS[args.level]
    skills = [args.skill] if args.skill else list(skills_config.keys())

    for skill in skills:
        path = generate_skill_pdf(args.level, skill, output_dir)
        print(f"[OK] Generated: {path}")

    print(f"\nAll PDFs written to: {output_dir}/")


if __name__ == "__main__":
    main()
