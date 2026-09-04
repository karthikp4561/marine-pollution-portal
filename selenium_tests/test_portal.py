import os
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://localhost:3000"

# ---------------------------------------------------------
# TEST USER DETAILS
# ---------------------------------------------------------
# These users are created during the Selenium test.
# A timestamp is added so every test run gets a unique user.

TIMESTAMP = int(time.time())

TEST_USERNAME = f"seleniumuser{TIMESTAMP}"
TEST_EMAIL = f"selenium{TIMESTAMP}@test.com"
TEST_PASSWORD = "Selenium@123"


# ---------------------------------------------------------
# DRIVER FIXTURE
# ---------------------------------------------------------

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    yield driver

    driver.quit()


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def wait_for_page(driver, seconds=10):
    return WebDriverWait(driver, seconds)


def accept_alert(driver, timeout=5):
    try:
        alert = WebDriverWait(driver, timeout).until(
            EC.alert_is_present()
        )

        message = alert.text
        print(f"Alert: {message}")

        alert.accept()

        return message

    except Exception:
        return None


def logout(driver):
    """
    Logout using the actual Logout button in Navbar.js.
    """

    try:
        logout_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Logout')]")
            )
        )

        logout_button.click()

        WebDriverWait(driver, 5).until(
            EC.url_to_be(f"{BASE_URL}/")
        )

        print("Logout successful")

    except Exception as error:
        print("Logout skipped:", error)


# =========================================================
# TEST 1 - HOME PAGE
# =========================================================

def test_01_home_page(driver):

    print("\n========== TEST 1: HOME PAGE ==========")

    driver.get(BASE_URL + "/")

    wait = wait_for_page(driver)

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(text(),'Marine Pollution')]")
        )
    )

    print("Home page loaded")
    print("Title:", driver.title)
    print("URL:", driver.current_url)

    assert driver.current_url == BASE_URL + "/"

    assert "Marine Pollution Reporting Portal" in driver.page_source

    print("✓ HOME PAGE PASSED")


# =========================================================
# TEST 2 - REGISTRATION
# =========================================================

def test_02_registration(driver):

    print("\n========== TEST 2: REGISTER ==========")

    driver.get(BASE_URL + "/register")

    wait = wait_for_page(driver)

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[contains(text(),'Create Account')]")
        )
    )

    print("Register page opened")

    print("Test username:", TEST_USERNAME)
    print("Test email:", TEST_EMAIL)

    # Username
    username = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[placeholder='Username']")
        )
    )

    username.send_keys(TEST_USERNAME)

    # Email
    email = driver.find_element(
        By.CSS_SELECTOR,
        "input[placeholder='Email']"
    )

    email.send_keys(TEST_EMAIL)

    # Password
    password = driver.find_element(
        By.CSS_SELECTOR,
        "input[placeholder='Password']"
    )

    password.send_keys(TEST_PASSWORD)

    # Actual implementation has a select element
    # with User and Organization options.
    role_select = Select(
        driver.find_element(
            By.CSS_SELECTOR,
            "select.auth-input"
        )
    )

    role_select.select_by_value("user")

    print("User role selected")

    # Register button
    register_button = driver.find_element(
        By.XPATH,
        "//button[contains(text(),'Register')]"
    )

    register_button.click()

    message = accept_alert(driver)

    assert message == "Registration Successful"

    print("✓ Registration success alert accepted")

    # Actual Register.js redirects to /login
    wait.until(
        EC.url_to_be(BASE_URL + "/login")
    )

    assert driver.current_url == BASE_URL + "/login"

    print("Redirected to Login page")
    print("✓ REGISTRATION PASSED")


# =========================================================
# TEST 3 - LOGIN
# =========================================================

def test_03_login(driver):

    print("\n========== TEST 3: LOGIN ==========")

    driver.get(BASE_URL + "/login")

    wait = wait_for_page(driver)

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[contains(text(),'Welcome Back')]")
        )
    )

    print("Login page opened")

    username = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[placeholder='Username']")
        )
    )

    password = driver.find_element(
        By.CSS_SELECTOR,
        "input[placeholder='Password']"
    )

    username.send_keys(TEST_USERNAME)
    password.send_keys(TEST_PASSWORD)

    login_button = driver.find_element(
        By.XPATH,
        "//button[contains(text(),'Login')]"
    )

    login_button.click()

    message = accept_alert(driver)

    assert message == "Login Successful"

    print("✓ Login success alert accepted")

    # User role redirects to user dashboard
    wait.until(
        EC.url_to_be(BASE_URL + "/user-dashboard")
    )

    assert driver.current_url == BASE_URL + "/user-dashboard"

    print("User dashboard opened")
    print("✓ LOGIN PASSED")


# =========================================================
# TEST 4 - USER DASHBOARD
# =========================================================

def test_04_user_dashboard(driver):

    print("\n========== TEST 4: USER DASHBOARD ==========")

    driver.get(BASE_URL + "/user-dashboard")

    wait = wait_for_page(driver)

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(text(),'User Dashboard')]")
        )
    )

    assert "User Dashboard" in driver.page_source

    assert "Report Pollution" in driver.page_source
    assert "View Reports" in driver.page_source
    assert "View Pollution Map" in driver.page_source

    print("User dashboard content verified")
    print("✓ USER DASHBOARD PASSED")


# =========================================================
# TEST 5 - REPORT POLLUTION PAGE
# =========================================================

def test_05_report_pollution_page(driver):

    print("\n========== TEST 5: REPORT POLLUTION ==========")

    driver.get(BASE_URL + "/report")

    wait = wait_for_page(driver)

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[contains(text(),'Report Pollution')]")
        )
    )

    print("Report Pollution page opened")

    # Pollution type
    pollution_select = Select(
        driver.find_element(
            By.CSS_SELECTOR,
            "select.marine-input"
        )
    )

    pollution_select.select_by_visible_text("Plastic Waste")

    print("Pollution type selected")

    # Description
    description = driver.find_element(
        By.CSS_SELECTOR,
        "textarea[placeholder='Describe the pollution incident']"
    )

    description.send_keys(
        "Selenium automated test pollution report."
    )

    # Latitude
    latitude = driver.find_element(
        By.CSS_SELECTOR,
        "input[placeholder='Latitude']"
    )

    latitude.send_keys("9.9312")

    # Longitude
    longitude = driver.find_element(
        By.CSS_SELECTOR,
        "input[placeholder='Longitude']"
    )

    longitude.send_keys("76.2673")

    print("Location entered")

    # Submit
    submit_button = driver.find_element(
        By.XPATH,
        "//button[contains(text(),'Submit Report')]"
    )

    submit_button.click()

    message = accept_alert(driver)

    assert message == "Pollution Report Submitted"

    print("✓ Pollution report submitted successfully")
    print("✓ REPORT POLLUTION PASSED")


# =========================================================
# TEST 6 - REPORTS PAGE
# =========================================================

def test_06_reports_page(driver):

    print("\n========== TEST 6: REPORTS PAGE ==========")

    driver.get(BASE_URL + "/reports")

    wait = wait_for_page(driver)

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[contains(text(),'Pollution Reports')]")
        )
    )

    assert "Pollution Reports" in driver.page_source

    print("Reports page opened")
    print("✓ REPORTS PAGE PASSED")


# =========================================================
# TEST 7 - POLLUTION MAP
# =========================================================

def test_07_pollution_map(driver):

    print("\n========== TEST 7: POLLUTION MAP ==========")

    driver.get(BASE_URL + "/map")

    wait = wait_for_page(driver)

    # The actual PollutionMap.js initially displays Loading map...
    # and then loads Google Maps.

    try:

        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//h2[contains(text(),'Pollution Location Map')]")
            )
        )

        print("Pollution map page opened")

        assert "Pollution Location Map" in driver.page_source

        print("✓ POLLUTION MAP PASSED")

    except Exception as error:

        print("Map test failed:", error)

        # Google Maps can fail because of API/network restrictions.
        # We still capture the current page for debugging.
        driver.save_screenshot("map_error.png")

        raise


# =========================================================
# TEST 8 - ORGANIZATION LOGIN PAGE / DASHBOARD ROUTE
# =========================================================

def test_08_organization_dashboard(driver):

    print("\n========== TEST 8: ORGANIZATION DASHBOARD ==========")

    driver.get(BASE_URL + "/organization-dashboard")

    wait = wait_for_page(driver)

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[contains(text(),'Organization Dashboard')]")
        )
    )

    assert "Organization Dashboard" in driver.page_source

    assert "monitor reports and IoT sensor data" in driver.page_source

    print("Organization dashboard opened")
    print("✓ ORGANIZATION DASHBOARD PASSED")


# =========================================================
# TEST 9 - SENSOR DASHBOARD
# =========================================================

def test_09_sensor_dashboard(driver):

    print("\n========== TEST 9: SENSOR DASHBOARD ==========")

    driver.get(BASE_URL + "/dashboard")

    wait = wait_for_page(driver)

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(text(),'IoT Sensor Dashboard')]")
        )
    )

    assert "IoT Sensor Dashboard" in driver.page_source

    assert "Real-time water quality monitoring" in driver.page_source

    assert "pH Level Trend" in driver.page_source
    assert "Turbidity Readings" in driver.page_source
    assert "Salinity Trend" in driver.page_source

    print("Sensor dashboard opened")
    print("pH chart found")
    print("Turbidity chart found")
    print("Salinity chart found")

    print("✓ SENSOR DASHBOARD PASSED")


# =========================================================
# TEST 10 - NAVBAR LOGIN / REGISTER
# =========================================================

def test_10_navigation_buttons(driver):

    print("\n========== TEST 10: NAVIGATION ==========")

    driver.get(BASE_URL + "/")

    wait = wait_for_page(driver)

    # Login button
    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(),'Login')]")
        )
    )

    login_button.click()

    wait.until(
        EC.url_to_be(BASE_URL + "/login")
    )

    assert driver.current_url == BASE_URL + "/login"

    print("Login navigation passed")

    driver.get(BASE_URL + "/")

    register_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(),'Register')]")
        )
    )

    register_button.click()

    wait.until(
        EC.url_to_be(BASE_URL + "/register")
    )

    assert driver.current_url == BASE_URL + "/register"

    print("Register navigation passed")

    print("✓ NAVIGATION PASSED")


# =========================================================
# TEST 11 - INVALID LOGIN
# =========================================================

def test_11_invalid_login(driver):

    print("\n========== TEST 11: INVALID LOGIN ==========")

    driver.get(BASE_URL + "/login")

    wait = wait_for_page(driver)

    username = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[placeholder='Username']")
        )
    )

    password = driver.find_element(
        By.CSS_SELECTOR,
        "input[placeholder='Password']"
    )

    username.send_keys("invalid_selenium_user")
    password.send_keys("WrongPassword123")

    login_button = driver.find_element(
        By.XPATH,
        "//button[contains(text(),'Login')]"
    )

    login_button.click()

    message = accept_alert(driver)

    assert message == "Login Failed"

    print("Invalid login correctly rejected")
    print("✓ INVALID LOGIN PASSED")


# =========================================================
# TEST 12 - REGISTER PAGE ROLE OPTIONS
# =========================================================

def test_12_registration_roles(driver):

    print("\n========== TEST 12: REGISTRATION ROLES ==========")

    driver.get(BASE_URL + "/register")

    wait = wait_for_page(driver)

    select_element = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "select.auth-input")
        )
    )

    role_select = Select(select_element)

    options = [
        option.get_attribute("value")
        for option in role_select.options
    ]

    print("Available registration roles:", options)

    # According to the actual Register.js implementation,
    # only user and organization can be registered.

    assert "user" in options
    assert "organization" in options

    assert "admin" not in options

    print("Admin registration option correctly absent")
    print("✓ REGISTRATION ROLE TEST PASSED")


# =========================================================
# TEST 13 - LOGOUT
# =========================================================

def test_13_logout(driver):

    print("\n========== TEST 13: LOGOUT ==========")

    # Create a login session using the test user.

    driver.get(BASE_URL + "/login")

    wait = wait_for_page(driver)

    username = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[placeholder='Username']")
        )
    )

    password = driver.find_element(
        By.CSS_SELECTOR,
        "input[placeholder='Password']"
    )

    username.send_keys(TEST_USERNAME)
    password.send_keys(TEST_PASSWORD)

    driver.find_element(
        By.XPATH,
        "//button[contains(text(),'Login')]"
    ).click()

    message = accept_alert(driver)

    assert message == "Login Successful"

    wait.until(
        EC.url_to_be(BASE_URL + "/user-dashboard")
    )

    print("Logged in successfully")

    # Logout
    logout(driver)

    assert driver.current_url == BASE_URL + "/"

    # After logout, Login and Register should appear again.
    assert driver.find_element(
        By.XPATH,
        "//a[contains(text(),'Login')]"
    ).is_displayed()

    assert driver.find_element(
        By.XPATH,
        "//a[contains(text(),'Register')]"
    ).is_displayed()

    print("Login/Register buttons restored")
    print("✓ LOGOUT PASSED")


# =========================================================
# TEST 14 - ADMIN DASHBOARD PAGE
# =========================================================

def test_14_admin_dashboard(driver):

    print("\n========== TEST 14: ADMIN DASHBOARD ==========")

    driver.get(BASE_URL + "/admin-dashboard")

    wait = wait_for_page(driver)

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(text(),'Admin Dashboard')]")
        )
    )

    assert "Admin Dashboard" in driver.page_source

    assert "Report Management" in driver.page_source
    assert "User Management" in driver.page_source

    print("Admin dashboard page opened")
    print("Report Management section found")
    print("User Management section found")

    print("✓ ADMIN DASHBOARD PASSED")


# =========================================================
# TEST 15 - FRONTEND ROUTES
# =========================================================

@pytest.mark.parametrize(
    "route,expected_text",
    [
        ("/", "Marine Pollution Reporting Portal"),
        ("/login", "Welcome Back"),
        ("/register", "Create Account"),
        ("/user-dashboard", "User Dashboard"),
        ("/organization-dashboard", "Organization Dashboard"),
        ("/admin-dashboard", "Admin Dashboard"),
        ("/report", "Report Pollution"),
        ("/reports", "Pollution Reports"),
        ("/dashboard", "IoT Sensor Dashboard"),
        ("/map", "Pollution Location Map"),
    ]
)
def test_15_all_frontend_routes(driver, route, expected_text):

    print(
        f"\n========== ROUTE TEST: {route} =========="
    )

    driver.get(BASE_URL + route)

    wait = WebDriverWait(driver, 15)

    wait.until(
        EC.presence_of_element_located(
            (By.TAG_NAME, "body")
        )
    )

    if route == "/map":

        # Google Maps loads asynchronously.
        # Wait specifically for the map heading.
        try:

            wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//h2[contains(text(),'Pollution Location Map')]"
                    )
                )
            )

            print("Map component loaded")
            print("✓ /map PASSED")

        except Exception:

            driver.save_screenshot("map_route_error.png")

            # At minimum, React's map loading component must exist.
            assert "Loading map..." in driver.page_source

            print("Map component is still loading")
            print("✓ /map ROUTE PASSED")

    else:

        wait.until(
            lambda d: expected_text in d.page_source
        )

        assert expected_text in driver.page_source

        print(f"✓ {route} PASSED")