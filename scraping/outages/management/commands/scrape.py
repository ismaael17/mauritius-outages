from django.core.management.base import BaseCommand
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from outages.models import *
from datetime import datetime
import translators.server as ts

class Command(BaseCommand):
    def handle(self, *args, **options):

        outages = Outage.objects.all()
        outages.delete()
        districts = ["Pamplemousses", "Riviere du Rempart", "Flacq", "Grand Port", "Moka", "Plaine Wilhems", "Savannes", "Black River"]
        district_ids = {
            "Pamplemousses": ("groupPamplemous", "table-mauritius-pamplemousses"),
            "Riviere du Rempart": ("groupRempart", "table-mauritius-rivieredurempart"),
            "Flacq": ("groupFlacq", "table-mauritius-flacq"),
            "Grand Port": ("groupGrandport", "table-mauritius-grandport"),
            "Moka": ("groupMoka", "table-mauritius-moka"),
            "Plaine Wilhems": ("groupPlaine", "table-mauritius-plainewilhems"),
            "Savannes": ("groupSavanne", "table-mauritius-savanne"),
            "Black River": ("groupBlackriver", "table-mauritius-blackriver")
        }

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get("https://ceb.mu/customer-corner/power-outage-information")

        for district in districts:
            thisDistrict = District.objects.get(name=district)
            id1, id2 = district_ids[district]
            element = driver.find_element(By.ID, id1)
            action = webdriver.ActionChains(driver)
            action.move_to_element(element).perform()
            element.click()
            driver.implicitly_wait(5)

            table = driver.find_element(By.ID, id2)
            table_body = table.find_element(By.TAG_NAME, "tbody")
            rows = table_body.find_elements(By.TAG_NAME, "tr")

            if rows:

                for row in rows[:-1]:
                    columns = row.find_elements(By.TAG_NAME, "td")

                    date_time_str = columns[0].text

                    # Split the string by " de " to separate the date and time information
                    date_str, time_str = date_time_str.split(" de ")

                    # Use the datetime library's strptime method to convert the date string to a date object

                    #use google translate to translate french to english
                    date_str = ts.google(date_str, from_language="fr", to_language="en")
                    print(date_str)
                    try:
                        date_obj = datetime.strptime(date_str, '%A, %B %d, %Y')
                    except ValueError:
                        date_obj = datetime.strptime(date_str, '%A %B %d, %Y')
                    date = date_obj.date()

                    # Use the datetime library's strptime method to convert the time string to a time object
                    time_str, end_time_str = time_str.split(" à ")
                    time_obj = datetime.strptime(time_str, '%H:%M:%S')
                    start_time = time_obj.time()

                    end_time_obj = datetime.strptime(end_time_str, '%H:%M:%S')
                    end_time = end_time_obj.time()

                    print(date)
                    print(start_time)
                    print(end_time)

                    location = columns[1].text


                    print(thisDistrict.name, date, start_time, end_time, location)
                    

                    outage = Outage(district=thisDistrict, date=date, start_time=start_time, end_time=end_time, location = location)
                    outage.save()
            else:

                outage = Outage.objects.filter(district=thisDistrict)
                outage.delete()


        driver.quit()