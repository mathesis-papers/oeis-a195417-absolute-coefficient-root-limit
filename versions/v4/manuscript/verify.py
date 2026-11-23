import argparse
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
from math import comb
from pathlib import Path


def multiply(left, right):
    return (left[0] * right[0] + 13 * left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def nonnegative(pair):
    rational, radical = pair
    if rational >= 0 and radical >= 0:
        return True
    if rational < 0 and radical < 0:
        return False
    if rational >= 0:
        return rational * rational >= 13 * radical * radical
    return 13 * radical * radical >= rational * rational


def product(left, right):
    output = [(Fraction(0), Fraction(0)) for degree in range(len(left) + len(right) - 1)]
    for left_degree, left_value in enumerate(left):
        for right_degree, right_value in enumerate(right):
            value = multiply(left_value, right_value)
            degree = left_degree + right_degree
            output[degree] = (output[degree][0] + value[0], output[degree][1] + value[1])
    return output


def independent_coefficient(exponent, degree):
    return sum((-1) ** cubic * comb(exponent, cubic) * comb(exponent - cubic, degree - 3 * cubic)
               for cubic in range(exponent + 1)
               if 0 <= degree - 3 * cubic <= exponent - cubic)


def circle_norm_polynomial(coefficients):
    degree = len(coefficients) - 1
    chebyshev = [[1], [0, 1]]
    for order in range(2, degree + 1):
        polynomial = [0] * (order + 1)
        for index, value in enumerate(chebyshev[-1]):
            polynomial[index + 1] += 2 * value
        for index, value in enumerate(chebyshev[-2]):
            polynomial[index] -= value
        chebyshev.append(polynomial)
    output = [0] * (degree + 1)
    output[0] = sum(value * value for value in coefficients)
    for difference in range(1, degree + 1):
        correlation = sum(coefficients[index] * coefficients[index + difference]
                          for index in range(len(coefficients) - difference))
        for index, value in enumerate(chebyshev[difference]):
            output[index] += 2 * correlation * value
    return output


def main():
    parser = argparse.ArgumentParser(description='Exact finite coefficient and inequality checks.')
    parser.add_argument('--bfile', type=Path)
    args = parser.parse_args()
    assert circle_norm_polynomial([1, 1, 0, -1]) == [5, 8, -4, -8]
    assert circle_norm_polynomial([1, 1, -1]) == [5, 0, -4]
    first_terms = [1, 3, 9, 25, 63, 171, 471, 1193, 3209, 8841, 22537,
                   60393, 165489, 424451, 1134849, 3093893, 7987289,
                   21288933, 57973543, 150409931, 399788279, 1085870421,
                   2831439537, 7501994181, 20330726077, 53274740933,
                   140615421393, 380366331549, 1002078031627, 2634444052559]
    factor = [(Fraction(1), Fraction(-1)), (Fraction(6), Fraction(0))]
    last_factor = [(Fraction(1), Fraction(2)), (Fraction(6), Fraction(0))]
    identity = product(product(factor, factor), last_factor)
    identity = [(rational / 27, radical / 27) for rational, radical in identity]
    assert identity == [(Fraction(-38, 27), Fraction(26, 27)),
                        (Fraction(-8), Fraction(0)), (Fraction(4), Fraction(0)),
                        (Fraction(8), Fraction(0))]
    coefficients = [1]
    quadratic = [1]
    power = (1, 0)
    denominator = 1
    quadratic_power = 1
    values = []
    for exponent in range(1001):
        total = sum(abs(value) for value in coefficients)
        values.append(total)
        scaled_square = denominator * total * total
        assert nonnegative((scaled_square - power[0], -power[1]))
        assert nonnegative(((3 * exponent + 1) * power[0] - scaled_square,
                            (3 * exponent + 1) * power[1]))
        squared_norm = sum(value * value for value in coefficients)
        assert nonnegative((power[0] - denominator * squared_norm, power[1]))
        quadratic_total = sum(abs(value) for value in quadratic)
        assert quadratic_power <= quadratic_total ** 2 <= (2 * exponent + 1) * quadratic_power
        if exponent < len(first_terms):
            assert total == first_terms[exponent]
            assert coefficients == [independent_coefficient(exponent, degree)
                                    for degree in range(3 * exponent + 1)]
        next_coefficients = [0] * (len(coefficients) + 3)
        for degree, value in enumerate(coefficients):
            next_coefficients[degree] += value
            next_coefficients[degree + 1] += value
            next_coefficients[degree + 3] -= value
        coefficients = next_coefficients
        next_quadratic = [0] * (len(quadratic) + 2)
        for degree, value in enumerate(quadratic):
            next_quadratic[degree] += value
            next_quadratic[degree + 1] += value
            next_quadratic[degree + 2] -= value
        quadratic = next_quadratic
        power = multiply(power, (97, 26))
        denominator *= 27
        quadratic_power *= 5
    with localcontext() as context:
        context.prec = 60
        radius = ((Decimal(97) + 26 * Decimal(13).sqrt()) / 27).sqrt()
    result = {
        'status': 'pass',
        'algebra': 'Both unit-circle norm-square polynomials and the cubic maximum-gap identity hold exactly.',
        'coefficient_identity_indices': '0 <= n <= 29; every coefficient',
        'A195417_initial_terms_matched': 30,
        'cubic_and_quadratic_bound_indices': '0 <= n <= 1000',
        'arithmetic': 'Integer arithmetic and exact rational arithmetic in Q(sqrt(13)).',
        'radius_decimal_60_significant_digits': str(radius),
        'A195417_a1000_sha256_decimal': hashlib.sha256(str(values[1000]).encode()).hexdigest(),
        'scope': 'Finite checks of coefficients, squared norm bounds and two-sided coefficient bounds; the all-index limits follow from the written proofs.'
    }
    if args.bfile:
        expected = {}
        for line in args.bfile.read_text().splitlines():
            if line.strip() and not line.lstrip().startswith('#'):
                exponent, value = map(int, line.split())
                expected[exponent] = value
        assert all(expected[exponent] == values[exponent] for exponent in range(1001))
        result['A195417_bfile'] = {'indices': '0 <= n <= 1000',
                                  'sha256': hashlib.sha256(args.bfile.read_bytes()).hexdigest(),
                                  'source_url': 'https://oeis.org/A195417/b195417.txt'}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
