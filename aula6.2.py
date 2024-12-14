import json
import os
from datetime import datetime


class Estoque:
    def __init__(self, arquivo_estoque, arquivo_vendas):
        self.arquivo_estoque = arquivo_estoque
        self.arquivo_vendas = arquivo_vendas
        self.estoque = self.carregar_estoque()

    def carregar_estoque(self):
        """Carrega o estoque a partir de um arquivo JSON, se existir."""
        if not os.path.exists(self.arquivo_estoque):
            self.salvar_estoque()  # Cria o arquivo caso não exista
        with open(self.arquivo_estoque, 'r') as f:
            return json.load(f)

    def salvar_estoque(self):
        """Salva o estoque no arquivo JSON."""
        with open(self.arquivo_estoque, 'w') as f:
            json.dump(self.estoque, f, indent=4)

    def registrar_venda(self, produto, quantidade, valor_unitario):
        """Registra uma venda no arquivo de vendas."""
        valor_total = quantidade * valor_unitario
        registro = {
            "produto": produto,
            "quantidade": quantidade,
            "valor_unitario": valor_unitario,
            "valor_total": valor_total,
            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        if not os.path.exists(self.arquivo_vendas):
            with open(self.arquivo_vendas, 'w') as f:
                json.dump([registro], f, indent=4)
        else:
            with open(self.arquivo_vendas, 'r') as f:
                vendas = json.load(f)
            vendas.append(registro)
            with open(self.arquivo_vendas, 'w') as f:
                json.dump(vendas, f, indent=4)

    def listar_produtos(self):
        """Lista os produtos no estoque com formatação aprimorada."""
        print("\nEstoque Atual:")
        if not self.estoque:
            print("O estoque está vazio.")
        else:
            # Cabeçalhos da tabela
            print(f"{'Produto':<25} {'Quantidade':<12} {'Valor Unitário':<15} {'Valor Total':<15}")
            print("-" * 70)  # Linha separadora

            # Exibindo os produtos
            for produto, info in self.estoque.items():
                valor_unitario = info['valor_unitario']
                quantidade = info['quantidade']
                valor_total = valor_unitario * quantidade
                print(f"{produto:<25} {quantidade:<12} R$ {valor_unitario:>12.2f} R$ {valor_total:>12.2f}")
            print("-" * 70)  # Linha separadora

    def adicionar_produto(self, produto, quantidade, valor_unitario):
        """Adiciona ou atualiza um produto no estoque."""
        if produto in self.estoque:
            self.estoque[produto]['quantidade'] += quantidade
            self.estoque[produto]['valor_unitario'] = valor_unitario  # Atualiza o valor unitário
        else:
            self.estoque[produto] = {"quantidade": quantidade, "valor_unitario": valor_unitario}
        print(f"{quantidade} unidades de '{produto}' adicionadas ao estoque.")

    def remover_produto_por_valor(self, produto, valor_total):
        """Remove produtos com base no valor total da venda."""
        if produto in self.estoque:
            valor_unitario = self.estoque[produto]['valor_unitario']
            quantidade = valor_total / valor_unitario  # Calcula a quantidade com base no valor total
            quantidade = int(quantidade)  # Certificando-se de que a quantidade é um número inteiro

            if self.estoque[produto]['quantidade'] >= quantidade:
                self.estoque[produto]['quantidade'] -= quantidade
                print(f"Venda registrada: {quantidade} unidades de '{produto}' removidas do estoque.")
                self.registrar_venda(produto, quantidade, valor_unitario)
                if self.estoque[produto]['quantidade'] == 0:
                    del self.estoque[produto]  # Remove o produto se a quantidade for zero
                    print(f"'{produto}' esgotado e removido do estoque.")
            else:
                print(f"Quantidade insuficiente de '{produto}' no estoque.")
        else:
            print(f"O produto '{produto}' não está no estoque.")


class Sistema:
    def __init__(self):
        self.arquivo_estoque = "estoque.json"
        self.arquivo_vendas = "vendas.json"
        self.estoque = Estoque(self.arquivo_estoque, self.arquivo_vendas)

    def menu(self):
        print("\nControle de Estoque")
        print("1. Listar produtos")
        print("2. Adicionar produto")
        print("3. Registrar venda (quantidade)")
        print("4. Registrar venda (valor total)")
        print("5. Sair")

    def executar(self):
        while True:
            self.menu()
            opcao = input("\nEscolha uma opção: ")

            if opcao == "1":
                self.estoque.listar_produtos()
            elif opcao == "2":
                produto = input("Digite o nome do produto: ")
                quantidade = self.validar_inteiro("Digite a quantidade a adicionar: ")
                valor_unitario = self.validar_float("Digite o valor unitário do produto: ")
                self.estoque.adicionar_produto(produto, quantidade, valor_unitario)
                self.estoque.salvar_estoque()
            elif opcao == "3":
                produto = input("Digite o nome do produto: ")
                quantidade = self.validar_inteiro("Digite a quantidade a remover (venda): ")
                self.estoque.remover_produto_por_valor(produto, quantidade)
                self.estoque.salvar_estoque()
            elif opcao == "4":
                produto = input("Digite o nome do produto: ")
                valor_total = self.validar_float("Digite o valor total da venda (R$): ")
                self.estoque.remover_produto_por_valor(produto, valor_total)
                self.estoque.salvar_estoque()
            elif opcao == "5":
                print("Saindo do sistema...")
                self.estoque.salvar_estoque()
                break
            else:
                print("Opção inválida. Tente novamente.")

    def validar_inteiro(self, mensagem):
        """Valida a entrada de um número inteiro."""
        while True:
            try:
                return int(input(mensagem))
            except ValueError:
                print("Valor inválido. Por favor, insira um número inteiro.")

    def validar_float(self, mensagem):
        """Valida a entrada de um número de ponto flutuante."""
        while True:
            try:
                return float(input(mensagem))
            except ValueError:
                print("Valor inválido. Por favor, insira um número válido.")

if __name__ == "__main__":
    sistema = Sistema()
    sistema.executar()
