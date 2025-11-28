# 🏢 Sistema de Gerenciamento de Funcionários

Atividade final da disciplina de **Arquitetura de Software Básica** - Mestrado CESAR School

---

## 📋 Descrição do Projeto

Sistema completo em Python para gerenciar funcionários e controlar ponto (entrada/saída). A aplicação permite cadastrar funcionários, registrar seus horários diários e gerar relatórios com visualizações gráficas.

---

## ✨ Funcionalidades Principais

### 👤 **Gerenciamento de Funcionários**
- ✅ Cadastro de funcionários com matrícula única
- ✅ Dados: nome, idade, turno (matutino, vespertino, noturno)
- ✅ Validações de integridade de dados
- ✅ Listagem de todos os funcionários cadastrados

### 🕐 **Controle de Ponto**
- ✅ Registrar entrada diária de funcionários
- ✅ Registrar saída vinculada à entrada
- ✅ Histórico completo de ponto por funcionário
- ✅ Datas e horários flexíveis ou automáticos

### 📊 **Relatórios e Análises**
- ✅ Relatório completo com estatísticas
- ✅ Gráfico de barras: Funcionários ordenados por idade
- ✅ Gráfico de pizza: Distribuição por turno
- ✅ Contagem de registros de ponto

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.7+**
- **Pandas** - Manipulação e análise de dados
- **Matplotlib** - Visualização de gráficos
- **NumPy** - Operações numéricas

---

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/claudes-dev/atvidade-arq-software.git
cd atvidade-arq-software
```

### 2. Instale as dependências
```powershell
python -m pip install pandas matplotlib numpy
```

---

## 🚀 Como Usar

### Executar o programa
```powershell
python arq.py
```

### Menu Interativo
O sistema exibe um menu com as seguintes opções:

```
1️⃣  Cadastrar Funcionário
2️⃣  Listar Funcionários
3️⃣  Registrar Entrada
4️⃣  Registrar Saída
5️⃣  Consultar Ponto de um Funcionário
6️⃣  Listar Todos os Registros de Ponto
7️⃣  Gerar Relatório Completo
8️⃣  Gráfico de Barras - Funcionários por Idade
9️⃣  Gráfico de Pizza - Funcionários por Turno
🚪 0️⃣  Sair
```

---

## 📝 Exemplo de Uso

### Cadastrar um funcionário:
```
👉 Escolha uma opção: 1
📝 CADASTRO DE FUNCIONÁRIO
Matrícula: 001
Nome: João Silva
Idade: 28
Turno (matutino/vespertino/noturno): matutino
✅ Funcionário João Silva cadastrado com sucesso!
```

### Registrar entrada:
```
👉 Escolha uma opção: 3
📥 REGISTRAR ENTRADA
Matrícula: 001
Data (DD/MM/YYYY) ou Enter para hoje: 
Hora (HH:MM) ou Enter para agora: 08:30
✅ Entrada registrada para João Silva em 28/11/2025 às 08:30
```

---

## 🎯 Estrutura de Dados

### DataFrame de Funcionários
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| matricula | str | Identificador único |
| nome | str | Nome completo |
| idade | int | Idade em anos |
| turno | str | matutino/vespertino/noturno |

### DataFrame de Registros de Ponto
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| matricula | str | Referência ao funcionário |
| nome | str | Nome do funcionário |
| data | str | Data (DD/MM/YYYY) |
| entrada | str | Hora de entrada (HH:MM) |
| saida | str | Hora de saída (HH:MM) |

---

## 🧪 Testar com Dados de Exemplo

No final do arquivo `arq.py`, descomente a linha:
```python
# dados_exemplo()
```

Para:
```python
dados_exemplo()
```

Isso carregará 5 funcionários com registros de ponto pré-configurados.

---

## 📊 Visualizações Gráficas

### Gráfico de Barras
Mostra funcionários ordenados por idade, facilitando visualizar a distribuição etária da equipe.

### Gráfico de Pizza
Apresenta a percentagem e quantidade de funcionários em cada turno de trabalho.

---

## 🔒 Validações Implementadas

- ✅ Matrícula única obrigatória
- ✅ Turno deve ser válido (matutino/vespertino/noturno)
- ✅ Entrada deve ser registrada antes da saída
- ✅ Idade deve ser número inteiro
- ✅ Impedimento de duplicação de registros

---

## 📈 Recursos do Relatório

O relatório completo exibe:
- Total de funcionários cadastrados
- Total de registros de ponto
- Distribuição por turno
- Idade média dos funcionários
- Funcionário mais jovem e mais velho

---

## 👨‍💻 Autor

Desenvolvido como atividade final do Mestrado em Arquitetura de Software - CESAR School

---

## 📄 Licença

Este projeto é fornecido como material educacional.

---

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas!

---

## ❓ Dúvidas Frequentes

**P: Como mudar as cores dos gráficos?**  
R: Modifique a variável `cores_lista` nas funções `grafico_pizza_turno()` ou `grafico_barras_idade()`.

**P: É possível exportar dados para CSV?**  
R: Sim! Use `funcionarios_df.to_csv('funcionarios.csv', index=False)` e `registros_ponto_df.to_csv('ponto.csv', index=False)`.

**P: Posso salvar os dados entre execuções?**  
R: Você pode implementar carregamento/salvamento com Pickle ou CSV.

---

**Desenvolvido com ❤️ em Python**
