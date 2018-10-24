import yaml


def main():
    cnab = "/var/www/html/fadivale/vendor/versatecnologia/cnab_yaml/cnab240/";
    remessa = "/home/eduardo/Downloads/BANCO_237.CEDENTE_7827764.DATA_2018-10-23_16-28-19.PARTE_1.REMESSA_2.rem"
    arquivo = {}
    erros = {}

    arquivo["headerArquivo"] = cnab + "237/header_arquivo.yml";
    arquivo["headerLote"] = cnab + "237/header_lote.yml";
    arquivo["trailerArquivo"] = cnab + "237/trailer_arquivo.yml";
    arquivo["trailerLote"] = cnab + "237/trailer_lote.yml";
    arquivo["segmentoP"] = cnab + "generic/remessa/detalhe_segmento_p.yml";

    remessa = open(remessa, "r")

    for arq in arquivo:
        segmento = carregarCnab(arquivo[arq])
        erros[arq] = {}
        for linha in remessa.readlines():
            for row in segmento:
                field = segmento[row]
                value = linha[field["posicaoInicial"]:field["posicaoFinal"]]

                if field["padrao"] != False and value == "":
                    print("\nPadrão é " + field["padrao"] + " mas o campo está vazio")

                if value.__len__() != field["tamanho"]:
                    print("\nTamanho deve ser " + str(field["tamanho"]) + ", mas o campo tem tamanho " + str(value.__len__()) + " em " + arq + " > " + row)

                if field["tipo"] == "int":
                    value = value.replace("[^0-9]", "")
                    if value == "":
                        print("\n" + row + " deve ser inteiro, passado " + str(value) + " em " + arq + " > " + row)


def carregarCnab(arquivo):
    d = {}
    p = yaml.load(open(arquivo, 'r'))
    for campo in p:
        posicao = p[campo]['pos']
        tamanho = int(posicao[1] - posicao[0]) + 1
        d[campo] = \
            {
                "posicaoInicial": int(p[campo]['pos'][0]) - 1,
                "posicaoFinal": int(p[campo]['pos'][1]),
                "tipo": "int" if p[campo]['picture'][0] == '9' else "str",
                "tamanho": tamanho,
                "padrao": p[campo]['default'] if 'default' in p[campo] else False
            }

    return d


if __name__ == '__main__':
    main()
