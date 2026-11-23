import argparse
from fractions import Fraction
import hashlib
import json
from math import comb
from pathlib import Path


def polynomial_product(left, right):
    result = {}
    for (left_parameter, left_variable), left_value in left.items():
        for (right_parameter, right_variable), right_value in right.items():
            degree = (left_parameter + right_parameter, left_variable + right_variable)
            result[degree] = result.get(degree, 0) + left_value * right_value
    return {degree: value for degree, value in result.items() if value}


def next_row(row, middle, last):
    result = [0] * (len(row) + 2)
    for degree, coefficient in enumerate(row):
        result[degree] += coefficient
        result[degree + 1] += middle * coefficient
        result[degree + 2] += last * coefficient
    return result


def independent_coefficient(exponent, degree, middle, last):
    return sum(comb(exponent, selected) * comb(exponent - selected, degree - 2 * selected)
               * middle ** (degree - 2 * selected) * last ** selected
               for selected in range(exponent + 1)
               if 0 <= degree - 2 * selected <= exponent - selected)


def read_table(path):
    return {int(fields[0]): int(fields[1])
            for line in path.read_text().splitlines()
            if (fields := line.split()) and not fields[0].startswith('#')}


def main():
    parser = argparse.ArgumentParser(description='Exact quadratic-family and row-identity checks.')
    parser.add_argument('--source-dir', type=Path)
    args = parser.parse_args()
    factor = {(1, 1): 4, (1, 0): 1, (0, 0): -1}
    assert polynomial_product(factor, factor) == {
        (2, 2): 16, (2, 1): 8, (1, 1): -8,
        (2, 0): 1, (1, 0): -2, (0, 0): 1}
    maximum_numerator = {(3, 0): 4, (2, 0): 9, (1, 0): 6, (0, 0): 1}
    norm_times_denominator = {
        (3, 0): 4, (2, 0): 8, (1, 0): 8,
        (1, 1): 8, (2, 1): -8, (2, 2): -16}
    difference = {degree: maximum_numerator.get(degree, 0) - norm_times_denominator.get(degree, 0)
                  for degree in maximum_numerator.keys() | norm_times_denominator.keys()}
    assert {degree: value for degree, value in difference.items() if value} == polynomial_product(factor, factor)
    expected_initial = {
        1: [1, 3, 7, 13, 35, 83, 165, 367, 899, 1957],
        2: [1, 4, 14, 44, 124, 394, 1418, 4706, 14322, 40712],
        3: [1, 5, 23, 99, 401, 1525, 6345, 27331, 122083, 520805]
    }
    identifiers = {1: 'A084611', 2: 'A084613', 3: 'A084615'}
    table_checks = []
    for parameter in (1, 2, 3):
        radius_square = Fraction((parameter + 1) ** 2 * (4 * parameter + 1), 4 * parameter)
        numerator, denominator = radius_square.numerator, radius_square.denominator
        numerator_power, denominator_power = 1, 1
        row = [1]
        values = []
        for exponent in range(1001):
            total = sum(abs(coefficient) for coefficient in row)
            values.append(total)
            scaled_square = total * total * denominator_power
            assert numerator_power <= scaled_square <= (2 * exponent + 1) * numerator_power
            assert sum(coefficient * coefficient for coefficient in row) * denominator_power <= numerator_power
            assert sum(row) == (2 - parameter) ** exponent
            assert sum((-1) ** degree * coefficient for degree, coefficient in enumerate(row)) == (-parameter) ** exponent
            assert row[-1] == (-parameter) ** exponent
            if exponent:
                assert row[-2] == exponent * (-parameter) ** (exponent - 1)
            if exponent < len(expected_initial[parameter]):
                assert total == expected_initial[parameter][exponent]
            if exponent < 30:
                assert row == [independent_coefficient(exponent, degree, 1, -parameter)
                               for degree in range(2 * exponent + 1)]
            row = next_row(row, 1, -parameter)
            numerator_power *= numerator
            denominator_power *= denominator
        if args.source_dir:
            identifier = identifiers[parameter]
            path = args.source_dir / ('b' + identifier[1:] + '.txt')
            table = read_table(path)
            indices = sorted(set(table) & set(range(1001)))
            assert indices and indices == list(range(indices[-1] + 1))
            assert all(values[index] == table[index] for index in indices)
            table_checks.append({'sequence': identifier, 'indices': [indices[0], indices[-1]],
                                 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                                 'source_url': f'https://oeis.org/{identifier}/b{identifier[1:]}.txt'})
    for middle, last in [(1, 2), (1, 3), (1, 4), (2, 2), (2, 3)]:
        row = [1]
        for exponent in range(101):
            assert all(coefficient >= 0 for coefficient in row)
            assert sum(row) == (1 + middle + last) ** exponent
            assert sum((-1) ** degree * coefficient for degree, coefficient in enumerate(row)) == (1 - middle + last) ** exponent
            if exponent < 15:
                assert row == [independent_coefficient(exponent, degree, middle, last)
                               for degree in range(2 * exponent + 1)]
            row = next_row(row, middle, last)
    rows = [[1]]
    for exponent in range(1, 101):
        rows.append(next_row(rows[-1], 1, -1))
    for index in range(101):
        diagonal = sum(rows[index - degree][degree] for degree in range(index + 1)
                       if degree < len(rows[index - degree]))
        assert diagonal == (index + 2) // 2
    output = {
        'status': 'pass',
        'algebra': 'The quadratic maximum-gap identity is a polynomial identity in m and u.',
        'quadratic_parameters': [1, 2, 3],
        'quadratic_squared_bounds_and_row_identities': '0 <= n <= 1000',
        'independent_quadratic_coefficients': '0 <= n <= 29; every coefficient',
        'initial_absolute_sums': 'First ten values of A084611, A084613 and A084615',
        'nonnegative_rows': '0 <= n <= 100; (b,c)=(1,2),(1,3),(1,4),(2,2),(2,3)',
        'independent_nonnegative_coefficients': '0 <= n <= 14; every coefficient',
        'A084610_diagonal_sum': '0 <= n <= 100',
        'arithmetic': 'Integer and rational arithmetic',
        'scope': 'Finite checks; the parameter-family limits and all-index identities have written proofs.'
    }
    if table_checks:
        output['oeis_tables'] = table_checks
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
