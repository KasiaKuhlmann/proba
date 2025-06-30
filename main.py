import itertools

n = 7

# funkcja przesuwająca wektor o k w prawo
def shift_vector(k, vec):
    return vec[-k:] + vec[:-k]

def max_vector(vectors):
    return [max(coord) for coord in zip(*vectors)]

# wygenerowanie wektorów o długości n i zawierających przynajmniej jedną jedynkę
vectors = [vector for vector in itertools.product([0, 1], repeat=n) if 1 in vector]

#generowanie produktow
if n % 2 == 0:
    products_first = itertools.product(vectors, repeat=n//2+1)
    products_start = [p for p in products_first if p[-1][:n//2] == p[-1][n//2:] and p[0][0] == 0]
else:
    products_first = itertools.product(vectors, repeat=n//2+1)
    products_start = [p for p in products_first if p[0][0] == 0]


# dodawanie nowych wektorów do produktów
new_products = set()
for product in products_start:

    if n % 2 == 0:
        new_vectors = []
        for i in range(n//2-1):
            new_vector = shift_vector(n//2+1+i, product[n//2-1-i])
            new_vectors.append(new_vector)
        new_product = product + tuple(new_vectors)

    else:
        new_vectors = []
        for i in range(n//2):
            new_vector = shift_vector(n//2+1+i, product[n//2-i])
            new_vectors.append(new_vector)
        new_product = product + tuple(new_vectors)

    new_products.add(new_product)

# sprawdzenie, czy wynik operacji merge_vectors dla new_product składa się tylko z jedynek
products = set()
for product in new_products:
    merged_vector = max_vector(v for v in product)
    if all(merged_vector[k]==1 for k in range(n)):
       products.add(product)

#warunek z 1-1 i 1+1
special_products= set()
for p in products:
    I = set(i for i in range(n) if p[0][i] == 1)
    J = set(j for j in range(n) if p[j][0] == 1)
    if not I.intersection(J):
        special_products.add(p)

for p in special_products:
    A = set()
    for i in I:
        for j in J:
            A.add((i + j) % n)
 #   print(p, A)

# products zdefiniowane jako te p w products_start w ktorych jesli p[k][0]=1 to k nalezy do A(p)
correct_products = set()
for p in special_products:
     if all(k in A for k in range(n) if p[k][0] == 1):
        correct_products.add(p)



# obliczanie sum s_kl

def s(product, k, l):
    return shift_vector(k, product[(l - k) % n])

def ppp(product, m, k, l):
    return max_vector(s(product, i, l) for i in range(n) if s(product, m, k)[i] == 1)

#sprawdzanie lacznosci dla dodatnich
good_products = set()
for product in correct_products:
    if all(ppp(product, 0, k, l) == ppp(product, k, l, 0) for k in range(n) for l in range(n)):
          good_products.add(product)


# obliczanie roznic r_kl
def r_pos(product, k, l):
    result = [0] * n
    for i in range(n):
        if s(product, i, l)[k] == 1:
            result[i] = 1
        else:
            result[i] = 0
    return result


def r_neg(product, k, l):
    result = [0] * n
    for i in range(n):
        if s(product, i, k)[l] == 1:
            result[i] = 1
        else:
            result[i] = 0
    return result

# lacznosc
def pmp_pos(product, m, k, l):
    return max_vector([
        max_vector(s(product, i, l) for i in range(n) if r_pos(product, m, k)[i] == 1),
        max_vector(r_pos(product, l, i) for i in range(n) if r_neg(product, m, k)[i] == 1)
    ])


def pmp_neg(product, m, k, l):
    return max_vector(r_neg(product, l, i) for i in range(n) if r_neg(product, m, k)[i] == 1)


def mpp_pos(product, m, k, l):
    return max_vector(r_pos(product, i, m) for i in range(n) if s(product, k, l)[i] == 1)


def mpp_neg(product, m, k, l):
    return max_vector(r_neg(product, i, m) for i in range(n) if s(product, k, l)[i] == 1)


best_products = set()
for product in good_products:
    if all(pmp_pos(product, 0, k, l) == pmp_pos(product, k, l, 0) and
           pmp_neg(product, 0, k, l) == pmp_neg(product, k, l, 0) and
           pmp_pos(product, k, 0, l) == mpp_pos(product, 0, k, l) and
           pmp_neg(product, k, 0, l) == mpp_neg(product, 0, k, l) and
           pmp_pos(product, 0, k, k)[0] == 1 for k in range(n) for l in range(n)):
        best_products.add(product)


def cchar(product, vector):
    if vector[0] == 0:
        k = 2
    else:
        k = 1
    while True:
        ama = [(s_vectors[product][(0, i)], i) for i in range(n) if vector[i] == 1]
        amal = max_vector([v for v, i in ama])
        if amal[0] == 1:
            break
        vector = [amal[i] for i in range(n)]
        k += 1
    return k

# Wyświetl wyniki dla każdego najlepszego produktu

    # sortowanie produktów po wartościach cchar
sorted_products = sorted(best_products, key=lambda p: cchar(p, s_vectors[p][(0, 0)]))
# wyświetlenie wyników
for product in sorted_products:
    vector = s_vectors[product][(0, 0)]
    iterations = cchar(product, vector)
    vector = s_vectors[product][(0, 0)]
    iterations = cchar(product, vector)
    print("Product:", product)
    print(f"cchar: {iterations}")
