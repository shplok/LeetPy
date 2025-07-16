import leetpy as lp

# Fetch and show a specific problem
p = lp.get_problem("two-sum")
if p:
    p.show()

random_p = lp.get_problem()
if random_p:
    random_p.show()

# Or fetch and show the daily problem
daily = lp.get_daily_problem()
if daily:
    daily.show()

print(lp.solve(p))
lp.wait_for_all_windows_to_close()