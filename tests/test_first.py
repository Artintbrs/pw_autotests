import pytest
from playwright.sync_api import Page, expect
import steps.base_steps as steps

@pytest.mark.parametrize("param", [
    10**7,
    1.5*10**7,
    100,
    5*10**7,
    10**8,
    5*10**8,
    10**9,
    1.5*10**9
])
def test_wiki(page: Page, param):
    wiki_data = steps.get_data_wiki_table(page)
    steps.check_unique_visitors_for_data_table(wiki_data, param)

