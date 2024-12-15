from dash.testing.application_runners import import_app
from selenium import webdriver

link = "https://accounts.google.com"
driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
driver.get(link)


def test_bbaaa001(dash_duo):
    app = import_app("dash_test.app")
    dash_duo.start_server(app)

    dash_duo.wait_for_text_to_equal("h1", "Europe Climate Extremes", timeout=10)

    assert dash_duo.get_logs() == [], "Browser console should contain no error"

    return None
