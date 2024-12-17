# Program title: Coin MarketCap Application

# import part
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from PIL import ImageGrab
import time 
import pandas as pd
import re

# Class part
class coinmarketcap:
    # Program constructor
    def __init__(self):
        try:  
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service)

        except WebDriverException as e:
            print(f"Error initializing WebDriver: {e}")
            exit() 

    # Allowing user to search for a cryptocurrency and enter currency page
    def searching(self):
        try:
            self.driver.get("https://coinmarketcap.com/")
            time.sleep(1)
            Cryto = input('What Crytocurrency would you like to search for?')
            self.driver.maximize_window()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[1]').click()
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, 'input[maxlength="200"]').send_keys(Cryto)
            time.sleep(1)

            self.driver.find_element(By.CSS_SELECTOR, 'input[maxlength="200"]').send_keys(Keys.RETURN)
            time.sleep(1)

            # Get currency rating with corresponding comments 
            try:
                rating = float(self.driver.find_element(By.CLASS_NAME, 'RatingSection_wrapper__T_YeR').text) - 3
                if rating > 4.5:
                    print(f"The rating is {rating}! That's really good")
                elif rating > 3.5:
                    print(f"The rating is alright!")
                elif rating <= 3.5:
                    print(f"Terriable rating! Perhaps you should invest in something else")
            except:
                print('no rating available')

        except Exception as e:
            print(f"An unexpected error occurred while searching: {e}")  

    # Getting top 10 cryptocurrency info 
    def top_10_info(self):
        try: 
            while True:
                link = input('''
                            Please select the link you want to visit
                            1. Top cryptocurrency derivatives exchanges 
                            2. Top cryptocurrency by market cap
                            3. Exit the function
                            ''')

                if link == "1":
                    self.driver.get("https://coinmarketcap.com/rankings/exchanges/derivatives/")
                    assert "Top Cryptocurrency Derivatives Exchanges Ranked | CoinMarketCap" in self.driver.title

                    # Wait for the exchange table to load
                    WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr[style="cursor:pointer"]')))

                    # Initialize DataFrame with meaningful column names
                    df = pd.DataFrame(columns=['Rank', 'Exchange', 'Trading Volume (24h), Market Share, Last Update, Country, Type'])

                    # Find all relevant table rows
                    ele_list = self.driver.find_elements(By.CSS_SELECTOR, 'tr[style="cursor:pointer"]')

                    if not ele_list:
                        print("No data found.")
                        return

                    # Extracting data
                    for ele in ele_list:
                        # Split the text into lines
                        data = ele.text.splitlines()
                        # Ensure the number of data points matches the number of columns
                        if len(data) == len(df.columns):
                            df.loc[len(df)] = data
                        else:
                            print("Row data does not match expected columns:", data)

                    # Get filename from user
                    de = input("Please enter the name for the file without .csv extension: ")

                    # Validate filename
                    if not re.match("^[A-Za-z0-9_-]*$", de):
                        print("Invalid filename. Please use only letters, numbers, underscores, or hyphens.")
                        return

                    # Save to CSV with index starting from 1
                    df.index += 1  # Start index from 1
                    df.to_csv(f'{de}.csv', index=True)
                    print(f"Data saved to {de}.csv")

                elif link == "2":    
                    self.driver.get("https://coinmarketcap.com/")

                    # Wait for the exchange table to load
                    WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr[style="cursor:pointer"]')))

                    # Initialize DataFrame with meaningful column names
                    df = pd.DataFrame(columns=['Rank', 'Name', 'Price', '1h%', '24h%', '7d%', 'Market cap', 'Volume (24h)', 'Circulating supply'])

                    # Find all relevant table rows
                    ele_list = self.driver.find_elements(By.CSS_SELECTOR, 'tr[style="cursor:pointer"]')

                    if not ele_list:
                        print("No data found.")
                        return

                    # Extracting data
                    for ele in ele_list:
                        # Split the text into lines
                        data = ele.text.splitlines()
                        # Ensure the number of data points matches the number of columns
                        if len(data) == len(df.columns):
                            df.loc[len(df)] = data
                        else:
                            print("Row data does not match expected columns:", data)

                    # Get filename from user
                    se = input("Please enter the name for the file without .csv extension: ")

                    # Validate filename
                    if not re.match("^[A-Za-z0-9_-]*$", se):
                        print("Invalid filename. Please use only letters, numbers, underscores, or hyphens.")
                        return

                    # Save to CSV with index starting from 1
                    df.index += 1  # Start index from 1
                    df.to_csv(f'{se}.csv', index=True)
                    print(f"Data saved to {se}.csv")

                elif link == "3":
                    return
                else:
                    print("Invalid please select a valid option!")
                    return      

        except TimeoutException:
            print("Error: The page took too long to load. Please check your internet connection or the website's status.")
        except NoSuchElementException as e:
            print(f"Error: Could not find elements on the page. {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")


    # Top 5 exchanges 
    def top_exchanges(self):
            try:
                while True: 
                    service = Service(ChromeDriverManager().install())
                    self.driver = webdriver.Chrome(service=service) 
                    visit = input('''Please select a link you want to visit
                                1. Top cryptocurrency spot exchanges 
                                2. Top cryptocurrency derivatives exchanges 
                                3. Exit the function
                                ''') 

                    if visit == "1":
                        self.driver.get("https://coinmarketcap.com/rankings/exchanges/")
                        assert "Top Cryptocurrency Exchanges Ranked By Volume | CoinMarketCap" in self.driver.title

                        # Wait for the exchange table to load
                        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sc-71024e3e-0.ehyBa-d')))

                        # Initialize lists
                        name = []
                        volume = []

                        #Top 5 name list
                        name_ele_list = self.driver.find_elements(By.CLASS_NAME, 'sc-71024e3e-0.ehyBa-d')
                        for name_ele in name_ele_list[0:9:2]:
                            name.append(name_ele.text)

                        #Top 5 volume list
                        volume_ele_list = self.driver.find_elements(By.CSS_SELECTOR, 'td[style="text-align:end"]')
                        for volume_ele in volume_ele_list[0:30:6]:
                            volume.append(volume_ele.text)

                        # Create Dataframe and save to csv
                        df = pd.DataFrame({'Name':name, 'Volume':volume})
                        df.index += 1 

                        top_crypto = input("Please enter the name for the file without .csv extension")
                        
                        # Validate the filename 
                        if not re.match("^[A-Za-z0-9_-]*$", top_crypto):
                            print("Invalid filename. Please use only letters, numbers, underscores, or hyphens.")
                            return
                        
                        # Save to CSV
                        df.to_csv(f'{top_crypto}.csv', index=True)
                        print(f"Data saved to {top_crypto}.csv")

                    elif visit == "2":
                        self.driver.get("https://coinmarketcap.com/rankings/exchanges/derivatives/")
                        assert "Top Cryptocurrency Derivatives Exchanges Ranked | CoinMarketCap" in self.driver.title
                        
                        # Initialize lists
                        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sc-71024e3e-0.ehyBa-d')))

                        # Initialize lists
                        name = []
                        volume = []

                        #Top 5 name list
                        name_ele_list = self.driver.find_elements(By.CSS_SELECTOR,'div[class="sc-4c05d6ef-0 sc-dff2ad65-1 dlQYLv hdzkHJ  hide-ranking-number"]')
                        for name_ele in name_ele_list[0:9:2]:
                            name.append(name_ele.text)

                            #Top 5 volume list
                        volume_ele_list = self.driver.find_elements(By.CSS_SELECTOR, 'td[style="text-align:end"]')
                        for volume_ele in volume_ele_list[0:30:6]:
                                volume.append(volume_ele.text)

                        # Create Dataframe and save to csv
                        df = pd.DataFrame({'Name':name, 'Volume':volume})
                        df.index += 1 

                        top_crypto = input("Please enter the name for the file without .csv extension")
                            
                        # Validate the filename 
                        if not re.match("^[A-Za-z0-9_-]*$", top_crypto):
                                print("Invalid filename. Please use only letters, numbers, underscores, or hyphens.")
                                return
                            
                            # Save to CSV
                        df.to_csv(f'{top_crypto}.csv', index=True)
                        print(f"Data saved to {top_crypto}.csv")

                    elif visit == "3":
                        return
                    
                    else:
                        print("Please select valide options!")
                        return    
                
            except TimeoutException:
                print("Error: The page took too long to load.")
            except NoSuchElementException:
                print("Error: Could not find elements on the page.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")


    # Additional feature: Screenshot 
    def screenshot(self):
        try:
            screenshot = ImageGrab.grab()
            png_name = input("Enter a name for the screenshot (without extension): ")

            # Validate the filename
            if not png_name or any(char in png_name for char in ['/', '\\', '?', '%', '*', ':', '|', '"', '<', '>']):
                print("Invalid filename. Please avoid using special characters.")
                return
            filename = f"{png_name}.png"
            self.driver.save_screenshot(filename)
            print(f"Screenshot saved as {filename}")

        except Exception as e:
            print(f"An error occurred while taking the screenshot: {e}")    
      
    # Compare currency data 
    def compare_cryptos(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        time.sleep(1)

        # Initialize a DataFrame to store the comparison data
        df = pd.DataFrame(columns=['Cryptocurrency', 'Price', 'Market Cap'])

        num_cryptos = int(input("How many cryptocurrencies would you like to compare? "))

        for idx in range(num_cryptos):
            # Search for each cryptocurrency on CoinMarketCap
            self.driver.get("https://coinmarketcap.com/")
            self.driver.maximize_window()

            crypto = input('What cryptocurrency would you like to search for?')

            time.sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[1]').click()
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, 'input[maxlength="200"]').send_keys(crypto)
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, 'input[maxlength="200"]').send_keys(Keys.RETURN)
            time.sleep(1)

            try:
                # Wait for the results to load and find the first result
                name_element = self.driver.find_element(By.CSS_SELECTOR, 'span[data-role="coin-name"]' )            

                price_element = self.driver.find_element(By.CSS_SELECTOR, 'span[data-test="text-cdp-price-display"]')

                market_cap_element = self.driver.find_element(By.CSS_SELECTOR,'div[class="BasePopover_base__T5yOf popover-base"]')

                # Extract text and append to DataFrame
                crypto_data = pd.DataFrame({
                    'Cryptocurrency': [name_element.text],
                    'Price': [price_element.text],
                    'Market Cap': [market_cap_element.text]
                })

                df = pd.concat([df, crypto_data], ignore_index=True)
                df.index += 1 

            except Exception as e:
                print(f"Could not retrieve data for {crypto}: {e}")

        # Display the comparison results
        print("\nCryptocurrency Comparison:")
        print(df)

    # Program destrcutor   
    def __del__(self):
        try:
            self.driver.quit()
            print("Exiting the program")
        except Exception as e:
            print(f"Error while existint the program: {e}")     

# function part 
def main():
    coin_marketcap = coinmarketcap()
    while True:
        choice = input(
            '''
            Would you like to:
            1. Search for cryptocurrency
            2. Getting top 10 information in exchanges or market cap website
            3. Top 5 exchanges name list with trading volume 
            4. Compare cryptocurrency
            5. Exit the program
            '''
            )
        
        if choice == "1":
            coin_marketcap.searching()
            addition = input("Would you like to have a screenshot of the current page? (Yes / No)").upper()
            if addition == "YES":
                coin_marketcap.screenshot()

            elif addition == "NO":
                pass
            else:
                print("Please enter valid options!")        

        elif choice == "2":
            coin_marketcap.top_10_info()

        elif choice == "3":
            coin_marketcap.top_exchanges() 

        elif choice == "4":
            coin_marketcap.compare_cryptos()

        elif choice == "5":
            coin_marketcap.__del__()   
            break

        else:
            print("Invalid! Please choose a valid number!")
            continue

# main program
if __name__ == "__main__":
    main()  
