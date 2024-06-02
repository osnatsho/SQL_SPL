from persistence import *

import sys

def main(args):
    inputfilename : str = args[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(", ")
            #TODO: apply the action (and insert to the table) if possible
            prod_id = int(splittedline[0])
            quantity = int(splittedline[1])
            activator_id = int(splittedline[2])
            date = splittedline[3]
            prod = repo.products.find(id=prod_id)[0]
            new_product_quantity = prod.quantity + quantity

            if new_product_quantity > 0:
                repo.activities.insert(Activitie(prod_id, quantity, activator_id, date))
                repo.products.update(set_values=dict(quantity=new_product_quantity),cond=dict(id=prod_id))




if __name__ == '__main__':
    main(sys.argv)