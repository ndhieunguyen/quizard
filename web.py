from selenium import webdriver
from selenium.webdriver.common.by import By
import streamlit as st

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

url = st.text_input("Enter first url")
enter_button = st.button("OK")

if enter_button:
    urls = [url]
    content = ""

    while True:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        try:
            entry_header = driver.find_element(By.CLASS_NAME, "entry-header")
            next_url_button = entry_header.find_element(By.XPATH, "//a[text()='Next']")
            next_url = next_url_button.get_attribute("href")
        except Exception as e:
            next_url = ""

        entry_content = driver.find_element(By.CLASS_NAME, "entry-content")
        questions = entry_content.find_elements(By.TAG_NAME, "p")
        final_questions = []
        for question in questions:
            if question.text.endswith("View Answer"):
                final_questions.append(question.text.replace("View Answer", ""))

        clickable = entry_content.find_elements(By.TAG_NAME, "span")

        for i, c in enumerate(clickable):
            driver.execute_script("window.scrollBy(0, 500);")
            flag = True
            while flag:
                driver.execute_script("window.scrollBy(0, 500);")
                try:
                    c.click()
                    print(".", end="")
                    flag = False
                except:
                    flag = True
        answers = [ele.text for ele in entry_content.find_elements(By.CLASS_NAME, "collapseomatic_content")]

        for question, answer in zip(final_questions, answers):
            correct_answer = answer[answer.find("Answer:") + 8]
            explanation = answer[answer.find("Explanation:") + 13 :]

            content = content + question.replace("’", "'") + "~" + correct_answer + "#"  # + "\n\nExplanation: " + explanation

        driver.quit()

        if next_url != "" and next_url not in urls:
            url = next_url
            urls.append(url)
        else:
            break

    content = content.encode()
    st.download_button("Download question bank", content)
