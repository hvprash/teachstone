#!/usr/bin/python3

import requests
import os
import pandas as pd
import datetime
import time


''' Download this CSV file to the container '''
def download_csv(url) -> bool:
  try:
    req_csv = requests.get(url)
    req_csv.raise_for_status()
    open('organizations-100.csv', 'wb').write(req_csv.content)
  except Exception as e:
    print('Failed getting the file', e)
    return False
  return True

''' Extract a list of the full names of all the people - sorted '''
def extract_names(csv_file, name_file) -> None:
  df = pd.read_csv(csv_file).sort_values(by=['Name'])
  names = df.Name.to_list()
  file = open(name_file,'w')
  file.writelines([name + '\n' for name in names])
  file.close()
  return names

''' Total Employees (add employees in all companies) '''
def total_employees(csv_file) -> int:
  file_employee_count = '/tmp/employee_count.txt'
  df = pd.read_csv(csv_file)
  num_of_empl = df['Number of employees'].to_list()
  total = sum(num_of_empl)
  file = open(file_employee_count,'w')
  file.write('Total number of employees: ' + str(total))
  return total

''' Extract all company names with abbreviation 'Inc' '''
def fetch_company_abbr(file_name, abbr) -> list:
  file_lines_with_abbr = '/tmp/lines-with-inc.txt'
  abbr_companies = []
  if os.path.exists(file_lines_with_abbr):
    os.remove(file_lines_with_abbr)
  companies = [line.strip() for line in open(file_name, 'r')]
  for company in companies:
    with open(file_lines_with_abbr, 'a') as abbr_file:
      if abbr.lower() in company.lower().split():
        abbr_file.write(company + '\n')
        abbr_companies.append(company)
  return abbr_companies

''' Get my IP '''
def get_my_ip() -> str:
  my_ip = requests.get('https://api.ipify.org/')
  return my_ip.text


def main():
  file_company_names = '/tmp/names.txt'
  file_final_report  = '/tmp/final-report.txt'
  csv_url = 'https://media.githubusercontent.com/media/datablist/sample-csv-files/main/files/organizations/organizations-100.csv'

  ''' Actions '''
  file_status = download_csv(csv_url)
  if file_status:
    names = extract_names('organizations-100.csv', file_company_names)
    total = total_employees('organizations-100.csv')
    abbr = 'Inc'
    abbr_companies = fetch_company_abbr(file_company_names, abbr)
    my_ip = get_my_ip()
    
    ''' Generate final report '''
    current_time = datetime.date.today()
    current_date = datetime.date.strftime(current_time, '%m/%d/%Y')
    final_report = open(file_final_report,'a')
    final_report.write('Report created on {} from {} \n\n'.format(current_date, my_ip))
    final_report.write('Total number of employees: {} \n\n'.format(total))
    final_report.write('Companies that contain the word {}:\n\n'.format(abbr))
    for abbr_company in abbr_companies:
      final_report.write('* {} \n'.format(abbr_company))
    final_report.write('\n')
    final_report.write('All names, sorted:\n* {} '.format('\n* '.join(names)))
    final_report.close()
  else:
    print('ERROR: Unable to download CSV File')

if __name__ == '__main__':
  main()