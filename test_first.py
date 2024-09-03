from playwright.sync_api import Page, expect

def test_wiki(page: Page):
    page.goto('https://en.wikipedia.org/wiki/Programming_languages_used_in_most_popular_websites')
    page.get_by_role('link', name='Website')
    expect(page.get_by_text('Popularity')).to_be_visible()