from selenium import webdriver
from selenium_stealth import stealth
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from vhod import username, password
import time
import random
from selenium.common.exceptions import NoSuchElementException
import os
import json


class InstagramBot:
    def __init__(self):
        # вы также можете импортировать SoftwareEngine, HardwareType, SoftwareType, Popularity из random_user_agent.params
        # вы также можете установить необходимое количество пользовательских агентов, указав `limit` в качестве параметра
        # software_names = [SoftwareName.CHROME.value]
        # operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        # user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=120)
        # Получить случайную строку пользовательского агента.
        # user_agent = user_agent_rotator.get_random_user_agent()
        # options
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.headless = True
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.browser = webdriver.Chrome(options=options)
        self.browser.delete_all_cookies()
        self.browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        stealth(
            self.browser,
            user_agent="Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,

        )

    def close_browser(self):  # метод для закрытия браузера
        self.browser.close()
        self.browser.quit()

    def test(self):
        browser = self.browser
        browser.get("https://bot.sannysoft.com/")

    def login(self, username, password):  # метод логина
        browser = self.browser
        browser.get('https://www.instagram.com')
        print('Идет авторизация в инстаграме...')
        time.sleep(random.randrange(2, 5))

        username_input = browser.find_element(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys(username)
        time.sleep(random.randrange(2, 5))

        password_input = browser.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys(password)
        time.sleep(random.randrange(2, 5))

        password_input.send_keys(Keys.ENTER)
        print("Мы авторизовались!!!")
        time.sleep(random.randrange(8, 12))

    # метод ставит лайки по hashtag
    def like_foto_by_hashtag(self, haschtag, click_num_likes):
        browser = self.browser
        time.sleep(2)
        browser.get(f'https://www.instagram.com/explore/tags/{haschtag}/')
        print(f'Переходим на поиск хештега: {haschtag}')
        time.sleep(5)

        try:
            print(f'Открываем первую публикацию с хештэгом: {haschtag}')
            xpath_post = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/article/div[1]/div/div/div[1]/div[1]/a"
            browser.find_element(By.XPATH, xpath_post).click()
            time.sleep(random.randrange(3, 7))

            button_xpath = "//div[@class='_aear']/div[@class=' _aaqg _aaqh']/button[@class='_abl-']"
            css_selector_button_like = ' svg[aria-label="Like"]._ab6-[height="24"][width="24"]'
            num_like = 0
            for i in range(click_num_likes):
                num_like += 1
                if not self.css_selector_exists(css_selector_button_like):
                    print(f'Лайк уже стоит на {num_like} публикацию с хэштэгом {haschtag}, переходим на следующую ->>>')
                    hover = browser.find_element(By.XPATH, button_xpath)
                    ActionChains(browser).move_to_element(hover).perform()
                    browser.find_element(By.XPATH, button_xpath).click()
                    time.sleep(random.randrange(3, 6))
                    continue
                if self.css_selector_exists(css_selector_button_like):
                    browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/button").click()
                    print(f'Поставили лайк на {num_like} публикацию с хэштэгом {haschtag}, ждем некоторое время для следующего лайка, чтобы не забанили')
                    time.sleep(random.randrange(85, 130))
                    print(f'Переходим на следующую публикацию с хэштэгом {haschtag}')
                    button_xpath = "//div[@class='_aear']/div[@class=' _aaqg _aaqh']/button[@class='_abl-']"
                    hover = browser.find_element(By.XPATH, button_xpath)
                    ActionChains(browser).move_to_element(hover).perform()
                    browser.find_element(By.XPATH, button_xpath).click()
                    time.sleep(random.randrange(3, 6))
            else:
                print(f"Следующего поста не будет, т.к. поставили {click_num_likes} лайков как и заказывали.\nНе стоит благодарностей, до встречи!")
        except Exception as ex:
            print(ex)
        self.close_browser()

    # метод проверяет по xpath существует ли элемент на странице
    def xpath_exists(self, url):
        browser = self.browser
        try:
            browser.find_element(By.XPATH, url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # метод проверяет по css-selectoru существует ли элемент на странице
    def css_selector_exists(self, selector):
        browser = self.browser
        try:
            browser.find_element(By.CSS_SELECTOR, selector)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # метод ставит лайк на пост по прямой ссылке
    def like_url(self, userpost):
        browser = self.browser
        browser.get(userpost)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого поста не существует, проверьте URL")
            self.close_browser()
        else:
            print("Пост успешно найден, ставим лайк!")
            time.sleep(2)

            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                         "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button"))).click()
            time.sleep(2)
            print(f"Лайк на пост: {userpost} поставлен!")
            self.close_browser()

    def put_many_likes(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(5)

        wrong_userpage = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого пользователя не существует, проверьте URL")
            self.close_browser()
        else:
            print("Пользователь успешно найден, ставим лайки!")
            time.sleep(2)

            posts_count = int(WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                                           "//li[@class='_aa_5'][1]/div[@class='_aacl _aacp _aacu _aacx _aad6 _aade']/span[@class='_ac2a']"))).text)
            loops_count = int(posts_count / 12)
            print(loops_count)

            posts_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements(By.TAG_NAME, 'a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

                for href in hrefs:
                    posts_urls.append(href)

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(3, 5))
                print(f"Итерация #{i}")

            file_name = userpage.split("/")[-2]

            with open(f'{file_name}.txt', 'a') as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")

            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)

            with open(f'{file_name}_set.txt', 'a') as file:
                for post_url in set_posts_urls:
                    file.write(post_url + '\n')

            with open(f'{file_name}_set.txt') as file:
                urls_list = file.readlines()

                for post_url in urls_list:
                    try:
                        browser.get(post_url)
                        time.sleep(2)

                        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                                     "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button"))).click()
                        time.sleep(random.randrange(80, 100))
                        time.sleep(2)

                        print(f"Лайк на пост: {post_url} успешно поставлен!")
                    except Exception as ex:
                        print(ex)
                        self.close_browser()

            self.close_browser()

    def get_all_followers(self, userpage):  # метод подписки на всех подписчиков переданного аккаунта
        browser = self.browser
        browser.get(userpage)
        time.sleep(random.randrange(3, 5))
        file_name = userpage.split("/")[-2]

        # создаём папку с именем пользователя для чистоты проекта
        if os.path.exists(f"{file_name}"):
            print(f"Папка {file_name} уже существует!")
        else:
            print(f"Создаём папку пользователя {file_name}.")
            os.mkdir(file_name)

        wrong_userpage = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/h2"
        if self.xpath_exists(wrong_userpage):
            print(f"Такого пользователя {file_name} не существует, проверьте URL")
            self.close_browser()
        else:
            print(f"Пользователь {file_name} успешно найден, начинаем скачивать ссылки на подписчиков!")

            elements_ = browser.find_elements(By.XPATH, "//span[@title]")
            for element in elements_:
                followers = element.get_attribute("title")
                if ',' in followers:
                    followers = int(''.join(followers.split(',')))
                    print(f"Количество подписчиков: {followers} аккаунта {file_name}")
                    loops_count = int(followers / 16)
                    print(f"Число итераций: {loops_count}")
                else:
                    print(f"Количество подписчиков: {followers} аккаунта {file_name}")
                    loops_count = int(int(followers) / 16)
                    print(f"Число итераций: {loops_count}")

            browser.get(userpage + 'followers/')
            time.sleep(random.randrange(3, 5))

            followers_li = browser.find_element(By.XPATH, "//div[@class='_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9o _abcm']/div[@class='_aano']")

            try:
                followers_urls = []
                for i in range(1, loops_count + 1):
                    time.sleep(random.randrange(1, 3))
                    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_li)
                    time.sleep(random.randrange(2, 4))
                    print(f"Итерация #{i}")

                hrefs = followers_li.find_elements(By.TAG_NAME, 'a')

                for item in hrefs:
                    href = item.get_attribute('href')
                    followers_urls.append(href)

                followers_urls = set(followers_urls)
                followers_urls = list(followers_urls)

                # сохраняем всех подписчиков пользователя в файл
                print(f"Сохраняем ссылки подписчиков аккаунта {file_name}")
                with open(f"{file_name}/{file_name}.txt", "a") as text_file:
                    num_link = 0
                    for link in followers_urls:
                        num_link += 1
                        text_file.write(link + "\n")
                    print(f"Получилось взять {num_link} сылок подписчиков аккаунта {file_name} которые отдал инстаграм")

                with open(f"{file_name}/{file_name}.txt") as text_file:
                    users_urls = text_file.readlines()

                    num_subscribe = 0
                    for user in users_urls:
                        num_subscribe += 1
                        print(f"Переходим на сылку {num_subscribe}")
                        try:
                            try:
                                with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                          'r') as subscribe_list_file:
                                    lines = subscribe_list_file.readlines()
                                    if user in lines:
                                        print(f'Мы уже подписаны на {user}, переходим к следующему пользователю!')
                                        continue

                            except Exception as ex:
                                print('Файл с ссылками ещё не создан!')
                                # print(ex)

                            browser = self.browser
                            browser.get(user)
                            page_owner = user.split("/")[-2]
                            time.sleep(random.randrange(3, 6))

                            if self.xpath_exists("/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div/a"):
                                print("Это наш профиль, уже подписан, пропускаем итерацию!")
                                continue
                            elif browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button/div/div[1]").text == 'Following':
                                print(f"Уже подписаны, на {page_owner} пропускаем итерацию!")
                                continue
                            else:
                                time.sleep(random.randrange(3, 7))
                                if self.xpath_exists("/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/div/article/div[1]/div/h2"):
                                    try:
                                        if browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div/button").text == 'Requested':
                                            print(f'Уже запросили подписку у закрытого аккаунта {page_owner}')
                                            continue
                                        else:
                                            browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div/button").click()
                                            print(f'Запросили подписку на пользователя {page_owner}. Закрытый аккаунт!')
                                    except Exception as ex:
                                        print(ex)
                                else:
                                    try:
                                        if self.xpath_exists("/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button/div/div[1]"):
                                            if browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button/div/div[1]").text == 'Follow':
                                                browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button").click()
                                                print(f'Подписались на пользователя {page_owner}. Открытый аккаунт! Ждем некоторое время, чтобы не нарушать условия инстаграма')
                                        else:
                                            browser.find_element(By.XPATH, "//div[@class='_ab8w  _ab94 _ab99 _ab9h _ab9k _ab9p  _ab9- _abcm']/div[@class='_aacl _aaco _aacw _aad6 _aade']").click()
                                            print(f'Подписались на пользователя {page_owner}. Открытый аккаунт! Ждем некоторое время, чтобы не нарушать условия инстаграма')
                                    except Exception as ex:
                                        print(ex)

                                # записываем данные в файл для ссылок всех подписок, если файла нет, создаём, если есть - дополняем
                                with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                          'a') as subscribe_list_file:
                                    subscribe_list_file.write(user)

                                time.sleep(random.randrange(110, 140))

                        except Exception as ex:
                            print(ex)
                            self.close_browser()

            except Exception as ex:
                print(ex)
                self.close_browser()

        self.close_browser()

    # метод отписки от всех пользователей
    def unsubscribe_for_all_users(self, userpage):
        browser = self.browser
        browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.randrange(3, 6))
        print(f"Переходим к себе не страницу")

        following_button = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a")
        following_count = following_button.find_element(By.TAG_NAME, "span").text
        if ',' in following_count:
            following_count = int(''.join(following_count.split(',')))
        else:
            following_count = int(following_count)
        print(f"Количество подписчиков: {following_count}")
        time.sleep(random.randrange(3, 6))

        loops_count = int(following_count / 10) + 1
        print(f"Количество перезагрузок страницы: {loops_count}")

        following_users_dict = {}
        for loop in range(1, loops_count + 1):
            count = 10
            # browser.get(f"https://www.instagram.com/{username}/")
            # time.sleep(random.randrange(3, 6))
            print(f"Обновляем свою страничку")
            following_button = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a")
            following_button.click()
            # time.sleep(random.randrange(3, 6))
            num = 0
            for us in range(10):
                num += 1
                if num == 11:
                    num -= 11
                if not count:
                    break
                "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[1]/div[2]/div[1]/div/div/span/a"
                "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div/span/a"
                "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[3]/div[2]/div[1]/div/div/span/a"
                "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[14]/div[2]/div[1]/div/div/span/a"
                if not self.xpath_exists(f"/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div/div/div[{num}]/div[3]/button"):
                    print(f"Подписки закончились!")
                    break
                user = browser.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[{num}]/div[2]/div[1]/div/div/span/a")
                href = user.get_attribute('href')
                user_name = href.split('/')[-2]

                following_users_dict[user_name] = href

                browser.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div/div/div[{num}]/div[3]/button").click()
                time.sleep(1)
                browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[1]").click()
                browser.find_element(By.XPATH, "//html/body/div[1]/div/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[1]")
                # time.sleep(random.randrange(65, 90))
                count -= 1
        with open("following_users_dict.txt", 'w', encoding="utf-8") as file:
            json.dump(following_users_dict, file)
        self.close_browser()


my_bot = InstagramBot()
# my_bot.test()
# time.sleep(random.randrange(5, 7))
my_bot.login(username, password)
my_bot.like_foto_by_hashtag('family', 500)
# my_bot.get_all_followers('https://www.instagram.com/kubyshkina484/')
# my_bot.unsubscribe_for_all_users('oksoap_soligorsk')
# my_bot.download_userpage_content("https://www.instagram.com/username/")
