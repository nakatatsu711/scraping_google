import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


URL = 'https://www.google.co.jp'
URL_TITLE = 'Google'
# 設定値
chromedriver_path = 'ChromeDriverのパス'
max_page = 3


def main():
    '''
    メインの処理
    Googleの検索エンジンで入力したキーワードを検索し、各ページのURLを取得
    クリックして各ページに遷移し、前ページに戻るを繰り返す
    '''

    driver = webdriver.Chrome(chromedriver_path)  # ChromeのWebDriverオブジェクトを作成
    driver.get(URL)  # Googleのトップページを開く
    time.sleep(2)  # 2秒待機
    assert URL_TITLE in driver.title  # タイトルに'Google'が含まれていることを確認

    key_list = []
    for key in sys.argv:  # ターミナルに入力した検索キーワードのリスト
        if '.py' in key:  # 最初の要素はファイル名なので除外
            continue
        key_list.append(key)
    keyword = ' '.join(key_list)  # 複数のキーワードにも対応

    input_element = driver.find_element_by_name('q')  # 検索テキストボックスの要素をname属性から取得
    input_element.send_keys(keyword)  # 検索テキストボックスにキーワードを入力
    input_element.send_keys(Keys.RETURN)  # Enterキーを送信
    time.sleep(2)  # 2秒待機

    assert keyword in driver.title  # タイトルにkeywordが含まれていることを確認

    page = 1
    print('検索キーワード ->', keyword)

    while True:
        get_url(driver)
        link_to_next = get_next_page(driver)
        if not link_to_next:  # 次ページがない場合はwhile文をbreak
            break
        page += 1
        if page > max_page:  # 指定したページ数スクレイピングしたらwhile文をbreak
            break
        link_to_next.click()  # 次ページへ遷移

    driver.quit()  # ブラウザーを閉じる


def get_url(driver):
    '''
    各ページに遷移し、URLを取得
    '''

    top_url = driver.current_url
    objects = driver.find_elements_by_css_selector('div.r > a')  # a要素のオブジェクトを取得
    objects = [object.get_attribute('href') for object in objects if 'translate.google.co.jp' not in object.get_attribute('href')]  # 翻訳ページは除外

    for object in objects:
        driver.get(object)
        time.sleep(2)  # 2秒待機
        print(driver.current_url)

    driver.get(top_url)
    time.sleep(2)  # 2秒待機


def get_next_page(driver):
    '''
    次ページを取得
    '''

    return driver.find_element_by_link_text('次へ')  # リンクテキスト名からリンク要素を取得


if __name__ == '__main__':
    main()
