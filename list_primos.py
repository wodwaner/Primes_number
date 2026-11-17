"""Lista os primos até um limite e mede o tempo de CPU da busca."""

import sys
from time import process_time_ns


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


#def eh_primo(numero: int) -> bool:
#	if numero < 2:
#		return False
#	if numero % 2 == 0:
#		return numero == 2

#	divisor = 3
	# Testa apenas divisores ímpares até a raiz quadrada.
#	while divisor <= numero // divisor:
#		if numero % divisor == 0:
#			return False
#		divisor += 2

#	return True

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

def main() -> int:
	try:
		limite = ler_limite()
	except ValueError as erro:
		print(erro, file=sys.stderr)
		return 1

	total = 0
	numero = 2
	rec_numero = 0
	diff_numbers = 0
	mul_6 = 0
	pow_3 = 0
	pow_2 = 0
	temp0 = 0
	temp1 = 0
	temp2 = 0

	tempo_saida_ns = 0
	inicio = process_time_ns()

	while numero <= limite:
		if eh_primo(numero):
			antes = process_time_ns()
			#print(numero)
			tempo_saida_ns += process_time_ns() - antes
			total += 1
			temp0 = 1
			pow_3 = 0
			while temp0 < numero:
				temp0 *= 3
				pow_3 += 1

			temp0 //= 3
			pow_3 -= 1
			temp1 = numero - temp0
			#mul_6 = temp1//6
			#temp2 = temp1 - mul_6*6
			#pow_2 = temp2//2
			#diff_num = 3**pow_3 + mul_6*6 + 2**pow_2
			#print(f"{numero} = 3^{pow_3} + 6*{mul_6} + 2^{pow_2} -> {numero} - {diff_num} = {numero-diff_num}")

			mul_6 = temp1//6			
			pow_2 = (temp1%6)//2
			rec_numero = 3**pow_3 + mul_6*6 + 2**pow_2
			diff_num = numero - rec_numero
			print(f"{numero} | {rec_numero} = 3^{pow_3} + 6*{mul_6} + 2^{pow_2} -> e: {diff_num}")
			
			if diff_num != 0:
				print("Erro na formula")
				return 0


		# Depois de 2, verifica apenas candidatos ímpares.
		numero += 1 if numero == 2 else 2

	tempo_calculo_ns = process_time_ns() - inicio - tempo_saida_ns

	if total == 0:
		print("Nenhum primo.")
	print(f"Total de primos: {total}")
	print(f"Tempo de CPU no cálculo (ms): {tempo_calculo_ns / 1_000_000:.3f}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
