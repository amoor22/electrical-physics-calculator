import math
from pytexit.pytexit import py2tex
from sympy import solve, Eq, symbols, nsimplify, simplify, parse_expr

var_symbol = '$'

x = symbols('x')
eq = Eq((9*10**9 * 6*10**-6 * x) / 0.05**2, 6)
# print(nsimplify(solve(eq)[0]))
# print(solve(Eq(parse_expr('5'), parse_expr('c3 + 2'))))
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
    # if 0 < x < 1:
    #     return f'{round(x, 3)}'
    return ( '%s%s%s') % ( sign, x3, exp3_text)

def totex(string):
    string = str(string)
    try:
        return py2tex(string, simplify_multipliers=False, print_formula=False, print_latex=False)
    except:
        return None

class Equation_calc:
    def __init__(self, raw):
        self.eq = None
        self.raw = raw.strip()
        self.raw = self.raw.lower()
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

        value_map_c = self.clean_map(value_map.copy())

        for i in value_map_c:
            value_map_c[i] = self.format(value_map_c[i])

        for i in value_map_c:
            if i in lhs_copy:
                lhs_copy = lhs_copy.replace(f'{var_symbol}{i}{var_symbol}', value_map_c[i])

        for i in value_map_c:
            if i in rhs_copy:
                rhs_copy = rhs_copy.replace(f'{var_symbol}{i}{var_symbol}', value_map_c[i])
        
        lhs_copy = lhs_copy.replace('$', '')
        rhs_copy = rhs_copy.replace('$', '')

        eq = Eq(parse_expr(lhs_copy), parse_expr(rhs_copy))
        solving = solve(eq)
        if len(solving) == 2:
            answer = solving[1]
        else:
            answer = solving[0]
        try:
            answer = eng_string(answer)
        except:
            pass
        return answer
    
    def format(self, string):
        string = string.replace('^', '**')
        return string

    def clean_map(self, mp):
        to_delete = []
        to_add = {}
        for i in mp:
            if i.isupper():
                to_add[i.lower()] = mp[i]
                to_delete.append(i)
        for i_lower in to_add:
            mp[i_lower] = to_add[i_lower]
        for j in to_delete:
            del mp[j]
        return mp

def format(string):
    string = string.replace('^', '**')
    return string

b = Equation_calc('$E$ = $F$ / $q$')
# print(solve(Eq(parse_expr('E'), parse_expr('4 / 10'))))
# print(b.solve_equation({'F':"4", 'q':'8^2'}))