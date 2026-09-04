from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def test_home_page():

    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("http://localhost:3000/")

        print("Page title:", driver.title)
        print("Current URL:", driver.current_url)

        assert driver.current_url == "http://localhost:3000/"

    finally:
        driver.quit()


if __name__ == "__main__":
    test_home_page()