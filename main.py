import os
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import string

#banco de palavras chave
palavras_positivas = ['ótimo', 'excelente', 'incrível', 'fantástico', 'maravilhoso', 'feliz', 'surpreendente', 'amei', 'deliciosa',
                      'sensacional', 'espetacular', 'magnífico', 'encantador', 'excepcional', 'empolgante', 'divertido','notável',
                      'estupendo', 'fabuloso', 'brilhante', 'incrível', 'adorável', 'gratificante', 'impressionante', 'perfeito',
                      'radiante', 'surpreendente', 'único', 'alegre', 'energizante', 'entusiasmado', 'legal', 'bacana', 'maravilhosa',
                      'aproveitei']

palavras_negativas = ['péssimo', 'horrível', 'terrível', 'desagradável', 'decepcionante', 'triste', 'frustrante', 'ruim', 'grosso',
                      'grosseria', 'desastroso', 'desanimador', 'desprezível', 'insatisfatório', 'desconfortável', 'irritante', 'desagradável',
                      'inaceitável', 'aborrecido', 'injusto', 'lamentável', 'detestável', 'desanimador', 'estressante', 'inferior', 'indesejado',
                      'incomodo', 'miserável', 'problemático', 'decepção', 'incompetência']


intensificadores = ['muito', 'bastante', 'extremamente', 'incrivelmente', 'realmente', 'completamente', 'absolutamente', 'enormemente', 'imensamente',
                    'profundamente', 'altamente', 'excessivamente', 'notavelmente', 'consideravelmente', 'extraordinariamente', 'surpreendentemente']


negacoes = ['não', 'jamais', 'nenhum', 'nem', 'nada']


#Variáveis fuzzy e funções de pertinência
fp_range = np.linspace(0, 1, 100)
fn_range = np.linspace(0, 1, 100)
i_range = np.linspace(0, 1, 100)
n_range = np.linspace(0, 1, 100)
ps_range = np.linspace(0, 1, 100)

FP = ctrl.Antecedent(fp_range, 'FP')
FP['baixa'] = fuzz.trimf(fp_range, [0, 0, 0.3])
FP['media'] = fuzz.trimf(fp_range, [0.2, 0.6, 0.8])
FP['alta'] = fuzz.trimf(fp_range, [0.7, 1, 1])

FN = ctrl.Antecedent(fn_range, 'FN')
FN['baixa'] = fuzz.trimf(fn_range, [0, 0, 0.3])
FN['media'] = fuzz.trimf(fn_range, [0.2, 0.4, 0.6])
FN['alta'] = fuzz.trimf(fn_range, [0.4, 1, 1])

I = ctrl.Antecedent(i_range, 'I')
I['baixa'] = fuzz.trimf(i_range, [0, 0, 0.3])
I['media'] = fuzz.trimf(i_range, [0.2, 0.4, 0.6])
I['alta'] = fuzz.trimf(i_range, [0.4, 1, 1])

N = ctrl.Antecedent(n_range, 'N')
N['baixa'] = fuzz.trimf(n_range, [0, 0, 0.3])
N['media'] = fuzz.trimf(n_range, [0.2, 0.4, 0.6])
N['alta'] = fuzz.trimf(n_range, [0.4, 1, 1])

PS = ctrl.Consequent(ps_range, 'PS')
PS['negativa'] = fuzz.trimf(ps_range, [0, 0, 0.3])
PS['neutra'] = fuzz.trimf(ps_range, [0.2, 0.4, 0.6])
PS['positiva'] = fuzz.trimf(ps_range, [0.4, 1, 1])

#Regras fuzzy
regra1 = ctrl.Rule(FP['alta'] | (FP['media'] & ~FN['alta']), PS['positiva'])
regra2 = ctrl.Rule(FN['alta'] | (FN['media'] & ~FP['alta']), PS['negativa'])
regra3 = ctrl.Rule((FP['baixa'] | FP['media']) & (FN['baixa'] | FN['media']), PS['neutra'])
regra4 = ctrl.Rule(N['alta'], PS['negativa'])
regra5 = ctrl.Rule(I['baixa'] & N['baixa'], PS['neutra'])
regra6 = ctrl.Rule(FP['baixa'] & FN['baixa'] & ~I['alta'] & ~N['alta'], PS['neutra'])
sistema = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6])
simulacao = ctrl.ControlSystemSimulation(sistema)


#solicitar a frase
frase = input("Digite uma frase: ")
#remover a pontuação
frase = frase.translate(str.maketrans('', '', string.punctuation))

#calcular os valores
fp = sum(1 for palavra in frase.lower().split() if palavra in palavras_positivas) > 0
fn = sum(1 for palavra in frase.lower().split() if palavra in palavras_negativas) > 0
i = sum(1 for palavra in frase.lower().split() if palavra in intensificadores) > 0
n = sum(1 for palavra in frase.lower().split() if palavra in negacoes) > 0

'''
print('Valor de FP:', fp)
print('Valor de FN:', fn)
print('Valor de I:', i)
print('Valor de N:', n)
'''

#definir os valores das variáveis de entrada na simulação
simulacao.input['FP'] = fp
simulacao.input['FN'] = fn
simulacao.input['I'] = i
simulacao.input['N'] = n

#executar a simulação
simulacao.compute()

#obter o valor de saída (polaridade do sentimento)
valor_polaridade = simulacao.output['PS']

#imprimir o resultado
print('Polaridade do sentimento:', valor_polaridade)

#classificar a polaridade do sentimento com base na saída
if valor_polaridade <= 0.3:
    sentimento = 'Negativo'
elif valor_polaridade <= 0.6:
    sentimento = 'Neutro'
else:
    sentimento = 'Positivo'

print('Sentimento:', sentimento)


#plotar grafico
if not os.path.exists("Testes"):
    os.makedirs("Testes")

plt.figure(figsize=(8, 6))
plt.plot(ps_range, fuzz.trimf(ps_range, [0, 0, 0.3]), 'r', linewidth=1.5, label='Polaridade negativa')
plt.plot(ps_range, fuzz.trimf(ps_range, [0.2, 0.4, 0.6]), 'g', linewidth=1.5, label='Polaridade neutra')
plt.plot(ps_range, fuzz.trimf(ps_range, [0.4, 1, 1]), 'b', linewidth=1.5, label='Polaridade positiva')

plt.axvline(x=valor_polaridade, color='k', linestyle='--', linewidth=1.5, label='Valor de Polaridade')

plt.xlabel('Polaridade do Sentimento')
plt.ylabel('Pertinência')
plt.title('Gráfico de Polaridade do Sentimento')
plt.legend()
plt.grid(True)

plt.text(0.5, -0.18, f'Frase: {frase}', fontweight='bold', transform=plt.gca().transAxes, ha='center')
plt.subplots_adjust(bottom=0.15)

#salvar o gráfico no projeto
nome_arquivo = f'Testes/{frase.replace(" ", "_")}.png'
plt.savefig(nome_arquivo)

plt.show()