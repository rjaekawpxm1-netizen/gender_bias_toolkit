import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

APP_URL = "https://genderbiastoolkit-ftdwfl47js43gi58ragpud.streamlit.app/"

def main():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,900")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=opts)
    driver.set_page_load_timeout(60)

    try:
        print(f"[keep_awake] opening {APP_URL}")
        driver.get(APP_URL)
        time.sleep(8)  # 페이지 초기 로드 대기

        # 잠든 앱이면 "get this app back up" 버튼이 뜸 → 클릭
        woke = False
        for attempt in range(3):
            buttons = driver.find_elements(By.TAG_NAME, "button")
            target = None
            for b in buttons:
                label = (b.text or "").lower()
                if "back up" in label or "get this app" in label or "wake" in label:
                    target = b
                    break
            if target:
                print(f"[keep_awake] sleeping app detected — clicking wake button (attempt {attempt+1})")
                driver.execute_script("arguments[0].click();", target)
                woke = True
                time.sleep(30)  # 앱 재기동 대기
            else:
                print("[keep_awake] no wake button — app appears already awake")
                break

        # 실제로 앱이 렌더됐는지 확인 (iframe 또는 본문 텍스트)
        time.sleep(5)
        page = driver.page_source.lower()
        if "streamlit" in page or "성평등" in driver.page_source:
            print("[keep_awake] OK — app is up")
        else:
            print("[keep_awake] WARN — app content not confirmed, but no error")

        print(f"[keep_awake] woke={woke}")

    except Exception as e:
        print(f"[keep_awake] ERROR: {e}")
        sys.exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()