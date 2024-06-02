from persistence import *


def main():
    # TODO: implement
    print('Activities')
    activities = repo.activities.find_all()
    for activity in activities:
        print(activity.__str__())
    print('Branches')
    branches = repo.branches.find_all()
    branches.sort(key=lambda x: x.id)
    for branch in branches:
        print(branch.__str__())
    print('Employees')
    employees = repo.employees.find_all()
    employees.sort(key=lambda x: x.id)
    for employee in employees:
        print(employee.__str__())
    print('Products')
    products = repo.products.find_all()
    products.sort(key=lambda x: x.id)
    for product in products:
        print(product.__str__())
    print('Suppliers')
    suppliers = repo.suppliers.find_all()
    suppliers.sort(key=lambda x: x.id)
    for supplier in suppliers:
        print(supplier.__str__())

    # print employee report
    print('')
    print('Employees report')

    query = """      select name, salary, location,ifnull(total_sale_income,0) from
                (select name, salary, location, e.id from employees e
                inner join branches b on b.id = e.branche ) emp
                -- inner join activities
                left join
                (
               select activator_id, sum(total_income) as total_sale_income from
                    (select *, abs(price*activities.quantity) as total_income from activities inner join products p on p.id = activities.product_id
                    where activities.quantity <0)
                    group by 1 ) prods
                on emp.id = prods.activator_id
                order by name"""
    employee_report_rows = repo.execute_command(query)
    employee_report_rows = [
        (row[0].decode('utf-8'), row[1], row[2].decode('utf-8'), row[3]) if row[3] is not None else (
            row[0].decode('utf-8'), row[1], row[2].decode('utf-8'), 0) for row in employee_report_rows]
    for row in employee_report_rows:
        print(row[0], row[1], row[2], row[3])
    # print(len(data))
    print('')
    print('Activities report')
    # date descriptipon from products quantity name of seller (check if sellser ) supplier
    query_activities_report = """select * from (
                                    select activities.quantity, date, activator_id, product_id ,description, name from activities
                                    inner join products p on p.id = activities.product_id
                                    inner join employees e on e.id = activator_id
                                    union
                                    select activities.quantity, date, activator_id, product_id ,description, name from activities
                                    inner join products p on p.id = activities.product_id
                                    inner join suppliers s on s.id = activator_id )
                                    order by date"""
    activities_report_rows = repo.execute_command(query_activities_report)
    activities_report_rows = [
        (row[1].decode('utf-8'), row[4].decode('utf-8'), row[0],None, row[5].decode('utf-8')) if row[0] >0 else
            (row[1].decode('utf-8'), row[4].decode('utf-8'), row[0], row[5].decode('utf-8'),None) for row in activities_report_rows]
    for row in activities_report_rows:
        print(row)
        #
        # if row[0] < 0:
        #     print(f"'{row[1].decode('utf-8')}', '{row[4]}', {row[0]}, {row[5]},{None}")
        # else:
        #     print(f"'{row[1]}', '{row[4]}', {row[0]},{None},{row[5]}")




if __name__ == '__main__':
    main()
