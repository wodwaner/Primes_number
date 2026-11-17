"""Lista os primos até um limite e mede o tempo de CPU da busca."""
#3317044064679887385961981
#3317044064679887385961980 Miller–Rabin
import sys
from time import process_time_ns
from typing import Dict

LIMITE_MAXIMO = 2**63 - 1


def ler_limite() -> int:
	try:
		entrada = input("Limite: ")
	except EOFError:
		entrada = ""

	if not entrada.isascii() or not entrada.isdecimal():
		raise ValueError("Digite apenas dígitos de 0 a 9.")

	limite = 0
	for digito in entrada:
		limite = limite * 10 + int(digito)
	#    if limite > LIMITE_MAXIMO:
	#        raise ValueError(f"Máximo: {LIMITE_MAXIMO}")

	return limite

def eh_primo(numero: int) -> bool:
	if numero < 2:
		return False
	if numero % 2 == 0:
		return numero == 2

	if numero >= 2**16:
		if numero < 2**64:
			# Bases de Jim Sinclair para inteiros de 64 bits.
			bases = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)
		else:
			# As 13 bases até 41 cobrem o limite de Sorenson e Webster.
			# A base 43 rejeita também o pseudoprimo na fronteira.
			bases = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43)

		# Escreve numero - 1 na forma 2**s * d, com d ímpar.
		anterior = numero - 1
		d = anterior
		s = 0
		while d % 2 == 0:
			d //= 2
			s += 1

		for base in bases:
			base %= numero
			if base == 0:
				continue

			resto = pow(base, d, numero)
			if resto in (1, anterior):
				continue

			for _ in range(s - 1):
				resto = (resto * resto) % numero
				if resto == anterior:
					break
			else:
				return False

		# Limite exclusivo do teste determinístico para as bases até 41.
		# https://arxiv.org/abs/1509.00864
		if numero < 3_317_044_064_679_887_385_961_981:
			return True

	# Divisão direta para números pequenos ou sobreviventes acima do limite.
	divisor = 3
	while divisor <= numero // divisor:
		if numero % divisor == 0:
			return False
		divisor += 2
	return True

def fatorar(n: int) -> Dict[int, int]:
	"""Retorna {fator: expoente} para 0 < |n| <= 3317044064679887385961980.

	Os fatores aparecem em ordem crescente. Para negativos, inclui -1.
	Para 1, retorna um dicionário vazio.

	Miller–Rabin: https://doi.org/10.1090/mcom/3134
	Pollard–Brent: https://doi.org/10.1007/BF01933190
	"""
	from collections import Counter
	from math import gcd, isqrt
	from random import randrange

	limite = 3_317_044_064_679_887_385_961_980
	# Remove fatores pequenos antes de usar Pollard–Brent.
	primos_pequenos = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)

	def _divisor_rho(n: int) -> int:
		"""Encontra um divisor próprio de um composto pelo rho de Pollard–Brent."""
		tamanho_bloco = 128
		while True:
			y = randrange(1, n)
			c = randrange(1, n)
			comprimento = 1
			divisor = 1

			# Reinicia com outro polinômio se a tentativa se alongar.
			while divisor == 1 and comprimento <= 2**22:
				x = y
				for _ in range(comprimento):
					y = (y * y + c) % n

				for inicio in range(0, comprimento, tamanho_bloco):
					y_inicial = y
					passos = min(tamanho_bloco, comprimento - inicio)
					produto = 1

					# Um MDC por bloco de diferenças reduz o custo.
					for _ in range(passos):
						y = (y * y + c) % n
						produto = (produto * (x - y)) % n
					divisor = gcd(produto, n)
					if divisor > 1:
						break

				comprimento *= 2

			if 1 < divisor < n:
				return divisor

			if divisor == n:
				# Refaz o último bloco com um MDC por diferença.
				y = y_inicial
				for _ in range(passos):
					y = (y * y + c) % n
					divisor = gcd(x - y, n)
					if 1 < divisor < n:
						return divisor

	if isinstance(n, bool) or not isinstance(n, int):
		raise TypeError("Informe um número inteiro.")
	if n == 0:
		raise ValueError("Zero não tem fatoração em primos.")
	if abs(n) > limite:
		raise ValueError(f"O valor absoluto deve ser menor ou igual a {limite}.")

	fatores = Counter()
	if n < 0:
		fatores[-1] = 1
		n = -n

	for primo in primos_pequenos:
		while n % primo == 0:
			fatores[primo] += 1
			n //= primo

	pendentes = [(n, 1)]
	while pendentes:
		atual, multiplicidade = pendentes.pop()
		if atual == 1:
			continue
		if eh_primo(atual):
			fatores[atual] += multiplicidade
			continue

		raiz = isqrt(atual)
		if raiz * raiz == atual:
			pendentes.append((raiz, 2 * multiplicidade))
		else:
			divisor = _divisor_rho(atual)
			pendentes.append((divisor, multiplicidade))
			pendentes.append((atual // divisor, multiplicidade))

	return dict(sorted(fatores.items()))
	
def main() -> int:
	try:
		limite = ler_limite()
	except ValueError as erro:
		print(erro, file=sys.stderr)
		return 1

	numero2 = 0
	numero4 = 0
	mul_6 = 0
	pow_3 = 1
	
	while True:		
		numero2 = 3**pow_3 + mul_6*6 + 2
		numero4 = 3**pow_3 + mul_6*6 + 4
		
		print(f"{numero2}",end=" ")
		if eh_primo(numero2):
			print(f"is prime = 3^{pow_3} + 6*{mul_6} + 2^{1}")
		else:
			print("not prime = ",end=" ")
			print(fatorar(numero2))
	
		print(f"{numero2}",end=" ")
		if eh_primo(numero4):
			print(f"is prime = 3^{pow_3} + 6*{mul_6} + 2^{4}")
		else:
			print("not prime = ",end=" ")
			print(fatorar(numero4))
		
		mul_6 += 1
		if mul_6 > 114:
			mul_6 = 0
			pow_3 += 1

		if numero4 > limite:
			print("Finalizando")
			return 0		
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
