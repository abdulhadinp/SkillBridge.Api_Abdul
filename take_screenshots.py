import os
import asyncio
from playwright.async_api import async_playwright

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Use full HD viewport
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        print("Navigating to Landing Page...")
        await page.goto("http://localhost:5173/")
        # wait a bit for images to load
        await page.wait_for_timeout(2000)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "01_LandingPage.png"), full_page=True)

        print("Navigating to Login Page...")
        await page.goto("http://localhost:5173/login")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "02_LoginPage.png"), full_page=True)

        print("Navigating to Register Page...")
        await page.goto("http://localhost:5173/register")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "03_RegisterPage.png"), full_page=True)

        # Login as Admin
        print("Logging in as Admin...")
        await page.goto("http://localhost:5173/login")
        await page.fill('input[type="email"]', 'admin@skillbridge.com')
        await page.fill('input[type="password"]', 'Admin@123')
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(2000)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "04_AdminDashboard.png"), full_page=True)

        print("Admin Create Job...")
        await page.goto("http://localhost:5173/admin/create-job")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "05_AdminCreateJob.png"), full_page=True)

        print("Admin Applications...")
        await page.goto("http://localhost:5173/admin/applications")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "06_AdminApplications.png"), full_page=True)

        # Logout Admin
        print("Logging out Admin...")
        # Since logout is a button in navbar or dropdown, we might need to click it. Or just clear localstorage.
        await page.evaluate("localStorage.removeItem('token'); localStorage.removeItem('user');")
        await page.goto("http://localhost:5173/login")
        await page.wait_for_timeout(1000)

        # Login as Candidate
        print("Logging in as Candidate...")
        await page.fill('input[type="email"]', 'candidate1@example.com')
        await page.fill('input[type="password"]', 'Candidate@123')
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(2000)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "07_CandidateDashboard.png"), full_page=True)

        print("Candidate Profile...")
        await page.goto("http://localhost:5173/candidate/profile")
        await page.wait_for_timeout(1500)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "08_CandidateProfile.png"), full_page=True)

        print("Candidate Track Applications...")
        await page.goto("http://localhost:5173/candidate/applications")
        await page.wait_for_timeout(1500)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "09_TrackApplications.png"), full_page=True)

        print("Job Details Page...")
        await page.goto("http://localhost:5173/jobs/1")
        await page.wait_for_timeout(1500)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "10_JobDetails.png"), full_page=True)

        print("Apply Job Page...")
        await page.goto("http://localhost:5173/jobs/1/apply")
        await page.wait_for_timeout(1500)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "11_ApplyJob.png"), full_page=True)
        
        await browser.close()
        print("All screenshots generated successfully.")

asyncio.run(run())
