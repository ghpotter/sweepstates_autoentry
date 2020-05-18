import os

from itertools import product
from json import load
from multiprocessing import Pool
from selenium import webdriver
from time import sleep

class WebSiteInfo:
    def __init__(self, website_json):
        self.website = website_json['website']
        self.iframe_element_id = website_json['iframe_id']
        self.email_element_id = 'xReturningUserEmail'
        self.login_element_id = 'xCheckUser'
        self.button_class = 'xCTA'

def get_entry_info(json_file_name):
    """
    Load entry info from json in the form of:
    {
        "emails": [
            "example@example.com",
        ],
        "websites": [
            {
                "website": "https://www.sample.com/sweepstakes",
                "iframe_id": "exampleFrame"
            },
        ]
    }
    """
    emails = []
    websites = []

    with open(json_file_name) as entry_info:
        data = load(entry_info)
        for email in data['emails']:
            emails.append(email)
        for website in data['websites']:
            websites.append(WebSiteInfo(website))
    
    return emails, websites

def main(params):
    email = params[0]
    website = params[1]
    success = False

    opts = webdriver.ChromeOptions()
    opts.headless = True
    opts.add_argument('log-level=2')
    driver = webdriver.Chrome(options=opts)

    try:
        driver.get(website.website)
        driver.implicitly_wait(10)

        frame = driver.find_element_by_id(website.iframe_element_id)
        driver.switch_to_frame(frame)

        driver.find_element_by_id(website.email_element_id).send_keys(email)
        driver.find_element_by_id(website.login_element_id).click()

        for button in driver.find_elements_by_class_name(website.button_class):
            # print("Trying to click button")
            try:
                button.click()
                # print("+++success")
                # print("{0} on {1} succedded".format(email, website.website))
                success = True
            except:
                # print("failure")
                pass
    except Exception:
        print("{0} on {1} failed.".format(email, website.website))
        print(Exception)
    driver.quit()
    return params, success

if __name__ == '__main__':
    script_dir = os.path.split(os.path.abspath(__file__))[0]
    json_file = 'entry_info.json'
    full_json_path = os.path.join(script_dir, json_file)
    emails, websites = get_entry_info(full_json_path)
    params = list(product(emails, websites))

    retry_count = 0
    while params and retry_count < 5:
        retry_count += 1
        outs = Pool().map(main, params)
        params = []
        for out in outs:
            if out[1]:
                print('{0} succeeded on {1}'.format(out[0][0], out[0][1].website))
            else:
                print('{0} failed on {1} on attempt {2}'.format(out[0][0], out[0][1].website, retry_count))
                params.append(out[0])
        
