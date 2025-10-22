class GeradorRelatorio:
    def gerar_relatorio_resumido(self, dados):
        print("\n" + "_"*80 + "\n")
        print("RELATÓRIO")
        print("\n" + "_"*80 + "\n")
        if 'informacoes_gerais' in dados:
            print("\nINFORMAÇÕES GERAIS:")
            for chave, valor in dados['informacoes_gerais'].items():
                print(f"  {chave}: {valor}")

        if 'componentes' in dados:
            print(f"\nCOMPONENTES IDENTIFICADOS: {len(dados['componentes'])}")
            for comp in dados['componentes']:
                print(f"  - {comp.get('nome', 'N/A')}")

        if 'problemas_relatados' in dados:
            print(f"\nPROBLEMAS RELATADOS: {len(dados['problemas_relatados'])}")
            for prob in dados['problemas_relatados']:
                print(f"  - [{prob.get('severidade', 'N/A')}] {prob.get('descricao', 'N/A')[:60]}...")

        if 'acoes_recomendadas' in dados:
            print(f"\nAÇÕES RECOMENDADAS: {len(dados['acoes_recomendadas'])}")
            for acao in dados['acoes_recomendadas']:
                print(f"  - [{acao.get('prioridade', 'N/A')}] {acao.get('descricao', 'N/A')[:60]}...")

        if 'informacoes_ambiguas' in dados and len(dados['informacoes_ambiguas']) > 0:
            print(f"\nINFORMACOES AMBÍGUAS OU INCOMPLETAS: {len(dados['informacoes_ambiguas'])}")
            for item in dados['informacoes_ambiguas']:
                print(f"  - {item.get('item', 'N/A')}")
                print(f"    Motivo: {item.get('motivo', 'N/A')}")

        print("\n" + "_"*80 + "\n")
