# PLANO DE PROJETO E ARQUITETURA DE BANCO DE DADOS II

**Instituição:** Universidade Estadual Paulista "Júlio de Mesquita Filho" (UNESP)  
**Disciplina:** Banco de Dados II — Projetos Práticos  
**Docente Responsável:** Prof. Dr. Ronaldo Celso Messias Correia  
**Tema 12:** Gênio do Prompt — Base e Análise dos Prompts (*Armazenar versões dos prompts e analisar sua evolução durante as atividades*)  
**Eixos Conceituais:** Modelagem histórica, texto, versionamento, mineração, NLP e analytics  
**Área de Aplicação:** Engenharia de Prompt (Integrado ao ecossistema *unesp.IA Lab*)  
**Discentes (Equipe *Nathan e Descubra*):** Nathan e Nicolas  
**Repositório Oficial:** `https://github.com/NicolasDCB/Trabalho-Banco-de-Dados-II.git`

---

## 1. Introdução e Contextualização do Problema

A crescente adoção de Modelos de Linguagem de Grande Escala (*Large Language Models* — LLMs) evidenciou que a qualidade das respostas obtidas depende diretamente da clareza, estruturação e especificidade das instruções fornecidas pelo usuário — disciplina conhecida como **Engenharia de Prompt**. No contexto educacional do laboratório **unesp.IA Lab**, a aplicação didática **O Gênio do Prompt** demonstra que a construção de um bom pedido não ocorre em uma única tentativa, mas sim por meio de um **processo iterativo de diagnóstico, refinamento e evolução**.

Atualmente, em ambientes puramente client-side (baseados em armazenamento local de navegador), o histórico de tentativas dos estudantes fica restrito à sessão individual, impossibilitando análises longitudinais, mineração de padrões textuais coletivos, auditoria temporal de versões e cruzamento analítico entre diferentes atividades e regiões.

Este projeto propõe o desenvolvimento de uma arquitetura completa centrada em um **Sistema Gerenciador de Banco de Dados Relacional (PostgreSQL)** para o **Tema 12: Gênio do Prompt — Base e Análise dos Prompts**. O sistema tem como propósito persistir de forma estruturada e histórica todas as versões dos prompts elaborados pelos usuários durante as atividades práticas, avaliando sua evolução técnica segundo as **6 Dimensões da Engenharia de Prompt** e aplicando recursos nativos de programação em banco de dados (Triggers, Stored Functions, Views, Índices de Busca Textual e Extensão Vetorial).

---

## 2. Objetivos do Projeto

### 2.1. Objetivo Geral
Projetar e implementar um sistema Full-Stack apoiado no SGBD **PostgreSQL** (utilizando comunicação em SQL puro via driver `psycopg`) capaz de armazenar o ciclo de vida completo das versões de prompts de Inteligência Artificial, rastrear sua evolução temporal durante atividades guiadas e fornecer análises estatísticas, léxicas, semânticas e geográficas sobre o aprimoramento dos pedidos.

### 2.2. Objetivos Específicos
1. **Modelagem Histórica e de Versionamento:** Estruturar tabelas relacionais e temporais (*Slowly Changing Dimensions* — SCD Tipo 2) que preservem cada versão de um prompt (`v1, v2, ..., vN`), registrando os intervalos exatos de vigência (`valid_from` e `valid_to`) por meio de *Triggers* em `PL/pgSQL`.
2. **Estruturação nas 6 Dimensões da Engenharia de Prompt:** Persistir individualmente os componentes pedagógicos do pedido (*Objetivo, Contexto, Público, Formato, Critérios/Limites* e *Cuidados*), bem como o prompt consolidado e o motivo diagnóstico de cada evolução.
3. **Processamento e Mineração de Texto no SGBD e Backend:** Extrair métricas quantitativas e qualitativas de cada versão (contagem de palavras, estimativa de tokens, pontuação de rubrica de `0 a 12`, detecção de verbos de comando, alertas de inconsistência e indexação textual via `tsvector`/`GIN`).
4. **Busca Semântica e Deriva Vetorial (`pgvector`):** Incorporar vetores de *embeddings* para mensurar a proximidade semântica entre versões consecutivas e recuperar exemplos similares na base de conhecimento.
5. **Analytics e Visualização Espacial (`Leaflet`):** Consolidar indicadores de evolução por atividade, missão e localização geográfica por meio de *Views* SQL consumidas por mapas interativos e painéis analíticos.

---

## 3. Especificação Tecnológica e Conformidade com a Disciplina

Em estrita observância às diretrizes estabelecidas para os Projetos Práticos de Banco de Dados II, a arquitetura adota as seguintes tecnologias:

| Camada Arquitetural | Tecnologia Especificada | Detalhamento da Implementação no Projeto |
| :--- | :--- | :--- |
| **Front-end** | `React + TypeScript + TSX` | Aplicação SPA modular tipada em TypeScript, estruturada em componentes `.tsx` com interface didática inspirada no *unesp.IA Lab*. |
| **Back-end / API** | `Python + FastAPI` | Servidor assíncrono expondo endpoints REST padronizados. |
| **SGBD** | `PostgreSQL` | PostgreSQL 16 responsável pela integridade relacional, processamento de *Triggers*, *Views*, busca textual e vetorial. |
| **Driver de Banco** | `psycopg` (v3) | Conexão direta utilizando cursores `dict_row` e consultas em **SQL Puro parametrizado** (`%s`). |
| **Biblioteca ORM** | **SQLAlchemy — NÃO USAR** | **Ausência total de ORM.** Toda manipulação de dados (`DDL`, `DML`, chamadas de *Views* e *Functions*) é codificada explicitamente em SQL. |
| **Extensão Vetorial** | `pgvector` (Opcional incluída) | Utilizada na 2ª Entrega para indexação de *embeddings* (`HNSW`) e cálculo de distância de cosseno (`<=>`) entre versões de prompts. |
| **Comunicação** | `API REST em JSON` | Troca de dados estruturada em JSON com validação de esquemas via *Pydantic*. |
| **Mapas** | `Leaflet` | Biblioteca `leaflet` / `react-leaflet` integrada a consultas geográficas do PostgreSQL para mapeamento das atividades por campus/cidade. |

---

## 4. Metodologia de Engenharia de Prompt Aplicada ao Banco de Dados

O modelo de domínio do banco de dados incorpora diretamente a metodologia pedagógica do **Gênio do Prompt**, estruturando a evolução de cada pedido em torno de três pilares:

### 4.1. As 6 Dimensões Estruturais do Pedido
Cada versão de um prompt armazenada no banco é decomposta e avaliada em seis dimensões fundamentais (pontuadas de `0` a `2` cada, totalizando de **`0 a 12` pontos**):

1. **Objetivo (`dim_objetivo` — 0 a 2 pts):** Define claramente a ação esperada (verbo de comando) e a entrega desejada.
2. **Contexto (`dim_contexto` — 0 a 2 pts):** Situa onde, quando e com qual finalidade prática a resposta será utilizada.
3. **Público (`dim_publico` — 0 a 2 pts):** Especifica o perfil, faixa etária ou nível de conhecimento de quem lerá a resposta.
4. **Formato (`dim_formato` — 0 a 2 pts):** Determina a estrutura de saída (ex.: lista em tópicos, tabela comparativa, JSON, roteiro, mensagem curta).
5. **Critérios e Limites (`dim_criterios` — 0 a 2 pts):** Estabelece restrições verificáveis (limite de palavras, inclusão de exemplos, regras de validação).
6. **Cuidados (`dim_cuidados` — 0 a 2 pts):** Previne riscos associados à tarefa (proteção de dados pessoais/LGPD, proibição de invenção de fatos/alucinação, exigência de revisão humana).

### 4.2. Classificação de Maturidade da Versão
A soma das pontuações das seis dimensões (`total_score` de `0 a 12`) determina o estágio evolutivo da versão no banco de dados:
- **`0 a 3` pontos (`insuficiente`):** *Ainda insuficiente* — pedido vago ou incompleto (comum na versão inicial `v1`).
- **`4 a 7` pontos (`pode_melhorar`):** *Pode melhorar* — pedido possui intenção clara, mas carece de delimitação de público, formato ou critérios.
- **`8 a 12` pontos (`suficiente`):** *Suficiente para testar* — pedido maduro, contextualizado e com critérios de verificação definidos.

### 4.3. Diagnóstico de Evolução entre Versões (`v1 → v2 → v3`)
Para registrar **por que** um prompt evoluiu de uma versão para outra durante uma atividade, cada nova versão armazena o diagnóstico pedagógico que motivou a refatoração:
- `GENERICA` (*"A resposta ficou muito genérica"* -> refinamento do **Contexto**);
- `FORMATO_ERRADO` (*"Veio no formato errado"* -> refinamento do **Formato**);
- `LINGUAGEM_INADEQUADA` (*"A linguagem não serviu para o público"* -> refinamento do **Público**);
- `FALTOU_CONTEUDO` (*"Faltou conteúdo importante"* -> refinamento dos **Critérios e Limites**);
- `INFORMACAO_INCORRETA` (*"Trouxe informação incorreta ou sem cuidado"* -> refinamento dos **Cuidados**).

---

## 5. Modelagem do Banco de Dados (MER / DER e Objetos SQL)

### 5.1. Diagrama Entidade-Relacionamento (DER)

```mermaid
erDiagram
    USERS ||--o{ ACTIVITIES : "cria e conduz"
    MISSIONS ||--o{ ACTIVITIES : "fundamenta"
    ACTIVITIES ||--o{ PROMPT_VERSIONS : "possui versoes (1:N)"
    ACTIVITIES ||--o{ PROMPT_HISTORY_LOG : "auditoria temporal"
    PROMPT_VERSIONS ||--o{ PROMPT_HISTORY_LOG : "gera vigencia"
    PROMPT_VERSIONS ||--o| PROMPT_NLP_MINING : "analise NLP e vetor (1:1)"

    USERS {
        serial id PK
        varchar name
        varchar email UK
        varchar institution
        varchar city
        double_precision latitude
        double_precision longitude
        timestamp created_at
    }

    MISSIONS {
        serial id PK
        varchar slug UK
        varchar level "Primeiros passos | Pratica guiada | Desafio"
        varchar title
        text situation
        text initial_idea
        text success_criteria
    }

    ACTIVITIES {
        serial id PK
        int user_id FK
        int mission_id FK
        varchar title
        varchar category
        varchar city
        double_precision latitude
        double_precision longitude
        timestamp created_at
        timestamp updated_at
    }

    PROMPT_VERSIONS {
        serial id PK
        int activity_id FK
        int version_number "Calculado via Trigger (v1, v2, v3...)"
        text dim_objetivo
        text dim_contexto
        text dim_publico
        text dim_formato
        text dim_criterios
        text dim_cuidados
        text assembled_prompt "Texto consolidado via Trigger"
        varchar diagnostic_reason "Motivo da evolucao"
        int total_score "Nota de 0 a 12"
        varchar classification "insuficiente | pode_melhorar | suficiente"
        int word_count "Calculado via Trigger"
        tsvector search_vector "Indice GIN para Full-Text Search"
        timestamp created_at
    }

    PROMPT_HISTORY_LOG {
        serial id PK
        int activity_id FK
        int version_id FK
        int version_number
        int total_score
        varchar classification
        timestamp valid_from "Inicio da vigencia temporal"
        timestamp valid_to "Fim da vigencia (NULL = versao ativa)"
    }

    PROMPT_NLP_MINING {
        serial id PK
        int version_id FK UK
        text_array extracted_keywords
        jsonb consistency_warnings
        jsonb genie_suggestions
        varchar simulated_style "Direto | Didatico | Criativo | Acolhedor | Tecnico"
        text simulated_response
        vector_64 embedding "Extensao pgvector (2a Entrega)"
        numeric semantic_drift "Distancia de cosseno em relacao a versao anterior"
    }
```

### 5.2. Inteligência Programada no SGBD (Triggers, Functions, Views e Índices)

1. **Trigger de Versionamento, Montagem Textual e Rubrica (`trg_before_insert_prompt_version`):**
   - Executada `BEFORE INSERT` na tabela `prompt_versions`.
   - Consulta o maior `version_number` daquela atividade e atribui `COALESCE(MAX(version_number), 0) + 1`.
   - Concatena as dimensões preenchidas gerando automaticamente o texto completo (`assembled_prompt`).
   - Contabiliza o número de palavras (`word_count`), avalia a pontuação (`total_score` de `0 a 12`), define a coluna `classification` e gera o vetor de busca textual `search_vector` (`to_tsvector('portuguese', ...)`).
2. **Trigger de Modelagem Histórica Temporal — SCD Tipo 2 (`trg_after_insert_prompt_version`):**
   - Executada `AFTER INSERT` na tabela `prompt_versions`.
   - Encerra a vigência da versão anteriormente ativa naquela atividade (`UPDATE prompt_history_log SET valid_to = CURRENT_TIMESTAMP WHERE activity_id = NEW.activity_id AND valid_to IS NULL`).
   - Insere o novo registro temporal com `valid_from = CURRENT_TIMESTAMP` e `valid_to = NULL`, permitindo reconstruir o estado exato de qualquer prompt em qualquer ponto do tempo (*time-travel queries*).
3. **Views Analíticas (`vw_activity_evolution` e `vw_geographic_analytics`):**
   - `vw_activity_evolution`: Compara os indicadores da primeira versão (`v1`) com a versão vigente (`Head`) de cada atividade, calculando o ganho absoluto de pontuação (`score_atual - score_inicial`), a evolução na contagem de palavras e o número de iterações necessárias para atingir a classificação *Suficiente para testar*.
   - `vw_geographic_analytics`: Agrupa por localidade (`city`, `latitude`, `longitude`) o volume de atividades, total de versões geradas e pontuação média na rubrica para renderização no mapa **Leaflet**.
4. **Índices Especializados:**
   - Índice `B-Tree` composto em `prompt_versions(activity_id, version_number)` e `prompt_history_log(activity_id, valid_to)`.
   - Índice `GIN` sobre a coluna `search_vector` (`tsvector`) para consultas de *Full-Text Search* em língua portuguesa.
   - Índice `HNSW` (via extensão `pgvector` na 2ª Entrega) sobre `embedding` com operador `vector_cosine_ops`.

---

## 6. Planejamento das Entregas (Cronograma de Execução)

O desenvolvimento está estruturado em **duas entregas incrementais**, garantindo que a base relacional e a interface funcional estejam plenamente validadas na primeira etapa antes da acoplagem dos algoritmos avançados de mineração e IA na segunda etapa.

### 📦 1ª Entrega: Base Relacional, Versionamento Histórico e Interface Conectada ao Banco
**Objetivo da Entrega:** Demonstrar o funcionamento completo do ciclo de persistência no PostgreSQL via FastAPI (`psycopg` sem ORM) e a interface React + TypeScript + Leaflet.

- **Escopo de Banco de Dados:**
  - Script `01_schema.sql`: Tabelas `users`, `missions`, `activities`, `prompt_versions` e `prompt_history_log`.
  - Script `02_triggers_and_functions.sql`: Triggers `PL/pgSQL` de numeração automática de versão, montagem do prompt estruturado, cálculo da nota (`0 a 12`), contagem de palavras e controle de vigência temporal (`valid_from` / `valid_to`).
  - Script `03_views_analytics.sql`: Views `vw_activity_evolution` e `vw_geographic_analytics`.
  - Script `04_seed_data.sql`: Carga inicial com as 6 Missões oficiais do Gênio do Prompt e atividades de exemplo demonstrando a evolução real `v1 → v2 → v3`.
- **Escopo de Back-end (`FastAPI + psycopg`):**
  - Endpoints REST em JSON para listagem de missões, criação de atividades, inserção de novas versões evoluídas, consulta à linha do tempo de versões, consulta ao log temporal (`prompt_history_log`) e dados geográficos do mapa.
- **Escopo de Front-end (`React + TypeScript + TSX + Leaflet`):**
  - Interface didática organizada em **3 abas**:
    1. **Faça e Evolua seu Pedido:** Seleção de missão, cadastro da ideia inicial (`v1`) e formulário guiado das **6 Dimensões** para evoluir o pedido (`v2, v3...`) com barra de progresso da nota (`0 a 12`).
    2. **Meu Caderno & Histórico no Banco:** Comparação visual entre as versões salvas (`v1 vs. v2 vs. v3`) e visualização da tabela de auditoria temporal (`valid_from` / `valid_to`).
    3. **Analytics & Mapa (Leaflet):** Tabela resumo da View de evolução e mapa interativo **Leaflet** exibindo os polos/cidades das atividades.

---

### 🧠 2ª Entrega: Mineração de Texto, NLP, Busca Semântica (`pgvector`) e Simulador de Estilos
**Objetivo da Entrega:** Expandir a análise textual e analítica com mineração automatizada de Engenharia de Prompt, álgebra vetorial no PostgreSQL e simulação de respostas da IA.

- **Escopo de Banco de Dados e `pgvector`:**
  - Ativação da extensão `CREATE EXTENSION vector;` e criação da tabela `prompt_nlp_mining`.
  - Armazenamento de *embeddings* semânticos e função SQL para cálculo da **Deriva Semântica** (`embedding_atual <=> embedding_anterior`), medindo matematicamente o quanto o significado do prompt mudou a cada versão.
  - Busca por similaridade semântica na base de exemplos do Gênio do Prompt.
- **Escopo de Mineração e NLP no Back-end:**
  - Analisador léxico e heurístico avançado das 6 dimensões (detecção de verbos de comando, especificidade de público, regras mensuráveis e termos de proteção de dados/LGPD).
  - Detector automático de **Alertas de Inconsistência** (ex.: conflito entre público infantil e formato acadêmico avançado; ausência de cuidado de privacidade ao mencionar dados pessoais).
  - Gerador automático de **Sugestões do Gênio** para orientar a próxima versão do aluno.
  - **Comparador de Estilos de Resposta:** Geração e comparação lado a lado de respostas nos 5 estilos do Gênio (*Direto, Didático, Criativo, Acolhedor* e *Técnico*).

---

## 7. Divisão de Responsabilidades e Fluxo de Trabalho da Equipe

Para garantir produtividade e domínio compartilhado de todo o projeto por ambos os integrantes (**Nathan** e **Nicolas**), o fluxo de trabalho no repositório GitHub (`https://github.com/NicolasDCB/Trabalho-Banco-de-Dados-II.git`) segue a organização abaixo:

| Frente de Trabalho | Atividades Principais | Artefatos no Repositório |
| :--- | :--- | :--- |
| **Modelagem e Programação SQL (PostgreSQL)** | Criação das tabelas, constraints, Triggers `PL/pgSQL` (versionamento e histórico temporal SCD2), Views analíticas e massa de dados (*seed*). | `database/01_schema.sql`<br>`database/02_triggers_and_functions.sql`<br>`database/03_views_analytics.sql`<br>`database/04_seed_data.sql` |
| **API REST e Acesso a Dados (`FastAPI + psycopg`)** | Implementação da camada de conexão `psycopg` em SQL puro, endpoints REST JSON, validação Pydantic e motor de avaliação/NLP. | `backend/app/database.py`<br>`backend/app/main.py`<br>`backend/init_db.py` |
| **Interface Web e Georreferenciamento (`React + TSX + Leaflet`)** | Construção das 3 abas interativas (Construtor das 6 Dimensões, Caderno/Histórico Temporal e Analytics com Mapa Leaflet). | `frontend/src/App.tsx`<br>`backend/app/web_ui.html` |
