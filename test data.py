from datetime import datetime, timedelta
from random import randint

n = 100


show_venue = sorted([(randint(1, 27),
                      randint(1, 20),
                      str(datetime(2023, 1, 1, 0, 0, 0)
                          + timedelta(days=randint(0, 356), hours=randint(8, 24))))
                     for i in range(n)])


bookings = sorted([(randint(1, 5), randint(1, n), randint(1, 5))
                  for i in range(20)])


print(*show_venue, sep=',\n', end=';\n')
print(*bookings, sep=',\n', end=';\n')
