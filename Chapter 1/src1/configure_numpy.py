from sklearn.utils import check_random_state
import numpy as np
from dautil import options
from dautil import log_api

random_state = check_random_state(42)
a = random_state.randn(5)

random_state = check_random_state(42)
b = random_state.randn(5)

np.testing.assert_array_equal(a, b)

printer = log_api.Printer()
printer.print("Default options", np.get_printoptions())

pi_array = np.pi * np.ones(30)
options.set_np_options()
print(pi_array)

# Reset
options.reset_np_options()
print(pi_array)
