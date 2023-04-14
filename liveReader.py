import pandas as pd
import inputData
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# Define prediction to be accessed by GUI
global prediction
prediction = ''
def liveRead():
    # Change URL to one specified in phyphox
    global prediction
    #url = 'http://10.216.105.182'
    url = 'http://172.20.10.1'

    # Set up selenium chrome driver
    options = Options()
    options.headless = True
    service = Service('/path/to/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    # Go to webpage
    driver.get(url)

    # Define and click simple button
    button = driver.find_element(By.CSS_SELECTOR, '#viewSelector > li:nth-child(4)')
    button.click()

    #create apandas data Frame
    column_labels = ['Time (s)', 'Linear Acceleration x (m/s^2)', 'Linear Acceleration y (m/s^2)',
                     'Linear Acceleration z (m/s^2)', 'Absolute acceleration (m/s^2)']
    record = pd.DataFrame(columns=column_labels)

    #create counter
    count = 0

    #get 10 readings
    while count < 10:

        #refresh webpage
        driver.refresh()
        button = driver.find_element(By.CSS_SELECTOR, '#viewSelector > li:nth-child(4)')
        button.click()

        #get readings
        x_element = driver.find_element(By.CSS_SELECTOR, 'div.valueElement.adjustableColor#element10 span.valueNumber')
        y_element = driver.find_element(By.CSS_SELECTOR, 'div.valueElement.adjustableColor#element11 span.valueNumber')
        z_element = driver.find_element(By.CSS_SELECTOR, 'div.valueElement.adjustableColor#element12 span.valueNumber')
        absolute_element = driver.find_element(By.CSS_SELECTOR, 'div.valueElement.adjustableColor#element13 span.valueNumber')


        #Add reasdings to dataframe if all are available
        if x_element.text != '' and y_element.text != '' and z_element.text != '' and absolute_element.text != '':
            new_row = {'Time (s)': 0, 'Linear Acceleration x (m/s^2)': x_element.text,
                       'Linear Acceleration y (m/s^2)': y_element.text,
                       'Linear Acceleration z (m/s^2)': z_element.text,
                       'Absolute acceleration (m/s^2)': absolute_element.text}
            for i in range(50): #add 50 times
                record = record.append(new_row, ignore_index=True)
            count += 1
            print(count)

    # make prediction on dataframe
    result = inputData.proc(record)
    prediction = result[0]
    print("prediction" + prediction)

    # close chrome driver
    driver.quit()
liveRead()