# Fusion 360 MCP Server - Changelog

## Version 2.0 - Atualização Major (2025)

### 🎯 Foco: Busca Inteligente e Descoberta de UI/GUI

Esta versão transforma o servidor em uma ferramenta poderosa de descoberta e exploração da API, especialmente para elementos de interface gráfica.

---

## 🆕 Novas Ferramentas (5 adições)

### 1. `search_api()` - Busca Inteligente
**Contexto Assimétrico: 10 antes, 30 depois**

```python
search_api(keyword: str, max_results: int = 5)
```

**Características:**
- ✅ Captura assinaturas completas de métodos
- ✅ Mostra implementações estendidas
- ✅ Perfeito para entender como usar uma função
- ✅ Contexto assimétrico otimizado (10+30 linhas)
- ✅ Máximo de 10 resultados configurável

**Caso de Uso:**
- "Como usar CommandInput?"
- "Quais métodos tem create?"
- "Ver assinatura de extrude"

---

### 2. `get_full_class()` - Extrator de Classes Completas

```python
get_full_class(class_name: str)
```

**Características:**
- ✅ Extrai classe INTEIRA baseada em indentação
- ✅ Inclui todos os métodos e propriedades
- ✅ Preserva docstrings
- ✅ Mostra módulo de origem e linha
- ✅ Conta total de linhas da classe

**Caso de Uso:**
- "Quero ver tudo sobre BRepBody"
- "Quais métodos tem a classe Sketch?"
- "Referência completa de CommandInput"

---

### 3. `search_by_category()` - Busca por Categoria Semântica

```python
search_by_category(category: str)
```

**8 Categorias Disponíveis:**
- `ui` - Interface (Commands, Inputs, Dialogs, HTML)
- `geometry` - Geometria (Points, Vectors, BRep)
- `sketch` - Sketch (Lines, Circles, Constraints)
- `feature` - Features (Extrude, Revolve, Fillet)
- `component` - Componentes (Assembly, Joints)
- `cam` - CAM (Operations, Tools, Toolpaths)
- `material` - Materiais e Appearances
- `document` - Documentos (Export, Import)

**Características:**
- ✅ Busca semântica por múltiplas keywords
- ✅ Agrupa resultados por módulo
- ✅ Extrai descrição de cada classe
- ✅ Mostra contagem total
- ✅ Organizado alfabeticamente

**Caso de Uso:**
- "O que existe de UI?"
- "Mostrar todas as features"
- "Listar operações CAM"

---

### 4. `explore_ui()` - Explorador Especializado de UI/GUI

```python
explore_ui()  # Sem parâmetros!
```

**Características:**
- ✅ Varre TODOS os módulos buscando UI
- ✅ Categoriza automaticamente:
  - Interface (Commands, Dialogs, Palettes)
  - Controls (Buttons, TextBoxes, CheckBoxes)
  - Input Types (Value, String, Bool, Selection)
  - Events (Handlers, Created, Changed)
  - Display (Graphics, Viewport, Camera)
  - Layout (Groups, Tabs, Rows)
- ✅ Retorna visão completa organizada
- ✅ Perfeito para descoberta sem saber o que procurar

**Keywords UI Indexadas:**
- Command, Input, Dialog, Palette, HTML, Browser
- Button, TextBox, CheckBox, Slider, DropDown
- Event, Handler, Validate, Execute
- Graphics, Viewport, Camera, Display
- Group, Tab, Row, Column

**Caso de Uso:**
- "O que posso fazer de interface?"
- "Quais tipos de input existem?"
- "Ver todas as opções de UI"

---

### 5. `search_fusion_api()` - Melhorada
**Contexto Simétrico: 20 antes, 20 depois**

Já existia, mas foi otimizada:
- ✅ Busca em todos os 7 módulos
- ✅ Filtragem por módulo específico
- ✅ Contexto balanceado
- ✅ Até 5 matches por módulo

---

## 🗂️ Sistema de Categorização

### Keywords por Categoria

**UI/Interface:**
- Commands, Inputs, Dialogs, Palettes
- HTML, Browser, Panel, Window
- Button, TextBox, CheckBox, Slider
- Event, Handler, Graphics

**Geometry:**
- Point, Vector, Line, Circle, Arc
- Curve, Surface, BRep, Body
- Face, Edge, Vertex

**Sketch:**
- Sketch, SketchLine, SketchCircle
- Profile, Constraint, Dimension

**Feature:**
- Extrude, Revolve, Sweep, Loft
- Fillet, Chamfer, Shell, Pattern

**CAM:**
- Operation, Setup, Tool, Toolpath
- Strategy, Post, NCProgram

E mais categorias...

---

## 🔧 Funções Auxiliares Novas

### `get_asymmetric_context()`
Extração de contexto assimétrico (10 antes, 30 depois)

```python
get_asymmetric_context(
    content: str,
    match_position: int,
    lines_before: int = 10,
    lines_after: int = 30
) -> tuple[str, int]
```

### `extract_full_class()`
Extração inteligente de classe baseada em indentação

```python
extract_full_class(
    content: str,
    class_name: str
) -> tuple[str, int] | None
```

---

## 📊 Estatísticas de Cobertura

### Módulos Indexados (7 total)
- ✅ adsk.core (916KB, 22,263 linhas)
- ✅ adsk.fusion (2.4MB, 55,453 linhas)
- ✅ adsk.cam (358KB, 9,952 linhas)
- ✅ adsk.drawing (5.9KB, 179 linhas)
- ✅ adsk.volume (41KB, 1,204 linhas)
- ✅ adsk.sim (231B, 9 linhas)
- ✅ adsk.__init__ (1.3KB, 12 linhas)

**Total: 3.7MB, ~89,000 linhas**

### Keywords UI Indexadas
- **Interface**: 8 keywords
- **Controls**: 8 keywords
- **Input**: 6 keywords
- **Events**: 7 keywords
- **Display**: 6 keywords
- **Layout**: 6 keywords

**Total: ~40 keywords UI**

### Categorias Semânticas
- 8 categorias principais
- ~60 keywords totais
- Cobertura completa da API

---

## 📝 Documentação Atualizada

### Novos Arquivos
- ✅ `QUICK_REFERENCE.md` - Guia rápido de 5 minutos
- ✅ `CHANGELOG.md` - Este arquivo
- ✅ `README_MCP.md` - Atualizado com 5 ferramentas

### Seções Adicionadas ao README
- 🎯 Casos de Uso Práticos (6 cenários)
- 📊 Comparação de Ferramentas
- 💡 Quando usar cada contexto
- 🚀 Exemplos com Claude
- 📋 Tabela de decisão

---

## 🔄 Melhorias em Funções Existentes

### `get_server_info()`
- ✅ Lista todas as 5 ferramentas
- ✅ Exemplos de uso para cada
- ✅ Estatísticas detalhadas
- ✅ Informações de módulos

### Resources
- ✅ Mantidos todos os 9 resources
- ✅ Documentação melhorada
- ✅ Warnings para full_context

---

## 🎨 Melhorias de UX

### Output Formatado
- ✅ Separadores visuais (═══, ───)
- ✅ Contadores de resultados
- ✅ Mensagens de erro amigáveis
- ✅ Dicas de uso inline
- ✅ Sugestões de ferramentas alternativas

### Validação de Input
- ✅ Verificação de queries vazias
- ✅ Validação de categorias
- ✅ Sugestões quando não encontra
- ✅ Limites configuráveis

---

## 🚀 Performance

### Otimizações
- ✅ Cache em memória (futuro)
- ✅ Busca limitada (max_results)
- ✅ Extração por indentação (rápida)
- ✅ Regex compilado

### Tempos Estimados
- `search_api()`: ~100-300ms
- `get_full_class()`: ~50-150ms
- `search_by_category()`: ~200-500ms
- `explore_ui()`: ~300-800ms
- `search_fusion_api()`: ~100-500ms

---

## 🎯 Objetivos Alcançados

### ✅ Busca Inteligente
- Contexto assimétrico implementado
- 10 antes, 30 depois para métodos
- Configurável via max_results

### ✅ Extração de Classes
- Baseada em indentação Python
- Classes completas extraídas
- Preserva estrutura original

### ✅ Descoberta de UI
- Keywords especializadas
- Categorização automática
- 6 subcategorias de UI

### ✅ Navegação Semântica
- 8 categorias principais
- ~60 keywords indexadas
- Busca multi-keyword

### ✅ Documentação Completa
- 3 documentos criados
- Exemplos práticos
- Guias de decisão

---

## 🔮 Próximas Melhorias (Futuro)

### V3.0 Potencial
- [ ] Cache persistente em disco
- [ ] Busca por regex avançada
- [ ] Índice invertido para performance
- [ ] Suporte a múltiplas versões da API
- [ ] Exportação de resultados (JSON/Markdown)
- [ ] Análise de dependências entre classes
- [ ] Geração de snippets de código

### Ferramentas Adicionais
- [ ] `find_related_classes()` - Classes relacionadas
- [ ] `get_inheritance_tree()` - Árvore de herança
- [ ] `search_by_signature()` - Busca por assinatura
- [ ] `get_usage_examples()` - Exemplos de uso

---

## 📦 Compatibilidade

### Requerimentos
- Python 3.8+
- fastmcp >= 0.1.0
- mcp >= 0.1.0

### API Version
- Fusion 360 API v2605.1.18

### Clientes MCP
- ✅ Claude Code
- ✅ Outros clientes MCP compatíveis

---

## 🙏 Agradecimentos

Este servidor MCP foi desenvolvido para facilitar o desenvolvimento com a API do Fusion 360, especialmente para criação de interfaces customizadas e automação CAD/CAM.

**Desenvolvido para:** Comunidade Fusion 360
**Foco:** Descoberta de UI/GUI e busca inteligente
**Versão:** 2.0

---

**Data:** Janeiro 2025
**Status:** Produção ✅
