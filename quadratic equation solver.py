import cmath

def solver(a, b, c):
    return [
        (-b + cmath.sqrt(b**2 - 4*a*c)) / (2*a),
        (-b - cmath.sqrt(b**2 - 4*a*c)) / (2*a)
    ]

print(solver(1, 2, 1))