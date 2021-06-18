from sympy import solve, Eq, symbols, nsimplify, simplify, parse_expr

var_symbol = '$'

x = symbols('x')
eq = Eq((9*10**9 * 6*10**-6 * x) / 0.05**2, 6)
print(nsimplify(solve(eq)[0]))
print(solve(Eq(parse_expr('5'), parse_expr('c3 + 2'))))
e = '5$c1$ / 3 * $m2$'
begin = 0
end = 0
last = False
for i in range(len(e)):
    if e[i] == '$':
        if last:
            end = i
            print(e[begin: end])
            last = False
        else:
            begin = i + 1
            last = True

class Equation_calc:
    def __init__(self, raw):
        self.eq = None
        self.raw = raw.strip()
        self.raw_clean = self.raw.replace('$', '')
        self.lhs = self.raw.split('=')[0]
        self.rhs = self.raw.split('=')[1]
        self.variables = {}
        self.extract_symbols()
    
    def extract_symbols(self):
        begin, end, last = 0, 0, False
        for i in range(len(self.raw)):
            if self.raw[i] == var_symbol:
                if last:
                    end = i
                    var = str(self.raw[begin: end])
                    self.variables[var] = symbols(var)
                    last = False
                else:
                    begin = i + 1
                    last = True

    def solve_equation(self, value_map):
        begin, end, last = 0, 0, False
        lhs_copy = self.lhs
        rhs_copy = self.rhs

        for i in value_map:
            value_map[i] = self.format(value_map[i])

        new_rhs_copy = ''
        for i in value_map:
            if i in lhs_copy:
                lhs_copy = lhs_copy.replace(f'{var_symbol}{i}{var_symbol}', value_map[i])
        print(lhs_copy)
        for i in range(len(rhs_copy)):
            if rhs_copy[i] == var_symbol:
                if last:
                    end = i
                    var = str(rhs_copy[begin: end])
                    if var in value_map:
                        new_rhs_copy = rhs_copy[: begin - 1] + str(value_map[var]) + rhs_copy[end + 1: ]
                    else:
                        new_rhs_copy = rhs_copy[: begin - 1] + rhs_copy[begin: end] + rhs_copy[end + 1: ]
                    last = False
                else:
                    begin = i + 1
                    last = True
        eq = Eq(parse_expr(lhs_copy), parse_expr(new_rhs_copy))
        return solve(eq)[0]
    def format(self, string):
        string = string.replace('^', '**')
        return string
b = Equation_calc('$x$/$q2$ = $t$')
print(b.solve_equation({'x':'10', 'q2': '1'}))

import math
def eng_string( x, sig_figs=3, si=False):
    """
    Returns float/int value <x> formatted in a simplified engineering format -
    using an exponent that is a multiple of 3.

    sig_figs: number of significant figures

    si: if true, use SI suffix for exponent, e.g. k instead of e3, n instead of
    e-9 etc.
    """
    x = float(x)
    sign = ''
    if x < 0:
        x = -x
        sign = '-'
    if x == 0:
        exp = 0
        exp3 = 0
        x3 = 0
    else:
        exp = int(math.floor(math.log10( x )))
        exp3 = exp - ( exp % 3)
        x3 = x / ( 10 ** exp3)
        x3 = round( x3, -int( math.floor(math.log10( x3 )) - (sig_figs-1)) )
        if x3 == int(x3): # prevent from displaying .0
            x3 = int(x3)

    if si and exp3 >= -24 and exp3 <= 24 and exp3 != 0:
        exp3_text = 'yzafpnum kMGTPEZY'[ exp3 // 3 + 8]
    elif exp3 == 0:
        exp3_text = ''
    else:
        exp3_text = '*10^%s' % exp3

    return ( '%s%s%s') % ( sign, x3, exp3_text)

print(eng_string(str(b.solve_equation({'x':'10', 'q2': '1'}))))