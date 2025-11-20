# Fusion 360 MCP Server

Servidor MCP (Model Context Protocol) para expor documentação local da API do Autodesk Fusion 360.

## Visão Geral

Este servidor MCP indexa e expõe **todos os 7 módulos da API Python do Fusion 360**, permitindo busca e acesso rápido à documentação completa (~89,000 linhas, 3.7MB).

### Módulos Indexados

| Módulo | Tamanho | Linhas | Descrição |
|--------|---------|--------|-----------|
| `adsk.core` | 916 KB | 22,263 | Funcionalidades core: UI, geometria, aplicação |
| `adsk.fusion` | 2.4 MB | 55,453 | Features de design: sketches, componentes, features |
| `adsk.cam` | 358 KB | 9,952 | Operações CAM/Manufacturing e toolpaths |
| `adsk.drawing` | 5.9 KB | 179 | Desenhos e documentação |
| `adsk.volume` | 41 KB | 1,204 | Operações volumétricas e mesh |
| `adsk.sim` | 231 B | 9 | Capacidades de simulação |
| `adsk.__init__` | 1.3 KB | 12 | Utilitários do módulo |

**API Version:** 2605.1.18

## Instalação

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar o servidor
python fusion_mcp_server.py
```

## Estrutura de Arquivos

```
./API/
├── Python/
│   └── defs/
│       └── adsk/
│           ├── __init__.py   # Utilitários
│           ├── core.py       # Core API
│           ├── fusion.py     # Fusion Design
│           ├── cam.py        # CAM/Manufacturing
│           ├── drawing.py    # Drawings
│           ├── volume.py     # Volume/Mesh
│           └── sim.py        # Simulation
└── version.txt               # Versão da API
```

## Funcionalidades

### 🔍 Ferramentas de Busca

#### 1. `search_fusion_api` - Busca Geral

Busca textual case-insensitive em todos os módulos com contexto simétrico (20 linhas antes e depois).

**Parâmetros:**
- `query` (str): Termo de busca
- `modules` (str, opcional): Módulos específicos separados por vírgula, ou "all" (padrão)

**Exemplos:**

```python
# Buscar em todos os módulos
search_fusion_api("BRepBody")

# Buscar apenas em módulos específicos
search_fusion_api("Sketch", modules="fusion,core")

# Buscar funcionalidades CAM
search_fusion_api("toolpath", modules="cam")
```

**Output:**
- Até 5 matches por módulo
- 20 linhas de contexto (simétrico)
- Número da linha para navegação
- Resumo de matches

---

#### 2. `search_api` - Busca Inteligente ⭐

**NOVA!** Busca avançada com contexto assimétrico (10 linhas antes, 30 linhas depois). Ideal para capturar assinaturas de métodos e suas implementações completas.

**Parâmetros:**
- `keyword` (str): Palavra-chave (ex: "CommandInput", "createExtrude")
- `max_results` (int, opcional): Máximo de resultados (padrão: 5, máx: 10)

**Exemplos:**

```python
# Buscar CommandInput com contexto estendido
search_api("CommandInput")

# Buscar métodos de criação
search_api("create", max_results=10)

# Buscar eventos
search_api("Event", max_results=3)
```

**Vantagens:**
- **10 linhas antes**: Contexto da classe/estrutura
- **30 linhas depois**: Implementação completa do método
- Perfeito para entender assinaturas e uso de métodos
- Máximo de 10 resultados (configurável)

---

#### 3. `get_full_class` - Extração Completa de Classes ⭐

**NOVA!** Extrai uma classe completa com TODOS os métodos, propriedades e docstrings.

**Parâmetros:**
- `class_name` (str): Nome exato da classe

**Exemplos:**

```python
# Obter classe completa do BRepBody
get_full_class("BRepBody")

# Ver todos os métodos de Sketch
get_full_class("Sketch")

# Explorar CommandInput
get_full_class("CommandInput")

# Ver definições de eventos
get_full_class("CommandCreatedEventHandler")
```

**Output:**
- Classe completa com indentação
- Todos os métodos e propriedades
- Docstrings incluídas
- Localização (módulo + linha)
- Contador de linhas totais

---

#### 4. `search_by_category` - Busca por Categoria ⭐

**NOVA!** Navega pela API usando categorias semânticas. Retorna todas as classes relacionadas.

**Categorias Disponíveis:**
- `ui` - Interface do usuário (Commands, Inputs, Dialogs, Palettes, HTML)
- `geometry` - Geometria (Points, Vectors, Curves, Surfaces, BRep)
- `sketch` - Sketch (Lines, Circles, Constraints, Profiles)
- `feature` - Features (Extrude, Revolve, Fillet, Pattern)
- `component` - Componentes (Assembly, Occurrence, Joints)
- `cam` - CAM/Manufacturing (Operations, Tools, Toolpaths)
- `material` - Materiais (Appearances, Physical Properties)
- `document` - Documentos (Design, Export, Import)

**Exemplos:**

```python
# Ver todas as classes de UI
search_by_category("ui")

# Explorar geometria
search_by_category("geometry")

# Descobrir features disponíveis
search_by_category("feature")
```

**Output:**
- Lista organizada por módulo
- Descrição breve de cada classe
- Número da linha
- Contador total

---

#### 5. `explore_ui` - Explorador de UI/GUI ⭐

**NOVA!** Ferramenta especializada para descobrir TODAS as capacidades de interface gráfica do Fusion 360.

**Não requer parâmetros** - retorna tudo relacionado a UI!

**Exemplo:**

```python
explore_ui()
```

**Categorias Incluídas:**
- **Interface**: Commands, Inputs, Dialogs, Palettes, HTML, Browser, Windows
- **Controls**: Buttons, TextBoxes, CheckBoxes, Sliders, DropDowns, Lists
- **Input Types**: ValueInput, StringInput, BoolInput, SelectionInput
- **Events**: Event Handlers, CommandCreated, InputChanged, Validate
- **Display**: Graphics, CustomGraphics, Viewport, Camera
- **Layout**: Groups, Tabs, Rows, Columns

**Output:**
- Organizado por categoria
- Todas as classes UI encontradas
- Módulo e linha de cada classe
- Descrições extraídas
- Dicas de uso

### 2. Resources (Recursos)

#### Informacionais
- `fusion://info` - Informações do servidor e status dos arquivos
- `fusion://version` - Informações de versão da API

#### Módulos Individuais
- `fusion://core` - Apenas adsk.core (916KB)
- `fusion://fusion` - Apenas adsk.fusion (2.4MB)
- `fusion://cam` - Apenas adsk.cam (358KB)
- `fusion://drawing` - Apenas adsk.drawing (5.9KB)
- `fusion://volume` - Apenas adsk.volume (41KB)
- `fusion://sim` - Apenas adsk.sim (231B)

#### Contexto Completo
- `fusion://full_context` - **TODOS** os módulos concatenados (~3.7MB)
  - ⚠️ **Atenção:** Este recurso retorna ~89,000 linhas de código

## 🎯 Casos de Uso Práticos

### Cenário 1: "Quero criar uma interface customizada"

```python
# Passo 1: Explorar todas as opções de UI
explore_ui()

# Passo 2: Ver uma classe específica de interesse
get_full_class("CommandInput")

# Passo 3: Buscar detalhes sobre tipos específicos de input
search_api("TextBoxCommandInput", max_results=3)

# Passo 4: Ver todas as classes de diálogo
search_by_category("ui")
```

**Resultado:** Você terá uma visão completa de todas as ferramentas UI disponíveis, suas assinaturas, e exemplos de uso.

---

### Cenário 2: "Como usar HTML/Browser no Fusion?"

```python
# Busca abrangente por HTML
search_api("HTML")

# Buscar HTMLPalette especificamente
get_full_class("HTMLPalette")

# Ver todas as classes relacionadas a Browser
search_api("Browser", max_results=5)
```

---

### Cenário 3: "Preciso trabalhar com geometria BRep"

```python
# Ver todas as classes de geometria
search_by_category("geometry")

# Extrair classe completa do BRepBody
get_full_class("BRepBody")

# Buscar métodos de criação
search_api("createBRep", max_results=10)

# Ver faces, edges, vertices
search_api("BRepFace")
search_api("BRepEdge")
```

---

### Cenário 4: "Descobrir funcionalidades CAM"

```python
# Categorias CAM
search_by_category("cam")

# Operações disponíveis
search_api("Operation", max_results=10)

# Toolpath completo
get_full_class("Toolpath")

# Estratégias específicas
search_fusion_api("Strategy", modules="cam")
```

---

### Cenário 5: "Quais eventos existem?"

```python
# Busca abrangente por eventos
search_api("Event", max_results=10)

# Handler específico
get_full_class("CommandCreatedEventHandler")

# Explorar categoria UI (inclui eventos)
search_by_category("ui")
```

---

### Cenário 6: "Não sei o nome exato, só uma ideia"

```python
# Busca por termo genérico
search_api("input")  # Retorna todos os tipos de input

# Categoria ampla
search_by_category("ui")  # Lista TUDO de interface

# Explorador dedicado
explore_ui()  # Visão completa organizada
```

## 📊 Comparação de Ferramentas - Qual Usar?

| Situação | Ferramenta Recomendada | Por quê? |
|----------|------------------------|----------|
| "Não sei o que existe de UI" | `explore_ui()` | Visão completa categorizada |
| "Quero ver tudo sobre X categoria" | `search_by_category("ui")` | Lista todas as classes |
| "Preciso da classe completa de X" | `get_full_class("X")` | Extrai tudo da classe |
| "Buscar método e ver implementação" | `search_api("methodName")` | 30 linhas depois |
| "Busca genérica com contexto" | `search_fusion_api("term")` | Contexto balanceado |
| "Buscar só em módulo específico" | `search_fusion_api("term", "core")` | Filtra módulo |

### Quando usar cada contexto?

**`search_api()` - 10 antes, 30 depois**
- ✅ Ver assinatura completa de métodos
- ✅ Entender implementação de funções
- ✅ Capturar docstrings completas
- ✅ Ver vários métodos de uma classe

**`search_fusion_api()` - 20 antes, 20 depois**
- ✅ Contexto balanceado
- ✅ Ver estrutura ao redor
- ✅ Busca mais rápida
- ✅ Quando não precisa de implementação longa

**`get_full_class()` - Classe inteira**
- ✅ Ver TODOS os métodos
- ✅ Entender hierarquia completa
- ✅ Referência completa
- ✅ Copiar definição inteira

## Integração com Claude Code

Este servidor é projetado para ser usado com Claude Code ou outros clientes MCP.

### Configuração no Claude Code

Adicione ao seu `mcp_config.json`:

```json
{
  "mcpServers": {
    "fusion360-api": {
      "command": "python",
      "args": ["/caminho/para/fusion_mcp_server.py"],
      "env": {}
    }
  }
}
```

### Exemplos de Uso com Claude

#### Exemplo 1: Descoberta de UI
```
Usuário: "Quais tipos de inputs posso usar em um comando customizado?"

Claude: [usa explore_ui()]
"Encontrei 47 classes relacionadas a UI. Na categoria 'input', você tem:
- TextBoxCommandInput: Entrada de texto
- ValueInput: Valores numéricos com unidades
- BoolValueCommandInput: Checkbox/toggle
- DropDownCommandInput: Lista suspensa
- SelectionCommandInput: Seleção de entidades
..."

Usuário: "Me mostre a classe completa de TextBoxCommandInput"

Claude: [usa get_full_class("TextBoxCommandInput")]
"Aqui está a definição completa com todos os métodos e propriedades..."
```

#### Exemplo 2: Busca Inteligente
```
Usuário: "Como criar uma extrusão?"

Claude: [usa search_api("createExtrude", max_results=3)]
"Encontrei 3 métodos relacionados a createExtrude. O principal está em adsk.fusion:

Match 1 - adsk.fusion (line 15234)
class ExtrudeFeatures():
    def createExtrude(self, input: ExtrudeFeatureInput) -> ExtrudeFeature:
        '''Creates a new extrude feature...
        Args:
            input: ExtrudeFeatureInput object...
        Returns:
            ExtrudeFeature object...
        '''
..."
```

#### Exemplo 3: Navegação por Categoria
```
Usuário: "O que posso fazer com CAM?"

Claude: [usa search_by_category("cam")]
"Encontrei 156 classes na categoria CAM:

--- adsk.cam ---
  • CAM (line 234)
    The CAM product
  • Operation (line 1456)
    Base class for all operations
  • Setup (line 2341)
    Defines the workpiece and fixtures
  • ToolLibrary (line 3567)
    Collection of tools
..."
```

## Arquitetura do Servidor

```
fusion_mcp_server.py
├── API_MODULES (dict)       # Mapeamento de módulos para arquivos
├── read_file_safe()         # Leitura segura de arquivos
├── get_context_lines()      # Extração de contexto com linhas
├── get_api_version()        # Lê versão da API
│
├── [TOOL] search_fusion_api()    # Busca em múltiplos módulos
│
└── [RESOURCES]
    ├── fusion://info            # Server info
    ├── fusion://version         # API version
    ├── fusion://core            # Core module
    ├── fusion://fusion          # Fusion module
    ├── fusion://cam             # CAM module
    ├── fusion://drawing         # Drawing module
    ├── fusion://volume          # Volume module
    ├── fusion://sim             # Sim module
    └── fusion://full_context    # All modules
```

## Performance

- **Busca:** ~100-500ms para buscar em todos os 7 módulos
- **Resource individual:** ~50-200ms dependendo do tamanho do módulo
- **Full context:** ~1-2s para carregar todos os 3.7MB

## Tratamento de Erros

O servidor trata graciosamente:
- Arquivos ausentes (retorna mensagem de erro clara)
- Queries vazias (valida entrada)
- Módulos inválidos (lista módulos disponíveis)
- Erros de leitura (captura exceções)

## Limitações

- **Output limitado:** Máximo de 5 matches por módulo por busca (evita overflow)
- **Contexto fixo:** 20 linhas antes/depois de cada match
- **Case-insensitive:** Busca não diferencia maiúsculas/minúsculas
- **Busca literal:** Não suporta regex na ferramenta de busca

## Desenvolvimento

### Estrutura do Código

```python
# Definição de paths
API_BASE_PATH = SCRIPT_DIR / "API" / "Python" / "defs" / "adsk"

# Módulos suportados
API_MODULES = {
    "core": API_BASE_PATH / "core.py",
    "fusion": API_BASE_PATH / "fusion.py",
    # ... outros módulos
}
```

### Adicionar Novos Módulos

1. Adicione o arquivo .py em `./API/Python/defs/adsk/`
2. Adicione entrada em `API_MODULES`
3. Crie resource dedicado (opcional)
4. Atualize documentação

## Troubleshooting

### Servidor não inicia
```bash
# Verificar instalação do fastmcp
pip list | grep fastmcp

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Arquivos não encontrados
```bash
# Verificar estrutura de pastas
ls -R ./API/Python/defs/adsk/

# Verificar paths no código
python -c "from pathlib import Path; print(Path('API/Python/defs/adsk').resolve())"
```

### Busca não retorna resultados
- Verifique se o termo está correto
- Tente busca parcial (ex: "Sketch" ao invés de "SketchClass")
- Use `modules="all"` para buscar em todos os módulos

## Licença

Este servidor é um wrapper para documentação da API do Fusion 360.
A documentação da API pertence à Autodesk.

## Suporte

Para issues e melhorias, entre em contato com o desenvolvedor do servidor.

---

**Desenvolvido para:** Claude Code MCP Integration
**Versão do Servidor:** 1.0
**API Suportada:** Fusion 360 v2605.1.18
