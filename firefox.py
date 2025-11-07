from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ログイン情報
URL = "https://clean-lease-gw.net/scripts/dneo/appsuite.exe?cmd=cdbasetappmanage&app_id=287#cmd=cdbasetrecalc"
USER_ID = "y-warizaya@clean-lease.co.jp"
PASSWORD = "pw@1452"

def main():
    options = Options()
    options.headless = True  # ヘッドレスモード
    options.binary = '/usr/bin/firefox'  # GitHub Actionsのfirefoxパスを明示指定

    service = Service()  # ここはパス指定なしでOK
    driver = webdriver.Firefox(service=service, options=options)
    wait = WebDriverWait(driver, 20)  # 最大20秒待機するWebDriverWaitを作成

    try:
        print("ページにアクセス中...")
        driver.get(URL)
        time.sleep(3)

        print("ログインフォームに入力中...")
        driver.find_element(By.NAME, "UserID").send_keys(USER_ID)
        driver.find_element(By.NAME, "_word").send_keys(PASSWORD)
        driver.find_element(By.NAME, "_word").send_keys(Keys.ENTER)
        time.sleep(5)
        print("ログイン完了")

        while True:
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

            print("再計算ボタンをクリックしました。完了を待機しています...")
            time.sleep(10)  # 処理待機時間（必要に応じて調整）

            print("再計算処理完了か要確認してください。次は1時間後に実行します。")
            time.sleep(3600)  # 1時間待機

    except Exception as e:
        print("エラーが発生しました:", e)

    finally:
        driver.quit()
        print("ブラウザを閉じました。")

if __name__ == "__main__":
    main()
