# # automation.py
# import re
# from playwright.async_api import async_playwright

# async def submit_student_feedback(reg_no: str, password: str, status_callback=None):
#     """
#     Automates the feedback submission. 
#     status_callback is an optional function to report progress to the frontend.
#     """
#     async def log(message: str):
#         if status_callback:
#             await status_callback(message)
#         print(message)

#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         context = await browser.new_context()
#         page = await context.new_page()

#         try:
#             await log("Navigating to dashboard...")
#             await page.goto("https://adamasknowledgecity.ac.in/student/dashboard")

#             await page.get_by_role("textbox", name="Registration No.").fill(reg_no)
#             await page.get_by_role("textbox", name="Password").fill(password)
#             await page.get_by_role("button", name="Login").click()
#             await page.wait_for_timeout(3000)

#             # Validate login success
#             if "dashboard" not in page.url:
#                 await log("Error: Invalid credentials or login failed.")
#                 await browser.close()
#                 return False

#             await log("Login successful. Starting feedback submission...")

#             subjects = [
#                 "Computer Networks", "Computer Organization and Architecture",
#                 "Software Engineering", "Computer Networks Lab",
#                 "Computer Organization and Architecture Lab", "Software Engineering Lab",
#                 "Mini Project-II", "Domain Specific Predictive Analysis",
#                 "Unstructured Databases", "Introduction to Python Programming"
#             ]

#             for subject in subjects:
#                 await log(f"Processing subject: {subject}")
#                 temp = 1
                
#                 while True:
#                     try:
#                         heading = page.get_by_role("heading", name=subject, exact=True)
#                         if await heading.count() == 0:
#                             await log(f"Subject not found: {subject}")
#                             break

#                         await heading.click()
#                         await page.wait_for_timeout(2000)

#                         locator = page.get_by_text("Pending Feedback", exact=False)
#                         if await locator.count() == 0:
#                             break

#                         text = await locator.first.inner_text()
#                         match = re.search(r"\d+", text)
#                         pending_count = int(match.group()) if match else 0

#                         if pending_count < 1:
#                             got_it_btn = page.get_by_text("Got it")
#                             if await got_it_btn.count() > 0:
#                                 await got_it_btn.click()
#                             break
#                         elif pending_count == 1:
#                             await page.get_by_text("Give Feedback", exact=True).click()
#                         else:
#                             await page.get_by_text("Give Feedback").nth(temp).click()

#                         await page.wait_for_timeout(2000)

#                         # Check for error toast
#                         if await page.get_by_text("×Feedback ErrorNo classes").count() > 0:
#                             if temp >= 2:
#                                 break
#                             temp += 1
#                             continue

#                         await page.locator("#yes_0_0").check()
#                         await page.locator("#yes_0_4").check()
#                         await page.get_by_role("button", name=" Submit Feedback").click()
#                         await page.wait_for_timeout(2000)

#                     except Exception as e:
#                         await log(f"Warning during {subject}: {str(e)}")
#                         break

#                 await log(f"Completed: {subject}")

#             await log("Logging out...")
#             logout_btn = page.get_by_role("link", name=" Logout")
#             if await logout_btn.count() > 0:
#                 await logout_btn.click()

#             await log("All feedback processing complete!")
#             return True

#         except Exception as e:
#             await log(f"Fatal error: {str(e)}")
#             return False
#         finally:
#             await browser.close()



# import re

# from playwright.async_api import async_playwright


# async def submit_student_feedback(
#     reg_no: str,
#     password: str,
#     status_callback=None
# ):

#     async def log(message: str):

#         if status_callback:

#             await status_callback(message)

#         print(message)


#     async with async_playwright() as p:

#         browser = None

#         try:

#             await log(
#                 "Starting Playwright..."
#             )

#             browser = await p.chromium.launch(
#                 headless=True
#             )

#             context = await browser.new_context()

#             page = await context.new_page()


#             await log(
#                 "Navigating to dashboard..."
#             )

#             await page.goto(
#                 "https://adamasknowledgecity.ac.in/student/dashboard",
#                 wait_until="domcontentloaded"
#             )


#             await log(
#                 "Entering credentials..."
#             )


#             await page.get_by_role(
#                 "textbox",
#                 name="Registration No."
#             ).fill(reg_no)


#             await page.get_by_role(
#                 "textbox",
#                 name="Password"
#             ).fill(password)


#             await page.get_by_role(
#                 "button",
#                 name="Login"
#             ).click()


#             await page.wait_for_timeout(3000)


#             # Validate login
#             if "dashboard" not in page.url:

#                 await log(
#                     "Error: Invalid credentials or login failed."
#                 )

#                 return False


#             await log(
#                 "Login successful. Starting feedback submission..."
#             )


#             subjects = [

#                 "Computer Networks",

#                 "Computer Organization and Architecture",

#                 "Software Engineering",

#                 "Computer Networks Lab",

#                 "Computer Organization and Architecture Lab",

#                 "Software Engineering Lab",

#                 "Mini Project-II",

#                 "Domain Specific Predictive Analysis",

#                 "Unstructured Databases",

#                 "Introduction to Python Programming"

#             ]


#             for subject in subjects:

#                 await log(
#                     f"Processing subject: {subject}"
#                 )


#                 temp = 1


#                 while True:

#                     try:

#                         heading = page.get_by_role(
#                             "heading",
#                             name=subject,
#                             exact=True
#                         )


#                         if await heading.count() == 0:

#                             await log(
#                                 f"Subject not found: {subject}"
#                             )

#                             break


#                         await heading.click()

#                         await page.wait_for_timeout(2000)


#                         locator = page.get_by_text(
#                             "Pending Feedback",
#                             exact=False
#                         )


#                         if await locator.count() == 0:

#                             break


#                         text = await locator.first.inner_text()


#                         match = re.search(
#                             r"\d+",
#                             text
#                         )


#                         pending_count = (
#                             int(match.group())
#                             if match
#                             else 0
#                         )


#                         if pending_count < 1:

#                             got_it_btn = page.get_by_text(
#                                 "Got it"
#                             )


#                             if await got_it_btn.count() > 0:

#                                 await got_it_btn.click()


#                             break


#                         elif pending_count == 1:

#                             await page.get_by_text(
#                                 "Give Feedback",
#                                 exact=True
#                             ).click()


#                         else:

#                             await page.get_by_text(
#                                 "Give Feedback"
#                             ).nth(temp).click()


#                         await page.wait_for_timeout(2000)


#                         # Feedback error check
#                         error_toast = page.get_by_text(
#                             "×Feedback ErrorNo classes"
#                         )


#                         if await error_toast.count() > 0:

#                             if temp >= 2:

#                                 break

#                             temp += 1

#                             continue


#                         # Submit feedback
#                         await page.locator(
#                             "#yes_0_0"
#                         ).check()


#                         await page.locator(
#                             "#yes_0_4"
#                         ).check()


#                         await page.get_by_role(
#                             "button",
#                             name=" Submit Feedback"
#                         ).click()


#                         await page.wait_for_timeout(2000)


#                     except Exception as e:

#                         await log(
#                             f"Warning during {subject}: {str(e)}"
#                         )

#                         break


#                 await log(
#                     f"Completed: {subject}"
#                 )


#             await log(
#                 "Logging out..."
#             )


#             logout_btn = page.get_by_role(
#                 "link",
#                 name=" Logout"
#             )


#             if await logout_btn.count() > 0:

#                 await logout_btn.click()


#             await log(
#                 "All feedback processing complete!"
#             )


#             return True


#         except Exception as e:

#             await log(
#                 f"Fatal error: {str(e)}"
#             )

#             return False


#         finally:

#             if browser:

#                 await browser.close()





import re
from typing import List, Optional
from playwright.async_api import async_playwright

DEFAULT_SUBJECTS = [
    "Computer Networks",
    "Computer Organization and Architecture",
    "Software Engineering",
    "Computer Networks Lab",
    "Computer Organization and Architecture Lab",
    "Software Engineering Lab",
    "Mini Project-II",
    "Domain Specific Predictive Analysis",
    "Unstructured Databases",
    "Introduction to Python Programming"
]

async def submit_student_feedback(
    reg_no: str,
    password: str,
    subjects: Optional[List[str]] = None,
    status_callback=None
) -> bool:
    """
    Automates the feedback submission on the portal.
    """
    async def log(message: str, status_type: str = "info"):
        if status_callback:
            await status_callback({"message": message, "type": status_type})
        print(f"[{status_type.upper()}] {message}")

    target_subjects = [s.strip() for s in subjects if s.strip()] if subjects else DEFAULT_SUBJECTS

    async with async_playwright() as p:
        browser = None
        try:
            await log("Launching headless browser context...", "info")
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await log("Navigating to Adamas Student Portal...", "info")
            await page.goto("https://adamasknowledgecity.ac.in/student/dashboard", wait_until="domcontentloaded", timeout=30000)

            await log("Authenticating user...", "info")
            await page.get_by_role("textbox", name="Registration No.").fill(reg_no)
            await page.get_by_role("textbox", name="Password").fill(password)
            await page.get_by_role("button", name="Login").click()

            await page.wait_for_timeout(3000)

            if "dashboard" not in page.url:
                await log("Authentication failed: Invalid Registration No. or Password.", "error")
                return False

            await log("Login successful! Starting feedback evaluation pipeline...", "success")

            completed_count = 0
            failed_count = 0

            for subject in target_subjects:
                await log(f"Evaluating subject: '{subject}'", "info")
                temp = 1
                subject_success = False

                while True:
                    try:
                        heading = page.get_by_role("heading", name=subject, exact=True)
                        if await heading.count() == 0:
                            await log(f"Subject '{subject}' not found on active dashboard.", "warning")
                            break

                        await heading.click()
                        await page.wait_for_timeout(2000)

                        locator = page.get_by_text("Pending Feedback", exact=False)
                        if await locator.count() == 0:
                            await log(f"No pending feedback section found for '{subject}'.", "info")
                            break

                        text = await locator.first.inner_text()
                        match = re.search(r"\d+", text)
                        pending_count = int(match.group()) if match else 0

                        if pending_count < 1:
                            got_it_btn = page.get_by_text("Got it")
                            if await got_it_btn.count() > 0:
                                await got_it_btn.click()
                            await log(f"No pending feedback for '{subject}'.", "info")
                            subject_success = True
                            break
                        elif pending_count == 1:
                            await page.get_by_text("Give Feedback", exact=True).click()
                        else:
                            await page.get_by_text("Give Feedback").nth(temp).click()

                        await page.wait_for_timeout(2000)

                        # Error toast validation
                        error_toast = page.get_by_text("×Feedback ErrorNo classes")
                        if await error_toast.count() > 0:
                            if temp >= 2:
                                break
                            temp += 1
                            continue

                        # Execute radio button selection
                        await page.locator("#yes_0_0").check()
                        await page.locator("#yes_0_4").check()
                        await page.get_by_role("button", name=" Submit Feedback").click()
                        await page.wait_for_timeout(2000)

                        await log(f"Successfully submitted entry for '{subject}'.", "success")
                        subject_success = True

                    except Exception as sub_err:
                        await log(f"Error handling feedback for '{subject}': {str(sub_err)}", "warning")
                        failed_count += 1
                        break

                if subject_success:
                    completed_count += 1

            await log("Finalizing session & logging out safely...", "info")
            logout_btn = page.get_by_role("link", name=" Logout")
            if await logout_btn.count() > 0:
                await logout_btn.click()

            await log(f"Automation finished. Processed: {completed_count}, Issues: {failed_count}.", "success")
            return True

        except Exception as fatal_err:
            await log(f"Fatal execution failure: {str(fatal_err)}", "error")
            return False

        finally:
            if browser:
                await browser.close()