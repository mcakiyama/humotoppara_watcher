import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Parameter
LINE_TOKEN = "Set your LINE Notify token"
TARGET_DAY = 22
DAY_OF_WEEK = "土"
INTERVAL_TIME = 60  # second
STOP_NOTIFY_TIME = 600  # second


def send_line_notify(message, token):
    """
    Notify to LINE talk room
    """
    line_notify_token = token
    line_notify_api = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {line_notify_token}"}
    data = {"message": f"message: {message}"}
    requests.post(line_notify_api, headers=headers, data=data)


def main():
    options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    try:
        send_line_notify("\nふもとっぱら監視BOT is started", LINE_TOKEN)
        while True:
            driver.get("https://fumotoppara.secure.force.com/RS_Top")
            table = driver.find_elements_by_xpath(
                "/html/body/div[1]/div[2]/div[2]/div[2]/table"
            )[0]
            col = table.find_elements_by_xpath("//table/tbody/tr")
            satday_data = [i.text.split(" ") for i in col if DAY_OF_WEEK in i.text]
            print(satday_data)

            # row index meaning
            #  0   1    2            3        4     5
            # [日付,曜日,キャンプサイト,コテージ柏,翠山荘,毛無山荘]
            isNotified = False
            for i in satday_data:
                if i[2] == "×":
                    # print(f'{i[0]} is disabled')
                    pass
                elif (i[2] == "○") or (i[2] == "△"):
                    if str(TARGET_DAY) in i[0]:
                        print(f"{i[0]} is enabled")
                        send_line_notify(f"\n{i[0]} is ENABLE", LINE_TOKEN)
                        isNotified = True

            # 通知を出したあとに，一時的に通知を停止する処理(LINE通知連打を防ぐ)
            if isNotified:
                time.sleep(STOP_NOTIFY_TIME)

            time.sleep(INTERVAL_TIME)

    finally:
        send_line_notify("\nふもとっぱら監視BOT is quit", LINE_TOKEN)
        driver.quit()


if __name__ == "__main__":
    main()
