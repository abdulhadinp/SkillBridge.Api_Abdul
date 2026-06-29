#!/usr/bin/env python3
"""
SkillBridge — Unit 22 Assignment Word Document Generator
Generates the complete 8000-word assignment DOCX with all sections,
diagrams embedded, tables, and proper formatting.
Author: Abdul Hadi | ISMT College | University of Sunderland, UK
"""
import os
import sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import docx.opc.constants

DIAGRAMS = os.path.join(os.path.dirname(__file__), "diagrams")
OUTPUT = os.path.join(os.path.dirname(__file__), "Abdul_Hadi_Unit22_Application_Development.docx")

doc = Document()

# ─── PAGE SETUP ──────────────────────────────────────────────────────────────
section = doc.sections[0]
section.page_width  = Inches(8.27)
section.page_height = Inches(11.69)
section.left_margin   = Inches(1)
section.right_margin  = Inches(1)
section.top_margin    = Inches(1)
section.bottom_margin = Inches(1)

# ─── STYLES ──────────────────────────────────────────────────────────────────
styles = doc.styles

def set_style(style_name, font_name='Times New Roman', font_size=12, bold=False, italic=False, color=None):
    try:
        s = styles[style_name]
    except KeyError:
        return
    f = s.font
    f.name = font_name
    f.size = Pt(font_size)
    f.bold = bold
    f.italic = italic
    if color:
        f.color.rgb = RGBColor(*color)

set_style('Normal', font_size=12)
set_style('Heading 1', font_size=16, bold=True, color=(13, 110, 253))
set_style('Heading 2', font_size=14, bold=True, color=(52, 58, 64))
set_style('Heading 3', font_size=12, bold=True, italic=True, color=(73, 80, 87))

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def add_heading(text, level=1):
    p = doc.add_heading(text, level=level)
    p.paragraph_format.space_after = Pt(8)
    for run in p.runs:
        run.font.name = 'Times New Roman'
    return p

def add_para(text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False, size=12, color=None):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = Pt(18)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)
    return p

def add_caption(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)
    run.italic = True
    run.font.color.rgb = RGBColor(100, 100, 100)

def add_diagram(filename, caption, width=5.5):
    path = os.path.join(DIAGRAMS, filename)
    if os.path.exists(path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(path, width=Inches(width))
    else:
        add_para(f'[Diagram: {filename} — not found]', align=WD_ALIGN_PARAGRAPH.CENTER, italic=True)
    add_caption(caption)

def add_table(headers, rows, shading=True):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Header row
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = h
        hdr[i].paragraphs[0].runs[0].font.bold = True
        hdr[i].paragraphs[0].runs[0].font.name = 'Times New Roman'
        hdr[i].paragraphs[0].runs[0].font.size = Pt(10)
        hdr[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        tc = hdr[i]._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), '0d6efd')
        tcPr.append(shd)
        for run in hdr[i].paragraphs[0].runs:
            run.font.color.rgb = RGBColor(255, 255, 255)
    # Data rows
    for ri, row in enumerate(rows):
        cells = table.rows[ri + 1].cells
        for ci, val in enumerate(row):
            cells[ci].text = str(val)
            cells[ci].paragraphs[0].runs[0].font.name = 'Times New Roman'
            cells[ci].paragraphs[0].runs[0].font.size = Pt(9)
            if shading and ri % 2 == 0:
                tc = cells[ci]._tc
                tcPr = tc.get_or_add_tcPr()
                shd = OxmlElement('w:shd')
                shd.set(qn('w:val'), 'clear')
                shd.set(qn('w:color'), 'auto')
                shd.set(qn('w:fill'), 'EBF5FB')
                tcPr.append(shd)
    doc.add_paragraph()
    return table

def add_bullet(text, level=0):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)

def page_break():
    doc.add_page_break()

# ─── HEADER AND FOOTER ───────────────────────────────────────────────────────
def add_header_footer():
    section = doc.sections[0]
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.text = "Unit 22: Application Development | Abdul Hadi | ISMT College"
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in hp.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(100, 100, 100)

    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = fp.add_run()
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.text = 'PAGE'
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)

add_header_footer()

# ═══════════════════════════════════════════════════════════════════════════════
# COVER PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def add_cover():
    # Institution
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("ISMT")
    r.font.name = 'Times New Roman'; r.font.size = Pt(36); r.bold = True
    r.font.color.rgb = RGBColor(13, 110, 253)

    add_para("International School of Management and Technology, Nepal", WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14)
    add_para("Faculty of Computing", WD_ALIGN_PARAGRAPH.CENTER, size=13)
    add_para("Affiliated to University of Sunderland, UK — Level 5", WD_ALIGN_PARAGRAPH.CENTER, size=12, italic=True)

    # Divider
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("─" * 60)
    run.font.color.rgb = RGBColor(13, 110, 253)
    doc.add_paragraph()

    # Title
    add_para("Unit 22: Application Development", WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=18, color=(13, 110, 253))
    add_para("Unit Code: Y/618/7436", WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=12)
    doc.add_paragraph()
    add_para("Assignment Title:", WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14)
    add_para("Elevate Workforce Solutions — SkillBridge Job Portal", WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16)
    doc.add_paragraph()
    doc.add_paragraph()

    # Details table
    table = doc.add_table(rows=9, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'
    details = [
        ("Student Name", "Abdul Hadi"),
        ("Student ID", ""),
        ("College", "ISMT — International School of Management and Technology"),
        ("University", "University of Sunderland, UK"),
        ("Assessor", "Bhuwan Subedi"),
        ("Issue Date", "13 May 2026"),
        ("Submission Date", "15 July 2026"),
        ("Word Count", "~8,200 words"),
        ("Document Format", "Microsoft Word (.docx), Times New Roman 12pt"),
    ]
    for i, (label, val) in enumerate(details):
        row = table.rows[i]
        row.cells[0].text = label
        row.cells[1].text = val
        for ci in range(2):
            run = row.cells[ci].paragraphs[0].runs
            if run:
                run[0].font.name = 'Times New Roman'
                run[0].font.size = Pt(11)
                if ci == 0:
                    run[0].bold = True
        tc = row.cells[0]._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), 'DBEAFE')
        tcPr.append(shd)

    page_break()

add_cover()

# ═══════════════════════════════════════════════════════════════════════════════
# TABLE OF CONTENTS
# ═══════════════════════════════════════════════════════════════════════════════
add_heading("Table of Contents", 1)
toc_entries = [
    ("Activity 1 — Software Design Document", "3"),
    ("  1.1 Introduction", "3"),
    ("  1.2 Problem Definition Statement (P1)", "4"),
    ("  1.3 User Requirements (P1)", "5"),
    ("  1.4 System Requirements (P1)", "6"),
    ("  1.5 Risk Analysis (P2)", "8"),
    ("  1.6 Software Development Tools and Techniques (P3, M2)", "10"),
    ("  1.7 Comparison of Tools and Methodology Justification (M2, D1)", "13"),
    ("  1.8 System Analysis (M1)", "16"),
    ("  1.9 System Design (M1)", "17"),
    ("  1.10 Database Design", "24"),
    ("Activity 2 — Application Development Evidence and Peer Review", "26"),
    ("  2.1 Overview", "26"),
    ("  2.2 Peer Review of Problem Definition (P4)", "26"),
    ("  2.3 Application Development Evidence (P5, M3)", "27"),
    ("  2.4 OOP Principles Implementation (M4)", "30"),
    ("  2.5 Critical Evaluation of Development Approach (D2)", "33"),
    ("Activity 3 — Testing and Evaluation", "35"),
    ("  3.1 Testing Overview", "35"),
    ("  3.2 Test Plan (P6)", "35"),
    ("  3.3 Testing Evidence", "37"),
    ("  3.4 Evaluation and Reflection (M5, D3)", "38"),
    ("References", "40"),
]
for entry, page in toc_entries:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    tab = p.add_run(f"{entry}")
    tab.font.name = 'Times New Roman'; tab.font.size = Pt(11)
    if not entry.startswith("  "):
        tab.bold = True
    dots = p.add_run(f"{'.' * max(1, 60 - len(entry))} {page}")
    dots.font.name = 'Times New Roman'; dots.font.size = Pt(11)
    dots.font.color.rgb = RGBColor(100, 100, 100)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# ACTIVITY 1 — SOFTWARE DESIGN DOCUMENT
# ═══════════════════════════════════════════════════════════════════════════════
add_heading("Activity 1 — Software Design Document", 1)

# 1.1 Introduction
add_heading("1.1 Introduction", 2)
add_para(
    "In this assignment, I have been engaged as a web developer at Code Art Web Technologies, a software consultancy "
    "firm based in Kathmandu, Nepal. My client for this project is Elevate Workforce Solutions, an established "
    "employment agency that facilitates connections between job seekers and employers across Nepal. The agency approached "
    "Code Art Web Technologies with a request to design and develop a modern, web-based job portal that would digitalise "
    "their traditionally manual recruitment operations and position them competitively in the growing online employment market."
)
add_para(
    "The resulting application is named SkillBridge — a job portal designed to serve two primary user groups: "
    "administrators who manage job postings and applications on behalf of Elevate Workforce Solutions, and candidates "
    "who search, apply for, and track the progress of their job applications. SkillBridge is built using ASP.NET Core 8 "
    "(C#) for the backend REST API, with a React + TypeScript frontend, a SQL Server database running within a Docker "
    "container, and Entity Framework Core as the Object-Relational Mapper (ORM). The application strictly follows the "
    "Model-View-Controller (MVC) architectural pattern and demonstrates Object-Oriented Programming (OOP) principles "
    "including Encapsulation, Abstraction, Inheritance, and Polymorphism."
)
add_para(
    "Activity 1 covers the complete Software Design Document (SDD) for SkillBridge. This includes the problem "
    "definition and requirements analysis (P1), a risk register (P2), a research and justification of all tools "
    "and technologies used (P3, M2), a feasibility and system analysis (M1), and a comprehensive set of UML and "
    "data-flow diagrams that illustrate the architecture and design of the system (M1). A critical evaluation of "
    "the chosen tools and methodology is provided at the end of this activity (D1)."
)

# 1.2 Problem Definition
add_heading("1.2 Problem Definition Statement (P1)", 2)
add_heading("Current Situation", 3)
add_para(
    "Elevate Workforce Solutions is a well-established employment agency operating in Kathmandu, Nepal. Since its "
    "founding, the agency has relied entirely upon manual, paper-based, and telephone-based processes to manage its "
    "recruitment operations. Job seekers are required to visit the agency's physical office or make enquiries by "
    "telephone, whilst employers submit their vacancy details by completing paper forms or by sending emails directly "
    "to the agency's inbox. Upon receipt, administrative staff manually match candidates to suitable roles, maintain "
    "spreadsheet-based records of all applications, and communicate status updates verbally or by telephone."
)
add_heading("Business Problem", 3)
add_para(
    "The absence of a centralised digital platform has resulted in a series of interconnected operational challenges "
    "that are increasingly unsustainable. Firstly, geographic limitation means that Elevate Workforce Solutions can "
    "only serve candidates who are physically able to visit the office or who possess the contact details of the "
    "agency, thereby excluding a substantial proportion of Nepal's working population. Secondly, there is no "
    "transparent mechanism for candidates to track the progress of their applications independently; this results "
    "in repeated telephone enquiries and an elevated administrative burden. Thirdly, the manual processing of "
    "application data introduces a significant risk of human error, including the potential for applications being "
    "misfiled, deadlines being missed, or candidate details being incorrectly recorded. Finally, Nepal's employment "
    "market is rapidly evolving, with a growing number of online job portals such as Merojob.com and Kumarijob.com "
    "capturing candidates and employers who prefer the convenience of digital recruitment. Without a comparable "
    "online presence, Elevate Workforce Solutions risks losing market share and institutional relevance."
)
add_heading("Proposed Solution", 3)
add_para(
    "The proposed solution is SkillBridge — a full-stack, web-based job portal application developed using ASP.NET "
    "Core 8 (C#) for the REST API backend, React with TypeScript for the frontend, SQL Server hosted within a Docker "
    "container for the database, and Entity Framework Core for database access. SkillBridge implements the "
    "Model-View-Controller (MVC) architectural pattern, which ensures a clear separation of concerns and facilitates "
    "the maintainability and scalability of the codebase. The application demonstrates four core Object-Oriented "
    "Programming principles — Encapsulation, Abstraction, Inheritance, and Polymorphism — in its class and service "
    "design. SkillBridge will enable Elevate Workforce Solutions to publish and manage job listings digitally, "
    "allow candidates across Nepal to discover and apply for positions online, and provide an automated status "
    "tracking system that eliminates the need for manual follow-up communications."
)
add_heading("Business Goals Aligned to the Solution", 3)
goals = [
    "Digital transformation of manual job listing and application processes.",
    "Equal and transparent access to employment opportunities regardless of geographic location.",
    "Reduction of administrative burden through automated status tracking and role-based dashboards.",
    "Professional online presence that is scalable and can accommodate future feature development.",
    "Improvement of candidate experience through real-time application status visibility.",
]
for g in goals:
    add_bullet(g)
doc.add_paragraph()

# 1.3 User Requirements
add_heading("1.3 User Requirements (P1)", 2)
add_para(
    "The user requirements for SkillBridge were gathered through a simulated consultancy process with the client, "
    "Elevate Workforce Solutions. Requirements are categorised by priority: High (must have for the system to function), "
    "Medium (important but not critical for launch), and Low (desirable future enhancement)."
)
ur_headers = ["ID", "User Requirement", "Priority"]
ur_rows = [
    ("UR-01", "Users must be able to register for an account by providing their full name, email, password, phone number, and qualification.", "High"),
    ("UR-02", "Registered users must be able to log in securely and log out of the system.", "High"),
    ("UR-03", "Job seekers must be able to browse, search, and filter all active job listings on the public landing page without requiring a login.", "High"),
    ("UR-04", "Authenticated candidates must be able to apply for a job by submitting a cover letter and uploading an optional tailored resume.", "High"),
    ("UR-05", "Candidates must be able to track the real-time status of all their submitted applications from a personal dashboard.", "High"),
    ("UR-06", "Admin users must be able to create, update, and delete job postings through a dedicated management interface.", "High"),
    ("UR-07", "Admin users must be able to view all submitted applications and update each application's status through a defined workflow.", "High"),
    ("UR-08", "The system must be accessible and fully functional on mobile, tablet, and desktop screen sizes.", "Medium"),
    ("UR-09", "Candidates must be able to set up and update a personal profile including their skills, education, experience, and resume.", "Medium"),
    ("UR-10", "The system should suggest relevant job listings to candidates based on the skills listed in their profile (AI-powered feature).", "Low"),
]
add_table(ur_headers, ur_rows)

# 1.4 System Requirements
add_heading("1.4 System Requirements (P1)", 2)
add_heading("1.4.1 Functional Requirements", 3)
add_para("Functional requirements define the specific behaviours and functions that the SkillBridge system must perform.")
fr_headers = ["ID", "Functional Requirement", "Description"]
fr_rows = [
    ("FR-01", "Authentication and Authorisation", "The system shall allow users to sign up, sign in, and sign out. Role-based access control shall distinguish between Admin and Candidate roles. JWT tokens shall be used for session management."),
    ("FR-02", "Job Management (Admin)", "The system shall allow Admins to create, read, update, and soft-delete job postings. Each job shall include: title, description, company, location, salary range, deadline, job type, and active status."),
    ("FR-03", "Application Management (Admin)", "The system shall allow Admins to view all submitted applications, filter by job, status, or date range, and update the application status through a defined six-stage workflow."),
    ("FR-04", "Candidate Profile Management", "The system shall allow candidates to create and update a profile containing their full name, experience, skills (comma-separated), education details, and CV/resume upload."),
    ("FR-05", "Public Job Listing", "The system shall display all active job listings on a public landing page with keyword search, category filter, and pagination (10 results per page)."),
    ("FR-06", "Job Application (Candidates)", "The system shall allow authenticated candidates to apply for a job once per posting, submitting a cover letter and optional tailored resume. Duplicate applications shall be prevented."),
    ("FR-07", "Application Tracking", "The system shall display all applications submitted by a candidate on their dashboard, showing the current status with visual colour-coded badges and a progress timeline."),
]
add_table(fr_headers, fr_rows)

add_heading("1.4.2 Non-Functional Requirements", 3)
nfr_headers = ["ID", "Requirement", "Description", "Measurement"]
nfr_rows = [
    ("NFR-01", "Responsive Design", "The application shall adapt to mobile (375px+), tablet (768px+), and desktop (1024px+) screen widths.", "Tailwind CSS breakpoints; tested on multiple viewports"),
    ("NFR-02", "Accessibility", "The application shall conform to WCAG 2.1 Level AA guidelines where feasible.", "Semantic HTML, alt text on images, colour contrast ratio >= 4.5:1"),
    ("NFR-03", "Security", "Passwords shall be hashed using BCrypt. All authenticated routes shall be protected. Input fields shall be validated server-side.", "BCrypt hash rounds = 10; ModelState validation; JWT expiry = 60 min"),
    ("NFR-04", "Data Privacy", "User personal data shall only be accessible to authorised roles. Passwords shall never be stored in plain text.", "Role-based [Authorize] attributes on all sensitive controllers"),
    ("NFR-05", "Performance", "Page load times shall not exceed three seconds under normal load.", "Measured using browser developer tools network tab"),
    ("NFR-06", "Scalability", "The database shall run in a Docker container enabling straightforward deployment to any cloud provider.", "Docker Compose configuration; environment-variable-based connection strings"),
    ("NFR-07", "Reliability", "The system shall handle invalid inputs gracefully and display appropriate error messages rather than crashing.", "Try-catch blocks; ModelState validation; custom error responses"),
]
add_table(nfr_headers, nfr_rows)

# 1.5 Risk Analysis
add_heading("1.5 Risk Analysis (P2)", 2)
add_para(
    "Risk analysis is a critical activity in software development that enables the development team to proactively "
    "identify, assess, and mitigate potential threats before they materialise into project failures. According to "
    "Sommerville (2016), risk management in software engineering involves identifying risks early, analysing their "
    "probability and impact, and putting contingency measures in place. For SkillBridge, seven key risks were "
    "identified and documented in the risk register below."
)
risk_headers = ["Risk ID", "Risk Description", "Likelihood", "Impact", "Risk Level", "Mitigation Strategy"]
risk_rows = [
    ("R-01", "Data security breach — unauthorised access to user credentials or personal data.", "Medium", "High", "High", "Passwords hashed with BCrypt (10 rounds); HTTPS enforced; JWT token expiry; server-side input validation prevents SQL injection."),
    ("R-02", "Database failure or data loss — SQL Server container crash or data corruption.", "Low", "High", "High", "Docker volume persistence configured (sql-data volume); regular .sql backup dumps during development; EF Core migrations tracked in version control."),
    ("R-03", "Scope creep — feature requests expanding beyond the agreed timeline.", "Medium", "Medium", "Medium", "Agile sprint planning with Trello; strict sprint backlog; features beyond MVP deferred to future releases as documented in the product backlog."),
    ("R-04", "Technology compatibility issues — .NET version conflicts or library deprecations.", "Low", "Medium", "Low", ".NET 10 LTS selected; Docker isolates the environment from host OS; NuGet package versions pinned in .csproj file."),
    ("R-05", "Poor UI/UX leading to low user adoption by candidates.", "Medium", "Medium", "Medium", "Tailwind CSS used for consistent responsive design; peer review session conducted; iterative UI improvements based on feedback."),
    ("R-06", "Single-developer knowledge risk — all knowledge held by one person.", "Low", "High", "Medium", "Comprehensive code comments; GitHub version control with commit history; this assignment document serves as technical documentation."),
    ("R-07", "File upload vulnerabilities — malicious file uploads to the server.", "Medium", "High", "High", "File type validation (PDF only enforced on client and server); file size limit; uploaded files stored in wwwroot/uploads outside main application logic."),
]
add_table(risk_headers, risk_rows)

# 1.6 Software Tools Research
add_heading("1.6 Software Development Tools and Techniques Research (P3, M2)", 2)
add_para(
    "This section analyses each tool and technology used in the development of SkillBridge. For each tool, I provide "
    "not only a description but also a critical analysis of why it was selected, its advantages, and any limitations "
    "encountered during development."
)

add_heading("1.6.1 Programming Language — C# and ASP.NET Core 8", 3)
add_para(
    "C# (C-Sharp) is a modern, statically typed, general-purpose object-oriented programming language developed by "
    "Microsoft. It was first introduced in 2000 and has since evolved into one of the most widely adopted languages "
    "for enterprise application development. ASP.NET Core 8 is Microsoft's cross-platform, open-source web framework "
    "built on top of C#. It supports the development of RESTful APIs, web applications, and microservices, and runs "
    "on Windows, macOS, and Linux operating systems (Microsoft, 2024a)."
)
add_para(
    "For the SkillBridge backend, ASP.NET Core 8 was selected primarily because of its built-in dependency injection "
    "container, which facilitates the implementation of OOP design patterns such as Abstraction and Polymorphism "
    "through interface registration. The framework's strongly typed model binding eliminates an entire class of "
    "runtime errors that are common in dynamically typed languages such as Python. Additionally, ASP.NET Core's "
    "attribute-based routing (e.g., [HttpGet], [Authorize(Roles = \"Admin\")]) provides a clean, declarative "
    "mechanism for role-based access control without requiring complex middleware configuration. The Scalar OpenAPI "
    "integration enabled rapid API testing during development, significantly reducing the time spent on manual "
    "HTTP request construction."
)

add_heading("1.6.2 Database Management — SQL Server with Docker", 3)
add_para(
    "SQL Server (specifically the Azure SQL Edge image, which is ARM64/x86 compatible) is a fully featured "
    "relational database management system (RDBMS) developed by Microsoft. Docker is an open-source containerisation "
    "platform that packages applications and their dependencies into isolated, lightweight containers (Docker, 2024). "
    "In SkillBridge, the SQL Server instance runs within a Docker container defined in docker-compose.yml, ensuring "
    "environment consistency between development machines."
)
add_para(
    "The containerisation approach eliminates the notorious 'it works on my machine' problem — any developer who "
    "clones the repository can bring up an identical database environment by running docker-compose up -d. The "
    "docker-compose.yml defines the SQL Server service with a named volume (sql-data) to persist data between "
    "container restarts. SQL Server was selected over MySQL primarily because the existing codebase and all EF Core "
    "migrations had already been written for SQL Server, and switching databases mid-project would have required "
    "rewriting all migration files — a significant and unnecessary risk given the project timeline."
)

add_heading("1.6.3 Object-Relational Mapper — Entity Framework Core", 3)
add_para(
    "Entity Framework Core (EF Core) is Microsoft's official, open-source Object-Relational Mapper (ORM) for .NET. "
    "It enables developers to interact with the database using .NET objects rather than writing raw SQL queries, "
    "significantly reducing boilerplate data-access code (Microsoft, 2024b). SkillBridge uses EF Core's Code-First "
    "approach, whereby the database schema is derived from C# entity class definitions (User, Job, JobApplication, "
    "CandidateProfile) and migrations are generated and applied using the dotnet ef migrations add and "
    "dotnet ef database update commands."
)
add_para(
    "The Fluent API in OnModelCreating was used to configure all entity relationships, including the one-to-one "
    "relationship between User and CandidateProfile and the cascade delete behaviour on JobApplications. "
    "One limitation of EF Core that became apparent during development is that complex queries involving multiple "
    "joins can generate inefficient SQL, particularly with navigation properties. In such cases, it is preferable "
    "to use projection (Select) to retrieve only the required columns rather than loading entire entity graphs."
)

add_heading("1.6.4 Version Control — Git and GitHub", 3)
add_para(
    "Git is a distributed version control system that tracks changes to files over time, enabling multiple developers "
    "to collaborate on a codebase concurrently (Chacon and Straub, 2014). GitHub is a cloud-based hosting service "
    "for Git repositories that provides additional collaboration features such as pull requests, issue tracking, "
    "and branch protection rules. For SkillBridge, a branching strategy was implemented with five feature branches "
    "(feature/authentication, feature/job-management, feature/candidate-features, feature/admin-panel, "
    "feature/ui-enhancement), a develop branch for integration, and a main branch representing the production-ready "
    "codebase. Semantic commit messages following the Conventional Commits specification were used throughout "
    "(e.g., feat:, fix:, docs:). The repository was tagged with v1.0.0 at the point of submission."
)

add_heading("1.6.5 Development Environment — VS Code with C# DevKit", 3)
add_para(
    "Visual Studio Code (VS Code) is a lightweight, cross-platform, open-source code editor developed by Microsoft. "
    "The C# DevKit extension provides IntelliSense (code auto-completion), syntax highlighting, integrated debugging, "
    "and EF Core migration tooling within the editor. This combination provides a productive development environment "
    "without the resource overhead of the full Visual Studio IDE. The REST Client extension was used for API testing "
    "alongside the Scalar OpenAPI interface that is automatically generated by ASP.NET Core in development mode."
)

add_heading("1.6.6 Project Management — Agile Methodology with Trello", 3)
add_para(
    "The development of SkillBridge followed the Agile software development methodology. Agile is an iterative, "
    "incremental approach to software development in which requirements and solutions evolve through the collaborative "
    "effort of cross-functional teams (Beck et al., 2001). The Agile Manifesto emphasises individuals and interactions "
    "over processes and tools, working software over comprehensive documentation, customer collaboration over contract "
    "negotiation, and responding to change over following a plan."
)
add_para(
    "The project was organised into five two-week sprints. Trello was used as the Kanban board tool to manage "
    "the sprint backlog, work-in-progress, and completed items. Each sprint had a defined goal: Sprint 1 covered "
    "project initialisation and database setup; Sprint 2 implemented the authentication system; Sprint 3 delivered "
    "job management functionality; Sprint 4 completed candidate features; and Sprint 5 focused on the admin panel, "
    "AI recommendations, and UI polish. User stories were written in the format 'As a [role], I want to [action] "
    "so that [benefit]' and linked to specific functional requirements."
)

# 1.7 Comparison
add_heading("1.7 Comparison of Tools and Methodology Justification (M2, D1)", 2)

add_heading("1.7.1 Programming Framework Comparison", 3)
fw_headers = ["Criterion", "ASP.NET Core (C#)", "Django (Python)", "Node.js (Express)", "Spring Boot (Java)"]
fw_rows = [
    ("Language", "C#", "Python", "JavaScript", "Java"),
    ("Architecture", "MVC, REST API", "MVT (Model-View-Template)", "Non-opinionated", "MVC, REST API"),
    ("Performance", "High (compiled)", "Medium (interpreted)", "High (async I/O)", "High (JVM)"),
    ("ORM Support", "Entity Framework Core", "Django ORM", "Sequelize / Prisma", "Hibernate / JPA"),
    ("Learning Curve", "Medium", "Low", "Low–Medium", "High"),
    ("Deployment", "Cross-platform (Docker)", "Cross-platform (Docker)", "Cross-platform (Docker)", "Cross-platform (Docker)"),
    ("Type Safety", "Strong (static typing)", "Dynamic (optional type hints)", "Dynamic (TypeScript adds types)", "Strong (static typing)"),
    ("Community", "Large (.NET ecosystem)", "Very Large", "Very Large (npm)", "Large (enterprise-heavy)"),
]
add_table(fw_headers, fw_rows)
add_para(
    "ASP.NET Core was selected over the alternatives for several compelling reasons. Its static type system, "
    "enforced through C#, catches a significantly higher proportion of errors at compile time rather than at "
    "runtime — a critical advantage in a backend API where data integrity is paramount. The built-in dependency "
    "injection container natively supports the interface-based design that is central to the OOP requirements "
    "of this assignment. Entity Framework Core's Code-First migrations provide a superior developer experience "
    "compared to Django's migration system when the database schema changes frequently during iterative development. "
    "Furthermore, as the existing codebase was already written in C# with ASP.NET Core, refactoring it to use a "
    "different framework would have introduced unacceptable technical risk without corresponding benefit."
)

add_heading("1.7.2 Database Comparison", 3)
db_headers = ["Criterion", "SQL Server", "PostgreSQL", "MySQL", "SQLite"]
db_rows = [
    ("Cost", "Free (Express / Developer edition)", "Free / Open Source", "Free / Open Source", "Free"),
    ("Performance", "Excellent", "Excellent", "Good", "Limited to single file"),
    ("Docker Support", "Excellent (official image)", "Excellent", "Excellent", "N/A — file-based"),
    ("EF Core Support", "Full native support", "Full support", "Full support", "Full support"),
    ("Windows Integration", "Excellent (native)", "Good", "Good", "Good"),
    ("JSON Support", "Good (JSON functions)", "Excellent (JSONB)", "Good", "Limited"),
]
add_table(db_headers, db_rows)
add_para(
    "SQL Server was retained as the database of choice because all existing EF Core migrations had already been "
    "generated and tested against it. Switching to an alternative RDBMS such as MySQL or PostgreSQL at this "
    "stage of development would have necessitated deleting and regenerating all six migration files, with "
    "attendant risk of data loss and significant time cost. SQL Server's performance characteristics are "
    "entirely adequate for the scale of SkillBridge, and its deep integration with EF Core and the .NET "
    "ecosystem ensures that all advanced features, including connection resiliency and query tagging, "
    "function correctly."
)

add_heading("1.7.3 Development Methodology Comparison", 3)
meth_headers = ["Criterion", "Waterfall", "Agile / Scrum", "RAD", "Spiral"]
meth_rows = [
    ("Flexibility", "Rigid — changes are costly", "Highly Flexible", "Flexible — fast prototyping", "Moderate"),
    ("Client Involvement", "Low — primarily at start and end", "High — continuous collaboration", "High", "Medium"),
    ("Suitable for Small Teams", "No — heavyweight process", "Yes — designed for small teams", "Yes", "No — overhead-heavy"),
    ("Risk Management", "Low — risks surface late", "Continuous — sprints enable early risk detection", "Low", "High — explicit risk analysis"),
    ("Documentation", "Heavy upfront documentation", "Lightweight — just enough", "Minimal", "Moderate"),
    ("Timeline Predictability", "High (if requirements are stable)", "Medium (scope adapts)", "Low", "Medium"),
]
add_table(meth_headers, meth_rows)
add_para(
    "Agile was selected as the development methodology for SkillBridge for three primary reasons. Firstly, "
    "as a solo developer, the overhead of Waterfall's extensive upfront documentation and rigid phase-gate "
    "reviews would have consumed time that was better spent on coding and testing. Secondly, the requirements "
    "for SkillBridge evolved significantly during development — for example, the decision to add AI-powered job "
    "recommendations was taken after the initial sprint planning session, which would have required a formal "
    "change request under Waterfall. Agile accommodated this addition seamlessly within Sprint 5. Thirdly, "
    "the iterative nature of Agile's sprint structure enabled continuous delivery of working software, meaning "
    "that key features such as authentication and job listing were functional and testable within the first "
    "two sprints, providing early validation of the technical approach."
)

add_heading("1.7.4 Evaluation of Solution and Methodology (D1)", 3)
add_para(
    "Critically evaluating the choices made during this project, ASP.NET Core MVC was ultimately the right "
    "framework selection for SkillBridge. The static typing system of C# proved invaluable during refactoring "
    "— when entity class names were changed (e.g., Userprofile was renamed to CandidateProfile), the compiler "
    "immediately flagged all affected code locations, preventing subtle runtime bugs that would have been far "
    "harder to diagnose in a dynamically typed language. However, one limitation that became apparent is that "
    "the framework's learning curve is steeper than Python/Django for developers who are not already familiar "
    "with the .NET ecosystem. This added non-trivial setup time at the project's outset."
)
add_para(
    "In retrospect, the decision to use SQL Server via the Azure SQL Edge Docker image was pragmatic given "
    "the existing codebase, but it introduced an unnecessary dependency on a proprietary database product. "
    "Had the project been designed from scratch with a database-agnostic approach in mind, PostgreSQL would "
    "have been the preferred choice due to its superior JSON support, fully open-source licence, and broader "
    "cloud deployment options. Entity Framework Core's database-provider abstraction would have made such a "
    "migration relatively straightforward at the outset."
)
add_para(
    "The Agile methodology proved highly effective for this project's scope and team size. The five-sprint "
    "structure maintained consistent forward momentum and prevented the paralysis-by-analysis that can afflict "
    "Waterfall projects when requirements are poorly defined. However, one area where Agile's lightweight "
    "documentation approach created challenges was in the retrospective writing of this design document — "
    "had more detailed sprint retrospective notes been maintained in real time, the documentation phase "
    "would have been significantly more efficient. This reflects a genuine tension between Agile's 'working "
    "software over comprehensive documentation' principle and the academic requirement for extensive written "
    "evidence. In future projects, I would maintain a living technical log alongside the Trello board to "
    "bridge this gap."
)

# 1.8 System Analysis
add_heading("1.8 System Analysis (M1)", 2)
add_heading("1.8.1 Feasibility Study", 3)
add_para(
    "Before committing to the design of SkillBridge, a three-dimensional feasibility study was conducted to "
    "assess whether the proposed system was viable across technical, economic, and operational dimensions."
)
add_para(
    "Technical Feasibility: The chosen technology stack — ASP.NET Core 8, Entity Framework Core, SQL Server, "
    "Docker, and React — are all mature, well-documented, and actively maintained technologies with extensive "
    "community support. All required tools are freely available for development use, and the development "
    "environment (VS Code on macOS) supports all required toolchains without modification. The .NET SDK "
    "provides the dotnet ef CLI tool for database migrations, and Docker Desktop provides a simple graphical "
    "interface for container management. The technical team (comprising the student developer) had sufficient "
    "prior experience with C# and web development to execute the project within the allotted time frame."
)
add_para(
    "Economic Feasibility: All tools and technologies used in SkillBridge are either free, open-source, or "
    "available under free developer licences. ASP.NET Core is fully open-source under the MIT licence. SQL "
    "Server's Developer Edition is free for non-production use. Docker Desktop is free for individual "
    "developers. The React and TypeScript ecosystem is entirely open-source. The total cost of development "
    "tools is therefore zero, with ongoing hosting costs dependent on the deployment target (a cloud-hosted "
    "Docker deployment on Azure or DigitalOcean would cost approximately USD 10–20 per month for a small "
    "production instance)."
)
add_para(
    "Operational Feasibility: SkillBridge is a web-based application accessible from any modern browser, "
    "requiring no software installation on the end user's device. The role-based access control system "
    "ensures that administrative functions are restricted to authorised staff, reducing the risk of "
    "accidental data modification by candidates. The application's responsive design means it functions "
    "correctly on smartphones, tablets, and desktop computers — critical for a user base that includes "
    "both young, tech-savvy job seekers and less technically experienced administrative staff."
)

add_heading("1.8.2 Stakeholder Analysis", 3)
add_para("Three primary stakeholder groups were identified for SkillBridge:")
stakeholders = [
    ("Admin / Employer Representative",
     "Staff at Elevate Workforce Solutions responsible for posting jobs, reviewing applications, and updating statuses. "
     "Their primary concern is efficiency — they need a system that reduces administrative overhead and provides a clear "
     "overview of all outstanding applications. The admin dashboard with its statistics cards and filterable applications "
     "table directly addresses this concern."),
    ("Candidate / Job Seeker",
     "Individuals seeking employment who wish to browse jobs, submit applications, and track their progress without "
     "needing to contact the agency by telephone. Candidates require a system that is intuitive, provides clear "
     "feedback on application status, and is accessible from mobile devices."),
    ("System Administrator",
     "The technical user responsible for deploying and maintaining the application and its Docker infrastructure. "
     "Their needs are met by the use of environment-variable-based configuration (appsettings.json and "
     "appsettings.Development.json), Docker Compose for environment management, and EF Core auto-migration on startup."),
]
for name, desc in stakeholders:
    add_para(f"• {name}: {desc}")

# 1.9 System Design
add_heading("1.9 System Design (M1)", 2)

add_heading("1.9.1 System Architecture", 3)
add_diagram("01_system_design.png", "Figure 1 — SkillBridge System Architecture Diagram")
add_para(
    "The SkillBridge system is built on a three-tier architecture. The Presentation Tier consists of the "
    "React + TypeScript frontend, which communicates with the backend through HTTP/HTTPS requests using the "
    "Axios library. The Business Logic Tier is implemented in the ASP.NET Core 8 REST API, which contains "
    "all application logic within Controller and Repository classes. The Data Tier consists of the SQL Server "
    "database running in a Docker container, accessed exclusively through Entity Framework Core. An AI "
    "Recommendation Service (keyword matching against candidate skills) resides within the application "
    "tier, returning personalised job recommendations without requiring an external ML service. This clean "
    "separation of tiers facilitates independent scaling and maintenance of each layer."
)

add_heading("1.9.2 MVC Architecture", 3)
add_diagram("10_mvc_architecture.png", "Figure 2 — MVC Architecture Diagram for SkillBridge")
add_para(
    "SkillBridge strictly follows the MVC pattern. The Model layer (left) contains all entity classes "
    "(User, Job, JobApplication, CandidateProfile) and their corresponding Data Transfer Objects (DTOs), "
    "as well as the SkillBridgeDbContext and service interfaces. The Controller layer (centre) contains "
    "five controllers: UserController (authentication), JobController (job listing and management), "
    "ApplicationController (apply, track, recommendations), AdminController (dashboard stats), and "
    "the legacy WeatherForecastController. No business logic resides in controllers — all logic is "
    "delegated to repository classes. The View layer (right) is implemented as a separate React "
    "frontend application, which consumes the REST API endpoints. Each page component corresponds to "
    "a logical view: LandingPage (public job listing), LoginPage/Register (auth), "
    "AdminDashboard/AdminApplications (admin views), CandidateDashboard/TrackApplications/CandidateProfile "
    "(candidate views), and JobDetail/ApplyJob (job interaction views). The request lifecycle flows: "
    "Browser → HTTP Request → Controller → Repository (EF Core) → SQL Server → Repository → Controller "
    "→ JSON Response → React Component."
)

add_heading("1.9.3 Use Case Diagram", 3)
add_diagram("02_use_case.png", "Figure 3 — UML Use Case Diagram")
add_para(
    "The UML Use Case Diagram illustrates the interactions between the three system actors and the "
    "SkillBridge job portal. The Admin actor has seven primary use cases: signing in, creating, updating "
    "and deleting job postings, viewing all applications, updating application statuses, and generating "
    "reports. The Candidate actor has six use cases: signing in, setting up their profile, viewing and "
    "searching job listings, applying for a job, tracking their application status, and viewing AI "
    "job recommendations. The AI Agent actor is connected to the 'Recommend Jobs' use case, which is "
    "triggered by the candidate's request for personalised recommendations. Two key UML relationships "
    "are shown: 'Apply for a Job' <<includes>> 'Sign In', meaning that authentication is a mandatory "
    "precondition for applying; and 'View AI Job Recommendations' <<extends>> 'View and Search Job "
    "Listings', meaning that recommendations are an optional extension of the browsing experience."
)

add_heading("1.9.4 Flowchart", 3)
add_diagram("03_flowchart.png", "Figure 4 — Application Flowchart")
add_para(
    "The application flowchart illustrates the top-level decision logic from system entry to completion. "
    "Following sign-in, the system evaluates the user's role. Admin users follow the left branch: CRUD "
    "job postings, view and filter applications, update application status, and generate reports. "
    "Candidate users follow the right branch: set up their profile, browse and filter jobs, receive "
    "AI-powered recommendations, apply for positions, and track application progress on their dashboard."
)

add_heading("1.9.5 Activity Diagram", 3)
add_diagram("04_activity_diagram.png", "Figure 5 — UML Activity Diagram (Job Application Process)")
add_para(
    "The UML Activity Diagram depicts the job application process as a swimlane diagram with three "
    "lanes: Candidate, System (SkillBridge), and Admin. The flow begins with the Candidate browsing "
    "the public job listing, the System displaying active jobs with search and filter options, the "
    "Candidate selecting a job, and the System checking whether the candidate is authenticated. If "
    "not authenticated, the System redirects to the login page. Once authenticated, the Candidate "
    "fills in their cover letter and uploads an optional resume. The System validates and stores the "
    "application with a default status of 'Applied', then triggers a dashboard notification for the "
    "Admin. The Admin reviews the application and updates its status. The System persists the status "
    "change. The Candidate can then view the updated status on their dashboard."
)

add_heading("1.9.6 State Diagram", 3)
add_diagram("05_state_diagram.png", "Figure 6 — UML State Diagram (Application Status Lifecycle)")
add_para(
    "The UML State Diagram illustrates the lifecycle of a job application's status from initial "
    "submission to final outcome. The initial state (filled circle) transitions to 'Applied' when "
    "a candidate submits an application. From 'Applied', an Admin can move the application to "
    "'Under Review' by opening it for assessment. From 'Under Review', the Admin may either "
    "'Shortlist' the candidate (if they meet the criteria) or 'Reject' them. From 'Shortlisted', "
    "the Admin can schedule an 'Interview'. Following the interview, the application transitions "
    "to either 'Hired' or 'Rejected'. Both 'Hired' and 'Rejected' are terminal states, represented "
    "by the final state symbol (double circle). These six states are implemented in the "
    "ApplicationRepository.UpdateApplicationStatusAsync method, which validates the new status "
    "against this defined set before persisting the change."
)

add_heading("1.9.7 Entity-Relationship (E-R) Diagram", 3)
add_diagram("06_er_diagram.png", "Figure 7 — Entity-Relationship Diagram")
add_para(
    "The ER Diagram depicts the four database entities and their relationships. The User entity "
    "holds authentication and identification data, including the hashed password and role. The "
    "Job entity contains all vacancy details and includes a foreign key (PostedById) referencing "
    "the User who created the posting — a one-to-many relationship (one Admin can post many Jobs). "
    "The CandidateProfile entity stores professional profile data for job seekers and maintains "
    "a one-to-one relationship with User via the UserId foreign key. The Application entity "
    "represents a submission by a Candidate for a specific Job, with foreign keys to both Job "
    "(JobId) and User (UserId), establishing a many-to-many relationship between candidates and "
    "jobs mediated by this junction entity. Referential integrity is enforced through DELETE "
    "RESTRICT constraints configured in EF Core's Fluent API."
)

add_heading("1.9.8 Data Flow Diagram — Level 0 (Context Diagram)", 3)
add_diagram("07_dfd_level0.png", "Figure 8 — DFD Level 0 (Context Diagram)")
add_para(
    "The Context Diagram presents SkillBridge at the highest level of abstraction, showing the "
    "entire system as a single process (0.0 SkillBridge System) surrounded by two external entities "
    "(Admin and Candidate) and one data store (MySQL/SQL Server Database). The Admin sends job data, "
    "status decisions, and login credentials to the system; the system returns application lists, "
    "management confirmations, and reports to the Admin. The Candidate sends registration data, "
    "profile information, application data, and login credentials; the system returns job listings, "
    "application status updates, and AI-powered recommendations."
)

add_heading("1.9.9 Data Flow Diagram — Level 1", 3)
add_diagram("08_dfd_level1.png", "Figure 9 — DFD Level 1")
add_para(
    "The Level 1 DFD decomposes the central SkillBridge system into five sub-processes, each "
    "corresponding to a major functional area. Process 1.0 (Authentication) handles user "
    "registration, login, and JWT token generation, reading and writing to the Users data store (D1). "
    "Process 2.0 (Job Management) implements Admin CRUD operations on job postings, accessing the "
    "Jobs data store (D2). Process 3.0 (Application Management) handles candidate submissions and "
    "Admin status updates, reading from both the Jobs and Users stores whilst writing to the "
    "Applications store (D3). Process 4.0 (Profile Management) allows candidates to create and "
    "update their professional profiles, accessing the CandidateProfiles store (D4). Process 5.0 "
    "(Reporting) aggregates data from all stores to generate the Admin dashboard statistics and "
    "any application report functionality."
)

add_heading("1.9.10 UML Class Diagram", 3)
add_diagram("09_class_diagram.png", "Figure 10 — UML Class Diagram")
add_para(
    "The UML Class Diagram illustrates the full class hierarchy of SkillBridge. BaseEntity is an "
    "abstract class (shown with the «abstract» stereotype) that provides the common audit fields "
    "(Id, CreatedAt, IsActive) inherited by all four entity classes: User, Job, CandidateProfile, "
    "and JobApplication. This demonstrates the OOP principle of Inheritance — code shared across "
    "all entities is written once in BaseEntity and reused through the inheritance relationship, "
    "adhering to the DRY (Don't Repeat Yourself) principle."
)
add_para(
    "The User class extends BaseEntity and adds authentication-specific properties and methods. "
    "The Candidate class conceptually extends User with profile management and application methods; "
    "the Admin class extends User with job management and reporting methods. In the actual "
    "implementation, Candidate and Admin are differentiated through the Role field and role-specific "
    "API endpoints rather than through separate class inheritance, as this is more appropriate for "
    "a database-backed user model. Two service interfaces are shown: IJobRepository (implementing "
    "the Repository pattern for job data access) and IApplicationRepository (for application "
    "management). Their concrete implementations (JobRepository and ApplicationRepository) are "
    "connected by dashed implementation arrows, demonstrating interface-based Polymorphism. "
    "Encapsulation is demonstrated throughout through the use of public properties with getters "
    "and setters, whilst internal logic (such as the GetCompletionPercentage method on "
    "CandidateProfile) is appropriately encapsulated within its owning class."
)

add_heading("1.9.11 Trello Board — Agile Sprint Planning", 3)
add_diagram("11_trello_board.png", "Figure 11 — SkillBridge Trello Board (Agile Kanban)")
add_para(
    "The Trello Kanban board illustrates the project management approach used for SkillBridge. "
    "Seven columns represent the stages of the development workflow: Backlog (initial feature "
    "ideas), Sprint 1 through Sprint 5 (two-week development iterations), and Done (completed "
    "items). Each card represents a user story or technical task, colour-coded by priority "
    "(red = high, yellow = medium, green = done/low). This board served as the single source "
    "of truth for sprint planning, daily task selection, and progress tracking throughout "
    "the project."
)

# 1.10 Database Design
add_heading("1.10 Database Design", 2)
add_heading("1.10.1 Table Definitions", 3)

for tbl_name, cols in [
    ("Users", [
        ("Id", "INT", "Primary Key, Identity(1,1)", "Unique identifier for each user"),
        ("FullName", "NVARCHAR(250)", "NOT NULL", "Full display name of the user"),
        ("Email", "NVARCHAR(MAX)", "NOT NULL, Unique", "User's email address, used for login"),
        ("PasswordHash", "NVARCHAR(MAX)", "NOT NULL", "BCrypt-hashed password (never stored in plaintext)"),
        ("Role", "NVARCHAR(50)", "DEFAULT 'Candidate'", "User role: 'Admin' or 'Candidate'"),
        ("IsActive", "BIT", "DEFAULT 1", "Soft-delete flag: 0 = deactivated account"),
        ("CreatedAt", "DATETIME2", "NOT NULL", "UTC timestamp of account creation"),
    ]),
    ("Jobs", [
        ("Id", "INT", "Primary Key, Identity(1,1)", "Unique identifier for each job posting"),
        ("Title", "NVARCHAR(600)", "NOT NULL", "Job title (e.g., 'Senior .NET Developer')"),
        ("Description", "NVARCHAR(MAX)", "NULL", "Full job description text"),
        ("Company", "NVARCHAR(MAX)", "NULL", "Employer's company name"),
        ("Location", "NVARCHAR(MAX)", "NULL", "Job location (city / remote)"),
        ("JobType", "NVARCHAR(MAX)", "NULL", "Category: IT, Accounting, Teaching, Management, Other"),
        ("MinSalary", "DECIMAL(18,2)", "NULL", "Minimum monthly salary in NPR"),
        ("MaxSalary", "DECIMAL(18,2)", "NULL", "Maximum monthly salary in NPR"),
        ("PostedDate", "DATETIME2", "NOT NULL", "UTC timestamp when job was posted"),
        ("DeadLineDate", "DATETIME2", "NOT NULL", "Application closing date"),
        ("IsActive", "BIT", "DEFAULT 1", "Soft-delete flag: 0 = job removed from public listing"),
        ("PostedById", "INT", "Foreign Key → Users.Id", "ID of the Admin user who created the posting"),
        ("CreatedAt", "DATETIME2", "NOT NULL", "UTC timestamp of record creation"),
    ]),
    ("CandidateProfiles (Userprofiles)", [
        ("Id", "INT", "Primary Key, Identity(1,1)", "Unique profile identifier"),
        ("UserId", "INT", "Foreign Key → Users.Id, UNIQUE", "One-to-one link to the User entity"),
        ("FullName", "NVARCHAR(500)", "NULL", "Candidate's display name on profile"),
        ("Email", "NVARCHAR(MAX)", "NULL", "Contact email for the profile"),
        ("PhoneNumber", "NVARCHAR(50)", "NULL", "Contact telephone number"),
        ("Experience", "NVARCHAR(MAX)", "NULL", "Professional experience summary"),
        ("Skills", "NVARCHAR(MAX)", "NULL", "Comma-separated skills list (used for AI recommendations)"),
        ("Education", "NVARCHAR(MAX)", "NULL", "Educational background details"),
        ("ResumePath", "NVARCHAR(500)", "NULL", "Relative path to uploaded CV/resume PDF file"),
        ("Summary", "NVARCHAR(MAX)", "NULL", "Professional bio / executive summary"),
        ("IsActive", "BIT", "DEFAULT 1", "Profile active flag"),
        ("CreatedAt", "DATETIME2", "NOT NULL", "UTC timestamp of profile creation"),
    ]),
    ("JobApplications", [
        ("Id", "INT", "Primary Key, Identity(1,1)", "Unique application identifier"),
        ("AppliedJobId", "INT", "Foreign Key → Jobs.Id", "Reference to the job being applied for"),
        ("ApplicantId", "INT", "Foreign Key → Users.Id", "Reference to the applying Candidate"),
        ("Status", "NVARCHAR(100)", "DEFAULT 'Applied'", "Current application status in the workflow"),
        ("AppliedAt", "DATETIME2", "NOT NULL", "UTC timestamp of application submission"),
        ("CoverLetter", "NVARCHAR(MAX)", "NULL", "Cover letter text submitted by the candidate"),
        ("ResumePath", "NVARCHAR(500)", "NULL", "Path to uploaded tailored resume PDF"),
        ("TailoredResumePath", "NVARCHAR(500)", "NULL", "Alias for ResumePath (backward compatibility)"),
        ("IsActive", "BIT", "DEFAULT 1", "Soft-delete flag for cancelled applications"),
        ("CreatedAt", "DATETIME2", "NOT NULL", "UTC timestamp of record creation"),
    ]),
]:
    add_para(f"Table: {tbl_name}", bold=True, size=11)
    add_table(["Column", "Data Type", "Constraints", "Description"], cols)

add_heading("1.10.2 Database Relationships", 3)
add_para(
    "The four tables in the SkillBridge database are connected through three foreign key relationships. "
    "Users (1) → Jobs (N): One Admin user may post many job listings; each job belongs to exactly one "
    "posting user. This relationship is enforced by the PostedById foreign key with a DELETE RESTRICT "
    "rule (deleting an admin user will not cascade-delete their job postings). Users (1) ↔ CandidateProfiles "
    "(0..1): A one-to-one relationship wherein each candidate may have at most one profile; the UserId column "
    "on CandidateProfiles is both a foreign key and carries a UNIQUE constraint, enforced by the Fluent API "
    "HasOne/WithOne configuration. Jobs (1) → JobApplications (N) and Users (1) → JobApplications (N): "
    "A single job may receive many applications; a single candidate may submit many applications (but only one "
    "per job posting, enforced at the application layer). DELETE RESTRICT is applied to both foreign keys to "
    "prevent orphaned application records."
)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# ACTIVITY 2 — APPLICATION DEVELOPMENT EVIDENCE AND PEER REVIEW
# ═══════════════════════════════════════════════════════════════════════════════
add_heading("Activity 2 — Application Development Evidence and Peer Review", 1)

add_heading("2.1 Overview", 2)
add_para(
    "Activity 2 presents the practical development evidence for SkillBridge, including a formal peer review "
    "session that evaluated the problem definition, proposed solution, and development strategy. This activity "
    "documents the key implementation decisions made during development, demonstrates how OOP principles are "
    "concretely realised in the codebase, and provides a retrospective critical evaluation of the development "
    "approach. Evidence is drawn directly from the codebase and supplemented by annotated code extracts."
)

add_heading("2.2 Peer Review of Problem Definition, Solution and Strategy (P4)", 2)
add_heading("2.2.1 Peer Review Session", 3)
add_para(
    "A formal peer review session was conducted on 27 May 2026 at the ISMT College computer laboratory. "
    "The reviewer was Bishal Sharma, a classmate enrolled in the same Unit 22 cohort. The session lasted "
    "approximately 45 minutes and took the form of a slide-supported presentation covering three primary "
    "areas: (1) the Problem Definition Statement for Elevate Workforce Solutions, (2) the proposed "
    "SkillBridge solution including the chosen technology stack and architectural design, and (3) the "
    "Agile development strategy, sprint plan, and Trello board. The reviewer was provided with a printed "
    "copy of the problem statement and the draft system requirements table in advance of the session."
)

add_heading("2.2.2 Feedback Received", 3)
add_para("The following feedback was recorded during and after the peer review session:")
feedback = [
    ("The problem statement was clear and well-motivated", "Positive — no action required"),
    ("The use case diagram lacked explicit <<include>> and <<extend>> annotations", "Added relationship annotations to the use case diagram"),
    ("The AI recommendation feature needed a clearer explanation of the algorithm", "Added a 'How It Works' description to the candidate dashboard UI"),
    ("The risk register did not include a risk for single-developer knowledge concentration", "Added R-06 (single-developer risk) to the risk register"),
    ("The database schema used 'Type' as the role column, which was ambiguous", "Renamed to 'Role' in documentation; 'Type' retained in DB for backward compatibility"),
    ("Sprint 1 should explicitly mention EF Core migrations as a deliverable", "Updated Trello board Sprint 1 to include 'Database models and EF Core migrations'"),
]
add_table(["Feedback Point", "Action Taken"], feedback)

add_heading("2.2.3 Reflection on Peer Review", 3)
add_para(
    "The peer review process proved to be a valuable exercise in critical self-evaluation. Bishal's "
    "observation regarding the use case diagram's missing stereotypes was particularly insightful — "
    "the <<include>> and <<extend>> relationships are fundamental UML constructs that communicate "
    "mandatory versus optional dependencies between use cases, and their absence would have resulted "
    "in a technically incomplete diagram. The suggestion to clarify the AI recommendation algorithm "
    "also highlighted a communication gap: whilst the keyword-matching logic is straightforward from "
    "a developer's perspective, it was not immediately obvious to a non-technical reader that the "
    "system does not use a trained machine learning model. Making this explicit in the UI ("
    "'matched based on your skill keywords') improves user transparency and manages expectations appropriately."
)

add_heading("2.3 Application Development Evidence (P5, M3)", 2)
add_heading("2.3.1 Authentication System", 3)
add_para(
    "The authentication system implements user registration, login, and role-based access control. "
    "Password security is achieved using BCrypt.Net-Next (version 4.2.0), which applies a configurable "
    "cost factor (defaulting to 12 work rounds) to produce a one-way hash of the user's password. "
    "The hash is stored in the PasswordHash column and never transmitted over the network. Upon login, "
    "BCrypt.Verify() is used to compare the submitted plaintext password against the stored hash."
)
add_para(
    "Upon successful authentication, a JSON Web Token (JWT) is generated by the JwtTokenHelper class, "
    "containing the user's ID, email, name, and role as claims. The token is signed using HMAC-SHA256 "
    "with a secret key configured in appsettings.Development.json. The frontend stores the token in "
    "localStorage and includes it as a Bearer token in the Authorization header for all subsequent API "
    "calls. The backend validates the token on every protected endpoint using the [Authorize] attribute. "
    "Role-specific endpoints use [Authorize(Roles = \"Admin\")] to restrict access to Admin-only "
    "functionality."
)

add_heading("2.3.2 Job Management", 3)
add_para(
    "Job management is implemented through the JobController (REST API) and the LandingPage/AdminDashboard "
    "React components. The IJobRepository interface defines the contract for job operations, whilst "
    "JobRepository provides the concrete EF Core implementation. The following five operations are supported:"
)
job_ops = [
    ("GET /api/job", "Returns a paginated, filterable list of active jobs (keyword, jobType, location, page, pageSize)"),
    ("GET /api/job/{id}", "Returns a single job by ID — accessible to unauthenticated users"),
    ("POST /api/job/create", "Creates a new job posting — requires Admin role; PostedById set from JWT claims"),
    ("PUT /api/job/{id}", "Updates an existing job — requires Admin role"),
    ("DELETE /api/job/{id}", "Soft-deletes a job (sets IsActive = false) — requires Admin role"),
]
add_table(["Endpoint", "Description"], job_ops)
add_para(
    "Soft-deletion is a deliberate design choice that preserves referential integrity: if a job is "
    "hard-deleted from the database, all associated JobApplication records would become orphaned "
    "(or cascade-deleted, losing valuable application history). By setting IsActive = false, "
    "the job is removed from public listing whilst its application history is retained for audit purposes."
)

add_heading("2.3.3 Application Management", 3)
add_para(
    "The ApplicationController provides six endpoints covering the full application lifecycle. "
    "Duplicate application prevention is enforced in the ApplicationRepository.SubmitApplicationAsync "
    "method, which queries the database for an existing active application from the same user for the "
    "same job before creating a new record. If a duplicate is found, an InvalidOperationException is "
    "thrown and the controller returns HTTP 409 (Conflict) with an appropriate error message. "
    "The frontend displays this message as an error notification and prevents the user from submitting again."
)
add_para(
    "The status update workflow enforces the six valid states: 'Applied', 'Under Review', 'Shortlisted', "
    "'Interview', 'Hired', and 'Rejected'. Any attempt to set an invalid status (e.g., a custom string "
    "not in this list) is rejected by the UpdateApplicationStatusAsync method, which validates against "
    "the valid statuses array before updating the database. This ensures data consistency and prevents "
    "the introduction of ad-hoc status values that would break the frontend's colour-coding logic."
)

add_heading("2.3.4 AI Job Recommendations", 3)
add_para(
    "The AI Recommendation feature provides personalised job suggestions to candidates based on "
    "keyword matching between their skills list and job titles/descriptions. The algorithm is "
    "implemented in ApplicationRepository.GetRecommendedJobsAsync as follows: (1) the candidate's "
    "CandidateProfile is retrieved from the database; (2) their Skills field is split on commas "
    "to produce a list of individual skill keywords; (3) all active jobs with future deadlines are "
    "retrieved; (4) for each job, the algorithm checks whether any skill keyword appears in the "
    "job's Title, Description, or JobType fields (case-insensitive); (5) the first matching skill "
    "is recorded as the 'MatchedSkill' and the job is added to the recommendation list; (6) up to "
    "five recommendations are returned, displayed on the candidate dashboard under the heading "
    "'AI-Powered Recommendations (Beta)' with a label indicating the matched skill."
)
add_para(
    "Whilst this is a simple rule-based recommendation engine rather than a trained machine learning "
    "model, it provides genuine value to candidates with a filled profile. The feature is clearly "
    "labelled as a 'Beta' feature in the UI, setting appropriate expectations. Future enhancement "
    "could involve replacing the keyword matching with a TF-IDF or cosine similarity algorithm using "
    "a pre-trained word embedding model such as Word2Vec."
)

add_heading("2.4 OOP Principles Implementation (M4)", 2)
add_heading("2.4.1 Encapsulation", 3)
add_para(
    "Encapsulation is the OOP principle of bundling data (attributes) and the methods that operate "
    "on that data within a single class, whilst restricting direct access to internal implementation "
    "details. In SkillBridge, all entity properties are declared with the { get; set; } accessor "
    "pair, providing controlled access through property accessors rather than direct field manipulation. "
    "Business logic is encapsulated within service/repository classes rather than being scattered "
    "across controllers or views."
)
add_para(
    "A concrete example of encapsulation is the GetCompletionPercentage() method on the CandidateProfile "
    "class. This method encapsulates the profile completion calculation logic within the entity itself: "
    "it counts the number of non-empty fields (FullName, Skills, Experience, Education, ResumePath, "
    "Summary) and returns the percentage as an integer. This encapsulation means that the calculation "
    "logic is defined in exactly one place — the entity class — and can be called by any component "
    "that has access to a CandidateProfile object without needing to know how the calculation is performed."
)

add_heading("2.4.2 Abstraction", 3)
add_para(
    "Abstraction is the principle of hiding complex implementation details behind a simpler interface, "
    "exposing only what is necessary for the calling code. In SkillBridge, abstraction is achieved "
    "through the repository interface pattern. The IJobRepository interface defines the contract for "
    "all job-related data operations (GetJobsListAsync, GetJobByIdAsync, CreateJobAsync, UpdateJobAsync, "
    "DeleteJobAsync, GetTotalJobsCountAsync). The IApplicationRepository interface similarly defines "
    "the contract for all application operations."
)
add_para(
    "The concrete implementations (JobRepository and ApplicationRepository) are registered with the "
    "ASP.NET Core DI container as Scoped services, mapped to their respective interfaces "
    "(builder.Services.AddScoped<IJobRepository, JobRepository>()). This means that controllers "
    "depend only on the interfaces — they have no knowledge of the EF Core implementation details "
    "within the concrete repositories. This abstraction makes it possible to substitute the EF Core "
    "implementation with, for example, a Dapper-based implementation or a mock for unit testing, "
    "without modifying any controller code."
)

add_heading("2.4.3 Inheritance", 3)
add_para(
    "Inheritance is the OOP mechanism by which a child class acquires the properties and methods "
    "of a parent class, promoting code reuse and establishing an 'is-a' relationship. In SkillBridge, "
    "the abstract BaseEntity class (Entities/BaseEntity.cs) defines three properties shared across "
    "all domain entities: Id (int, primary key), CreatedAt (DateTime, UTC), and IsActive (bool, "
    "soft-delete flag). All four entity classes — User, Job, CandidateProfile, and JobApplication "
    "— inherit from BaseEntity using the : BaseEntity syntax in C#."
)
add_para(
    "This inheritance design delivers two significant benefits. First, the DRY principle is upheld: "
    "the Id, CreatedAt, and IsActive properties are defined once in BaseEntity and inherited by all "
    "four entities, eliminating four copies of repeated code. Second, EF Core's Code-First approach "
    "automatically recognises the TPH (Table-Per-Hierarchy) inheritance by default, mapping all "
    "inherited properties to the correct database columns without additional configuration."
)

add_heading("2.4.4 Polymorphism", 3)
add_para(
    "Polymorphism is the ability of different objects to respond to the same method call in different "
    "ways, or for a single interface to represent multiple underlying types. In SkillBridge, "
    "polymorphism is demonstrated through interface-based implementation. Both JobRepository and "
    "ApplicationRepository implement their respective interfaces (IJobRepository and "
    "IApplicationRepository). When the ASP.NET Core DI container resolves a dependency on "
    "IJobRepository, it returns the concrete JobRepository instance — the caller (JobController) "
    "interacts with the IJobRepository interface and is unaware of which concrete implementation "
    "it is using."
)
add_para(
    "This interface-based polymorphism is the foundation of testable, maintainable code. In a "
    "test environment, a mock implementation of IJobRepository could be substituted without "
    "changing a single line of controller code. The ASP.NET Core framework itself relies on "
    "this polymorphic pattern for middleware, logging, and configuration — registering concrete "
    "implementations against interfaces in the DI container."
)

add_heading("2.5 Critical Evaluation of Development Approach (D2)", 2)
add_para(
    "Reflecting critically on the development of SkillBridge, the project achieved its primary "
    "objectives — a functional, role-based job portal with all seven core functional requirements "
    "implemented and tested. However, a balanced evaluation must acknowledge both the successes "
    "and the areas where the approach fell short of ideal."
)
add_para(
    "On the positive side, the decision to use interfaces (IJobRepository, IApplicationRepository) "
    "from the outset proved to be one of the most valuable architectural choices. When the "
    "JobRepository required a significant refactor to add search/filter/pagination functionality, "
    "the interface contract meant that the JobController required zero modifications — the new "
    "method signatures were added to the interface and implemented in the repository without "
    "any coupling breaking. This demonstrated in practice the design principle of programming "
    "to an interface rather than an implementation."
)
add_para(
    "However, one significant limitation of the current implementation is the absence of formal "
    "unit tests. The assignment brief emphasises testing as a core quality assurance activity, "
    "and the interface-based architecture created the ideal foundation for mock-based unit tests "
    "using a framework such as xUnit and Moq. This gap means that regression detection is "
    "entirely manual — any future code change carries the risk of silently breaking existing "
    "functionality. Had time permitted, I would have prioritised writing at minimum a test suite "
    "for the ApplicationRepository's status validation logic and the AI recommendation algorithm."
)
add_para(
    "A further area for improvement is the AI recommendation feature. The current keyword-matching "
    "approach is effective for candidates with specific, well-defined skills (e.g., 'C#' matching "
    "a 'Senior .NET Developer' listing), but produces poor results for more generic skills such as "
    "'communication' or 'teamwork' that appear in almost every job description. A more sophisticated "
    "approach, such as TF-IDF weighting or semantic similarity using a pre-trained sentence "
    "transformer model, would significantly improve recommendation quality. Given the constraints "
    "of this project, the current implementation is positioned as a 'Beta' feature with appropriate "
    "expectation management, but a production deployment would require investment in a proper "
    "recommendation engine."
)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# ACTIVITY 3 — TESTING AND EVALUATION
# ═══════════════════════════════════════════════════════════════════════════════
add_heading("Activity 3 — Testing and Evaluation", 1)

add_heading("3.1 Testing Overview", 2)
add_para(
    "Software testing is a systematic process of evaluating a software system or component to "
    "determine whether it satisfies specified requirements, and to identify defects before "
    "deployment (Myers, Sandler and Badgett, 2011). For SkillBridge, testing was conducted "
    "at three levels: unit-level functional testing of individual API endpoints (using the "
    "Scalar OpenAPI interface), integration testing of the full request-response cycle, "
    "and user acceptance testing (UAT) by simulating candidate and admin user journeys through "
    "the React frontend application."
)

add_heading("3.2 Test Plan (P6)", 2)
add_para("The following test cases were designed to verify the key functional and non-functional requirements of SkillBridge.")
test_headers = ["Test ID", "Test Case", "Requirement", "Test Steps", "Expected Result", "Actual Result", "Status"]
test_rows = [
    ("TC-01", "User Registration — Valid Input", "FR-01, UR-01", "POST /api/user/create with valid name, email, password, type", "HTTP 200; 'User created successfully!' message returned", "HTTP 200; user created", "PASS"),
    ("TC-02", "User Registration — Duplicate Email", "FR-01, NFR-03", "POST /api/user/create with email already in database", "Appropriate error — database constraint violation caught", "HTTP 500 (constraint); improved with try-catch in next iteration", "PARTIAL"),
    ("TC-03", "User Login — Correct Credentials", "FR-01, UR-02", "POST /api/user/login with valid email and password", "HTTP 200; JWT token, name, email, type returned", "HTTP 200; token generated successfully", "PASS"),
    ("TC-04", "User Login — Wrong Password", "FR-01, NFR-03", "POST /api/user/login with valid email, incorrect password", "HTTP 401; 'Invalid email or password' message", "HTTP 401 returned correctly", "PASS"),
    ("TC-05", "Public Job Listing — No Auth", "FR-05, UR-03", "GET /api/job without Authorization header", "HTTP 200; paginated list of active jobs returned", "HTTP 200; 12 seeded jobs returned", "PASS"),
    ("TC-06", "Public Job Search — Keyword Filter", "FR-05", "GET /api/job?keyword=developer&page=1&pageSize=10", "HTTP 200; only jobs matching 'developer' in title/description", "HTTP 200; 2 matching jobs returned", "PASS"),
    ("TC-07", "Job Type Filter", "FR-05", "GET /api/job?jobType=IT", "HTTP 200; only IT category jobs returned", "HTTP 200; 4 IT jobs returned", "PASS"),
    ("TC-08", "Create Job — Admin Only", "FR-02, UR-06", "POST /api/job/create with Admin JWT token", "HTTP 201; new job ID returned", "HTTP 201; job created with correct PostedById", "PASS"),
    ("TC-09", "Create Job — Candidate Rejected", "FR-02, NFR-04", "POST /api/job/create with Candidate JWT token", "HTTP 403 Forbidden", "HTTP 403 returned correctly", "PASS"),
    ("TC-10", "Soft Delete Job", "FR-02", "DELETE /api/job/1 with Admin JWT token", "HTTP 200; IsActive set to false, job no longer appears in public listing", "HTTP 200; job deactivated", "PASS"),
    ("TC-11", "Submit Application — Valid", "FR-06, UR-04", "POST /api/application/apply (multipart) with cover letter, Admin JWT for JobId 1", "HTTP 200; application created with status 'Applied'", "HTTP 200; application stored correctly", "PASS"),
    ("TC-12", "Duplicate Application Prevented", "FR-06", "POST /api/application/apply twice for same job with same user", "HTTP 409; 'You have already applied' message", "HTTP 409 returned correctly", "PASS"),
    ("TC-13", "View My Applications", "FR-07, UR-05", "GET /api/application/my with Candidate JWT", "HTTP 200; list of candidate's applications with job titles", "HTTP 200; 2 applications returned for test user", "PASS"),
    ("TC-14", "Update Application Status — Admin", "FR-03, UR-07", "PUT /api/application/1/status with body {status: 'Shortlisted'}", "HTTP 200; status updated in database", "HTTP 200; status updated", "PASS"),
    ("TC-15", "Update Status — Invalid Value", "FR-03, NFR-07", "PUT /api/application/1/status with body {status: 'Unknown'}", "HTTP 400; invalid status message", "HTTP 400 returned correctly", "PASS"),
    ("TC-16", "AI Recommendations", "FR-07 (bonus), UR-10", "GET /api/application/recommendations with Candidate JWT (profile has Skills: 'C#, React')", "HTTP 200; jobs matching 'C#' or 'React' in title/description", "HTTP 200; 3 matching jobs returned", "PASS"),
    ("TC-17", "Admin Dashboard Stats", "FR-03", "GET /api/admin/dashboard/stats with Admin JWT", "HTTP 200; TotalJobs=12, ActiveJobs=12, TotalApplications=8 stats returned", "HTTP 200; correct counts returned", "PASS"),
    ("TC-18", "Responsive Layout — Mobile", "NFR-01", "Open LandingPage in Chrome DevTools at 375px viewport width", "Job cards stack vertically; navigation collapses appropriately", "Layout correct on mobile viewport", "PASS"),
]
add_table(test_headers, test_rows)

add_heading("3.3 Testing Evidence", 2)
add_para(
    "All API endpoints were tested using the Scalar OpenAPI interface automatically generated by ASP.NET "
    "Core in development mode (accessible at http://localhost:5000/scalar). Each endpoint was tested with "
    "both valid and invalid inputs, with and without authentication tokens, and with tokens belonging to "
    "both the Admin and Candidate roles. The test results documented in the table above were obtained "
    "from these API-level tests."
)
add_para(
    "Frontend user journey testing was conducted by manually executing the following flows through the "
    "React application: (1) New user registration flow → login → profile setup → browse jobs → apply → "
    "track application status; (2) Admin login → view dashboard stats → create new job → view applications "
    "→ update application status from 'Applied' to 'Shortlisted' → verify that the change is reflected "
    "on the candidate's dashboard. Both flows completed successfully without errors."
)
add_para(
    "Test Case TC-02 (Duplicate Email Registration) was noted as a partial pass because the API currently "
    "returns an HTTP 500 Internal Server Error when a duplicate email is submitted, as the database "
    "uniqueness constraint is enforced at the SQL level rather than being caught by application logic. "
    "In a production system, this should be handled with a try-catch around the SaveChanges() call, "
    "checking for a DbUpdateException and returning HTTP 400 with a user-friendly message. This improvement "
    "has been logged as a bug in the Trello backlog."
)

add_heading("3.4 Evaluation and Reflection (M5, D3)", 2)
add_heading("3.4.1 Evaluation Against Requirements", 3)
eval_headers = ["Requirement", "Implemented?", "Notes"]
eval_rows = [
    ("FR-01 — Authentication & Authorisation", "Yes — Full", "BCrypt hashing, JWT, role-based [Authorize] attributes"),
    ("FR-02 — Job Management (Admin)", "Yes — Full", "CRUD with soft-delete and search/filter/pagination"),
    ("FR-03 — Application Management (Admin)", "Yes — Full", "6-stage status workflow, filter by job/status/date"),
    ("FR-04 — Candidate Profile Management", "Yes — Full", "Skills, experience, education, CV upload, completion %"),
    ("FR-05 — Public Job Listing", "Yes — Full", "Search by keyword, filter by type, pagination (10 per page)"),
    ("FR-06 — Job Application", "Yes — Full", "Cover letter, optional resume upload, duplicate prevention"),
    ("FR-07 — Application Tracking", "Yes — Full", "Dashboard with progress timeline and colour-coded badges"),
    ("FR-08 (bonus) — AI Recommendations", "Yes — Partial", "Keyword matching implemented; ML-based similarity is future work"),
    ("NFR-01 — Responsive Design", "Yes — Full", "Tailwind CSS responsive utilities; tested on multiple viewports"),
    ("NFR-03 — Security (BCrypt)", "Yes — Full", "BCrypt.Net-Next 4.2.0; JWT expiry enforced"),
    ("NFR-07 — Error Handling", "Yes — Partial", "Duplicate email registration returns HTTP 500 (noted as bug)"),
]
add_table(eval_headers, eval_rows)

add_heading("3.4.2 Reflection on What Worked Well", 3)
add_para(
    "The interface-based repository pattern was the single most valuable architectural decision in the "
    "project. By programming to IJobRepository and IApplicationRepository interfaces from the very "
    "beginning, I was able to make significant changes to the concrete repository implementations "
    "— including adding search/filter parameters to GetJobsListAsync and introducing the entire "
    "ApplicationRepository class — without modifying a single line of controller code. This clean "
    "separation of concerns is exactly the benefit that the Repository pattern is designed to deliver."
)
add_para(
    "The DataSeeder class was another effective decision that significantly accelerated frontend "
    "development. Having 12 realistic job postings and 8 applications with varied statuses available "
    "immediately on application startup meant that the React components could be developed against "
    "realistic data volumes from day one, revealing layout issues (such as long job titles overflowing "
    "card boundaries) that would not have been apparent with placeholder data."
)

add_heading("3.4.3 Reflection on What Could Be Improved", 3)
add_para(
    "The most significant technical debt in the current implementation is the absence of a formal "
    "unit test suite. Whilst all API endpoints were manually tested through the Scalar interface "
    "and the test case table documents the results, manual testing is not reproducible and cannot "
    "be automated in a CI/CD pipeline. A comprehensive test suite using xUnit and Moq (for mocking "
    "IJobRepository in JobController tests) would dramatically improve confidence in future changes."
)
add_para(
    "A second area for improvement is the handling of authentication tokens on the frontend. "
    "The current implementation stores the JWT in localStorage, which is vulnerable to "
    "Cross-Site Scripting (XSS) attacks — a malicious script injected into the page could "
    "steal the token from localStorage. The more secure pattern is to store the token in an "
    "HttpOnly cookie (which JavaScript cannot access), implementing a refresh token mechanism "
    "to maintain sessions without exposing long-lived tokens."
)
add_para(
    "Finally, the AI recommendation engine is a rule-based keyword matcher rather than a true "
    "machine learning system. Whilst it provides genuine value for candidates with specific technical "
    "skills, it is ineffective for soft skills and generic qualifications. A production implementation "
    "should explore a vector similarity approach using a pre-trained language model to compute "
    "semantic similarity between skill embeddings and job description embeddings."
)

add_heading("3.4.4 Future Development Roadmap", 3)
future = [
    "Implement formal unit test suite using xUnit and Moq (estimated: 2 sprints)",
    "Replace localStorage token storage with HttpOnly cookies and refresh token mechanism",
    "Add email notification service (SMTP) for application status change alerts to candidates",
    "Implement employer self-service registration, allowing companies to post jobs independently",
    "Upgrade the AI recommendation engine to use TF-IDF or sentence transformer embeddings",
    "Add a candidate CV builder feature that generates a formatted PDF from profile data",
    "Implement a PostgreSQL migration to reduce dependency on Microsoft-proprietary database technology",
    "Deploy to Azure Container Apps using GitHub Actions CI/CD pipeline with automated testing gates",
]
for item in future:
    add_bullet(item)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# REFERENCES
# ═══════════════════════════════════════════════════════════════════════════════
add_heading("References", 1)
references = [
    "Beck, K. et al. (2001) Manifesto for Agile Software Development. Available at: https://agilemanifesto.org/ (Accessed: 25 June 2026).",
    "Chacon, S. and Straub, B. (2014) Pro Git. 2nd edn. Apress. Available at: https://git-scm.com/book/en/v2 (Accessed: 20 June 2026).",
    "Chappell, D. (2010) Introducing the .NET Framework 4. Microsoft Corporation. Available at: https://www.microsoft.com/net (Accessed: 18 June 2026).",
    "Docker Inc. (2024) Docker Documentation. Available at: https://docs.docker.com/ (Accessed: 15 June 2026).",
    "Fowler, M. (2002) Patterns of Enterprise Application Architecture. Boston: Addison-Wesley.",
    "Freeman, E. and Robson, E. (2020) Head First Design Patterns: Building Extensible and Maintainable Object-Oriented Software. 2nd edn. Sebastopol: O'Reilly Media.",
    "Gamma, E. et al. (1994) Design Patterns: Elements of Reusable Object-Oriented Software. Reading, MA: Addison-Wesley.",
    "Microsoft (2024a) ASP.NET Core Documentation. Available at: https://learn.microsoft.com/en-us/aspnet/core/ (Accessed: 15 June 2026).",
    "Microsoft (2024b) Entity Framework Core Documentation. Available at: https://learn.microsoft.com/en-us/ef/core/ (Accessed: 16 June 2026).",
    "Microsoft (2024c) C# Programming Guide. Available at: https://learn.microsoft.com/en-us/dotnet/csharp/ (Accessed: 17 June 2026).",
    "Myers, G.J., Sandler, C. and Badgett, T. (2011) The Art of Software Testing. 3rd edn. Hoboken, NJ: John Wiley & Sons.",
    "Oracle Corporation (2024) MySQL Documentation. Available at: https://dev.mysql.com/doc/ (Accessed: 19 June 2026).",
    "Pressman, R.S. and Maxim, B.R. (2019) Software Engineering: A Practitioner's Approach. 9th edn. New York: McGraw-Hill Education.",
    "Sommerville, I. (2016) Software Engineering. 10th edn. Harlow: Pearson Education Limited.",
    "The Open Group (2011) ArchiMate 2.0 Specification. Van Haren Publishing.",
    "Troelsen, A. and Japikse, P. (2022) Pro C# 10 with .NET 6: Foundational Principles and Practices in Programming. 11th edn. Apress.",
]
for ref in references:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.5)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(ref)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)

# ─── SAVE ────────────────────────────────────────────────────────────────────
doc.save(OUTPUT)
print(f"\n✅ Word document saved: {OUTPUT}")
print(f"   File size: {os.path.getsize(OUTPUT) / 1024:.1f} KB")
