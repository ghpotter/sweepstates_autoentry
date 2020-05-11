from time import sleep
from selenium import webdriver

class WebSiteInfo:
    def __init__(self, website, iframe_id, email_id = 'xReturningUserEmail', login_id='xCheckUser'):
        self.website = website
        self.iframe_element_id = iframe_id
        self.email_element_id = email_id
        self.login_element_id = login_id

emails = ['adrienne.fidelino@gmail.com', 'ghpotter@gmail.com']
websites = [WebSiteInfo('https://www.diynetwork.com/hgtv-smart-home', 'ngxFrame171589'), WebSiteInfo('https://www.hgtv.com/sweepstakes/hgtv-smart-home/sweepstakes', 'ngxFrame171583')]



for email in emails:
    for website in websites:
        
        opts = webdriver.ChromeOptions()
        opts.headless = True
        opts.add_argument('log-level=2')
        driver = webdriver.Chrome(options=opts)
        # driver = webdriver.Chrome()

        try:
            driver.get(website.website)
            driver.implicitly_wait(10)

            frame = driver.find_element_by_id(website.iframe_element_id)
            driver.switch_to_frame(frame)

            driver.find_element_by_id(website.email_element_id).send_keys(email)
            driver.find_element_by_id(website.login_element_id).click()

            for button in driver.find_elements_by_class_name('xCTA'):
                print("Trying to click button")
                try:
                    button.click()
                    print("+++success")
                    print("{0} on {1} succedded".format(email, website.website))
                    driver.close()
                except:
                    print("failure")

            sleep(1)
        except Exception:
            print("{0} on {1} failed.".format(email, website.website))
            print(Exception)
        driver.quit()

