import os
import aiofiles
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)


def create_pdf(data):

    report = data["report"]

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=16,
        spaceBefore=15,
        spaceAfter=10
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10.5,
        leading=16,
        spaceAfter=10
    )

    source_style = ParagraphStyle(
        "Source",
        parent=styles["BodyText"],
        fontSize=8,
        leading=11
    )

    content = []

    # Title
    content.append(
        Paragraph(report["title"], title_style)
    )

    # Introduction
    content.append(
        Paragraph("Introduction", heading_style)
    )

    content.append(
        Paragraph(report["introduction"], body_style)
    )

    # Sections
    for section in report["sections"]:

        content.append(
            Paragraph(section["heading"], heading_style)
        )

        content.append(
            Paragraph(section["content"], body_style)
        )

        if section.get("sources"):

            content.append(
                Paragraph("Sources:", body_style)
            )

            for source in section["sources"]:
                content.append(
                    Paragraph(source, source_style)
                )

            content.append(Spacer(1, 10))

    # Conclusion
    content.append(
        Paragraph("Conclusion", heading_style)
    )

    content.append(
        Paragraph(report["conclusion"], body_style)
    )

    doc.build(content)

    return buffer.getvalue()


async def save_to_disk(file: bytes, path: str) -> bool:

    directory = os.path.dirname(path)

    if directory:
        os.makedirs(directory, exist_ok=True)

    async with aiofiles.open(path, "wb") as out_file:
        await out_file.write(file)

    return True