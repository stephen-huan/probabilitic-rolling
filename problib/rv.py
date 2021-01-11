import bisect, math
# library implementing a random variable

EPSILON = 10**-3 # permissible distance from 1

### normalization and verification methods

def norm(l: list, f: float=None) -> list:
    """ Normalizes a list into a pmf by dividing by its sum. """
    s = sum(l) if f is None else f
    return [x/s for x in l]

def norm_cmf(l: list) -> list:
    """ Normalizes a list into a cmf by dividing by its max. """
    return norm(l, max(l))

def nonneg(l: list) -> bool:
    """ Whether all the values in a list are positive. """
    return all(map(lambda x: x >= 0, l))

def diff(x: float, y: float, tol: float=EPSILON) -> bool:
    """ Whether two numbers are sufficiently close. """
    return abs(x - y) < tol

def pmf(l: list, tol: float=EPSILON) -> bool:
    """ Whether a list can be interpreted as a pmf. """
    return nonneg(l) and diff(sum(l), 1, tol)

def cmf(l: list, tol: float=EPSILON) -> bool:
    """ Whether a list can be interpreted as a cmf. """
    return nonneg(l) and l == sorted(l) and diff(l[-1], 1, tol)

### random variable

def prefix_sum(l: list) -> list:
    """ Returns the prefix sum of l. """
    prefix = [0]*(len(l) + 1)
    for i in range(len(l)):
        prefix[i + 1] = prefix[i] + l[i]
    return prefix

class RandomVariable:

    """ A random variable. """

    def __init__(self, X: list, p: list, name: str="rv", norm: bool=False):
        self.X, self.p = X, p       # list of values and list of probabilities
        self.name, self.p = name, norm(self.p) if norm else self.p
        self.D = {x: i for i, x in enumerate(X)} # value to index
        self.F = prefix_sum(self.p) # cmf

        assert sorted(X) == list(X), "support set must be sorted"
        assert pmf(self.p), "not a valid pmf"
        assert cmf(self.F), "not a valid cmf"

    ### Python "magic" class methods

    def __repr__(self) -> str: return f"RandomVariable({self.X}, {self.p})"
    def  __str__(self) -> str: return f"RandomVariable {self.name}: \n\
mean = {self.E():.3f} +/- {self.std():.3f} (std)"
    def __len__(self) -> int: return len(self.X)
    def __iter__(self): return self.X.__iter__()
    def __getitem__(self, i: int) -> float: return self.X[i]
    def __call__(self, k: float) -> float: return self.pmf(k)

    ### properties intrinsic to a random variable

    def pmf(self, u: float) -> float:
        """ Finds the pmf at a value in/not in the underlying r.v. """
        return self.p[self.D[u]] if u in self.D else 0

    def cmf(self, u: float) -> float:
        """ Finds the cmf at a value in/not in the underlying r.v. """
        # use F if u is in the range of the r.v., otherwise binary search
        return self.F[self.D[u] + 1] if u in self.D else \
               self.F[bisect.bisect(self.X, u)]

    ### transformations

    def transform(self, f):
        """ Returns a new random variable transformed by a given function. """
        freq = {}
        for x in self:
            y = f(x)
            freq[y] = freq.get(y, 0) + self.pmf(x)
        return RandomVariable(*map(list, zip(*sorted(freq.items()))))

    def map(self, f):
        """ Returns a new random variable with probabilities given by f. """
        return RandomVariable(self, list(map(f, self)))

    ### probability theory statistics

    def E(self, f=lambda x: x) -> float:
        """ Expected value of a pmf represented by a list. """
        return sum(f(self.X[i])*self.p[i] for i in range(len(self.X)))

    def Var(self) -> float:
        """ Var[X] = E[(x - u)^2] = E[X^2] - E[x]^2. """
        return self.E(lambda x: x*x) - self.E()**2

    def std(self) -> float:
        """ sigma^2 = Var[x] so sigma = standard deviation = sqrt(Var[X]). """
        return math.sqrt(self.Var())

    def range(self) -> float:
        """ Maximum element minus the minimum element. """
        return self[-1] - self[0]

if __name__ == "__main__":
    X = [   1,    5,  10,   15,   16,   20,  30,   35,   50,  100]
    p = [0.05, 0.08, 0.1, 0.12, 0.17, 0.22, 0.1,  0.1, 0.05, 0.01]

    rv = RandomVariable(X, p)
    print(rv, rv(10))
    print(len(rv), min(rv), max(rv), sum(rv))
    print(sum(x*x for x in rv))
    print(rv[1])

    print(rv.E(), rv.Var(), rv.std(), rv.range())

    X = [ -2,  -1,   1,   2,   3]
    p = [0.1, 0.2, 0.5, 0.1, 0.1]
    rv = RandomVariable(X, p)
    print(rv.transform(lambda x: x*x))

