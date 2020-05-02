import time
from re import fullmatch

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# def example_action(action_args, browser_instance):
#     some_arg = action_args.get("some_arg")
#     if some_arg is None:
#         return False, {"err": "Lipseste argumentul some_arg"}


def element_from_xpath(action_args, browser_instance):
    x_path_val = action_args.get("xpath")
    if x_path_val is None:
        return False, {"err": "You didnt give me an xpath in action_args"}
    wait = WebDriverWait(browser_instance, 20)
    try:
        element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, x_path_val)
        ))
        time.sleep(0.5)
    except TimeoutException:
        return False, {"err": "Timeout exception when looking for element at given xpath"}
    return True, element


def click_element(action_args, browser_instance):
    result, data = element_from_xpath(action_args, browser_instance)
    if result is False:
        return result, data
    data.click()
    return True, {"success": "Clicked on xpath given in action_args"}


def input_element(action_args, browser_instance):
    result, data = element_from_xpath(action_args, browser_instance)
    input_text = action_args.get("input_text")
    if result is False:
        return result, data
    if input_text is None:
        return False, {"err": "You didnt give me a text in  'input_text'"}
    data.send_keys(input_text)
    return True, {"success": "Element from xpath took the received value"}


def go_to_url(action_args, browser_instance):
    url = action_args.get("url")
    if url is None:
        return False, {"err": "No valid url"}
    browser_instance.get(url)
    return True, {"success": "Valid url"}


def switch_to_iframe(action_args, browser_instance):
    x_path_val = action_args.get("xpath")
    if x_path_val is None:
        return False, {"err": "You didnt give me a xpath in action_args (switch_to_iframe)"}
    wait = WebDriverWait(browser_instance, 2)
    try:
        wait.until(EC.frame_to_be_available_and_switch_to_it(
            (By.XPATH, x_path_val)
        ))
    except TimeoutException:
        return False, {"err": "Timeout exception when looking for element at given xpath"}
    return True, {"success": "switched to iframe"}


def switch_to_default_content(action_args, browser_instance):
    browser_instance.switch_to.default_content()
    return True, {"succes": "switched to default content"}


def matches_regex(action_args, browser_instance):
    result, data = element_from_xpath(action_args, browser_instance)
    if result is False:
        return result, data
    regex = action_args.get("regex")
    text = data.text
    if fullmatch(regex, text) is None:
        return False, {"err": "The regex does not match text"}
    return True, {"success": "The regex matched the text"}


def contains_text(action_args, browser_instance):
    result, data = element_from_xpath(action_args, browser_instance)
    if result is False:
        return result, data
    text_value = action_args.get("text_value")
    text = data.text
    if text_value in text:
        return True, {"success": "Text inside element matched pattern"}
    return False,  {"err": "Text inside element does not match pattern"}


ACTION_LIST = {
    # "example_action": example_action,
    # element_from_xpath does not meet the standard to be here
    "click_element": click_element,
    "input_element": input_element,
    "go_to_url": go_to_url,
    "matches_regex": matches_regex,
    "contains_text": contains_text,
    "switch_to_iframe": switch_to_iframe,
    "switch_to_default_content": switch_to_default_content
}
