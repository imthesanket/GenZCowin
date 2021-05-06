import requests
from datetime import datetime
import calendar
import smtplib
import time

class GenZCowin():

    def send_email_if_available(self):
        email_body = self.user_place_inputs()
        while email_body:
            letters = sum(chars.isalpha() for chars in email_body)
            if letters>67:
                self.send_mail(email_body)
                break
            else:
                print("No centers available.. Checking after 15 mins.")
                time.sleep(30)
                email_body = self.date_formatter()

    def user_place_inputs(self):
        global state_id, dist_id, center_dict
        state_dict = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/states')
        state_id = input("Enter state id: ")
        dist_id = input("Enter district id: ")
        # Filter by pincode is future enhancement
        # pincode_dict = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=411048&date=05-05-2021')  
        email_body = self.date_formatter()
        return email_body

    def date_formatter(self):
        email_body = "\nHi! COVID-19 Vaccines are available for the age group between 18-44 years at below centers :\n"
        today = datetime.now().date().day
        day_count= calendar.monthlen(2021, datetime.now().date().month)
        for date in range(today, day_count+1):
            if date < 10:
                date = '0' + str(date)
                today_date_format = f'{date}-05-2021'
            else:
                today_date_format = f'{date}-05-2021'
            dist_dict = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}'.format(state_id))
            center_dict = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}'.format(dist_id, today_date_format))
            email_body += self.check_availability_by_dist(center_dict, state_id, dist_id, today_date_format)
        return email_body

    def check_availability_by_dist(self, center_dict, state_id, dist_id, today_date_format):
        body = ""
        for center, value in eval(center_dict.text).items():
            for center_list in value: 
                for sessions in center_list['sessions']:
                    if sessions['min_age_limit'] > 44 and center_list['sessions'][0]['available_capacity'] > 0 and sessions['date'] == today_date_format:
                        body += "\nCenter Name : {}\n".format(center_list['name'])
                        body += "Date : {}\n".format(today_date_format)
                        body += "Block Name : {}\n".format(center_list['block_name'])
                        body += "Pin Code: {}\n".format(center_list['pincode'])
                        body += "Vaccine: {}\n".format(center_list['sessions'][0]['vaccine'])
                        body += "Available Capacity : {}\n".format(center_list['sessions'][0]['available_capacity'])
                        body += "Slots : {}\n".format(center_list['sessions'][0]['slots']) 
                        body += "\n"
        return body

    def send_mail(self, body):
        try:
            gmail_user = '<Enter you email id>'
            gmail_password = '<Enter app generated password>'
            sent_from = gmail_user
            receivers_list = [<Enter email-ids of receivers>]
            subject = "COVID-19 Vaccines Available : Resgister ASAP"

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            # Check Email body locally
            # temp_file=open('temp.txt', 'w')
            # temp_file.write(body)
            # temp_file.close()
            server.login(gmail_user, gmail_password)

            for user in receivers_list:
                email_text = """Subject: {} \nFrom: {} \n{}""".format(subject, gmail_user, body)
                server.sendmail(sent_from, user, email_text)
                print("Hooray! I've sent you an email with available vaccination centers and their time. Register ASAP. URL: https://www.cowin.gov.in/home")
            server.close()
        except Exception as e:
            print('Error: {}'.format(e))    

    
Sanket = GenZCowin()
Sanket.send_email_if_available()
