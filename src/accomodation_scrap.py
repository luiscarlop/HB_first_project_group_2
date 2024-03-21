import pandas as pd
import numpy as np
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By

from time import sleep



DATA_DIR = Path("..") / "data"


driver = webdriver.Chrome()  # Instances WebDriver for Chrome

driver.get("https://airbnb.com")  # Opens Airbnb website

sleep(5)  # Waits for 5 seconds

# Clicks on the Accept button for cookies if it appears
try:
    driver.find_element(
        By.XPATH,
        value="/html/body/div[5]/div/div/div[1]/div/div[6]/section/div[2]/div[2]/button",
    ).click()
except:
    pass

cities = ["Valencia"]  # City to search for

# Initializes the lists to store the data

name = list()
type = list()
price_per_night = list()
host = list()
rating = list()
reviews = list()
place = list()


for city in cities:
    # Finds the search input and types the city

    driver.find_element(
        By.ID,
        value="bigsearch-query-location-input",
    ).send_keys(city)

    sleep(1)  # Waits for 1 second

    # Clicks on the search button

    driver.find_element(By.CLASS_NAME, value="bhtghtc").click()
    
    sleep(2)
    
    # Store the ID of the original window
    original_window = driver.current_window_handle
    
    next_page = driver.find_element(
    By.XPATH,
    value="""
    /html/body/div[5]/div/div/div[1]/div/div[3]/div[2]
    /main/div[2]/div/div[3]/div/div/div/nav/div/a[5]
    """,
    )

    while next_page != None:

        # Iterates over the listings and opens each one in a new tab. Then, it closes the tab and goes back to the original window

        listings = driver.find_elements(
            By.CLASS_NAME, value="c4mnd7m"
        )  # Finds all the listings

        for listing in listings:
            listing.click()  # Clicks on the listing
            sleep(2)
            driver.switch_to.window(driver.window_handles[1])  # Switches to the new tab

            sleep(5)

            # Sometimes, a pop-up appears. This code closes it if it does
            try:
                driver.find_element(
                    By.XPATH,
                    value="/html/body/div[9]/div/div/section/div/div/div[2]/div/div[1]/button",
                ).click()
            except:
                pass

            """
            The next part scrapes the data from each listing. The first data can be found easily,
            but the rating and number of reviews can be in different places depending on the listing.
            
            If the listing is marked with the "Traveller recommended" label, there are a new div where
            the rating and number of reviews are. If the page is scrolled down, there are a new visible span
            that contains the rating and number of reviews and it always appears in the same place.
            """

            sleep(2)

            # Getting the data

            # Name of the listing
            try:
                name.append(
                    driver.find_element(
                        By.XPATH,
                        value="""
                        /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main
                        /div/div[1]/div[1]/div[1]/div/div/div/div/div/section/div/div[1]/span/h1
                        """,
                    ).text
                )
            except:
                name.append(np.nan)

            # ----------------------------------------------------------------------
            # Type of accommodation

            try:
                type.append(
                    driver.find_element(
                        By.XPATH,
                        value="""
                        /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main
                        /div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[1]/h2
                        """,
                    ).text
                )
            except:
                type.append(np.nan)

            # ----------------------------------------------------------------------
            # Price per night

            try:
                try:
                    price_per_night.append(
                        driver.find_elements(By.CLASS_NAME, value="_tyxjp1")[1].text.split(
                            " "
                        )[0]
                    )
                except:
                    price_per_night.append(
                        driver.find_element(
                            By.XPATH,
                            value="""
                            /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main
                            /div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div/div/span/div/span[2]
                            """,
                        ).text.split(" ")[0]
                    )
            except:
                price_per_night.append(np.nan)

            # ----------------------------------------------------------------------
            # Host name

            try:
                try:
                    host.append(
                        driver.find_element(
                            By.XPATH,
                            value="""
                            /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main
                            /div/div[1]/div[3]/div/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[1]
                            """,
                        ).text
                    )

                # When the accommodation is marked as "Traveller recommended", the host name is in a different place
                except:
                    host.append(
                        driver.find_element(
                            By.XPATH,
                            value="""
                            /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main
                            /div/div[1]/div[3]/div/div[1]/div/div[3]/div/div/div/div/div[2]/div[1]
                            """,
                        ).text
                    )
            except:
                host.append(np.nan)

            # Hacer scroll hacia abajo
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            sleep(1)

            # ----------------------------------------------------------------------
            # Rating

            try:
                rating.append(
                    driver.find_element(
                        By.CLASS_NAME,
                        value="_12si43g",
                    ).text.split(
                        " "
                    )[0]
                )
            except:
                rating.append(np.nan)

            # ----------------------------------------------------------------------
            # Reviews

            try:
                reviews.append(
                    driver.find_element(
                        By.CLASS_NAME,
                        value="_bq6krt",
                    ).text.split(
                        " "
                    )[0]
                )
            except:
                reviews.append(np.nan)
                
            place.append(city)

            sleep(2)

            driver.close()
            sleep(1)
            driver.switch_to.window(original_window)

        next_page.click()

        sleep(5)

        try:
            next_page = driver.find_element(
                By.XPATH,
                value="""
                /html/body/div[5]/div/div/div[1]/div/div[3]/div[2]
                /main/div[2]/div/div[3]/div/div/div/nav/div/a[6]
                """,
            )
        except:
            next_page = None

        sleep(1)
    
driver.quit()

"""
Once all the listings have been scraped, the data is stored in a DataFrame and saved as a CSV file.
"""
        
airbnb_data = pd.DataFrame(
    {
        "Name": name,
        "Type": type,
        "Price per night": price_per_night,
        "Host": host,
        "Rating": rating,
        "Reviews": reviews,
        "City": place
    }
)

airbnb_data.to_csv(DATA_DIR / "airbnb_data.csv", index=False)