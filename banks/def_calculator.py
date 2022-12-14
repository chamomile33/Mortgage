def calc(rate, term, deposit, cost):
    credit = cost-deposit
    annual_payment = credit*(rate/100/12)/(1-(1+rate/100/12)**(-term*12))
    return annual_payment

