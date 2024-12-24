
import json
from playwright.sync_api import sync_playwright

base_url = 'https://github.com/topics/playwright'

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    # Create a new browser context
    context = browser.new_context(
        # set a custom user agent
        user_agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        viewport = {"width": 800, "height": 600},  # set the viewport size
        bypass_csp = True,  # Optionally bypass Content Security Policy
    )
    
    try:
        page = context.new_page()
        page.goto(base_url)
        
        # Get data from website
        repo_cards = page.query_selector_all("article.border")
        repositories = []
        
        for card in repo_cards:
            user, repo = card.query_selector_all('h3 a')
            format_text = lambda element: element.inner_text().strip() if element else None
            
            repository = {
                "user": format_text(user),
                "repo": format_text(repo),
                "url": repo.get_attribute('href'),
            }
            repositories.append(repository)
        
        # Move file operations and printing outside the loop
        print(repositories)
        json_data = json.dumps(repositories, indent=4)
        with open("data.txt", "w") as file:
            file.write(json_data)
            
    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)