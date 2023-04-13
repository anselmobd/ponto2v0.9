from random import randint


class CNPJ():
    """Cadastro Nacional da Pessoa Jurídica (CNPJ)"""

    weights = list(range(2, 10)) + list(range(2, 10))

    def __init__(self, cnpj9=None, cnpj4=None, cnpj2=None):
        self.cnpj9 = cnpj9
        self.cnpj4 = cnpj4
        self.cnpj2 = cnpj2

        if cnpj9 is not None:
            if isinstance(cnpj9, str):
                self.cnpj = cnpj9
                self.cnpj9 = None
            else:
                self.cnpj = self.to_str()

    def __str__(self):
        return self.to_str()

    def _only_digits(self, cnpj):
        return "".join([d for d in cnpj if d.isdigit()])

    def _generate_digit(self, cnpj):
        cnpj = self._only_digits(cnpj)
        sum = 0
        for i, d in enumerate(cnpj[::-1]):
            sum += int(d) * self.weights[i]
        sum = sum % 11
        sum = 0 if sum < 2 else 11 - sum
        return str(sum)

    def valid(self, cnpj=None):
        cnpj = cnpj if cnpj else self.cnpj
        cnpj = self._only_digits(cnpj)
        if len(cnpj) != 14:
            return False
        return (
            self._generate_digit(cnpj[:12]) == cnpj[12] and
            self._generate_digit(cnpj[:13]) == cnpj[13]
        )

    def list_valid(self, cnpjs):
        return [self.valid(cnpj) for cnpj in cnpjs]

    def generate(self):
        cnpj = list(f"{randint(1, 99999999):08d}{randint(1, 9999):04d}")
        cnpj.append(self._generate_digit(cnpj))
        cnpj.append(self._generate_digit(cnpj))
        return "".join(cnpj)

    def list_generate(self, count):
        cnpjs = set()
        while len(cnpjs) < count:
            cnpjs.add(self.generate())
        return list(cnpjs)

    def to_str(self, cnpj9=None, cnpj4=None, cnpj2=None):
        if cnpj9 is None:
            cnpj9 = self.cnpj9
            cnpj4 = self.cnpj4
            cnpj2 = self.cnpj2
        return f'{cnpj9:08d}/{cnpj4:04d}-{cnpj2:02d}'

    def str_mask(self, cnpj=None):
        if cnpj is None:
            cnpj = self.cnpj
        cnpj = self._only_digits(cnpj)
        return f"{cnpj[:8]}/{cnpj[8:12]}-{cnpj[-2:]}"

    def str_mask_dot(self, cnpj=None):
        if cnpj is None:
            cnpj = self.cnpj
        cnpj = self._only_digits(cnpj)
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[-2:]}"
