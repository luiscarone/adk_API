# Fusion 360 MCP Server - Referência Rápida

## 🚀 Guia de 5 Minutos

### Instalação
```bash
pip install -r requirements.txt
python fusion_mcp_server.py
```

---

## 📋 Tabela de Ferramentas

| Ferramenta | Uso | Quando Usar |
|------------|-----|-------------|
| `explore_ui()` | Sem parâmetros | "Não sei o que existe de UI" |
| `search_by_category(cat)` | `"ui"`, `"geometry"`, `"sketch"`, etc | "Quero ver tudo sobre X" |
| `get_full_class(nome)` | `"BRepBody"`, `"Sketch"` | "Preciso da classe completa" |
| `search_api(palavra)` | `"CommandInput"` | "Buscar método + implementação" |
| `search_fusion_api(termo)` | `"extrude"` | "Busca geral balanceada" |

---

## 🎯 Fluxo de Trabalho Comum

### 1️⃣ Descoberta (O que existe?)
```python
# Opção A: Explorar UI completa
explore_ui()

# Opção B: Ver categoria específica
search_by_category("ui")
search_by_category("geometry")
search_by_category("cam")
```

### 2️⃣ Investigação (Como funciona?)
```python
# Buscar por palavra-chave com contexto estendido
search_api("CommandInput", max_results=5)

# OU busca mais ampla
search_fusion_api("Button")
```

### 3️⃣ Detalhamento (Quero tudo sobre isso)
```python
# Extrair classe completa
get_full_class("TextBoxCommandInput")
get_full_class("BRepBody")
```

---

## 📚 Categorias Disponíveis

| Categoria | Inclui | Exemplo |
|-----------|--------|---------|
| `ui` | Commands, Inputs, Dialogs, Palettes, HTML | `search_by_category("ui")` |
| `geometry` | Points, Vectors, Curves, BRep | `search_by_category("geometry")` |
| `sketch` | Lines, Circles, Constraints | `search_by_category("sketch")` |
| `feature` | Extrude, Revolve, Fillet | `search_by_category("feature")` |
| `component` | Assembly, Occurrence, Joints | `search_by_category("component")` |
| `cam` | Operations, Tools, Toolpaths | `search_by_category("cam")` |
| `material` | Materials, Appearances | `search_by_category("material")` |
| `document` | Design, Export, Import | `search_by_category("document")` |

---

## 💡 Dicas Rápidas

### Cenário: "Quero criar uma UI customizada"
```python
1. explore_ui()                        # Ver tudo disponível
2. get_full_class("CommandInput")      # Detalhar classe base
3. search_api("TextBox")               # Ver inputs específicos
```

### Cenário: "Como trabalhar com HTML?"
```python
1. search_api("HTML")                  # Busca geral
2. get_full_class("HTMLPalette")       # Classe completa
3. search_api("Browser")               # Classes relacionadas
```

### Cenário: "Preciso criar geometria"
```python
1. search_by_category("geometry")      # Ver todas as opções
2. get_full_class("BRepBody")          # Detalhar classe
3. search_api("create", max_results=10) # Métodos de criação
```

---

## 🔍 Diferenças de Contexto

| Ferramenta | Contexto | Melhor Para |
|------------|----------|-------------|
| `search_api()` | 10 antes + **30 depois** | Assinaturas e implementações |
| `search_fusion_api()` | 20 antes + 20 depois | Contexto balanceado |
| `get_full_class()` | **Classe inteira** | Referência completa |

---

## 📖 Resources (URIs)

### Informação
- `fusion://info` - Info do servidor
- `fusion://version` - Versão da API

### Módulos Individuais
- `fusion://core` - adsk.core (916KB)
- `fusion://fusion` - adsk.fusion (2.4MB)
- `fusion://cam` - adsk.cam (358KB)
- `fusion://drawing` - adsk.drawing (5.9KB)
- `fusion://volume` - adsk.volume (41KB)
- `fusion://sim` - adsk.sim (231B)

### Completo
- `fusion://full_context` - TUDO (3.7MB, 89k linhas)

---

## ⚡ Atalhos Mentais

| Pergunta Mental | Use Isto |
|-----------------|----------|
| "O que tem de X?" | `search_by_category("X")` |
| "Como é a classe Y?" | `get_full_class("Y")` |
| "Onde usar Z?" | `search_api("Z")` |
| "O que tem de UI?" | `explore_ui()` |
| "Busca ampla de W" | `search_fusion_api("W")` |

---

## 🎓 Exemplos de Queries

### UI/Interface
```python
explore_ui()
get_full_class("CommandInput")
search_api("Dialog")
search_api("Palette")
search_api("HTML")
search_by_category("ui")
```

### Geometria
```python
search_by_category("geometry")
get_full_class("BRepBody")
search_api("Point3D")
search_api("Vector3D")
get_full_class("Curve")
```

### Features
```python
search_by_category("feature")
search_api("Extrude")
get_full_class("ExtrudeFeature")
search_api("createExtrude")
```

### CAM/Manufacturing
```python
search_by_category("cam")
search_api("Operation")
get_full_class("Toolpath")
search_api("Strategy")
```

### Eventos
```python
search_api("Event", max_results=10)
get_full_class("CommandCreatedEventHandler")
search_api("Handler")
```

---

## 🔧 Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| Nenhum resultado | Tente termo mais genérico ou `explore_ui()` |
| Classe não encontrada | Use `search_api("nome")` para achar similar |
| Muitos resultados | Aumente `max_results` ou use `get_full_class()` |
| Quer contexto maior | Use `search_api()` (30 linhas depois) |
| Quer classe completa | Use `get_full_class()` |

---

## 📊 Estatísticas do Servidor

- **7 módulos** indexados
- **~89,000 linhas** de código
- **3.7 MB** de definições
- **API v2605.1.18**

---

## 🚀 Start Rápido para Agentes LLM

```python
# Se não sabe o que procurar
explore_ui()  # Para UI
search_by_category("geometry")  # Para geometria
search_by_category("cam")  # Para CAM

# Se sabe a classe
get_full_class("ClassName")

# Se sabe palavra-chave
search_api("keyword", max_results=5)

# Busca ampla
search_fusion_api("term")
```

---

**Versão do Servidor:** 2.0
**API Fusion 360:** 2605.1.18
**Última Atualização:** 2025
