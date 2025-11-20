#!/usr/bin/env python3
"""
Exemplos de Uso do Fusion 360 MCP Server
Demonstra todas as ferramentas disponíveis com casos de uso práticos
"""

# NOTA: Este arquivo contém exemplos de chamadas.
# Para executar, você precisa ter o servidor MCP rodando e um cliente MCP conectado.

# ============================================================================
# EXEMPLO 1: EXPLORAÇÃO GERAL DE UI
# ============================================================================
# Caso: Você não sabe o que existe de interface no Fusion 360

def exemplo_1_descoberta_ui():
    """
    Use quando: Você está começando e quer ver tudo disponível de UI/GUI
    """
    # Ferramenta: explore_ui()
    # Retorna: Todas as classes UI organizadas por categoria

    print("EXEMPLO 1: Descobrir todas as opções de UI/GUI")
    print("Chamada: explore_ui()")
    print("\nEspera-se ver:")
    print("- Interface: Commands, Dialogs, Palettes, HTML")
    print("- Controls: Buttons, TextBoxes, CheckBoxes")
    print("- Input Types: ValueInput, StringInput, BoolInput")
    print("- Events: Handlers, Created, Changed")
    print("- Display: Graphics, Viewport")
    print("- Layout: Groups, Tabs")
    print("\nTotal: ~40-60 classes UI categorizadas")


# ============================================================================
# EXEMPLO 2: BUSCA POR CATEGORIA
# ============================================================================
# Caso: Você quer ver tudo relacionado a uma área específica

def exemplo_2_busca_categoria():
    """
    Use quando: Quer explorar uma área específica (UI, geometria, CAM, etc)
    """
    # Ferramenta: search_by_category(category)
    # Categorias: ui, geometry, sketch, feature, component, cam, material, document

    print("\nEXEMPLO 2: Buscar por categoria")
    print("Chamada: search_by_category('ui')")
    print("\nRetorna:")
    print("- Lista de todas as classes UI")
    print("- Organizado por módulo (core, fusion, etc)")
    print("- Descrição de cada classe")
    print("- Linha onde está definida")

    print("\n\nOutros exemplos:")
    print("search_by_category('geometry')  # Ver todas as classes de geometria")
    print("search_by_category('cam')       # Ver operações CAM")
    print("search_by_category('sketch')    # Ver recursos de sketch")


# ============================================================================
# EXEMPLO 3: EXTRAÇÃO DE CLASSE COMPLETA
# ============================================================================
# Caso: Você encontrou uma classe interessante e quer ver TUDO sobre ela

def exemplo_3_classe_completa():
    """
    Use quando: Quer ver todos os métodos e propriedades de uma classe
    """
    # Ferramenta: get_full_class(class_name)

    print("\nEXEMPLO 3: Obter classe completa")
    print("Chamada: get_full_class('CommandInput')")
    print("\nRetorna:")
    print("- Definição completa da classe")
    print("- TODOS os métodos e propriedades")
    print("- Docstrings incluídas")
    print("- Módulo de origem (adsk.core)")
    print("- Linha inicial")

    print("\n\nOutros exemplos:")
    print("get_full_class('BRepBody')           # Geometria BRep completa")
    print("get_full_class('Sketch')             # Tudo sobre sketches")
    print("get_full_class('HTMLPalette')        # Interface HTML")
    print("get_full_class('ExtrudeFeature')     # Feature de extrusão")


# ============================================================================
# EXEMPLO 4: BUSCA INTELIGENTE COM CONTEXTO ESTENDIDO
# ============================================================================
# Caso: Você quer encontrar métodos e ver suas assinaturas + implementação

def exemplo_4_busca_inteligente():
    """
    Use quando: Quer ver assinatura de método E contexto de implementação
    """
    # Ferramenta: search_api(keyword, max_results)
    # Contexto: 10 linhas antes, 30 linhas depois

    print("\nEXEMPLO 4: Busca inteligente (contexto assimétrico)")
    print("Chamada: search_api('CommandInput', max_results=5)")
    print("\nRetorna:")
    print("- 10 linhas ANTES: Contexto da classe/estrutura")
    print("- Match na linha")
    print("- 30 linhas DEPOIS: Implementação completa")
    print("- Até 5 resultados (configurável até 10)")

    print("\n\nPerfeito para:")
    print("search_api('createExtrude')          # Ver como criar extrusão")
    print("search_api('Event', max_results=10)  # Ver todos os eventos")
    print("search_api('HTML')                   # Interfaces HTML")
    print("search_api('Button')                 # Botões e controles")


# ============================================================================
# EXEMPLO 5: BUSCA GERAL BALANCEADA
# ============================================================================
# Caso: Busca ampla com contexto simétrico

def exemplo_5_busca_geral():
    """
    Use quando: Quer busca ampla com contexto balanceado
    """
    # Ferramenta: search_fusion_api(query, modules)
    # Contexto: 20 linhas antes, 20 linhas depois

    print("\nEXEMPLO 5: Busca geral balanceada")
    print("Chamada: search_fusion_api('BRepBody')")
    print("\nRetorna:")
    print("- Busca em todos os módulos (ou filtrado)")
    print("- 20 linhas antes e depois (simétrico)")
    print("- Até 5 matches por módulo")

    print("\n\nCom filtro de módulo:")
    print("search_fusion_api('Sketch', modules='fusion')      # Só em fusion")
    print("search_fusion_api('Point', modules='core,fusion')  # Em 2 módulos")
    print("search_fusion_api('toolpath', modules='cam')       # Só CAM")


# ============================================================================
# FLUXOS DE TRABALHO COMPLETOS
# ============================================================================

def workflow_criar_comando_customizado():
    """
    WORKFLOW: Criar um comando customizado com interface
    """
    print("\n" + "="*80)
    print("WORKFLOW COMPLETO: Criar Comando Customizado com UI")
    print("="*80)

    print("\nPasso 1: Descobrir opções de UI")
    print("  → explore_ui()")
    print("  Resultado: Ver Commands, Inputs, Dialogs disponíveis")

    print("\nPasso 2: Entender Command base")
    print("  → get_full_class('Command')")
    print("  Resultado: Ver métodos de Command")

    print("\nPasso 3: Ver tipos de input disponíveis")
    print("  → search_by_category('ui')")
    print("  Resultado: Lista de TextBox, ValueInput, etc")

    print("\nPasso 4: Detalhar input específico")
    print("  → get_full_class('TextBoxCommandInput')")
    print("  Resultado: Métodos e propriedades completas")

    print("\nPasso 5: Ver como criar inputs")
    print("  → search_api('addTextBoxInput')")
    print("  Resultado: Assinatura + contexto de uso")

    print("\nPasso 6: Entender eventos")
    print("  → search_api('CommandCreatedEventHandler')")
    print("  Resultado: Como lidar com eventos do comando")


def workflow_trabalhar_com_html():
    """
    WORKFLOW: Criar interface HTML customizada
    """
    print("\n" + "="*80)
    print("WORKFLOW COMPLETO: Interface HTML Customizada")
    print("="*80)

    print("\nPasso 1: Buscar tudo sobre HTML")
    print("  → search_api('HTML', max_results=10)")
    print("  Resultado: HTMLPalette, HTMLDialog, etc")

    print("\nPasso 2: Detalhar HTMLPalette")
    print("  → get_full_class('HTMLPalette')")
    print("  Resultado: Métodos completos da paleta")

    print("\nPasso 3: Ver como criar paleta")
    print("  → search_api('createHTMLPalette')")
    print("  Resultado: Assinatura e exemplo de uso")

    print("\nPasso 4: Entender Browser")
    print("  → search_api('Browser')")
    print("  Resultado: Como interagir com o navegador embutido")

    print("\nPasso 5: Ver eventos HTML")
    print("  → search_api('HTMLEvent')")
    print("  Resultado: Eventos disponíveis para HTML")


def workflow_geometria_brep():
    """
    WORKFLOW: Trabalhar com geometria BRep
    """
    print("\n" + "="*80)
    print("WORKFLOW COMPLETO: Geometria BRep")
    print("="*80)

    print("\nPasso 1: Ver todas as classes de geometria")
    print("  → search_by_category('geometry')")
    print("  Resultado: BRep, Face, Edge, Vertex, etc")

    print("\nPasso 2: Entender BRepBody")
    print("  → get_full_class('BRepBody')")
    print("  Resultado: Propriedades e métodos do corpo")

    print("\nPasso 3: Ver faces")
    print("  → get_full_class('BRepFace')")
    print("  Resultado: Como trabalhar com faces")

    print("\nPasso 4: Buscar métodos de criação")
    print("  → search_api('createBRep', max_results=10)")
    print("  Resultado: Todas as formas de criar BRep")

    print("\nPasso 5: Transformações")
    print("  → search_api('transform')")
    print("  Resultado: Como transformar geometria")


def workflow_cam_manufacturing():
    """
    WORKFLOW: Operações CAM
    """
    print("\n" + "="*80)
    print("WORKFLOW COMPLETO: CAM/Manufacturing")
    print("="*80)

    print("\nPasso 1: Ver tudo de CAM")
    print("  → search_by_category('cam')")
    print("  Resultado: Operations, Tools, Toolpaths, Setup")

    print("\nPasso 2: Entender Operation")
    print("  → get_full_class('Operation')")
    print("  Resultado: Base para todas as operações")

    print("\nPasso 3: Ver estratégias")
    print("  → search_api('Strategy', max_results=10)")
    print("  Resultado: Todas as estratégias disponíveis")

    print("\nPasso 4: Configuração de ferramentas")
    print("  → search_api('Tool')")
    print("  Resultado: Como configurar ferramentas")

    print("\nPasso 5: Gerar toolpath")
    print("  → search_api('generateToolpath')")
    print("  Resultado: Como gerar o toolpath")


# ============================================================================
# COMPARAÇÃO DE FERRAMENTAS
# ============================================================================

def comparacao_ferramentas():
    """
    Quando usar cada ferramenta
    """
    print("\n" + "="*80)
    print("COMPARAÇÃO: Qual Ferramenta Usar?")
    print("="*80)

    comparacoes = [
        ("Não sei o que existe de UI", "explore_ui()", "Visão completa categorizada"),
        ("Quero ver categoria X", "search_by_category('X')", "Lista todas as classes"),
        ("Preciso classe completa", "get_full_class('Nome')", "Tudo da classe"),
        ("Buscar método + código", "search_api('palavra')", "10 antes + 30 depois"),
        ("Busca geral balanceada", "search_fusion_api('termo')", "20 antes + 20 depois"),
        ("Filtrar por módulo", "search_fusion_api('X', 'core')", "Busca focada"),
    ]

    print("\n{:<30} {:<35} {:<30}".format("SITUAÇÃO", "FERRAMENTA", "VANTAGEM"))
    print("-" * 95)
    for situacao, ferramenta, vantagem in comparacoes:
        print("{:<30} {:<35} {:<30}".format(situacao, ferramenta, vantagem))


# ============================================================================
# DICAS E TRUQUES
# ============================================================================

def dicas_uso():
    """
    Dicas para usar o servidor eficientemente
    """
    print("\n" + "="*80)
    print("DICAS E TRUQUES")
    print("="*80)

    print("\n✅ FAÇA:")
    print("  • Use explore_ui() quando não souber por onde começar")
    print("  • Use search_by_category() para explorar áreas")
    print("  • Use get_full_class() quando precisar de referência completa")
    print("  • Use search_api() para ver assinaturas e código")
    print("  • Aumente max_results se precisar de mais exemplos")

    print("\n❌ EVITE:")
    print("  • Buscar termos muito genéricos sem categoria")
    print("  • Usar get_full_class() para busca exploratória")
    print("  • Usar fusion://full_context sem necessidade (3.7MB)")

    print("\n💡 TRUQUES:")
    print("  • Combine ferramentas: explore_ui() → get_full_class()")
    print("  • Use max_results=10 para ver mais variações")
    print("  • Busque por verbos: 'create', 'add', 'get', 'set'")
    print("  • Categorias são case-insensitive")
    print("  • Classes são case-sensitive (preciso)")


# ============================================================================
# MAIN - EXECUTAR EXEMPLOS
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print(" FUSION 360 MCP SERVER - EXEMPLOS DE USO")
    print("="*80)
    print("\nNOTA: Estes são exemplos de chamadas MCP.")
    print("Para executar, você precisa de um cliente MCP conectado ao servidor.\n")

    # Executar exemplos
    exemplo_1_descoberta_ui()
    exemplo_2_busca_categoria()
    exemplo_3_classe_completa()
    exemplo_4_busca_inteligente()
    exemplo_5_busca_geral()

    # Workflows completos
    workflow_criar_comando_customizado()
    workflow_trabalhar_com_html()
    workflow_geometria_brep()
    workflow_cam_manufacturing()

    # Comparação e dicas
    comparacao_ferramentas()
    dicas_uso()

    print("\n" + "="*80)
    print("Para mais informações, veja:")
    print("  • README_MCP.md - Documentação completa")
    print("  • QUICK_REFERENCE.md - Referência rápida")
    print("  • CHANGELOG.md - Novidades da v2.0")
    print("="*80)
