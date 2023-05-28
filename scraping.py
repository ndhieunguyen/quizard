from selenium import webdriver
from selenium.webdriver.common.by import By
import time


url = "https://www.sanfoundry.com/1000-digital-image-processing-questions-answers/"
options = webdriver.ChromeOptions()

options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
driver.get(url)

entry_content = driver.find_element(By.CLASS_NAME, "entry-content")
questions = entry_content.find_elements(By.TAG_NAME, "p")
final_questions = []
for question in questions:
    if question.text.endswith("View Answer"):
        final_questions.append(question.text.replace("View Answer", ""))

clickable = entry_content.find_elements(By.TAG_NAME, "span")
print("Scraping data", end="")
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

content = ""
for question, answer in zip(final_questions, answers):
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    print()

    correct_answer = answer[answer.find("Answer:") + 8]
    explanation = answer[answer.find("Explanation:") + 13 :]

    content = content + question.replace("’", "'") + "~" + correct_answer + "#"
    # + "\n\nExplanation: " + explanation
driver.quit()

with open("output.txt", "w") as f:
    f.write(content)
