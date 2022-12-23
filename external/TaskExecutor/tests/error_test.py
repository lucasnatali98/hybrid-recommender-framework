import random
import sys
import time

out = sys.stderr if random.randint(1, 100) == 1 else sys.stdout
print('Hello\n\tWorld!', file=out, flush=True)
time.sleep(1)
sys.exit(1 if random.randint(1, 100) == 1 else 0)
