import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from base.base_driver import BaseDriver
from pages.search_flight_result_page import SearchFlightResults
from utilities.utils import Utils


class LaunchPage(BaseDriver):
    log = Utils.custom_logger()

    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    # DEPART_FROM_FIELD = "//input[@id='BE_flight_origin_city']"
    # GOING_TO_FIELD = "//input[@id='BE_flight_arrival_city']"
    # GOING_TO_RESULT_LIST ="//div[@class='viewport']//div[1]/li"
    # SELECT_DATE_FIELD = "//input[@id='BE_flight_origin_date']"
    # ALL_DATES = "//div[@id='monthWrapper']//tbody//td[@class!='inActiveTD']"
    # SEARCH_BUTTON = "//input[@value='Search Flights']"
    POPUP_UNKNOWN = "//a[@id='webklipper-publisher-widget-container-notification-close-div']"

    def getUnkowgetUnkownPopup(self):
        # time.sleep(10)
        return self.wait_until_element_is_clickble(By.XPATH, self.POPUP_UNKNOWN)



    def getDepartFromField(self):
        return self.wait_until_element_is_clickble(By.XPATH,self.DEPART_FROM_FIELD)

    def getGoingToField(self):
        return self.wait_until_element_is_clickble(By.XPATH, self.GOING_TO_FIELD)
    def getGoingToResult(self):
        # print("res............",self.GOING_TO_RESULT_LIST)
        return self.wait_for_presence_of_all_elements(By.XPATH, self.GOING_TO_RESULT_LIST)
    def getDdepartureDateField(self):
        return self.wait_until_element_is_clickble(By.XPATH,self.SELECT_DATE_FIELD)

    def getAllDatesField(self):
        return self.wait_until_element_is_clickble(By.XPATH, self.ALL_DATES)
    def getSearchButton(self):
        return self.wait_until_element_is_clickble(By.XPATH, self.SEARCH_BUTTON)

    def clickUnknownPopup(self):
        print("Attempting to click unknown popup")
        # account_btn = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "//a[@class='close']")))
        # account_btn.click()

        self.getUnkowgetUnkownPopup().click()
        print("Clicked unknown popup successfully")
        time.sleep(4)


    def enterDepartFromLocation(self, departlocation):
        self.getDepartFromField().click()
        time.sleep(3)

        self.getDepartFromField().send_keys(departlocation)
        self.getDepartFromField().send_keys(Keys.ENTER)

    def enterGoingToLocation(self,goingtolocation):
        self.getGoingToField().click()
        self.log.info("Clicked on going to")
        time.sleep(2)
        self.getGoingToField().send_keys(goingtolocation)
        time.sleep(3)
        self.log.info("Type text into going to field successfully.")

        self.getGoingToField().send_keys(Keys.ENTER)

        self.log.info("Type text into enter successfully.")
        time.sleep(3)

        search_results = self.getGoingToResult()
        print(search_results,"search........")
        self.log.info(search_results,"search res...")
        time.sleep(3)
        for results in search_results:
            print(results.text)
            if goingtolocation in results.text:
                results.click()
                time.sleep(3)
                self.log.info("in loop..")
                break
    def enterDepatureDate(self,departuredate):
        self.getDdepartureDateField().click()
        time.sleep(3)
        time.sleep(3)
        all_dates1 = self.getAllDatesField().find_elements(By.XPATH,self.ALL_DATES)
        time.sleep(3)
        for date in all_dates1:
            if date.get_attribute("data-date") == departuredate:
                date.click()
                time.sleep(3)
                # time.sleep(3)
                break

    def clickSearchFlightButton(self):
        self.getSearchButton().click()
        time.sleep(3)

    def searchFlights(self,depaturelocation,goingtolocation,departuredate):
        self.clickUnknownPopup()
        self.enterDepartFromLocation(depaturelocation)
        self.enterGoingToLocation(goingtolocation)
        self.enterDepatureDate(departuredate)
        print("enter departure date..")
        self.clickSearchFlightButton()
        search_flight_result = SearchFlightResults(self.driver)
        return search_flight_result