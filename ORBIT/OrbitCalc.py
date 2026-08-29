import math
import cmath

def calc(string:str):
    string += " "
    nums = []
    num_in = ""
    symbols = ["+", "-", "*", "/", "//", "%", "^", "**", "√"]
    symbol = []

    i = 0

    while i < len(string):

        # --------------------------------
        # NUMBER
        # --------------------------------

        if string[i].isdigit() or string[i] == ".":

            num_in += string[i]

        # --------------------------------
        # NEGATIVE NUMBER
        # --------------------------------

        elif string[i] == "-" and (
            i == 0 or string[i - 1] in symbols or string[i - 1] == " "
        ):
            num_in += string[i]

        # --------------------------------
        # SYMBOL
        # --------------------------------

        else:

            if num_in != "":
                nums.append(float(num_in))
                num_in = ""

            found_symbol = ""

            # Check for longest symbols first
            for j in range(len(symbols)):

                if string.startswith(symbols[j], i):

                    if len(symbols[j]) > len(found_symbol):
                        found_symbol = symbols[j]

            if found_symbol != "":

                symbol.append(found_symbol)
                i += len(found_symbol) - 1

        i += 1

    # --------------------------------
    # ERROR CHECKING
    # --------------------------------

    if len(symbol) != 1:
        return "Symbol Error"

    if len(nums) != 2:
        return "Num Amount Error"

    # --------------------------------
    # CALCULATIONS
    # --------------------------------

    if symbol[0] == "+":
        return float(nums[0] + nums[1])

    if symbol[0] == "-":
        return float(nums[0] - nums[1])

    if symbol[0] == "*":
        return float(nums[0] * nums[1])

    if symbol[0] == "/":
        if nums[1] == 0:
            return "Math Error"
        return float(nums[0] / nums[1])

    if symbol[0] == "//":
        if nums[1] == 0:
            return "Math Error"
        return float(nums[0] // nums[1])

    if symbol[0] == "%":
        if nums[1] == 0:
            return "Math Error"
        return float(nums[0] % nums[1])

    if symbol[0] == "^":
        return float(nums[0] ** nums[1])

    if symbol[0] == "**":
        return float(nums[0] ** nums[1])

    if symbol[0] == "√":
        if nums[0] == 0:
            return "Math Error"
        return float(nums[1] ** (1 / nums[0]))

def quadraticSolver(a, b, c):
    return [
        (-b + cmath.sqrt(b**2 - 4*a*c)) / (2*a),
        (-b - cmath.sqrt(b**2 - 4*a*c)) / (2*a)
    ]