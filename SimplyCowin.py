import requests
from datetime import datetime
import calendar
import smtplib
import time
from playsound import playsound

class GenZCowin():

    def send_email_if_available(self):
        '''
            Calls the send_mail function only if the correct response is received by user_place_inputs function
        '''
        
        email_body = self.user_place_inputs()
        while email_body:
            letters = sum(chars.isalpha() for chars in email_body)
            if letters>67:
                self.send_mail(email_body)
                # if you wish to play any audio when you get slot uncomment next line 
                # playsound('<path to your audio file>')
                break
            else:
                print("No centers available.. Checking after 5 sec.")
                time.sleep(5)
                email_body = self.date_formatter()

    def user_place_inputs(self):
        '''
            Checks if returned API response is correct and is in the expected format
            
            Returns:
                email_body      :   Final email content containing the vaccine details for the specified sate, district and dates
                
            Exception:
                Incorrect API call 
        ''' 
        global state_dict, state_id, dist_id
        try:
            state_dict = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/states')
            # to accept user input values on every run, uncomment next two line
            # state_id = input("Enter state id: ")
            # dist_id = input("Enter district id: ")
            # For state_id and dist_id json files for the same are present in the project directory
            state_id = 21               #   Maharashtra
            dist_id = 363               #   Pune
            # Filter by pincode is future enhancement
            # pincode_dict = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=411048&date=05-05-2021')  
            email_body = self.date_formatter()
            return email_body
        except Exception as e:
            print("API Not returning current call. Retry will be done after 1 min.") 
            time.sleep(60)
            self.user_place_inputs()

    def date_formatter(self):
        '''
            Checks the response for given district and date 
            
            Returns:
                email_body      :   Final email content containing the vaccine details for the specified sate, district and dates 
        '''
        email_body = "\nHi! COVID-19 Vaccines are available for the age group between 18-44 years at below centers :\n"
        today = datetime.now().date().day
        # if you want to keep last searching date as month's last date uncomment below line and comment line 45
        # day_count= calendar.monthlen(2021, datetime.now().date().month)
        day_count = today + 3
        for date in range(today, day_count+1):
            if date < 10:
                date = '0' + str(date)
                today_date_format = f'{date}-05-2021'
            else:
                today_date_format = f'{date}-05-2021'
            print("Checking for date: {}".format(today_date_format))
            dist_dict = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}'.format(state_id))
            center_dict = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}'.format(dist_id, today_date_format))
            email_body += self.check_availability_by_dist(center_dict, state_id, dist_id, today_date_format)
        return email_body

    def check_availability_by_dist(self, center_dict, state_id, dist_id, today_date_format):
        '''
            Checks the vaccine availability of age group less than 45 for the desired center
            
            Arguments:
                center_dict         :   API response of the district id and desired date input
                state_id            :   API response of the specified state     
                dist_id             :   API response of the specified district
                today_date_format   :   Date of the format dd/mm/yyyy
            
            Returns:
                body                :   Day wise result of vaccine details
        '''
        body = ""
        for center, value in eval(center_dict.text).items():
            for center_list in value: 
                for sessions in center_list['sessions']:
                    if sessions['min_age_limit'] < 45 and center_list['sessions'][0]['available_capacity'] > 1 and sessions['date'] == today_date_format:
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
        '''
            Sends the email to the receiver's email id with the available slot information
            
            Arguments:
                body        :   Final body content of email
               
            Returns:
                None
        '''
        try:
            gmail_user = "<sender's email id>"
            gmail_password = "<Enter app generated password of above email id>"
            sent_from = gmail_user
            receivers_list = ["<Enter comma seperated values of receiver's email ids>"]
            subject = "COVID-19 Vaccines Available : Resgister ASAP"

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            # Check Email body locally
            # temp_file=open('temp.txt', 'w')
            # temp_file.write(body)
            # temp_file.close()
            # server.login(gmail_user, gmail_password)

            for user in receivers_list:
                email_text = """Subject: {} \nFrom: {} \n{}""".format(subject, gmail_user, body)
                server.sendmail(sent_from, user, email_text)
                print("Hooray! I've sent you an email with available vaccination centers and their time. Register ASAP. URL: https://www.cowin.gov.in/home")
            server.close()
        except Exception as e:
            print('Error: {}'.format(e))    

    
Sanket = GenZCowin()
Sanket.send_email_if_available()
