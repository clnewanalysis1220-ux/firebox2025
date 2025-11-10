from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys

# ログイン情報
URL = "https://clean-lease-gw.net/scripts/dneo/appsuite.exe?cmd=cdbasetappmanage&app_id=287#cmd=cdbasetrecalc"
USER_ID = os.environ.get("GROUPWARE_USER")
PASSWORD = os.environ.get("GROUPWARE_PASS")

def main():
    options = Options()
    options.headless = True
    options.binary_location = '/usr/bin/firefox'

    service = Service('/usr/local/bin/geckodriver')
    driver = webdriver.Firefox(service=service, options=options, timeout=180)
    wait = WebDriverWait(driver, 60)

    try:
        print("ページにアクセス中...")
        driver.get(URL)
        time.sleep(3)

        print("ログインフォームに入力中...")
        driver.find_element(By.NAME, "UserID").send_keys(USER_ID)
        driver.find_element(By.NAME, "_word").send_keys(PASSWORD)
        driver.find_element(By.NAME, "_word").send_keys(Keys.ENTER)
        time.sleep(6)
        print("ログイン完了")

        print("チェックボックスをチェック中...")
        checkbox = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'div.cdb-recalculate-check > label > input[type="checkbox"]')
            )
        )
        if not checkbox.is_selected():
            checkbox.click()
            print("チェックボックスにチェックを入れました")
        else:
            print("チェックボックスはすでにチェック済みです")

        print("再計算ボタンをクリックします...")
        recalc_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "cdb-recalculate-button"))
        )
        recalc_button.click()

        print("再計算ボタンをクリックしました。完了を待機しています…")

        done_message = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.neo-message"))
        )
        print("完了メッセージ:", done_message.text)

        job_detail = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.cdb-job-detail"))
        )
        print("処理済みデータ件数:", job_detail.text)

        close_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ui-dialog-buttonpane button.ui-button"))
        )
        close_button.click()
        print("閉じるボタンをクリックしました")

        driver.quit()
        sys.exit(0)

    except Exception as e:
        print("エラーが発生しました:", e)
        driver.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
