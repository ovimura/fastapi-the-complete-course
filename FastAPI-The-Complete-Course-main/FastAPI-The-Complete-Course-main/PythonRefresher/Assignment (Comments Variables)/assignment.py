"""
- You have $50
- You buy an item that is $15
- With a tax of 3%
- print how much money you have left
"""

money = 50
item = 15
tax = .03

money_left = money - item - (item * tax)

print(money_left)

print(50 - 15 - (15 * .03))

total = 50
tax_perc = 0.03
item = 15
tax = item * tax_perc
price = item + tax
money_left = total - price
print(money_left)

