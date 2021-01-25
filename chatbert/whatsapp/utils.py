import time
import re

def waitForXPathLoad(driver, xpath, pause=1e-1, timeout=-1): # get element from xpath once it has loaded
    while timeout > 0 or timeout == -1:
        try:
            time.sleep(pause)
            return driver.find_elements_by_xpath(xpath)

        except:
            timeout -= pause

    return False

def waitForAttributeLoad(driver, attribute, pause=1e-1, timeout=-1): # get attribute once it has loaded
    while timeout > 0 or timeout == -1:
        try:
            time.sleep(pause)
            return driver.get_attribute(attribute)

        except:
            timeout -= pause

    return False

def findImages(text): # find locations of image tags in message
    found = re.finditer('<img.+>', text)
    found = [[f.start(), f.end()] for f in found]

    return found
        
    
