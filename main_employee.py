import employee_info_scraping
import quickstart_company

quickstart_company.main()
employee_links = quickstart_company.getEmployeeLink()
compnay_names = quickstart_company.getCompanyNames()

print(employee_links)
print(compnay_names)

index = 0
for _ in range(len(employee_links)):
    employee_info_scraping.get_employee_info(employee_links[index], compnay_names[index])
    index += 1
