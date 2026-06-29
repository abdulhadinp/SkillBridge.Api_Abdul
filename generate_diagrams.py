#!/usr/bin/env python3
"""
SkillBridge Diagram Generator — Unit 22 Assignment
Generates all 11 required diagrams as high-quality PNG files.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
import numpy as np
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "diagrams")
os.makedirs(OUTPUT_DIR, exist_ok=True)

DPI = 150
FIG_W, FIG_H = 16, 9

def save(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  ✓ Saved {name}")

# ─── Diagram 1: System Architecture ──────────────────────────────────────────
def diagram_01():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    fig.patch.set_facecolor('#f8fafc')
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis('off')
    ax.set_title('SkillBridge — System Architecture Diagram', fontsize=18, fontweight='bold', pad=20, color='#1e293b')

    def box(ax, x, y, w, h, label, sublabel='', color='#3b82f6', textcolor='white', fontsize=11):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15", linewidth=2,
                               edgecolor=color, facecolor=color, zorder=3)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2 + (0.15 if sublabel else 0), label, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', color=textcolor, zorder=4)
        if sublabel:
            ax.text(x + w/2, y + h/2 - 0.3, sublabel, ha='center', va='center',
                    fontsize=8, color=textcolor, alpha=0.85, zorder=4)

    def arrow(ax, x1, y1, x2, y2, label='', color='#64748b'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=2), zorder=2)
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my + 0.12, label, ha='center', va='bottom', fontsize=8,
                    color='#475569', style='italic')

    # Components
    box(ax, 0.3, 3.0, 1.8, 1.0, '🌐 Browser', 'User / Client', '#6366f1')
    box(ax, 3.5, 2.5, 3.0, 2.0, '⚙️ ASP.NET Core 8', 'REST API + MVC\nControllers / Services', '#0d6efd')
    box(ax, 3.5, 0.4, 3.0, 1.4, '🗃️ Entity Framework Core', 'ORM Layer\nCode-First Migrations', '#0f766e')
    box(ax, 3.5, -0.8, 3.0, 1.0, '🐋 SQL Server', 'Docker Container\nPort 1433', '#7c3aed')
    box(ax, 7.8, 3.0, 1.9, 1.0, '🤖 AI Service', 'Keyword Matching\nRecommendations', '#d97706')

    # Arrows
    arrow(ax, 2.1, 3.5, 3.5, 3.5, 'HTTPS Request', '#1e40af')
    arrow(ax, 3.5, 3.2, 2.1, 3.2, 'HTML Response', '#1e40af')
    arrow(ax, 5.0, 2.5, 5.0, 1.8, 'EF Core Queries')
    arrow(ax, 5.0, 1.4, 5.0, 0.6, 'SQL Queries')
    arrow(ax, 4.9, 0.6, 4.9, 1.4, 'Data Results')
    arrow(ax, 6.5, 3.8, 7.8, 3.8, 'Skill Match Request')
    arrow(ax, 7.8, 3.5, 6.5, 3.5, 'Job Recommendations')

    # Legend
    ax.text(0.3, 6.5, '📌 Three-Tier Architecture: Presentation → Business Logic → Data', fontsize=10, color='#475569',
            style='italic')

    save(fig, '01_system_design.png')

# ─── Diagram 2: Use Case Diagram ─────────────────────────────────────────────
def diagram_02():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    fig.patch.set_facecolor('#f8fafc')
    ax.set_xlim(0, 16); ax.set_ylim(0, 10); ax.axis('off')
    ax.set_title('SkillBridge — UML Use Case Diagram', fontsize=18, fontweight='bold', pad=20, color='#1e293b')

    # System Boundary
    rect = FancyBboxPatch((3, 0.5), 10, 9, boxstyle="round,pad=0.2", linewidth=2.5,
                           edgecolor='#3b82f6', facecolor='#eff6ff', zorder=1)
    ax.add_patch(rect)
    ax.text(8, 9.2, 'SkillBridge — Job Portal System', ha='center', va='center',
            fontsize=13, fontweight='bold', color='#1e40af')

    def actor(ax, x, y, label):
        # Stick figure
        ax.plot(x, y + 0.6, 'o', markersize=18, color='#374151', zorder=5)
        ax.plot([x, x], [y - 0.2, y + 0.3], color='#374151', lw=2, zorder=5)
        ax.plot([x - 0.4, x, x + 0.4], [y + 0.05, y + 0.3, y + 0.05], color='#374151', lw=2, zorder=5)
        ax.plot([x, x - 0.3], [y - 0.2, y - 0.7], color='#374151', lw=2, zorder=5)
        ax.plot([x, x + 0.3], [y - 0.2, y - 0.7], color='#374151', lw=2, zorder=5)
        ax.text(x, y - 1.0, label, ha='center', va='top', fontsize=10, fontweight='bold', color='#1e293b')

    def usecase(ax, x, y, label, color='#dbeafe', ecolor='#3b82f6'):
        ellipse = mpatches.Ellipse((x, y), 3.2, 0.8, linewidth=1.5, edgecolor=ecolor,
                                    facecolor=color, zorder=3)
        ax.add_patch(ellipse)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, color='#1e293b', zorder=4,
                wrap=True)

    def connect(ax, ax_pt, uc_pt, style='solid', label=''):
        ls = '--' if style == 'dashed' else '-'
        ax.annotate('', xy=uc_pt, xytext=ax_pt,
                    arrowprops=dict(arrowstyle='->', color='#6b7280', lw=1.2, linestyle=ls), zorder=2)
        if label:
            mx, my = (ax_pt[0]+uc_pt[0])/2, (ax_pt[1]+uc_pt[1])/2
            ax.text(mx, my, label, ha='center', fontsize=7, color='#374151', style='italic')

    # Actors
    actor(ax, 1.2, 7.0, 'Admin')
    actor(ax, 1.2, 2.5, 'Candidate')
    actor(ax, 14.8, 5.0, 'AI Agent')

    # Admin use cases (left side of system)
    admin_cases = [
        (6.5, 8.5, 'Sign Up / Sign In\n/ Reset Password'),
        (6.5, 7.5, 'Create Job Posting'),
        (6.5, 6.5, 'Update Job Posting'),
        (6.5, 5.5, 'Delete Job Posting'),
        (6.5, 4.5, 'View All Applications'),
        (6.5, 3.5, 'Update Application Status'),
        (6.5, 2.5, 'Generate Report'),
    ]
    for x, y, label in admin_cases:
        usecase(ax, x, y, label, '#dbeafe', '#3b82f6')
        connect(ax, (1.8, 7.0), (x - 1.6, y))

    # Candidate use cases (right side)
    cand_cases = [
        (10.5, 8.5, 'Sign Up / Sign In\n/ Reset Password'),
        (10.5, 7.2, 'Setup / Edit Profile'),
        (10.5, 6.0, 'View & Search Jobs'),
        (10.5, 4.8, 'Apply for a Job'),
        (10.5, 3.6, 'Track Application Status'),
        (10.5, 2.4, 'View AI Job Recommendations'),
    ]
    for x, y, label in cand_cases:
        usecase(ax, x, y, label, '#dcfce7', '#16a34a')
        connect(ax, (1.8, 2.5), (x - 1.6, y))

    # AI Agent
    usecase(ax, 10.5, 1.2, 'Recommend Jobs', '#fef3c7', '#d97706')
    connect(ax, (14.3, 5.0), (12.1, 1.2))

    # include/extend arrows
    ax.annotate('', xy=(9.0, 4.8), xytext=(9.0, 6.0),
                arrowprops=dict(arrowstyle='->', color='#9333ea', lw=1.5, linestyle='--'))
    ax.text(9.3, 5.4, '<<include>>\nSign In', fontsize=7, color='#9333ea', style='italic', ha='left')

    ax.annotate('', xy=(10.5, 2.4), xytext=(10.5, 6.0),
                arrowprops=dict(arrowstyle='->', color='#dc2626', lw=1.2, linestyle='--'))
    ax.text(10.7, 4.2, '<<extend>>', fontsize=7, color='#dc2626', style='italic')

    save(fig, '02_use_case.png')

# ─── Diagram 3: Flowchart ─────────────────────────────────────────────────────
def diagram_03():
    fig, ax = plt.subplots(figsize=(12, 14))
    fig.patch.set_facecolor('#f8fafc')
    ax.set_xlim(0, 10); ax.set_ylim(0, 20); ax.axis('off')
    ax.set_title('SkillBridge — Application Flowchart', fontsize=18, fontweight='bold', pad=20, color='#1e293b')

    def oval(ax, x, y, w, h, label, color='#6366f1'):
        e = mpatches.Ellipse((x, y), w, h, linewidth=2, edgecolor=color, facecolor=color, zorder=3)
        ax.add_patch(e)
        ax.text(x, y, label, ha='center', va='center', fontsize=10, fontweight='bold', color='white', zorder=4)

    def rect(ax, x, y, w, h, label, color='#3b82f6'):
        r = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.1", linewidth=1.5,
                            edgecolor=color, facecolor=color, zorder=3)
        ax.add_patch(r)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, color='white', zorder=4, wrap=True)

    def diamond(ax, x, y, w, h, label, color='#f59e0b'):
        pts = np.array([[x, y + h/2], [x + w/2, y], [x, y - h/2], [x - w/2, y]])
        poly = plt.Polygon(pts, linewidth=2, edgecolor=color, facecolor=color, zorder=3)
        ax.add_patch(poly)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold', color='white', zorder=4)

    def arr(ax, x1, y1, x2, y2, label=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#475569', lw=1.5))
        if label:
            ax.text((x1+x2)/2 + 0.15, (y1+y2)/2, label, fontsize=8, color='#374151')

    # Flow elements
    oval(ax, 5, 19, 2.5, 0.7, 'START')
    arr(ax, 5, 18.65, 5, 17.8)
    rect(ax, 5, 17.4, 3.5, 0.7, 'Sign Up / Sign In')
    arr(ax, 5, 17.05, 5, 16.1)
    diamond(ax, 5, 15.6, 3.5, 0.9, 'User Type?')

    # Admin branch
    arr(ax, 3.25, 15.6, 2.0, 15.6)
    ax.text(2.5, 15.75, 'Admin', fontsize=9, color='#374151', ha='center')
    rect(ax, 2.0, 14.8, 2.5, 0.7, 'CRUD Job\nPostings', '#0d6efd')
    arr(ax, 2.0, 14.45, 2.0, 13.5)
    rect(ax, 2.0, 13.1, 2.5, 0.7, 'View / Filter\nApplications', '#0d6efd')
    arr(ax, 2.0, 12.75, 2.0, 11.8)
    rect(ax, 2.0, 11.4, 2.5, 0.7, 'Update Application\nStatus', '#0d6efd')
    arr(ax, 2.0, 11.05, 2.0, 10.1)
    rect(ax, 2.0, 9.7, 2.5, 0.7, 'Generate Report', '#0d6efd')
    arr(ax, 2.0, 9.35, 2.0, 8.5)
    oval(ax, 2.0, 8.2, 1.8, 0.5, 'END', '#6366f1')

    # Candidate branch
    arr(ax, 6.75, 15.6, 8.0, 15.6)
    ax.text(7.5, 15.75, 'Candidate', fontsize=9, color='#374151', ha='center')
    rect(ax, 8.0, 14.8, 2.5, 0.7, 'Setup Profile', '#16a34a')
    arr(ax, 8.0, 14.45, 8.0, 13.5)
    rect(ax, 8.0, 13.1, 2.5, 0.7, 'View / Search\n/ Filter Jobs', '#16a34a')
    arr(ax, 8.0, 12.75, 8.0, 11.8)
    rect(ax, 8.0, 11.4, 2.5, 0.7, '🤖 AI Job\nRecommendations', '#d97706')
    arr(ax, 8.0, 11.05, 8.0, 10.1)
    rect(ax, 8.0, 9.7, 2.5, 0.7, 'Apply for Job', '#16a34a')
    arr(ax, 8.0, 9.35, 8.0, 8.4)
    rect(ax, 8.0, 8.0, 2.5, 0.7, 'Track Application\nStatus', '#16a34a')
    arr(ax, 8.0, 7.65, 8.0, 6.8)
    oval(ax, 8.0, 6.5, 1.8, 0.5, 'END', '#6366f1')

    save(fig, '03_flowchart.png')

# ─── Diagram 4: Activity Diagram (Swimlane) ──────────────────────────────────
def diagram_04():
    fig, ax = plt.subplots(figsize=(FIG_W, 12))
    fig.patch.set_facecolor('#f8fafc')
    ax.set_xlim(0, 16); ax.set_ylim(0, 14); ax.axis('off')
    ax.set_title('SkillBridge — UML Activity Diagram: Job Application Process', fontsize=16, fontweight='bold', pad=20, color='#1e293b')

    lanes = [
        (0.5, 4.5, '#dbeafe', '#3b82f6', 'Candidate'),
        (5.5, 5.0, '#dcfce7', '#16a34a', 'System (SkillBridge)'),
        (11.5, 4.0, '#fef3c7', '#d97706', 'Admin'),
    ]
    for x, w, fc, ec, label in lanes:
        rect = FancyBboxPatch((x, 0.5), w, 13, boxstyle="round,pad=0.1", linewidth=2,
                               edgecolor=ec, facecolor=fc, alpha=0.3, zorder=1)
        ax.add_patch(rect)
        ax.text(x + w/2, 13.3, label, ha='center', va='center', fontsize=13, fontweight='bold', color=ec)

    def activity(ax, x, y, label, color='#3b82f6', w=3.8, h=0.65):
        r = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.1", linewidth=1.5,
                            edgecolor=color, facecolor=color, zorder=3)
        ax.add_patch(r)
        ax.text(x, y, label, ha='center', va='center', fontsize=8.5, color='white',
                fontweight='bold', zorder=4)

    def darr(ax, x1, y1, x2, y2):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#475569', lw=1.5), zorder=2)

    def decision(ax, x, y, label):
        pts = np.array([[x, y+0.5], [x+1.2, y], [x, y-0.5], [x-1.2, y]])
        poly = plt.Polygon(pts, linewidth=2, edgecolor='#f59e0b', facecolor='#fef3c7', zorder=3)
        ax.add_patch(poly)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, color='#92400e', zorder=4)

    # Activities
    # Initial state
    ax.plot(2.7, 12.8, 'o', markersize=12, color='#1e293b', zorder=5)

    activity(ax, 2.7, 12.0, 'Browse Job Listings', '#3b82f6')
    darr(ax, 2.7, 12.8, 2.7, 12.33)
    darr(ax, 2.7, 11.67, 8.0, 10.83)

    activity(ax, 8.0, 10.5, 'Display Active Jobs\n(Search / Filter)', '#16a34a')
    darr(ax, 8.0, 10.17, 2.7, 9.33)

    activity(ax, 2.7, 9.0, 'Select Job / Click Apply', '#3b82f6')
    darr(ax, 2.7, 8.67, 8.0, 8.0)

    decision(ax, 8.0, 7.5, 'Authenticated?')
    darr(ax, 2.7, 9.0, 5.5, 7.5)

    activity(ax, 8.0, 6.2, 'Display Login Page', '#16a34a')
    ax.text(9.3, 7.2, 'No', fontsize=9, color='#dc2626', fontweight='bold')
    darr(ax, 8.0, 7.0, 8.0, 6.53)
    darr(ax, 6.8, 7.5, 2.7, 7.5)
    ax.text(4.5, 7.7, 'Yes → Show Form', fontsize=8, color='#16a34a')

    activity(ax, 2.7, 6.7, 'Fill Cover Letter\nUpload Resume', '#3b82f6')
    darr(ax, 2.7, 7.17, 2.7, 7.03)
    darr(ax, 2.7, 6.37, 8.0, 5.53)

    activity(ax, 8.0, 5.2, 'Validate & Store\nApplication (status=Applied)', '#16a34a')
    darr(ax, 8.0, 4.87, 13.0, 4.33)
    darr(ax, 8.0, 4.87, 8.0, 3.83)

    activity(ax, 13.0, 4.0, 'Review Application', '#d97706')
    darr(ax, 13.0, 3.67, 13.0, 3.0)
    activity(ax, 13.0, 2.7, 'Update Status', '#d97706')
    darr(ax, 13.0, 2.37, 8.0, 1.83)
    activity(ax, 8.0, 3.5, 'Notify Admin\n(Dashboard Update)', '#16a34a')

    activity(ax, 8.0, 1.5, 'Update Status in DB', '#16a34a')
    darr(ax, 8.0, 1.17, 2.7, 0.83)
    activity(ax, 2.7, 0.5, 'Check Status on Dashboard', '#3b82f6')

    # Final state
    ax.plot(2.7, 0.0, 'o', markersize=14, color='#1e293b', zorder=5)
    ax.plot(2.7, 0.0, 'o', markersize=10, color='white', zorder=6)
    ax.plot(2.7, 0.0, 'o', markersize=6, color='#1e293b', zorder=7)
    darr(ax, 2.7, 0.17, 2.7, 0.05)

    save(fig, '04_activity_diagram.png')

# ─── Diagram 5: State Diagram ─────────────────────────────────────────────────
def diagram_05():
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor('#f8fafc')
    ax.set_xlim(0, 14); ax.set_ylim(0, 8); ax.axis('off')
    ax.set_title('SkillBridge — UML State Diagram: Application Status Lifecycle', fontsize=16, fontweight='bold', pad=20, color='#1e293b')

    def state(ax, x, y, label, color='#3b82f6'):
        r = FancyBboxPatch((x - 1.2, y - 0.4), 2.4, 0.8, boxstyle="round,pad=0.2", linewidth=2,
                            edgecolor=color, facecolor=color, zorder=3)
        ax.add_patch(r)
        ax.text(x, y, label, ha='center', va='center', fontsize=11, fontweight='bold', color='white', zorder=4)

    def trans(ax, x1, y1, x2, y2, label='', offset=(0, 0.2)):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#475569', lw=1.8), zorder=2)
        mx = (x1+x2)/2 + offset[0]
        my = (y1+y2)/2 + offset[1]
        if label:
            ax.text(mx, my, label, ha='center', va='center', fontsize=8, color='#374151',
                    style='italic', bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='#e2e8f0', alpha=0.9))

    # Initial state
    ax.plot(2.0, 7.2, 'o', markersize=14, color='#1e293b', zorder=5)
    ax.annotate('', xy=(2.0, 6.45), xytext=(2.0, 6.8),
                arrowprops=dict(arrowstyle='->', color='#1e293b', lw=2))

    # States
    state(ax, 2.0, 6.1, 'Applied', '#3b82f6')
    state(ax, 5.5, 6.1, 'Under Review', '#ca8a04')
    state(ax, 9.0, 6.1, 'Shortlisted', '#7c3aed')
    state(ax, 11.5, 4.0, 'Interview', '#ea580c')
    state(ax, 11.5, 2.0, 'Hired', '#16a34a')
    state(ax, 8.5, 2.0, 'Rejected', '#dc2626')

    # Transitions
    trans(ax, 3.2, 6.1, 4.3, 6.1, 'Admin opens\napplication')
    trans(ax, 6.7, 6.1, 7.8, 6.1, 'Admin shortlists')
    trans(ax, 10.0, 5.8, 10.8, 4.3, 'Interview\nscheduled', (-0.2, 0))
    trans(ax, 11.5, 3.6, 11.5, 2.4, 'Candidate passes')
    trans(ax, 10.3, 3.8, 9.3, 2.3, 'Does not proceed', (0.5, 0))
    trans(ax, 6.8, 5.8, 8.0, 2.3, 'Admin rejects', (-1.0, 0))
    trans(ax, 3.2, 5.8, 7.6, 2.3, 'Rejected\n(early)', (-1.5, 0.3))

    # Final states
    for x, y in [(11.5, 2.0), (8.5, 2.0)]:
        ax.plot(x, y - 0.55, 'o', markersize=14, color='#1e293b', zorder=5)
        ax.plot(x, y - 0.55, 'o', markersize=9, color='white', zorder=6)
        ax.plot(x, y - 0.55, 'o', markersize=5, color='#1e293b', zorder=7)
        ax.annotate('', xy=(x, y - 0.45), xytext=(x, y - 0.4),
                    arrowprops=dict(arrowstyle='->', color='#1e293b', lw=1.5))

    # Legend
    colours = [('#3b82f6','Applied'),('#ca8a04','Under Review'),('#7c3aed','Shortlisted'),
               ('#ea580c','Interview'),('#16a34a','Hired'),('#dc2626','Rejected')]
    for i, (c, l) in enumerate(colours):
        ax.add_patch(FancyBboxPatch((0.3 + i*2.2, 0.2), 0.3, 0.3, boxstyle="round,pad=0.05",
                                    facecolor=c, edgecolor=c))
        ax.text(0.7 + i*2.2, 0.35, l, fontsize=8, va='center', color='#374151')

    save(fig, '05_state_diagram.png')

# ─── Diagram 6: ER Diagram ────────────────────────────────────────────────────
def diagram_06():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    fig.patch.set_facecolor('#f8fafc')
    ax.set_xlim(0, 16); ax.set_ylim(0, 10); ax.axis('off')
    ax.set_title('SkillBridge — Entity-Relationship (ER) Diagram', fontsize=18, fontweight='bold', pad=20, color='#1e293b')

    def entity(ax, x, y, title, attrs, color='#3b82f6', w=3.2):
        h_total = 0.6 + len(attrs) * 0.45 + 0.2
        r = FancyBboxPatch((x, y - h_total), w, h_total, boxstyle="round,pad=0.1", linewidth=2,
                            edgecolor=color, facecolor='white', zorder=3)
        ax.add_patch(r)
        header = FancyBboxPatch((x, y - 0.65), w, 0.55, boxstyle="round,pad=0.05", linewidth=0,
                                 edgecolor=color, facecolor=color, zorder=4)
        ax.add_patch(header)
        ax.text(x + w/2, y - 0.37, title, ha='center', va='center', fontsize=11,
                fontweight='bold', color='white', zorder=5)
        for i, attr in enumerate(attrs):
            is_pk = attr.startswith('PK')
            is_fk = attr.startswith('FK')
            fc = '#fef9c3' if is_pk else ('#fce7f3' if is_fk else 'white')
            attr_rect = FancyBboxPatch((x + 0.05, y - 0.7 - (i+1)*0.45 + 0.05), w - 0.1, 0.38,
                                        boxstyle="round,pad=0.02", linewidth=0.5, edgecolor='#e2e8f0',
                                        facecolor=fc, zorder=4)
            ax.add_patch(attr_rect)
            ax.text(x + 0.2, y - 0.7 - (i+1)*0.45 + 0.24, attr, va='center', fontsize=8,
                    color='#1e293b', zorder=5, fontweight='bold' if is_pk else 'normal')

    def rel(ax, x1, y1, x2, y2, label, card1='1', card2='N'):
        ax.plot([x1, x2], [y1, y2], '-', color='#94a3b8', lw=2, zorder=2)
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my + 0.2, label, ha='center', fontsize=8, color='#475569',
                style='italic', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='#e2e8f0'))
        ax.text(x1, y1 + 0.15, card1, fontsize=10, ha='center', color='#0d6efd', fontweight='bold')
        ax.text(x2, y2 + 0.15, card2, fontsize=10, ha='center', color='#dc2626', fontweight='bold')

    # Entities
    entity(ax, 1.0, 9.5, 'User',
           ['PK  Id : int', '     FullName : string', '     Email : string', '     PasswordHash : string',
            '     Role : string', '     IsActive : bool', '     CreatedAt : DateTime'],
           '#0d6efd')

    entity(ax, 6.5, 9.5, 'Job',
           ['PK  Id : int', '     Title : string', '     Description : text', '     Company : string',
            '     Location : string', '     SalaryMin : decimal', '     SalaryMax : decimal',
            '     Deadline : DateTime', '     JobType : string', 'FK  PostedById : int'],
           '#7c3aed')

    entity(ax, 12.0, 9.5, 'CandidateProfile',
           ['PK  Id : int', 'FK  UserId : int', '     FullName : string',
            '     Experience : text', '     Skills : string', '     Education : string',
            '     ResumePath : string'],
           '#16a34a')

    entity(ax, 6.5, 3.8, 'Application',
           ['PK  Id : int', 'FK  JobId : int', 'FK  UserId : int', '     Status : string',
            '     AppliedAt : DateTime', '     CoverLetter : text', '     TailoredResumePath : string',
            '     IsActive : bool'],
           '#dc2626')

    # Relationships
    rel(ax, 3.7, 7.5, 5.8, 7.5, 'posts', '1', 'N')
    rel(ax, 4.2, 6.0, 7.2, 4.5, 'submits', '1', 'N')
    rel(ax, 9.6, 7.5, 11.3, 7.5, 'has', '1', '0..1')
    rel(ax, 8.0, 6.2, 8.0, 4.7, 'receives', '1', 'N')

    save(fig, '06_er_diagram.png')

# ─── Diagram 7: DFD Level 0 ───────────────────────────────────────────────────
def diagram_07():
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor('#f8fafc')
    ax.set_xlim(0, 14); ax.set_ylim(0, 8); ax.axis('off')
    ax.set_title('SkillBridge — DFD Level 0 (Context Diagram)', fontsize=16, fontweight='bold', pad=20, color='#1e293b')

    def ext_entity(ax, x, y, label, color='#374151'):
        r = FancyBboxPatch((x - 1.3, y - 0.5), 2.6, 1.0, boxstyle="square,pad=0.1", linewidth=2.5,
                            edgecolor=color, facecolor='#f1f5f9', zorder=3)
        ax.add_patch(r)
        ax.text(x, y, label, ha='center', va='center', fontsize=11, fontweight='bold', color=color, zorder=4)

    def system(ax, x, y, label):
        e = mpatches.Ellipse((x, y), 4.5, 2.5, linewidth=2.5, edgecolor='#0d6efd', facecolor='#dbeafe', zorder=3)
        ax.add_patch(e)
        ax.text(x, y + 0.2, label, ha='center', va='center', fontsize=12, fontweight='bold', color='#1e40af', zorder=4)
        ax.text(x, y - 0.35, 'SkillBridge Job Portal', ha='center', va='center', fontsize=9, color='#3b82f6', zorder=4)

    def arr(ax, x1, y1, x2, y2, label, color='#3b82f6'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.8))
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my + 0.18, label, ha='center', fontsize=8, color='#475569', style='italic',
                bbox=dict(boxstyle='round,pad=0.1', facecolor='white', edgecolor='#e2e8f0', alpha=0.9))

    ext_entity(ax, 1.5, 6.0, 'Admin', '#1e40af')
    ext_entity(ax, 1.5, 2.0, 'Candidate', '#16a34a')
    system(ax, 7.0, 4.0, '0.0 SkillBridge\nSystem')

    # Data store
    ax.plot([9.5, 12.5], [1.8, 1.8], '-', color='#374151', lw=2)
    ax.plot([9.5, 9.5], [1.4, 1.8], '-', color='#374151', lw=2)
    ax.plot([12.5, 12.5], [1.4, 1.8], '-', color='#374151', lw=2)
    ax.text(11.0, 1.6, 'D: MySQL Database', ha='center', fontsize=10, fontweight='bold', color='#374151')

    # Arrows Admin
    arr(ax, 2.8, 6.0, 4.8, 5.0, 'Job data, Status decisions,\nLogin credentials', '#1e40af')
    arr(ax, 4.8, 4.2, 2.8, 5.6, 'App lists, Reports,\nConfirmations', '#1e40af')

    # Arrows Candidate
    arr(ax, 2.8, 2.2, 4.8, 3.0, 'Registration, Profile,\nApplication data', '#16a34a')
    arr(ax, 4.8, 3.4, 2.8, 2.6, 'Job listings, App status,\nRecommendations', '#16a34a')

    # Data store arrows
    arr(ax, 8.5, 3.2, 9.8, 2.0, 'Read / Write', '#374151')
    arr(ax, 9.8, 1.8, 8.5, 2.9, 'Data results', '#374151')

    save(fig, '07_dfd_level0.png')

# ─── Diagram 8: DFD Level 1 ───────────────────────────────────────────────────
def diagram_08():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H + 1))
    fig.patch.set_facecolor('#f8fafc')
    ax.set_xlim(0, 16); ax.set_ylim(0, 11); ax.axis('off')
    ax.set_title('SkillBridge — DFD Level 1 (First-Level Decomposition)', fontsize=16, fontweight='bold', pad=20, color='#1e293b')

    def proc(ax, x, y, label, num, color='#3b82f6'):
        e = mpatches.Ellipse((x, y), 3.2, 1.2, linewidth=2, edgecolor=color, facecolor=color, alpha=0.85, zorder=3)
        ax.add_patch(e)
        ax.text(x, y + 0.15, f'{num}', ha='center', va='center', fontsize=8, fontweight='bold', color='white', zorder=4)
        ax.text(x, y - 0.2, label, ha='center', va='center', fontsize=8, color='white', zorder=4)

    def store(ax, x, y, label, w=3.0):
        ax.plot([x, x + w], [y, y], '-', color='#374151', lw=2, zorder=3)
        ax.plot([x, x], [y - 0.5, y], '-', color='#374151', lw=2, zorder=3)
        ax.plot([x + w, x + w], [y - 0.5, y], '-', color='#374151', lw=2, zorder=3)
        ax.text(x + w/2, y - 0.25, label, ha='center', fontsize=9, fontweight='bold', color='#374151', zorder=4)

    def ext(ax, x, y, label, w=2.0, h=0.8):
        r = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="square,pad=0.05", linewidth=2,
                            edgecolor='#374151', facecolor='#f1f5f9', zorder=3)
        ax.add_patch(r)
        ax.text(x, y, label, ha='center', va='center', fontsize=10, fontweight='bold', color='#374151', zorder=4)

    def arr(ax, x1, y1, x2, y2, label=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#6b7280', lw=1.3))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx + 0.1, my + 0.12, label, fontsize=7, color='#475569', style='italic')

    ext(ax, 1.3, 8.0, 'Admin')
    ext(ax, 1.3, 3.0, 'Candidate')

    proc(ax, 5.5, 9.0, 'Authentication', '1.0', '#6366f1')
    proc(ax, 9.5, 9.0, 'Job Management', '2.0', '#0d6efd')
    proc(ax, 5.5, 5.5, 'Application Mgmt', '3.0', '#16a34a')
    proc(ax, 9.5, 5.5, 'Profile Management', '4.0', '#7c3aed')
    proc(ax, 7.5, 2.0, 'Reporting', '5.0', '#d97706')

    store(ax, 11.5, 9.5, 'D1: Users', 3.0)
    store(ax, 11.5, 7.0, 'D2: Jobs', 3.0)
    store(ax, 11.5, 4.5, 'D3: Applications', 3.5)
    store(ax, 11.5, 2.0, 'D4: CandidateProfiles', 4.0)

    # Arrows
    arr(ax, 2.3, 8.2, 4.0, 9.0, 'Login/Register')
    arr(ax, 2.3, 7.8, 4.0, 8.5, 'Credentials')
    arr(ax, 2.3, 8.0, 4.0, 5.5, 'Job CRUD')
    arr(ax, 2.3, 3.0, 4.0, 5.3, 'Apply / Track')
    arr(ax, 2.3, 2.8, 4.0, 5.3, 'Profile Data')
    arr(ax, 6.9, 9.0, 11.5, 9.5, 'User R/W')
    arr(ax, 10.8, 9.0, 11.5, 7.3, 'Job R/W')
    arr(ax, 6.9, 5.5, 11.5, 4.8, 'App R/W')
    arr(ax, 10.8, 5.5, 11.5, 2.3, 'Profile R/W')
    arr(ax, 7.5, 2.6, 11.5, 7.2, 'Stats Queries')
    arr(ax, 2.3, 7.5, 6.5, 2.3, 'Report Request')

    save(fig, '08_dfd_level1.png')

# ─── Diagram 9: UML Class Diagram ────────────────────────────────────────────
def diagram_09():
    fig, ax = plt.subplots(figsize=(20, 14))
    fig.patch.set_facecolor('#f8fafc')
    ax.set_xlim(0, 20); ax.set_ylim(0, 14); ax.axis('off')
    ax.set_title('SkillBridge — UML Class Diagram', fontsize=18, fontweight='bold', pad=20, color='#1e293b')

    def uml_class(ax, x, y, name, attrs, methods=[], color='#3b82f6', stereotype='', w=3.8):
        row_h = 0.42
        h = 0.65 + (0.35 if stereotype else 0) + len(attrs) * row_h + (0.5 if methods else 0) + len(methods) * row_h
        r = FancyBboxPatch((x, y - h), w, h, boxstyle="square,pad=0", linewidth=2,
                            edgecolor=color, facecolor='white', zorder=3)
        ax.add_patch(r)
        # header
        header_h = 0.6 + (0.3 if stereotype else 0)
        hdr = FancyBboxPatch((x, y - header_h), w, header_h, boxstyle="square,pad=0",
                              linewidth=0, edgecolor=color, facecolor=color, zorder=4)
        ax.add_patch(hdr)
        if stereotype:
            ax.text(x + w/2, y - 0.2, f'«{stereotype}»', ha='center', fontsize=7, color='white', style='italic', zorder=5)
        ax.text(x + w/2, y - (0.45 if stereotype else 0.32), name, ha='center', va='center',
                fontsize=10, fontweight='bold', color='white', zorder=5)
        # divider
        div_y = y - header_h
        ax.plot([x, x + w], [div_y, div_y], '-', color=color, lw=1.5, zorder=4)
        for i, attr in enumerate(attrs):
            ax.text(x + 0.15, div_y - (i + 0.5) * row_h, attr, fontsize=7.5, va='center', color='#374151', zorder=5)
        if methods:
            div2_y = div_y - len(attrs) * row_h
            ax.plot([x, x + w], [div2_y, div2_y], '-', color=color, lw=1, alpha=0.5, zorder=4)
            for i, m in enumerate(methods):
                ax.text(x + 0.15, div2_y - (i + 0.5) * row_h, m, fontsize=7, va='center',
                        color='#374151', style='italic', zorder=5)

    def inherit_arrow(ax, x1, y1, x2, y2):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='-|>', color='#374151', lw=1.5,
                                   mutation_scale=15, facecolor='white'))

    def assoc_arrow(ax, x1, y1, x2, y2, label=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#6b7280', lw=1.2))
        if label:
            ax.text((x1+x2)/2, (y1+y2)/2 + 0.15, label, fontsize=7, color='#475569', ha='center')

    def impl_arrow(ax, x1, y1, x2, y2):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='-|>', color='#9333ea', lw=1.5,
                                   linestyle='dashed', mutation_scale=15, facecolor='white'))

    # Classes
    uml_class(ax, 7.5, 13.5, 'BaseEntity', ['+ Id : int', '+ CreatedAt : DateTime', '+ IsActive : bool'],
              [], '#374151', 'abstract')

    uml_class(ax, 7.5, 11.0, 'User', ['+ FullName : string', '+ Email : string', '+ PasswordHash : string', '+ Role : string'],
              ['+ SignUp() : void', '+ SignIn(email, pwd) : bool', '+ Logout() : void'], '#0d6efd')

    uml_class(ax, 3.0, 7.5, 'Candidate', ['+ Profile : CandidateProfile'],
              ['+ SetupProfile() : void', '+ ApplyForJob() : Application', '+ GetRecommendedJobs() : List<Job>'], '#16a34a')

    uml_class(ax, 11.5, 7.5, 'Admin', [],
              ['+ CreateJob(job) : void', '+ UpdateJob(job) : void', '+ DeleteJob(id) : void', '+ ProcessApplication() : void'], '#dc2626')

    uml_class(ax, 7.0, 7.5, 'Job', ['+ Title : string', '+ Company : string', '+ Location : string', '+ SalaryMin : decimal', '+ SalaryMax : decimal', '+ Deadline : DateTime', '+ JobType : string'],
              [], '#7c3aed')

    uml_class(ax, 0.2, 3.5, 'CandidateProfile', ['+ UserId : int', '+ FullName : string', '+ Skills : string', '+ Experience : string', '+ Education : string'],
              ['+ GetCompletionPct() : int'], '#0f766e')

    uml_class(ax, 11.0, 3.5, 'Application', ['+ JobId : int', '+ UserId : int', '+ Status : string', '+ CoverLetter : string'],
              ['+ ApplyJob() : void', '+ UpdateStatus(s) : void'], '#ca8a04')

    uml_class(ax, 0.3, 13.5, 'IJobService', ['+ CreateJob(job) : Task<Job>', '+ UpdateJob(job) : Task<Job>', '+ DeleteJob(id) : Task<bool>', '+ GetAllJobs() : Task<List<Job>>'],
              [], '#6366f1', 'interface', 3.5)

    uml_class(ax, 15.5, 13.5, 'IApplicationService', ['+ SubmitApp(app) : Task<App>', '+ UpdateStatus() : Task<bool>', '+ GetByUser(id) : Task<List<App>>'],
              [], '#6366f1', 'interface', 4.0)

    uml_class(ax, 0.3, 10.0, 'JobService', [], ['implements IJobService'], '#6366f1', '', 3.5)
    uml_class(ax, 15.5, 10.0, 'ApplicationService', [], ['implements IApplicationService'], '#6366f1', '', 4.0)

    # Arrows
    # Inheritance: User → BaseEntity
    inherit_arrow(ax, 9.4, 11.0, 9.4, 12.7)
    # Candidate, Admin → User
    inherit_arrow(ax, 4.8, 7.5, 7.5, 9.8)
    inherit_arrow(ax, 13.4, 7.5, 11.9, 9.8)
    # Job, CandidateProfile, Application → BaseEntity
    inherit_arrow(ax, 8.9, 7.5, 9.4, 12.7)
    inherit_arrow(ax, 2.0, 3.5, 8.8, 12.7)
    inherit_arrow(ax, 12.9, 3.5, 9.6, 12.7)
    # Associations
    assoc_arrow(ax, 11.0, 2.0, 7.0, 6.2, 'applies for')
    assoc_arrow(ax, 11.0, 2.5, 2.0, 3.0, 'submitted by')
    assoc_arrow(ax, 4.0, 6.2, 2.0, 4.4, 'has profile')
    # Implementation arrows
    impl_arrow(ax, 2.0, 10.0, 2.0, 12.7)
    impl_arrow(ax, 17.5, 10.0, 17.5, 12.7)

    save(fig, '09_class_diagram.png')

# ─── Diagram 10: MVC Architecture ────────────────────────────────────────────
def diagram_10():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    fig.patch.set_facecolor('#f8fafc')
    ax.set_xlim(0, 16); ax.set_ylim(0, 9); ax.axis('off')
    ax.set_title('SkillBridge — MVC Architecture Diagram', fontsize=18, fontweight='bold', pad=20, color='#1e293b')

    def layer(ax, x, y, w, h, title, items, hcolor, bcolor):
        r = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2", linewidth=2.5,
                            edgecolor=hcolor, facecolor=bcolor, alpha=0.15, zorder=1)
        ax.add_patch(r)
        ax.text(x + w/2, y + h - 0.4, title, ha='center', va='center',
                fontsize=13, fontweight='bold', color=hcolor)
        for i, item in enumerate(items):
            iy = y + h - 1.0 - i * 0.65
            r2 = FancyBboxPatch((x + 0.3, iy - 0.22), w - 0.6, 0.48, boxstyle="round,pad=0.05",
                                 linewidth=1, edgecolor=hcolor, facecolor='white', alpha=0.9, zorder=2)
            ax.add_patch(r2)
            ax.text(x + w/2, iy + 0.02, item, ha='center', va='center', fontsize=8.5, color='#1e293b', zorder=3)

    model_items = ['User.cs', 'Job.cs', 'Application.cs', 'CandidateProfile.cs',
                   'SkillBridgeDbContext.cs', 'IJobRepository', 'IApplicationRepository']
    ctrl_items = ['AuthController', 'JobController', 'ApplicationController',
                  'AdminController', 'UserController']
    view_items = ['LandingPage.tsx', 'LoginPage.tsx', 'Register.tsx', 'JobDetail.tsx',
                  'AdminDashboard.tsx', 'CandidateDashboard.tsx', 'AdminApplications.tsx']

    layer(ax, 0.5, 0.5, 4.5, 8.0, '📦 Model Layer', model_items, '#0d6efd', '#dbeafe')
    layer(ax, 5.8, 0.5, 4.4, 8.0, '⚙️ Controller Layer', ctrl_items, '#7c3aed', '#f3e8ff')
    layer(ax, 10.9, 0.5, 4.6, 8.0, '🖥️ View Layer', view_items, '#16a34a', '#dcfce7')

    def arr(ax, x1, y1, x2, y2, label, color='#374151'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='<->', color=color, lw=2.0))
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.25, label, ha='center', fontsize=8.5, color=color, fontweight='bold')

    arr(ax, 5.0, 5.0, 5.8, 5.0, 'EF Core', '#0d6efd')
    arr(ax, 10.2, 5.0, 10.9, 5.0, 'ViewModel', '#7c3aed')

    # Browser
    browser = FancyBboxPatch((-0.1, 3.8), 1.1, 1.4, boxstyle="round,pad=0.1", linewidth=2,
                              edgecolor='#374151', facecolor='#f1f5f9', zorder=3)
    ax.add_patch(browser)
    ax.text(0.45, 4.5, '🌐\nBrowser', ha='center', va='center', fontsize=9, fontweight='bold', color='#374151')
    ax.annotate('', xy=(0.5, 4.5), xytext=(5.8, 4.5),
                arrowprops=dict(arrowstyle='<->', color='#374151', lw=1.5))
    ax.text(3.1, 4.7, 'HTTP', ha='center', fontsize=8, color='#374151')

    # DB
    db = mpatches.Ellipse((15.4, 1.2), 1.0, 0.5, linewidth=2, edgecolor='#374151', facecolor='#f1f5f9', zorder=3)
    ax.add_patch(db)
    ax.text(15.4, 1.2, '🗄️ DB', ha='center', va='center', fontsize=8, fontweight='bold', color='#374151')
    ax.annotate('', xy=(15.0, 1.2), xytext=(10.9, 1.2),
                arrowprops=dict(arrowstyle='<->', color='#374151', lw=1.5))
    ax.text(12.8, 1.45, 'SQL', ha='center', fontsize=8, color='#374151')

    save(fig, '10_mvc_architecture.png')

# ─── Diagram 11: Trello Board Mockup ─────────────────────────────────────────
def diagram_11():
    fig, ax = plt.subplots(figsize=(20, 11))
    fig.patch.set_facecolor('#026aa7')
    ax.set_xlim(0, 20); ax.set_ylim(0, 11); ax.axis('off')
    ax.set_title('SkillBridge — Unit 22 Development Board  (Trello Kanban)', fontsize=16,
                 fontweight='bold', pad=15, color='white')

    columns = [
        ('📋 Backlog', '#b3bec4', ['Research ASP.NET Core MVC', 'Design database schema',
                                    'Create wireframes in Figma', 'Set up Docker MySQL'],
         ['#ef4444', '#f59e0b', '#f59e0b', '#10b981']),
        ('🚀 Sprint 1\nApr 20–May 3', '#63b3ed', ['Project initialisation (.NET setup)', 'Docker Compose for SQL Server',
                                                     'Database models + EF Core', 'Initial migration'],
         ['#ef4444', '#ef4444', '#f59e0b', '#10b981']),
        ('🔐 Sprint 2\nMay 4–17', '#63b3ed', ['User registration endpoint', 'Login/logout with JWT',
                                                'Password hashing (BCrypt)', 'Role-based access control'],
         ['#ef4444', '#ef4444', '#f59e0b', '#10b981']),
        ('💼 Sprint 3\nMay 18–31', '#63b3ed', ['Job CRUD (Admin)', 'Public job listing page',
                                                  'Search & filter + pagination', 'Soft-delete feature'],
         ['#ef4444', '#f59e0b', '#f59e0b', '#f59e0b']),
        ('👤 Sprint 4\nJun 1–14', '#63b3ed', ['Candidate profile setup', 'CV/resume upload feature',
                                                 'Job application form', 'Application tracking view'],
         ['#ef4444', '#ef4444', '#f59e0b', '#f59e0b']),
        ('📊 Sprint 5\nJun 15–28', '#63b3ed', ['Admin dashboard stats', 'Application status workflow',
                                                  'AI recommendation prototype', 'UI polish + responsive'],
         ['#ef4444', '#f59e0b', '#f59e0b', '#f59e0b']),
        ('✅ Done', '#48bb78', ['Requirements analysis', 'Software design document',
                                 'GitHub repository setup', 'Database schema finalised'],
         ['#10b981', '#10b981', '#10b981', '#10b981']),
    ]

    col_w = 2.6
    for ci, (title, hcolor, cards, label_colors) in enumerate(columns):
        cx = 0.5 + ci * 2.75
        col_rect = FancyBboxPatch((cx, 0.3), col_w, 10.2, boxstyle="round,pad=0.1", linewidth=0,
                                   edgecolor='none', facecolor='#e2e8f0', zorder=1, alpha=0.15)
        ax.add_patch(col_rect)
        # Column header
        hdr = FancyBboxPatch((cx, 9.5), col_w, 0.9, boxstyle="round,pad=0.1", linewidth=0,
                              edgecolor='none', facecolor=hcolor, alpha=0.25, zorder=2)
        ax.add_patch(hdr)
        ax.text(cx + col_w/2, 9.95, title, ha='center', va='center', fontsize=8.5,
                fontweight='bold', color='white', zorder=3)

        for ri, (card, lc) in enumerate(zip(cards, label_colors)):
            cy = 9.0 - ri * 2.1
            card_rect = FancyBboxPatch((cx + 0.1, cy - 1.6), col_w - 0.2, 1.7, boxstyle="round,pad=0.1",
                                        linewidth=1, edgecolor='#cbd5e0', facecolor='white', zorder=2)
            ax.add_patch(card_rect)
            label_bar = FancyBboxPatch((cx + 0.15, cy - 0.3), 0.7, 0.22, boxstyle="round,pad=0.05",
                                        linewidth=0, edgecolor='none', facecolor=lc, zorder=3)
            ax.add_patch(label_bar)
            ax.text(cx + col_w/2, cy - 0.85, card, ha='center', va='center', fontsize=7.5,
                    color='#1e293b', zorder=3, wrap=True,
                    bbox=dict(boxstyle='round,pad=0.0', facecolor='none', edgecolor='none'))

    ax.text(10.0, 0.15, '🟥 High Priority  🟨 Medium Priority  🟩 Done / Low Priority',
            ha='center', fontsize=9, color='white', alpha=0.8)
    save(fig, '11_trello_board.png')

# ─── Run all ──────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("Generating SkillBridge diagrams...")
    diagram_01()
    diagram_02()
    diagram_03()
    diagram_04()
    diagram_05()
    diagram_06()
    diagram_07()
    diagram_08()
    diagram_09()
    diagram_10()
    diagram_11()
    print("\n✅ All 11 diagrams generated successfully in ./diagrams/")
