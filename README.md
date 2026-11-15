# MeuBolso — Etapa de interface (View)

Reformulação visual do projeto integrador do aluno Arthur, utilizando **Python + Tkinter** e respeitando a tipografia e a paleta originalmente estabelecidas em `assets/Tipografia.md`.

## Executar

Requer Python 3.10 ou superior com Tkinter instalado.

```bash
python main.py
```

No Linux, algumas distribuições exigem a instalação do pacote `python3-tk`.

**A fonte Inter é utilizada se estiver instalada no sistema operacional; caso contrário, o Tkinter utiliza sua fonte substituta.** Instale a fonte Inter localmente para obter a aparência pretendida. Nenhum arquivo de fonte acompanha o projeto.

## Escopo desta entrega

- Sete páginas: Dashboard, Rendas, Categorias, Despesas, Objetivos, Regras e Aportes.
- Navegação por menu lateral, destaque do item ativo e estados de hover.
- Cartões, tabela ilustrativa, gráfico de evolução, composição de despesas, barras de progresso animadas.
- Formulários exclusivamente visuais para as principais operações de cadastro.
- Feedback explícito de modo de demonstração.
- Paleta do aluno: `#0F172A`, `#1E293B`, `#10B981`, `#EF4444`, `#94A3B8`.
- Tipografia: Inter, títulos 24 px, valores de destaque e textos com hierarquia.

## Não implementado deliberadamente

- Controllers, autenticação ou qualquer integração PostgreSQL.
- Gravação, edição ou exclusão de registros.
- Validação de dados, cálculo financeiro real e atualização dos gráficos.
- Operações bancárias.

Todos os números do projeto estão centralizados no arquivo `views/data_demo.py` e são **fictícios**. Os campos aceitam digitação para demonstrar a experiência, mas o botão **Salvar · em breve** está inativo intencionalmente.

## Estrutura

```text
main.py
views/
  main_view.py     # estrutura principal e troca de telas
  sidebar.py       # menu, seleção e hover
  pages.py         # páginas e formulários visuais
  components.py    # componentes reutilizáveis e animações
  styles.py        # identidade visual
  data_demo.py     # dados fictícios de demonstração
assets/
  Tipografia.md
  referencia_original.png
```

## Próxima etapa: Controllers

Conectar eventos dos botões a controllers e ligar models/repositories ao PostgreSQL. Não confundir os valores fictícios com registros reais. As páginas foram divididas por função para facilitar essa integração futura.


## Nitidez e ícones (correção de UI)

- Adicionados ícones PNG antialiasados em `views/assets/icons/`, usados por `Icon` com Pillow.
- Removidos os ícones geométricos desenhados diretamente sobre `Canvas` de 10–18 pixels.
- DPI awareness do Windows ativada em `main.py` **antes de importar Tkinter**.
- Removido `tk scaling=1.0`, que ignorava a escala real do monitor.
- Mantida a paleta e a tipografia Inter (instale Inter localmente no Windows se desejar essa fonte exata).
- Instale dependências: `python -m pip install -r requirements.txt`.
- Inicie a partir da raiz: `python main.py`. Evite iniciar `views/main_view.py` diretamente.
- Caso o Windows continue ampliando uma janela antiga, reinicie o programa e confira as configurações de escala do Windows.
- O projeto continua **apenas visual**, com dados demonstrativos e sem controllers.
