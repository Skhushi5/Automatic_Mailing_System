import datetime as dt
import smtplib
import random
import os
from dotenv import load_dotenv

load_dotenv()

MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")
YOUR_NAME = os.getenv("YOUR_NAME")

def get_current_date():
    return dt.datetime.now()

def read_birthdays_from_csv(file_name):
    birthdays = []
    with open(file_name, "r") as file:
        for line in file.readlines()[1:]:  # skip header
            name, email, _, month, day = line.strip().split(",")
            birthdays.append({"name": name, "email": email, "month": int(month), "day": int(day)})
    return birthdays

def send_birthday_email(name, email):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        
        template_index = random.randint(1, 3)
        with open(f"letter_templates/letter_{template_index}.txt", "r") as file:
            template = file.read()
            message = template.replace('[Name]', name).replace('[Your_Name]', YOUR_NAME)
        
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=email, msg=message)

def main():
    current_date = get_current_date()
    birthdays = read_birthdays_from_csv("birthdays.csv")
    
    for birthday in birthdays:
        if birthday["month"] == current_date.month and birthday["day"] == current_date.day:
            print("Sending email")
            send_birthday_email(birthday["name"], birthday["email"])

if __name__ == "__main__":
    main()