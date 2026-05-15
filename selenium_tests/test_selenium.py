from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    return driver


def test_home_page_loads():
    """Test Case 1: Verify home page loads with correct heading"""
    driver = get_driver()
    try:
        driver.get("http://webapp:5000")
        time.sleep(3)

        assert "Student Portal" in driver.page_source, \
            "FAILED: Student Portal heading not found!"

        print("✅ Test 1 PASSED: Home page loaded with correct heading")

    except Exception as e:
        print(f"❌ Test 1 FAILED: {e}")
        raise
    finally:
        driver.quit()


def test_students_endpoint_accessible():
    """Test Case 2: Verify /students endpoint returns valid response"""
    driver = get_driver()
    try:
        driver.get("http://webapp:5000/students")
        time.sleep(3)

        # Page should load without error
        assert "404" not in driver.page_source, \
            "FAILED: Got 404 on /students endpoint!"
        assert "500" not in driver.page_source, \
            "FAILED: Got 500 error on /students endpoint!"

        print("✅ Test 2 PASSED: /students endpoint accessible")

    except Exception as e:
        print(f"❌ Test 2 FAILED: {e}")
        raise
    finally:
        driver.quit()


if __name__ == '__main__':
    print("Running Selenium Tests...")
    print("-" * 40)
    test_home_page_loads()
    test_students_endpoint_accessible()
    print("-" * 40)
    print("✅ All Selenium tests completed!")