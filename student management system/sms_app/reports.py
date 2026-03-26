from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


def mark_to_grade(mark: int) -> str:
    """Convert a numeric mark (0-100) to a letter grade.
    
    Grading scale:
    - 75 – 100: A
    - 65 – 74: B
    - 50 – 64: C
    - 40 – 49: D
    - Below 40: F
    """
    if mark >= 75:
        return "A"
    elif mark >= 65:
        return "B"
    elif mark >= 50:
        return "C"
    elif mark >= 40:
        return "D"
    else:
        return "F"


@dataclass(frozen=True)
class ReportData:
    title: str
    lines: list[str]


def build_student_report(*, student_id: str, name: str, program: str, class_name: str | None, marks: list[tuple[str, str, int]]) -> ReportData:
    header = [
        f"Student ID: {student_id}",
        f"Name: {name}",
        f"Program: {program or '-'}",
        f"Class: {class_name or '-'}",
        "",
        "Marks & Grades:",
    ]
    lines = header[:]
    if not marks:
        lines.append("  (no marks)")
    else:
        for subject, term, mark in marks:
            grade = mark_to_grade(mark)
            lines.append(f"  - {term} | {subject}: {mark}% ({grade})")
    return ReportData(title=f"Student Report - {student_id}", lines=lines)


def export_report_to_pdf(report: ReportData, output_path: str | Path) -> None:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.pdfgen import canvas
    except Exception as e:  # pragma: no cover
        raise RuntimeError("reportlab is not installed. Run: pip install reportlab") from e

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4

    y = height - 2 * cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, y, report.title)
    y -= 1.0 * cm

    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, y, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y -= 1.0 * cm

    c.setFont("Helvetica", 11)
    for line in report.lines:
        if y < 2 * cm:
            c.showPage()
            y = height - 2 * cm
            c.setFont("Helvetica", 11)
        c.drawString(2 * cm, y, line)
        y -= 0.6 * cm

    c.save()

