#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import time
import os
import sys
import subprocess

# ====== 設定 ======
URL = "https://clean-lease-gw.net/scripts/dneo/appsuite.exe?cmd=cdbasetappmanage&app_id=287#cmd=cdbasetrecalc"
USER_ID = os.environ.get("GROUPWARE_USER")
PASSWORD = os.environ.get("GROUPWARE_PASS")
GECKO_PATH = "/usr/local/bin/geckodriver"
GECKO_LOG = "/tmp/geckodriver.log"
# ===================


def run_cmd(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        out = e.output
    return out.strip()


def print_versions():
    print("===== バージョン情報 =====")
    print("Python :", run_cmd("python --version"))
    print("Firefox:", run_cmd("firefox --version"))
    print("geckodriver:", run_cmd(f"{GECKO_PATH} --version"))
    print("==========================")


def main():
    if not USER_ID or not PASSWORD:
        print("❌ 環境変数 GROUPWARE_USER / GROUPWARE_PASS が設定されていません。")
        sys.exit(1)

    print_versions()

    options = Options()
    options.add_argument("--headless=new")  # 新しいヘッドレスモード
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = Service(GECKO_PATH, log_path=GECKO_LOG, timeout=180)

    driver = None
    for attempt in range(1, 4):
        try:
            print(f"🦊 WebDriver 起動試行 {attempt} 回目...")
            driver = webdriver.Firefox(service=service, options=options)
            print("✅ WebDriver 起動成功")
            break
        except WebDriverException as e:
            print(f"⚠️ WebDriver 起動失敗: {e}")
            if os.path.exists(GECKO_LOG):
                print("--- geckodriver.log tail ---")
                print("\n".join(open(GECKO_LOG).read().splitlines()[-20:]))
            time.sleep(10)
    else:
        print("❌ 3回試しても WebDriver が起動できませんでした。")
        sys.exit(1)

    wait = WebDriverWait(driver, 60)

    try:
        print("🌐 ページにアクセス中...")
        driver.get(URL)
        time.sleep(3)

        print("🔐 ログインフォームに入力中...")
        driver.find_element(By.NAME, "UserID").send_keys(USER_ID)
        driver.find_element(By.NAME, "_word").send_keys(PASSWORD)
        driver.find_element(By.NAME, "_word").send_keys(Keys.ENTER)
        time.sleep(6)
        print("✅ ログイン完了")

        print("☑️ チェックボックスをチェック中...")
        checkbox = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'div.cdb-recalculate-check > label > input[type="checkbox"]')
            )
        )
        if not checkbox.is_selected():
            checkbox.click()
            print("✅ チェックボックスにチェックを入れました")
        else:
            print("ℹ️ チェックボックスはすでにチェック済みです")

        print("🔁 再計算ボタンをクリックします...")
        recalc_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "cdb-recalculate-button"))
        )
        recalc_button.click()

        print("⏳ 再計算中...完了を待機しています")
        done_message = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.neo-message"))
        )
        print("✅ 完了メッセージ:", done_message.text)

        job_detail = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.cdb-job-detail"))
        )
        print("📊 処理済みデータ件数:", job_detail.text)

        close_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.ui-dialog-buttonpane button.ui-button")
            )
        )
        close_button.click()
        print("✅ 閉じるボタンをクリックしました")

        driver.quit()
        sys.exit(0)

    except Exception as e:
        print("❌ エラーが発生しました:", e)
        if os.path.exists(GECKO_LOG):
            print("--- geckodriver.log tail ---")
            print("\n".join(open(GECKO_LOG).read().splitlines()[-40:]))
        if driver:
            driver.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()
