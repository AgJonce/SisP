import pandas as pd
import streamlit as st
from PIL import Image
import datetime
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os
from datetime import datetime
import matplotlib.pyplot as plt
import streamlit as st
import re
import sqlite3
import requests
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO
import os
from datetime import datetime
import plotly.graph_objects as go

def validar_ide(linha):
    erros = []
    campos = linha.split(";")
    if len(campos) != 10:
        erros.append("❌ Linha do IDE deve conter exatamente 9 campos.")
    else:
        regex_tipoRegistro = r'^\d{5}$'
        regex_cnpj = r'^\d{14}$'
        regex_codOrgao = r'^\d{3}$'
        regex_tipoOrgao = r'^\d{2}$'
        regex_exercicioReferencia = r'^\d{4}$'
        regex_mesReferencia = r'^\d{2}$'
        regex_dataGeracao = r'^\d{8}$'
        regex_codControleRemessa = r'^\d{1,20}$'
        regex_codseqremessas = r'^\d{1,3}$'

        if not re.match(regex_tipoRegistro, campos[0]):
            erros.append("❌ Tipo de Registro inválido: deve conter 5 dígitos.")
        if not re.match(regex_cnpj, campos[1]):
            erros.append("❌ CNPJ inválido: deve conter 14 dígitos.")
        if not re.match(regex_codOrgao, campos[2]):
            erros.append("❌ Código do Órgão inválido: deve conter 3 dígitos.")
        if not re.match(regex_tipoOrgao, campos[3]):
            erros.append("❌ Tipo de Órgão inválido: deve conter 2 dígitos.")
        if not re.match(regex_exercicioReferencia, campos[4]):
            erros.append("❌ Exercício de Referência inválido: deve conter 4 dígitos.")
        if not re.match(regex_mesReferencia, campos[5]):
            erros.append("❌ Mês de Referência inválido: deve conter 2 dígitos.")
        if not re.match(regex_dataGeracao, campos[6]):
            erros.append("❌ Data de Geração inválida: deve estar no formato YYYYMMDD.")
        if campos[7].strip() and not re.match(regex_codControleRemessa, campos[7]):
            erros.append("❌ Código de Controle da Remessa inválido: deve conter até 20 dígitos.")
        if not re.match(regex_codseqremessas, campos[8]):
            erros.append("❌ Código de Sequência de Remessas inválido: deve conter até 3 dígitos.")

        return erros
def validar_redispi_linha10(campos):
    erros = []
    if len(campos) != 21:
        erros.append("❌ Linha 10 do REDISPI deve conter exatamente 30 campos.")
    else:
            regex_tipoRegistro = r'^\d{2}$'
            regex_codOrgaoResp = r'^\d{3}$'  # Código do órgão responsável (4 dígitos)
            regex_codUnidadeSubResp = r'^\d{5,8}$'  # Código da unidade/subunidade responsável (4 dígitos)
            regex_codUnidadeSubRespEstadual = r'^\d{4}$'  # Código da unidade/subunidade estadual (4 dígitos)
            regex_exercicioLicitacao = r'^\d{4}$'  # Exercício da licitação (4 dígitos)
            regex_nroProcessoLicitatorio = r'^\d{1,16}$'
            regex_codModalidadeDisp = r'^([1-6])$'# Número do processo licitatório (até 7 dígitos)
            regex_tipoCadastradoLicitacao = r'^[1-5]$'  # Tipo de cadastro (1 dígito)
            regex_dscCadastroLicitatorio = r'^[\wÀ-ÿ\s\-\.,!?\'"()\/]{1,200}$'  # Descrição do cadastro (texto livre)
            regex_leiLicitacao = r'^\d{1}$'  # Lei da licitação (4 dígitos)
            regex_dtabertura = r'^\d{8}$'
            regex_naturezaObjeto = r'^[1-7]$'
            regex_objeto = r'^[\wÀ-ÿ\s\-\.,!?\'"()\/]{1,200}$' # Objeto (texto livre)
            regex_regimeExecucaoObras = r'^[1-8]$'  # Regime de execução de obras (texto livre)
            regex_justificativa = r'^[\wÀ-ÿ\s\-\.,!?\'"()\/]{1,200}$' 
            regex_razao = r"^[\wÀ-ÖØ-öø-ÿÇçãÃ\s\-\.,!?\'\"()\/]{1,200}$"
            regex_VlrRercuso = r'^\d{1,8}(,\d{1,2})?$'
            regex_bdi = r'^\d{1,2}(,\d{1,2})?$' 
            regex_link = r'^(https?://)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(/[\w-]*)*\/?$'
            regex_emailContato = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$' 
            
            if not re.match(regex_tipoRegistro, campos[0]):
                nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                exercicioLicitacao = campos[4]
                erros.append(
                    f"❌ 1 - Erro no Tipo de Registro: deve ser 2 dígitos.\n\n"
                    f"🔧 Solução: Verifique o tipo de registro no processo {nroProcessoLicitatorio}/{exercicioLicitacao}, deve conter 2 dígitos. Exemplo: '01'.")
                
            if not re.match(regex_codOrgaoResp, campos[1]):
                nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                exercicioLicitacao = campos[4]
                erros.append(
                    f"❌ 2 - Erro no Código do Órgão Responsável: deve ser 4 dígitos.\n\n"
                    f"🔧 Solução: Verifique o código do órgão responsável no processo {nroProcessoLicitatorio}/{exercicioLicitacao}, deve ser composto por 4 dígitos. Exemplo: '1234'."
                )
                
            if not re.match(regex_codUnidadeSubResp, campos[2]):
                nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                exercicioLicitacao = campos[4]
                erros.append(
                    f"❌ 3 - Erro no Código da Unidade/Subunidade Responsável: deve ser 4 dígitos.\n\n"
                    f"🔧 Solução: Verifique o código da unidade/subunidade responsável do seu processo {nroProcessoLicitatorio}/{exercicioLicitacao}, deve ser composto por 4 dígitos."
                )
            if campos[3].strip() and not re.match(regex_codUnidadeSubRespEstadual, campos[3]):
                nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                exercicioLicitacao = campos[4]
                erros.append(
                    f"❌ 4 - Erro no Código da Unidade/Subunidade Estadual: deve ser 4 dígitos.\n\n"
                    f"🔧 Solução: Verifique o código da unidade/subunidade estadual do seu processo {nroProcessoLicitatorio}/{exercicioLicitacao}, deve ser composto por 4 dígitos."
                )
            if not re.match(regex_exercicioLicitacao, campos[4]):
                erros.append(
                    f"❌ 5 - Erro no Exercício da Licitação: deve ser 4 dígitos.\n\n"
                    f"🔧 Solução: O exercício da licitação deve ter 4 dígitos. Exemplo: '2024'."
                )
                if not re.match(regex_nroProcessoLicitatorio, campos[5]):
                    erros.append(
                        f"❌ 6 - Erro no Número do Processo Licitatório: deve ter até 7 dígitos.\n\n"
                        f"🔧 Solução: O número do processo licitatório deve ter no máximo 7 dígitos. Exemplo: '1234567'."
                    )
# Validação do campo Modalidade de Licitação
            if not re.match(regex_codModalidadeDisp, campos[6].strip()):
                nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                exercicioLicitacao = campos[4]  # Exercício da Licitação
                modalidade = campos[6].strip()  # Modalidade de Licitação
                erros.append(
                    f"❌ 7 - Erro na Modalidade de Licitação {nroProcessoLicitatorio}/{exercicioLicitacao}: O código da modalidade deve ser um número entre 01 e 10.\n\n"
                    f"🔧 Solução: A modalidade de licitação deve ser informada com um código válido entre '01' e '10'.\n\n"
                    f"ℹ️ Exemplos de modalidades válidas:\n"
                    f"01 – Dispensa;\n"
                    f"02 – Inexigibilidade\n"
                    f"03 – Inexigibilidade por credenciamento/chamada pública;\n"
                    f"04 – Dispensa por chamada publica;\n"
                    f"05 – Dispensa para Registro de Preços;\n"
                    f"06 – Inexigibilidade para Registro de Preços.\n"
                )
            else:
                modalidade = campos[6].strip()  # Modalidade de Licitação
                leiLicitacao = campos[8].strip()  # Lei de Licitação
                
    # Verificação específica para a modalidade 09 (Lei 13.303/2016)
                if modalidade == "05" and leiLicitacao != "1":
                    nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                    exercicioLicitacao = campos[4]  # Exercício da Licitação
                    erros.append(
                        f"❌ 7 - Erro na Modalidade de Licitação {nroProcessoLicitatorio}/{exercicioLicitacao}: A modalidade Dispensa para Registro de Preços só pode ser utilizada quando a Lei de Licitação for '1' (Lei 14133/21).\n\n"
                        f"🔧 Solução: Para a modalidade '05', a Lei de Licitação deve ser '1'."
                    )
                if modalidade == "06" and leiLicitacao != "1":
                    nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                    exercicioLicitacao = campos[4]  # Exercício da Licitação
                    erros.append(
                        f"❌ 7 - Erro na Modalidade de Licitação {nroProcessoLicitatorio}/{exercicioLicitacao}: A modalidade Inexigibilidade para Registro de Preços só pode ser utilizada quando a Lei de Licitação for '1' (Lei 14133/21).\n\n"
                        f"🔧 Solução: Para a modalidade '06', a Lei de Licitação deve ser '1'."
                    )
                if not re.match(regex_tipoCadastradoLicitacao, campos[7].strip()):
                    nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                    exercicioLicitacao = campos[4]      # Exercício da Licitação
                    erros.append(
                        f"❌ Erro no Tipo de Cadastro da Licitação ({nroProcessoLicitatorio}/{exercicioLicitacao}): deve ser um número de 1 a 5.\n\n"
                        f"🔧 Solução: Informe um valor entre 1 e 5 para o Tipo de Cadastro da Licitação.\n"
                        f"ℹ️ Tipos de Cadastro da Licitação:\n"
                        f"1 – Cadastro inicial;\n"
                        f"2 – Retificação;\n"
                        f"3 – Anulação;\n"
                        f"4 – Revogação;\n"
                        f"5 – Modificação do Edital."
                    )
                if campos[7].strip() == "1":
                    if campos[8].strip():  # Se campo 6 for "1", campo 7 deve estar vazio
                        erros.append(
                                    "❌ Erro: Campo 7 deve estar vazio quando o Tipo de Cadastro da Licitação (campo 6) for '1'."
                    )
                    elif campos[7].strip() in ["2", "3", "4", "5"]:
    # Se campo 6 for "2", "3", "4" ou "5", campo 7 deve ter exatamente 1 dígito
                        if not re.match(regex_dscCadastroLicitatorio, campos[7].strip()):
                            erros.append(
                                    "❌ Erro: Campo 7 deve conter exatamente 1 dígito quando o Tipo de Cadastro da Licitação (campo 6) for '2', '3', '4' ou '5'."
                    )
                if not re.match(regex_leiLicitacao, campos[9].strip()):
                    erros.append(
                        f"❌ 9 - Erro no campo Lei da Licitação: deve ser um único dígito.\n\n"
                        f"🔧 Solução: O campo Lei da Licitação deve ser preenchido com um único dígito. Exemplo válido: '1' ou '2'."
                    )
                elif campos[9].strip() not in ["1", "2"]:
                        erros.append(
                    f"❌ 9 - Erro no campo Lei da Licitação: apenas os códigos '1' e '2' são aceitos.\n\n"
                    f"🔧 Solução: Informe os valores corretos para a Lei da Licitação:\n"
                    f"    - ℹ️ Lei 14133/21 - código '1'.\n"
                    f"    - ℹ️ Lei 8666/93 - código '2'."
                    )
                if not re.match(regex_dtabertura, campos[10]):
                    erros.append(
                        f"❌ 10 - Erro na Data de abertura do Termo de  Dispensa ou Inexibilidade Número do Edital: deve ter até DD/MM/AAAA dígitos.\n\n"
                        f"🔧 Solução: Observe no seu processo Licitatório qual é a data de abertura.'."
                    )# Validação da natureza do objeto com mensagens de erro personalizadas
                    
                natureza_objeto = ""
                codModalidadeDisp = ""
                nroProcessoLicitatorio = ""
                exercicioLicitacao = ""
                lei_licitacao = ""
                
                if not re.match(regex_naturezaObjeto, campos[11]):
                    erros.append(
                    f"❌ 11 - Erro na Natureza do Objeto: valor inválido.\n\n"
                    f"🔧 Solução: O campo 'naturezaObjeto' deve conter um dos seguintes valores:\n"
                    f"    - 1 – Obras e/ou Serviços de Engenharia\n"
                    f"    - 2 – Compras e outros serviços\n"
                    f"    - 3 – Locação de imóveis\n"
                    f"    - 6 – Alienação de bens\n"
                    f"    - 7 – Compras para obras e/ou compras para serviços de engenharia\n"
                    f"Exemplo válido: '1 – Obras e/ou Serviços de Engenharia'."
                    )
# Validação adicional para a natureza '6 – Alienação de bens'
                elif natureza_objeto == "6" and codModalidadeDisp == "1":
                        erros.append(
                            f"❌ 11 - Erro no Regime de Execução de Obras PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"Não é permitido informar '5 – Execução Direta' quando a 'Natureza do Objeto' for '1 – Obras e/ou Serviços de Engenharia'.\n\n"
                            f"🔧 Solução: Verifique se o regime de execução está corretamente preenchido de acordo com a Natureza do Objeto."
                f"🔧 Solução: Altere o tipo de processo para '1 – Dispensa' ou corrija a natureza do objeto."
                    )
                
                if not re.match(regex_objeto, campos[12].strip()):
                        erros.append(
                            f"❌ 12 - Erro no Objeto: deve ser uma descrição válida com até 200 caracteres.\n\n"
                            f"🔧 Solução: O objeto deve conter apenas letras, números, espaços, hífens e acentuação, com no máximo 200 caracteres.\n"
                            f"   Exemplo: 'Construção de escola' ou 'Aquisição de materiais escolares'."
                    )
                natureza_objeto = ""
                codModalidadeDisp = ""
                nroProcessoLicitatorio = ""
                exercicioLicitacao = ""
                lei_licitacao = ""

# Extração dos campos
                nroProcessoLicitatorio = campos[5].strip()  # Número do Processo Licitatório
                exercicioLicitacao = campos[4].strip()  # Exercício da Licitação
                regime_execucao = campos[13].strip() if campos[13].strip() else ""  # Regime de Execução de Obras
                natureza_objeto = campos[11].strip() if campos[11].strip() else ""  # Natureza do Objeto
                codModalidadeDisp = campos[6].strip()  # Código da Modalidade de Licitação
                lei_licitacao = campos[9].strip()  # Lei da Licitação

# Se a natureza do objeto for diferente de "1" ou "7", o campo "Regime de Execução de Obras" deve estar em branco
                if natureza_objeto not in ["1", "7"]:
                    if regime_execucao:  # Se o campo 'Regime de Execução de Obras' não estiver vazio
                        erros.append(
                            f"❌ 13 - Erro no Regime de Execução de Obras PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"O campo 'Regime de Execução de Obras' não deve ser preenchido quando a 'Natureza do Objeto' não for '1 – Obras e/ou Serviços de Engenharia' ou '7 – Compras para obras e/ou compras para serviços de engenharia'.\n\n"
                            f"🔧 Solução: Remova o valor do campo 'Regime de Execução de Obras'."
                )
                else:
    # Se a natureza do objeto for "1" ou "7", a validação pode ser feita normalmente
                    if regime_execucao and not re.match(regex_regimeExecucaoObras, regime_execucao):  # Se o campo 'Regime de Execução de Obras' não corresponder ao regex
                        erros.append(
                            f"❌ 13 - Erro no Regime de Execução de Obras PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"O campo 'Regime de Execução de Obras' possui um valor inválido.\n\n"
                            f"🔧 Solução: Verifique se o valor do Regime de Execução de Obras está correto."
                )
    # Se a natureza do objeto for "1", não pode ser informado "5 – Execução Direta"
                    elif natureza_objeto == "1" and regime_execucao == "5":
                        erros.append(
                            f"❌ 13 - Erro no Regime de Execução de Obras PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"Não é permitido informar '5 – Execução Direta' quando a 'Natureza do Objeto' for '1 – Obras e/ou Serviços de Engenharia'.\n\n"
                            f"🔧 Solução: Verifique se o regime de execução está corretamente preenchido de acordo com a Natureza do Objeto."
                )
    # Se a natureza do objeto for "7", deve ser informado o regime de execução de acordo com a mão de obra
                    elif natureza_objeto == "7":
                        if regime_execucao != "5":  # Caso a mão de obra seja indireta
                            erros.append(
                                f"❌ 13 - Erro no Regime de Execução de Obras PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                                f"Quando a natureza do objeto for '7 – Compras para obras e/ou compras para serviços de engenharia' e a mão de obra for indireta, deve ser informado o regime de execução da mão de obra contratada.\n\n"
                                f"🔧 Solução: Verifique o regime de execução informado para a mão de obra."
                )                
# Validações para os regimes "6" e "7"
                if regime_execucao in ["6", "7"]:
                    if codModalidadeDisp != "08" and lei_licitacao != "1":
                        erros.append(
                            f"❌ 13 - Erro no Regime de Execução de Obras PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"O regime '{regime_execucao}' pode ser informado somente quando a 'Modalidade de Licitação' for '08 – Regime Diferenciado de Contratações Públicas – RDC' ou a 'Lei da Licitação' for '1 – Lei 14.133/2021'.\n\n"
                            f"🔧 Solução: Verifique os campos 'Modalidade de Licitação' e 'Lei da Licitação'."
                )
# Validação para o regime "8"
                if regime_execucao == "8" and lei_licitacao != "1":
                    erros.append(
                        f"❌ 13 - Erro no Regime de Execução de Obras PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                        f"O regime '8 – Fornecimento e prestação de serviço associado' pode ser informado somente quando a 'Lei da Licitação' for '1 – Lei 14.133/2021'.\n\n"
                        f"🔧 Solução: Verifique o campo 'Lei da Licitação'."
                )
                if not re.match(regex_justificativa, campos[14].strip()):
                        erros.append(
                            f"❌ 14 - Erro na Justificativa : deve ser uma descrição válida com até 200 caracteres.\n\n"
                            f"🔧 Solução: A justificativa da razão pelo vencimento do processo pelo forneceod deve conter apenas letras, números espaços, hífens e acentuação, com no máximo 200 caracteres.\n"
                            f"   Exemplo: 'Construção de escola' ou 'Aquisição de materiais escolares'."
                    )
                if not re.match(regex_razao, campos[15].strip()):
                        erros.append(
                            f"❌ 15 - Erro na Razão: deve ser uma descrição válida com até 200 caracteres.\n\n"
                            f"🔧 Solução: A razão pelo vencimento do processo pelo fornecedor  deve conter apenas letras, números, espaços, hífens e acentuação, com no máximo 200 caracteres.\n"
                            f"   Exemplo: 'Construção de escola' ou 'Aquisição de materiais escolares'."
                    )
                if not re.match(regex_VlrRercuso, campos[16]):
                        erros.append(
                        f"❌ 16 - Erro no Número do Processo Licitatório: deve ter até 7 dígitos.\n\n"
                        f"🔧 Solução: O número do processo licitatório deve ter no máximo 7 dígitos. Exemplo: '1234567'."
                    )
                naturezaObjeto = campos[11].strip()  # Natureza do Objeto
                nroProcessoLicitatorio = campos[5].strip()  # Número do Processo Licitatório
                exercicioLicitacao = campos[4].strip()  # Exercício da Licitação
                bdi = campos[17].strip()  # BDI
# Verificar se a Natureza do Objeto é "1" ou "7"
                if naturezaObjeto in ["1", "7"]:
    # Se o campo BDI estiver vazio, gerar erro
                    if not bdi:
                        erros.append(
                            f"❌ 17 - Erro no BDI PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"O campo 'BDI' é obrigatório quando a 'Natureza do Objeto' for '1 – Obras e/ou Serviços de Engenharia' ou '7 – Compras para obras e/ou compras para serviços de engenharia'.\n\n"
                            f"🔧 Solução: Preencha o campo 'BDI' com 1 ou 2 dígitos, podendo conter até 2 casas decimais após a vírgula. Exemplo: '15' ou '25,98'."
                )
    # Validar o formato do campo BDI
                    elif not re.match(regex_bdi, bdi):
                        erros.append(
                            f"❌ 17 - Erro no BDI PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"O campo 'BDI' deve ser composto por 1 ou 2 dígitos, podendo conter até 2 casas decimais após a vírgula.\n\n"
                            f"🔧 Solução: Preencha o BDI corretamente. Exemplo: '15' ou '25,98'."
                )
                else:
    # Caso a Natureza do Objeto não seja "1" ou "7", o campo BDI não deve ser preenchido
                    if bdi:
                        erros.append(
                            f"❌ 17 - Erro no BDI PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"O campo 'BDI' só deve ser preenchido quando a 'Natureza do Objeto' for '1 – Obras e/ou Serviços de Engenharia' ou '7 – Compras para obras e/ou compras para serviços de engenharia'.\n\n"
                            f"🔧 Solução: Deixe o campo 'BDI' em branco, pois a Natureza do Objeto não é '1' nem '7'."
                )
                if not re.match(regex_link, campos[18]):
                    erros.append(
                        f"❌ 18 - Erro no Link: deve ser uma URL válida.\n\n"
                        f"🔧 Solução: O link deve ser uma URL válida, como 'http://example.com'."
                )
                if not re.match(regex_emailContato, campos[19]):
                    erros.append(
                        f"❌ 19 - Erro no Email de Contato: deve ser um email válido.\n\n"
                        f"🔧 Solução: O email de contato deve ser válido. Exemplo: 'contato@exemplo.com'."
                )
    return erros
def validar_ralic_linha10(campos):
    erros = []
    if len(campos) != 30:
        erros.append("❌ Linha 10 do RALIC deve conter exatamente 15 campos.")
    else:
            regex_tipoRegistro = r'^\d{2}$'
            regex_codOrgaoResp = r'^\d{3}$'  # Código do órgão responsável (4 dígitos)
            regex_codUnidadeSubResp = r'^\d{5,8}$'  # Código da unidade/subunidade responsável (4 dígitos)
            regex_codUnidadeSubRespEstadual = r'^\d{4}$'  # Código da unidade/subunidade estadual (4 dígitos)
            regex_exercicioLicitacao = r'^\d{4}$'  # Exercício da licitação (4 dígitos)
            regex_nroProcessoLicitatorio = r'^\d{1,16}$'  # Número do processo licitatório (até 7 dígitos)
            regex_tipoCadastradoLicitacao = r'^[1-5]$'  # Tipo de cadastro (1 dígito)
            regex_dscCadastroLicitatorio = r'^[A-Za-z0-9\s\-]+$'  # Descrição do cadastro (texto livre)
            regex_leiLicitacao = r'^\d{1}$'  # Lei da licitação (4 dígitos)
            regex_codModalidadeLicitacao = r'^(0[1-9]|10)$'   # Código da modalidade de licitação (2 dígitos)
            regex_naturezaProcedimento = r'^[1-3]$'  # Natureza do procedimento (1 dígito)
            regex_nroEdital = r'^\d{1,10}$'  # Número do edital (até 10 dígitos)
            regex_exercicioEdital = r'^\d{4}$'  # Exercício do edital (4 dígitos)
            regex_dtPublicacaoEdital = r'^\d{8}$'  # Data de publicação do edital (formato YYYYMMDD)
            regex_dtAberturaEnvelopes = r'^\d{8}$'  # Data de abertura dos envelopes (formato YYYYMMDD)
            regex_link = r'^(https?://)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(/[\w-]*)*\/?$'  # URL válida
            regex_criterioJulgamento = r'^[1-8]$' # Critério de julgamento (texto livre)
            regex_modoDisputa = r'^[1-3]$'  # Modo de disputa (texto livre)
            regex_naturezaObjeto = r'^[1-7]$'   # Natureza do objeto (texto livre)
            regex_objeto = r'^[\wÀ-ÿ\s\-\.,]{1,200}$'  # Objeto (texto livre)
            regex_regimeExecucaoObras = r'^[1-8]$'  # Regime de execução de obras (texto livre)
            regex_tipoOrcamento = r'^[1-2]$'  # Tipo de orçamento (texto livre)
            regex_vlContratacao = r'^\d+(\,\d{1,14})?$'  # Valor de contratação (número com até 2 casas decimais)
            regex_bdi = r'^\d{1,2}(,\d{1,2})?$'  # BDI (1 ou 2 dígitos)
            regex_mesExercicioRefOrc = r'^\d{6}$'  # Mês de exercício de referência orçamentária (2 dígitos)
            regex_origemRecurso = r'^[1-6,9]$'  # Origem do recurso (texto livre)
            regex_dscOrigemRecurso = r'^[A-Za-z0-9\s]+$' # Descrição da origem do recurso (texto livre)
            regex_qtdLotes = r'^\d{1,6}$'  # Quantidade de lotes (número inteiro)
            regex_emailContato = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$' 
        

            if not re.match(regex_tipoRegistro, campos[0]):
                nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                exercicioLicitacao = campos[4]
                erros.append(
                    f"❌ 1 - Erro no Tipo de Registro: deve ser 2 dígitos.\n\n"
                    f"🔧 Solução: Verifique o tipo de registro no processo {nroProcessoLicitatorio}/{exercicioLicitacao}, deve conter 2 dígitos. Exemplo: '01'.")
                
            if not re.match(regex_codOrgaoResp, campos[1]):
                nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                exercicioLicitacao = campos[4]
                erros.append(
                    f"❌ 2 - Erro no Código do Órgão Responsável: deve ser 4 dígitos.\n\n"
                    f"🔧 Solução: Verifique o código do órgão responsável no processo {nroProcessoLicitatorio}/{exercicioLicitacao}, deve ser composto por 4 dígitos. Exemplo: '1234'."
                )
                
            if not re.match(regex_codUnidadeSubResp, campos[2]):
                nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                exercicioLicitacao = campos[4]
                erros.append(
                    f"❌ 3 - Erro no Código da Unidade/Subunidade Responsável: deve ser 4 dígitos.\n\n"
                    f"🔧 Solução: Verifique o código da unidade/subunidade responsável do seu processo {nroProcessoLicitatorio}/{exercicioLicitacao}, deve ser composto por 4 dígitos."
                )
            if campos[3].strip() and not re.match(regex_codUnidadeSubRespEstadual, campos[3]):
                nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                exercicioLicitacao = campos[4]
                erros.append(
                    f"❌ 4 - Erro no Código da Unidade/Subunidade Estadual: deve ser 4 dígitos.\n\n"
                    f"🔧 Solução: Verifique o código da unidade/subunidade estadual do seu processo {nroProcessoLicitatorio}/{exercicioLicitacao}, deve ser composto por 4 dígitos."
                )
            if not re.match(regex_exercicioLicitacao, campos[4]):
                erros.append(
                    f"❌ 5 - Erro no Exercício da Licitação: deve ser 4 dígitos.\n\n"
                    f"🔧 Solução: O exercício da licitação deve ter 4 dígitos. Exemplo: '2024'."
                )
            if not re.match(regex_nroProcessoLicitatorio, campos[5]):
                erros.append(
                    f"❌ 6 - Erro no Número do Processo Licitatório: deve ter até 7 dígitos.\n\n"
                    f"🔧 Solução: O número do processo licitatório deve ter no máximo 7 dígitos. Exemplo: '1234567'."
                )

# Validação do campo 6 (Tipo de Cadastro da Licitação)
            if not re.match(regex_tipoCadastradoLicitacao, campos[6].strip()):
                nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                exercicioLicitacao = campos[4]      # Exercício da Licitação
                erros.append(
                    f"❌ Erro no Tipo de Cadastro da Licitação ({nroProcessoLicitatorio}/{exercicioLicitacao}): deve ser um número de 1 a 5.\n\n"
                    f"🔧 Solução: Informe um valor entre 1 e 5 para o Tipo de Cadastro da Licitação.\n"
                    f"ℹ️ Tipos de Cadastro da Licitação:\n"
                    f"1 – Cadastro inicial;\n"
                    f"2 – Retificação;\n"
                    f"3 – Anulação;\n"
                    f"4 – Revogação;\n"
                    f"5 – Modificação do Edital."
                )
# Validação do campo 7
            if campos[6].strip() == "1":
                if campos[7].strip():  # Se campo 6 for "1", campo 7 deve estar vazio
                    erros.append(
                    "❌ Erro: Campo 7 deve estar vazio quando o Tipo de Cadastro da Licitação (campo 6) for '1'."
                )
            elif campos[6].strip() in ["2", "3", "4", "5"]:
    # Se campo 6 for "2", "3", "4" ou "5", campo 7 deve ter exatamente 1 dígito
                if not re.match(regex_dscCadastroLicitatorio, campos[7].strip()):
                    erros.append(
                    "❌ Erro: Campo 7 deve conter exatamente 1 dígito quando o Tipo de Cadastro da Licitação (campo 6) for '2', '3', '4' ou '5'."
                )

            if not re.match(regex_leiLicitacao, campos[8].strip()):
                erros.append(
                    f"❌ 8 - Erro no campo Lei da Licitação: deve ser um único dígito.\n\n"
                    f"🔧 Solução: O campo Lei da Licitação deve ser preenchido com um único dígito. Exemplo válido: '1' ou '2'."
                )
            elif campos[8].strip() not in ["1", "2"]:
                erros.append(
                    f"❌ 8 - Erro no campo Lei da Licitação: apenas os códigos '1' e '2' são aceitos.\n\n"
                    f"🔧 Solução: Informe os valores corretos para a Lei da Licitação:\n"
                    f"    - ℹ️ Lei 14133/21 - código '1'.\n"
                    f"    - ℹ️ Lei 8666/93 - código '2'."
                )
            
# Lista de modalidades permitidas apenas para Lei 8666/93
            modalidades_lei_8666 = ["01", "02", "08"]  # Convite, Tomada de Preços, RDC

# Validação do campo Modalidade de Licitação
            if not re.match(regex_codModalidadeLicitacao, campos[9].strip()):
                nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                exercicioLicitacao = campos[4]  # Exercício da Licitação
                modalidade = campos[9].strip()  # Modalidade de Licitação
                erros.append(
                    f"❌ 11 - Erro na Modalidade de Licitação {nroProcessoLicitatorio}/{exercicioLicitacao}: O código da modalidade deve ser um número entre 01 e 10.\n\n"
                    f"🔧 Solução: A modalidade de licitação deve ser informada com um código válido entre '01' e '10'.\n\n"
                    f"ℹ️ Exemplos de modalidades válidas:\n"
                    f"01 – Convite;\n"
                    f"02 – Tomada de Preços;\n"
                    f"03 – Concorrência;\n"
                    f"04 – Concurso;\n"
                    f"05 – Pregão presencial;\n"
                    f"06 – Pregão eletrônico;\n"
                    f"07 – Leilão;\n"
                    f"08 – Regime Diferenciado de Contratações Públicas – RDC;\n"
                    f"09 – Procedimento Licitatório (Lei 13.303/2016);\n"
                    f"10 – Diálogo competitivo."
                )
            else:
                modalidade = campos[9].strip()  # Modalidade de Licitação
                leiLicitacao = campos[8].strip()  # Lei de Licitação

    # Verificação de compatibilidade das modalidades com a Lei 8666/93
                if modalidade in modalidades_lei_8666 and leiLicitacao != "2":
                    nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                    exercicioLicitacao = campos[4]  # Exercício da Licitação
                    erros.append(
                        f"❌ 11 - Erro na Modalidade de Licitação {nroProcessoLicitatorio}/{exercicioLicitacao}: A modalidade '{modalidade}' só pode ser utilizada quando a Lei de Licitação for '2' (Lei 8666/93).\n\n"
                        f"🔧 Solução: Se a modalidade for '01 – Convite', '02 – Tomada de Preços' ou '08 – Regime Diferenciado de Contratações Públicas – RDC', a Lei de Licitação deve ser '2'."
                    )

    # Verificação específica para a modalidade 09 (Lei 13.303/2016)
                if modalidade == "09" and leiLicitacao != "1":
                    nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                    exercicioLicitacao = campos[4]  # Exercício da Licitação
                    erros.append(
                        f"❌ 11 - Erro na Modalidade de Licitação {nroProcessoLicitatorio}/{exercicioLicitacao}: A modalidade '09 – Procedimento Licitatório (Lei 13.303/2016)' só pode ser utilizada quando a Lei de Licitação for '1' (Lei 14133/21).\n\n"
                        f"🔧 Solução: Para a modalidade '09', a Lei de Licitação deve ser '1'."
                    )
                if modalidade == "10" and leiLicitacao != "1":
                    nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                    exercicioLicitacao = campos[4]  # Exercício da Licitação
                    erros.append(
                        f"❌ 11 - Erro na Modalidade de Licitação {nroProcessoLicitatorio}/{exercicioLicitacao}: A modalidade '10 – Diálogo competitivo' só pode ser utilizada quando a Lei de Licitação for '1' (Lei 14133/21).\n\n"
                        f"🔧 Solução: Para a modalidade '10', a Lei de Licitação deve ser '1'."
                    )
                if not re.match(regex_naturezaProcedimento, campos[10]):
                    nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                    exercicioLicitacao = campos[4]  # Exercício da Licitação
                    natureza_procedimento = campos[10]  # Natureza do Procedimento
                    erros.append(
                        f"❌ 11 - Erro na Natureza do Procedimento {nroProcessoLicitatorio}/{exercicioLicitacao}: O valor '{natureza_procedimento}' é inválido. A natureza do procedimento deve ser um número entre 1 e 3.\n\n"
                        f"🔧 Solução: A natureza do procedimento deve ser um número válido. Exemplos:\n\n"
                        f"1 – Normal;\n"
                        f"2 – Registro de Preços (Somente procedimento realizado pelo próprio órgão. A adesão à ata de outros órgãos não deve ser informada nesse Módulo);\n"
                        f"3 – Credenciamento/Chamada Pública.\n\n"
                        f"🔧 Verifique se o número informado está correto e corresponde a um dos valores permitidos."
                    )
                if not re.match(regex_nroEdital, campos[11]):
                    erros.append(
                        f"❌ 12 - Erro no Número do Edital: deve ter até 10 dígitos.\n\n"
                        f"🔧 Solução: O número do edital deve ter no máximo 10 dígitos. Exemplo: '1234567890'."
                    )
                if not re.match(regex_exercicioEdital, campos[12]):
                    erros.append(
                        f"❌ 13 - Erro no Exercício do Edital: deve ser 4 dígitos.\n\n"
                        f"🔧 Solução: O exercício do edital deve ter 4 dígitos. Exemplo: '2024'."
                    )
                if not re.match(regex_dtPublicacaoEdital, campos[13]):
                    erros.append(
                        f"❌ 14 - Erro na Data de Publicação do Edital: deve ser no formato YYYYMMDD.\n\n"
                        f"🔧 Solução: A data de publicação do edital deve seguir o formato YYYYMMDD. Exemplo: '20231201'."
                    )
                if not re.match(regex_dtAberturaEnvelopes, campos[14]):
                    erros.append(
                        f"❌ 15 - Erro na Data de Abertura dos Envelopes: deve ser no formato YYYYMMDD.\n\n"
                        f"🔧 Solução: A data de abertura dos envelopes deve seguir o formato YYYYMMDD. Exemplo: '20231205'."
                )
                if not re.match(regex_link, campos[15]):
                    erros.append(
                        f"❌ 16 - Erro no Link: deve ser uma URL válida.\n\n"
                        f"🔧 Solução: O link deve ser uma URL válida, como 'http://example.com'."
                )
                
                criterio_julgamento = ""
                nroProcessoLicitatorio = ""
                exercicioLicitacao = ""
                cod_modalidade_licitacao = ""
                lei_licitacao = ""
# Extração dos campos
                if campos[16].strip():
                    criterio_julgamento = campos[16].strip()
                    nroProcessoLicitatorio = campos[5]
                    exercicioLicitacao = campos[4]
                    cod_modalidade_licitacao = campos[9].strip()
                    lei_licitacao = campos[8].strip()

# Validação específica para modalidade "04"
                if cod_modalidade_licitacao == "04":  # Quando a modalidade for "04 – Concurso"
                    if criterio_julgamento:  # Critério de julgamento deve estar vazio
                        erros.append(
                            f"❌ 18 - Erro no Critério de Julgamento PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"Quando a modalidade for '04 – Concurso', o campo Critério de Julgamento deve estar vazio.\n\n"
                            f"🔧 Solução: Remova o valor informado no campo Critério de Julgamento."
                )
# Validações para outras modalidades
                else:
                    if not criterio_julgamento:  # Campo não pode estar vazio
                        erros.append(
                            f"❌ 17 - Erro no Critério de Julgamento PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"O critério de julgamento é obrigatório para a modalidade '{cod_modalidade_licitacao}'.\n\n"
                            f"🔧 Solução: Informe um critério de julgamento válido entre 1 e 8."
                )
                    elif criterio_julgamento not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                        erros.append(
                            f"❌ 17 - Erro no Critério de Julgamento PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"O critério de julgamento informado é inválido.\n\n"
                            f"🔧 Solução: O critério de julgamento deve ser um número entre 1 e 8."
                            f"1 – Menor Preço;\n"
                            f"2 – Melhor Técnica;\n"
                            f"3 – Técnica e Preço;\n"
                            f"4 – Maior Lance ou Oferta;\n"
                            f"5 – Maior Oferta de Preço (Somente se a modalidade for '08 – RDC');\n"
                            f"6 – Maior Retorno Econômico (Somente se a modalidade for '08 – RDC' ou a Lei for '1 – Lei 14.133/2021');\n"
                            f"7 – Maior Desconto (Somente se a modalidade for '06 – Pregão eletrônico' ou '08 – RDC', ou a Lei for '1 – Lei 14.133/2021');\n"
                            f"8 – Melhor Técnica ou conteúdo artístico (Somente se a Lei for '1 – Lei 14.133/2021')."
                )
# Validações adicionais para critérios específicos
                    if criterio_julgamento == "5" and cod_modalidade_licitacao != "08":
                        erros.append(
                            f"❌ 17 - Erro no Critério de Julgamento PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: O critério 'Maior Oferta de Preço' (5) só pode ser informado quando a modalidade for '08 – RDC'.\n\n"
                            f"🔧 Solução: Verifique o código da modalidade informado."
                )
                    elif criterio_julgamento == "6" and cod_modalidade_licitacao != "08" and lei_licitacao != "1":
                        erros.append(
                            f"❌ 17 - Erro no Critério de Julgamento PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: O critério 'Maior Retorno Econômico' (6) só é permitido para a modalidade '08 – RDC' ou com a Lei '1 – Lei 14.133/2021'.\n\n"
                            f"🔧 Solução: Verifique o código da modalidade ou a Lei de Licitação."
                )
                    elif criterio_julgamento == "7" and (lei_licitacao != "1" and cod_modalidade_licitacao not in ["06", "08"]):
                        erros.append(
                            f"❌ 17 - Erro no Critério de Julgamento PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: O critério 'Maior Desconto' (7) só é permitido com a modalidade '06 – Pregão eletrônico' ou '08 – RDC', ou com a Lei '1 – Lei 14.133/2021'.\n\n"
                            f"🔧 Solução: Verifique o código da modalidade ou a Lei de Licitação."
                )
                    elif criterio_julgamento == "8" and lei_licitacao != "1":
                        erros.append(
                            f"❌ 17 - Erro no Critério de Julgamento PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: O critério 'Melhor Técnica ou conteúdo artístico' (8) só pode ser usado com a Lei '1 – Lei 14.133/2021'.\n\n"
                            f"🔧 Solução: Verifique a Lei de Licitação."
                )
# Inicialização das variáveis
                    modo_disputa = ""
                    nroProcessoLicitatorio = ""
                    exercicioLicitacao = ""
                    cod_modalidade_licitacao = ""
                    lei_licitacao = ""
# Extração dos campos
                    nroProcessoLicitatorio = campos[5].strip()  # Número do Processo Licitatório
                    exercicioLicitacao = campos[4].strip()  # Exercício da Licitação
                    cod_modalidade_licitacao = campos[9].strip()  # Código da Modalidade de Licitação
                    lei_licitacao = campos[8].strip()  # Lei da Licitação
                    modo_disputa = campos[17].strip() if campos[17].strip() else ""  # Modo de Disputa
# Verificação do campo "Modo de Disputa"
                    if lei_licitacao == "1":
    # A Lei de Licitação é "1", então o campo "Modo de Disputa" deve ser preenchido
                        if not modo_disputa:
                            erros.append(
                                f"❌ 18 - Erro no Modo de Disputa PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                                f"Este campo deve ser preenchido quando o campo 'Lei de Licitação' for igual a '1 – Lei 14.133/2021'.\n\n"
                                f"🔧 Solução: Verifique se o campo 'Modo de Disputa' está preenchido corretamente quando a Lei de Licitação for '1'."
                )
                        elif modo_disputa not in ["1", "2", "3"]:
        # Verificar se o modo de disputa é válido (1, 2 ou 3)
                            erros.append(
                                f"❌ 18 - Erro no Modo de Disputa PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                                f"O modo de disputa deve ser um número entre 1 e 3.\n\n"
                                f"🔧 Solução: O modo de disputa deve ser um dos seguintes códigos válidos:\n"
                                f"1 – Aberto;\n"
                                f"2 – Fechado;\n"
                                f"3 – Conjunto."
                )
                    elif lei_licitacao == "2":
    # A Lei de Licitação é "2", então o campo "Modo de Disputa" não deve ser preenchido
                        if modo_disputa:
                            erros.append(
                                f"❌ 18 - Erro no Modo de Disputa PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                                f"Este campo não deve ser preenchido quando o campo 'Lei de Licitação' for igual a '2 – Lei 8.666/1993 e outras'.\n\n"
                                f"🔧 Solução: Verifique se a Lei de Licitação (campo leiLicitacao) está corretamente preenchida para este campo."
                )
                    else:
    # Se a Lei de Licitação for diferente de "1" e "2", o campo pode ser validado como necessário
                        if modo_disputa not in ["1", "2", "3"]:
                            erros.append(
                                f"❌ 18 - Erro no Modo de Disputa PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                                f"O modo de disputa deve ser um número entre 1 e 3.\n\n"
                                f"🔧 Solução: O modo de disputa deve ser um dos seguintes códigos válidos:\n"
                                f"1 – Aberto;\n"
                                f"2 – Fechado;\n"
                                f"3 – Conjunto."
                )
                    natureza_objeto = ""
                    modo_disputa = ""
                    cod_modalidade_licitacao = ""
                    nroProcessoLicitatorio = ""
                    exercicioLicitacao = ""
                    lei_licitacao = ""
                    nroProcessoLicitatorio = campos[5].strip()  # Número do Processo Licitatório
                    exercicioLicitacao = campos[4].strip()  # Exercício da Licitação
                    cod_modalidade_licitacao = campos[9].strip()  # Código da Modalidade de Licitação
                    lei_licitacao = campos[8].strip()  # Lei da Licitação
                    natureza_objeto = campos[18].strip() # Natureza do Objeto

# Se a modalidade for "04 – Concurso", a Natureza do Objeto deve estar vazia
                    if cod_modalidade_licitacao == "04":  # Quando a modalidade for "04 – Concurso"
                        if natureza_objeto:() # Se o campo 'Natureza do Objeto' estiver preenchido
                        erros.append(
                                f"❌ 19 - Erro na Natureza do Objeto PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                                f"Quando a modalidade for '04 – Concurso', o campo 'Natureza do Objeto' não deve ser preenchido.\n\n"
                                f"🔧 Solução: Remova o valor informado no campo 'Natureza do Objeto'."
                            )
                    else:
    # Se a modalidade não for '04 – Concurso', valida o valor da 'Natureza do Objeto'
                        if natureza_objeto not in ["1", "2", "3", "4", "5", "6", "7"]:
                            erros.append(
                                f"❌ 19 - Erro na Natureza do Objeto PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                                f"A natureza do objeto deve ser um número entre 1 e 7.\n\n"
                                f"🔧 Solução: A natureza do objeto deve ser um dos seguintes códigos válidos:\n"
                                f"1 – Obras e/ou Serviços de Engenharia;\n"
                                f"2 – Compras e outros serviços;\n"
                                f"3 – Locação de Imóveis;\n"
                                f"4 – Concessão;\n"
                                f"5 – Permissão;\n"
                                f"6 – Alienação de bens;\n"
                                f"7 – Compras para obras e/ou compras para serviços de engenharia."
                )
                        if not re.match(regex_objeto, campos[19].strip()):
                            erros.append(
                                f"❌ 20 - Erro no Objeto: deve ser uma descrição válida com até 200 caracteres.\n\n"
                                f"🔧 Solução: O objeto deve conter apenas letras, números, espaços, hífens e acentuação, com no máximo 200 caracteres.\n"
                                f"   Exemplo: 'Construção de escola' ou 'Aquisição de materiais escolares'."
                )
# Inicializando as variáveis
                natureza_objeto = ""
                modo_disputa = ""
                cod_modalidade_licitacao = ""
                nroProcessoLicitatorio = ""
                exercicioLicitacao = ""
                lei_licitacao = ""

# Extração dos campos
                nroProcessoLicitatorio = campos[5].strip()  # Número do Processo Licitatório
                exercicioLicitacao = campos[4].strip()  # Exercício da Licitação
                regime_execucao = campos[20].strip() if campos[20].strip() else ""  # Regime de Execução de Obras
                natureza_objeto = campos[18].strip() if campos[18].strip() else ""  # Natureza do Objeto
                cod_modalidade_licitacao = campos[9].strip()  # Código da Modalidade de Licitação
                lei_licitacao = campos[8].strip()  # Lei da Licitação

# Se a natureza do objeto for diferente de "1" ou "7", o campo "Regime de Execução de Obras" deve estar em branco
                if natureza_objeto not in ["1", "7"]:
                    if regime_execucao:  # Se o campo 'Regime de Execução de Obras' não estiver vazio
                        erros.append(
                            f"❌ 21 - Erro no Regime de Execução de Obras PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"O campo 'Regime de Execução de Obras' não deve ser preenchido quando a 'Natureza do Objeto' não for '1 – Obras e/ou Serviços de Engenharia' ou '7 – Compras para obras e/ou compras para serviços de engenharia'.\n\n"
                            f"🔧 Solução: Remova o valor do campo 'Regime de Execução de Obras'."
                )
                else:
    # Se a natureza do objeto for "1" ou "7", a validação pode ser feita normalmente
                    if regime_execucao and not re.match(regex_regimeExecucaoObras, regime_execucao):  # Se o campo 'Regime de Execução de Obras' não corresponder ao regex
                        erros.append(
                            f"❌ 21 - Erro no Regime de Execução de Obras PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"O campo 'Regime de Execução de Obras' possui um valor inválido.\n\n"
                            f"🔧 Solução: Verifique se o valor do Regime de Execução de Obras está correto."
                )
    # Se a natureza do objeto for "1", não pode ser informado "5 – Execução Direta"
                    elif natureza_objeto == "1" and regime_execucao == "5":
                        erros.append(
                            f"❌ 21 - Erro no Regime de Execução de Obras PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"Não é permitido informar '5 – Execução Direta' quando a 'Natureza do Objeto' for '1 – Obras e/ou Serviços de Engenharia'.\n\n"
                            f"🔧 Solução: Verifique se o regime de execução está corretamente preenchido de acordo com a Natureza do Objeto."
                )
    # Se a natureza do objeto for "7", deve ser informado o regime de execução de acordo com a mão de obra
                    elif natureza_objeto == "7":
                        if regime_execucao != "5":  # Caso a mão de obra seja indireta
                            erros.append(
                                f"❌ 21 - Erro no Regime de Execução de Obras PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                                f"Quando a natureza do objeto for '7 – Compras para obras e/ou compras para serviços de engenharia' e a mão de obra for indireta, deve ser informado o regime de execução da mão de obra contratada.\n\n"
                                f"🔧 Solução: Verifique o regime de execução informado para a mão de obra."
                )                
# Validações para os regimes "6" e "7"
                if regime_execucao in ["6", "7"]:
                    if cod_modalidade_licitacao != "08" and lei_licitacao != "1":
                        erros.append(
                            f"❌ 21 - Erro no Regime de Execução de Obras PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"O regime '{regime_execucao}' pode ser informado somente quando a 'Modalidade de Licitação' for '08 – Regime Diferenciado de Contratações Públicas – RDC' ou a 'Lei da Licitação' for '1 – Lei 14.133/2021'.\n\n"
                            f"🔧 Solução: Verifique os campos 'Modalidade de Licitação' e 'Lei da Licitação'."
                )
# Validação para o regime "8"
                if regime_execucao == "8" and lei_licitacao != "1":
                    erros.append(
                        f"❌ 21 - Erro no Regime de Execução de Obras PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                        f"O regime '8 – Fornecimento e prestação de serviço associado' pode ser informado somente quando a 'Lei da Licitação' for '1 – Lei 14.133/2021'.\n\n"
                        f"🔧 Solução: Verifique o campo 'Lei da Licitação'."
                )
                if not re.match(regex_tipoOrcamento, campos[21].strip()):
                    nroProcessoLicitatorio = campos[5].strip()  # Número do Processo Licitatório
                    exercicioLicitacao = campos[4].strip()  # Exercício da Licitação
                    tipo_orcamento = campos[21].strip()  # Tipo de Orçamento
                    erros.append(
                        f"❌ 22 - Erro no Tipo de Orçamento PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                        f"O campo 'Tipo de Orçamento' deve ser preenchido com '1 – Orçamento Não Sigiloso' ou '2 – Orçamento Sigiloso'.\n\n"
                        f"🔧 Solução: Verifique se o tipo de orçamento está corretamente preenchido conforme as opções: '1' para Orçamento Não Sigiloso ou '2' para Orçamento Sigiloso."
                )
                if campos[21].strip() == "1":
    # O campo Valor de Contratação (campos[22]) passa a ser obrigatório e validado
                    if not campos[22].strip() or not re.match(regex_vlContratacao, campos[22].strip()):
                        nroProcessoLicitatorio = campos[5].strip()  # Número do Processo Licitatório
                        exercicioLicitacao = campos[4].strip()  # Exercício da Licitação
                        erros.append(
                            f"❌ 23 - Erro no Valor de Contratação PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"O campo 'Valor de Contratação' é obrigatório e deve ser um número válido quando o 'Tipo de Orçamento' for '1 – Orçamento Não Sigiloso'.\n\n"
                            f"🔧 Solução: Preencha o valor de contratação com um número válido. Exemplo: '50000.00'."
                )
                naturezaObjeto = campos[18].strip()  # Natureza do Objeto
                nroProcessoLicitatorio = campos[5].strip()  # Número do Processo Licitatório
                exercicioLicitacao = campos[4].strip()  # Exercício da Licitação
                bdi = campos[23].strip()  # BDI
# Verificar se a Natureza do Objeto é "1" ou "7"
                if naturezaObjeto in ["1", "7"]:
    # Se o campo BDI estiver vazio, gerar erro
                    if not bdi:
                        erros.append(
                            f"❌ 24 - Erro no BDI PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"O campo 'BDI' é obrigatório quando a 'Natureza do Objeto' for '1 – Obras e/ou Serviços de Engenharia' ou '7 – Compras para obras e/ou compras para serviços de engenharia'.\n\n"
                            f"🔧 Solução: Preencha o campo 'BDI' com 1 ou 2 dígitos, podendo conter até 2 casas decimais após a vírgula. Exemplo: '15' ou '25,98'."
                )
    # Validar o formato do campo BDI
                    elif not re.match(regex_bdi, bdi):
                        erros.append(
                            f"❌ 24 - Erro no BDI PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"O campo 'BDI' deve ser composto por 1 ou 2 dígitos, podendo conter até 2 casas decimais após a vírgula.\n\n"
                            f"🔧 Solução: Preencha o BDI corretamente. Exemplo: '15' ou '25,98'."
                )
                else:
    # Caso a Natureza do Objeto não seja "1" ou "7", o campo BDI não deve ser preenchido
                    if bdi:
                        erros.append(
                            f"❌ 24 - Erro no BDI PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"O campo 'BDI' só deve ser preenchido quando a 'Natureza do Objeto' for '1 – Obras e/ou Serviços de Engenharia' ou '7 – Compras para obras e/ou compras para serviços de engenharia'.\n\n"
                            f"🔧 Solução: Deixe o campo 'BDI' em branco, pois a Natureza do Objeto não é '1' nem '7'."
                )
# Campos utilizados
                naturezaObjeto = campos[18].strip()  # Natureza do Objeto
                nroProcessoLicitatorio = campos[5].strip()  # Número do Processo Licitatório
                exercicioLicitacao = campos[4].strip()  # Exercício da Licitação
                mesExercicioRefOrc = campos[24].strip()  # Mês de Exercício de Referência Orçamentária
# Verificar se a Natureza do Objeto é "1" ou "7"
                if naturezaObjeto in ["1", "7"]:
    # Verificar se o campo Mês de Exercício de Referência Orçamentária foi preenchido
                        if not mesExercicioRefOrc:
                            erros.append(
                                f"❌ 25 - Erro no Mês de Exercício de Referência Orçamentária PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                                f"O campo é obrigatório quando a 'Natureza do Objeto' for '1 - Obras e/ou Serviços de Engenharia' ou '7 - Compras para obras e/ou compras para serviços de engenharia'.\n\n"
                                f"🔧 Solução: Preencha o campo com o formato correto 'mmaaaa'. Exemplo: '012023'."
                )
    # Validar o formato do campo Mês de Exercício de Referência Orçamentária
                        elif not re.match(regex_mesExercicioRefOrc, mesExercicioRefOrc):
                            erros.append(
                                f"❌ 25 - Erro no Mês de Exercício de Referência Orçamentária PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                                f"O campo deve ter o formato 'mmaaaa' com 2 dígitos para o mês e 4 para o ano.\n\n"
                                f"🔧 Solução: O mês de exercício de referência orçamentária deve ser preenchido corretamente. Exemplo: '012023'."
                )
                else:
    # Caso a Natureza do Objeto não seja "1" ou "7", o campo não deve ser preenchido
                        if mesExercicioRefOrc:
                            erros.append(
                                f"❌ 25 - Erro no Mês de Exercício de Referência Orçamentária PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                                f"O campo não deve ser preenchido quando a 'Natureza do Objeto' não for '1' ou '7'.\n\n"
                                f"🔧 Solução: Deixe o campo vazio, pois a Natureza do Objeto não é '1' nem '7'."
                )
# Validar a Origem do Recurso (campo 25)
                if not re.match(regex_origemRecurso, campos[25]):
                    origemRecurso = campos[25]  # Valor do campo Origem do Recurso
                    nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                    exercicioLicitacao = campos[4]  # Exercício da Licitação
                    erros.append(
                        f"❌ 26 - Erro na Origem do Recurso PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                        f"A origem do recurso deve ser uma descrição válida.\n\n"
                        f"🔧 Solução: A origem do recurso deve ser uma das opções válidas:\n\n"
                        f"1 – Próprio;\n"
                        f"2 – Estadual;\n"
                        f"3 – Federal;\n"
                        f"4 – Próprio e Estadual;\n"
                        f"5 – Próprio e Federal;\n"
                        f"6 – Acordo Vale;\n"
                        f"9 – Outros.\n\n"
                        f"ℹ️ O valor informado para a Origem do Recurso não é válido. Verifique e corrija o valor informado."
                )
# Se a Origem do Recurso for "9" (Outros), a descrição (campo 26) deve ser preenchida e válida
                if campos[25].strip() == "9":
                    if not campos[26].strip():
                        origemRecurso = campos[25]  # Valor do campo Origem do Recurso
                        nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                        exercicioLicitacao = campos[4]  # Exercício da Licitação
        
                        erros.append(
                            f"❌ 27 - Erro na Descrição da Origem do Recurso PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"A descrição da origem do recurso deve ser preenchida quando a origem for '9 – Outros'.\n\n"
                            f"🔧 Solução: A descrição da origem do recurso deve ser válida. Exemplo: 'Fundo Nacional'.\n\n"
                            f"ℹ️ Preenchimento obrigatório quando a origem for '9 – Outros'."
                )
                    elif not re.match(regex_dscOrigemRecurso, campos[26].strip()):
                        origemRecurso = campos[25]  # Valor do campo Origem do Recurso
                        nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                        exercicioLicitacao = campos[4]  # Exercício da Licitação
                        erros.append(
                            f"❌ 27 - Erro na Descrição da Origem do Recurso PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"A descrição da origem do recurso deve ser válida.\n\n"
                            f"🔧 Solução: A descrição da origem do recurso deve ser válida. Exemplo: 'Fundo Nacional'."
                )
# Se a Origem do Recurso NÃO for "9", o campo Descrição da Origem do Recurso não pode ser preenchido
                else:
                    if campos[26].strip():
                        origemRecurso = campos[25]  # Valor do campo Origem do Recurso
                        nroProcessoLicitatorio = campos[5]  # Número do Processo Licitatório
                        exercicioLicitacao = campos[4]  # Exercício da Licitação
                        erros.append(
                            f"❌ 27 - Erro na Descrição da Origem do Recurso PRC {nroProcessoLicitatorio}/{exercicioLicitacao}: "
                            f"A descrição da origem do recurso não deve ser preenchida quando a origem não for '9 – Outros'.\n\n"
                            f"🔧 Solução: Deixe o campo de descrição em branco, pois a origem do recurso não é '9'."
                )
                # Validar a Quantidade de Lotes (campo 27)
                if not re.match(regex_qtdLotes, campos[27]):
                    erros.append(
                        f"❌ 28 - Erro na Quantidade de Lotes: deve ser um número válido.\n\n"
                        f"🔧 Solução: A quantidade de lotes deve ser um número inteiro. Exemplo: '5'."
                )
# Validar o Email de Contato (campo 28)
                if not re.match(regex_emailContato, campos[28]):
                    erros.append(
                        f"❌ 29 - Erro no Email de Contato: deve ser um email válido.\n\n"
                        f"🔧 Solução: O email de contato deve ser válido. Exemplo: 'contato@exemplo.com'."
    )
    return erros

def main():
    # Menu principal com a opção "Jonce", "Gestão de Compras Públicas", "Sistema de Problemas Urbanos"
    sistema = st.sidebar.selectbox("Escolha um Sistema:", ["Analise de Erros"])

    if sistema == "Analise de Erros":
        opcao_erro = st.sidebar.radio("Escolha uma ação:",["Analisador de Mensagens de Erro", "Gerenciar Tipo de Arquivo"])
        if opcao_erro =="Analisador de Mensagens de Erro":
            if 'tipo_arquivo' not in st.session_state:
                st.session_state.tipo_arquivo = "ABERLIC"
            if 'entrada_usuario' not in st.session_state:
                st.session_state.entrada_usuario = ""
            st.write("###Analisador de Mensagens")
            # Seleção do tipo de arquivo
            tipo_arquivo_selecionado = st.selectbox(
                "Tipo do Arquivo", 
                ["ABERLIC", "PESSOA", "CONTRATOS", "RESPLIC", "HABLIC", "HOMOLIC","IDE",], 
                index=["ABERLIC", "PESSOA", "CONTRATOS", "RESPLIC", "HABLIC", "HOMOLIC","IDE",].index(st.session_state.tipo_arquivo) 
                if 'tipo_arquivo' in st.session_state else 0
            )

            # Exibe o campo de texto para o usuário inserir a mensagem de erro
            st.session_state.entrada_usuario = st.text_input("Informe o erro:", st.session_state.entrada_usuario)

            # Adiciona o botão para limpar o campo de erro
            if st.button("Limpar"):
                st.session_state.entrada_usuario = ""  # Limpa o campo de texto de erro

            # Verifica se o tipo de arquivo selecionado é "PESSOA"
            if tipo_arquivo_selecionado == "PESSOA":
                # Mostrar o botão de pesquisa
                pesquisar_button = st.button("Pesquisar")
                if pesquisar_button:
                    # Expressões regulares para buscar os erros
                    match_cadastro = re.search(r'Erro no arquivo PESSOA na linha \d+\..*número de documento (\d+)', st.session_state.entrada_usuario)
                    match_nao_localizado = re.search(r'Erro no arquivo PESSOA na linha (\d+). A pessoa informada no documento (\d+) não foi localizada', st.session_state.entrada_usuario)

                    # Verifica se encontrou o erro no cadastro
                    if match_cadastro:
                        documento = match_cadastro.group(1)  # Extrai o número do documento
                        st.warning(f"O Fornecedor informado pelo documento {documento} já se encontra cadastrado e enviado para o tribunal de contas.")
                    elif match_nao_localizado:
                        linha = match_nao_localizado.group(1)  # Extrai a linha
                        documento = match_nao_localizado.group(2)  # Extrai o número do documento
                        st.warning(f"O Fornecedor informado pelo documento {documento} não foi localizado no cadastro de pessoas do órgão no mês ou em meses anteriores.")
                    else:
                        st.error("Erro não reconhecido. Verifique a mensagem e tente novamente.")


        elif opcao_erro == "Gerenciar Tipo de Arquivo":
            st.write("### Gerenciar Tipo de Arquivo")

            # Selecione o tipo de arquivo
            tipo_arquivo = st.selectbox("Selecione o tipo de arquivo", ["IDE", "RALIC", "REDISPI"])
            st.session_state.tipo_arquivo = tipo_arquivo

            # Upload do arquivo CSV
            uploaded_file = st.file_uploader("Carregue o arquivo CSV", type=["csv"])

            if uploaded_file is not None:
                try:
                    # Ler o arquivo com codificação UTF-8
                    linhas = uploaded_file.read().decode("utf-8", errors="replace").splitlines()
                    st.success(f"Arquivo '{uploaded_file.name}' carregado com sucesso! 🎉")

                    # Seleção do tipo de validação
                    resultados = []
                    for i, linha in enumerate(linhas, start=1):
                        if linha.strip():  # Ignorar linhas vazias
                            erros = []
                            if tipo_arquivo == "IDE":
                                erros = validar_ide(linha)
                            elif tipo_arquivo == "RALIC":
                                campos = linha.split(";")
                                if len(campos) > 0 and campos[0] == "10":
                                    erros = validar_ralic_linha10(campos)
                            elif tipo_arquivo == "REDISPI":
                                campos = linha.split(";")
                                if len(campos) > 0 and campos[0] == "10":
                                    erros = validar_redispi_linha10(campos)
                            if erros:
                                resultados.append((i, erros))

                    # Exibir resultados
                    if resultados:
                        st.error("Foram encontrados erros nas seguintes linhas:")
                        for linh in resultados:
                            st.write(f"Linha {linh[0]}: {', '.join(linh[1])}")
                except Exception as e:
                    st.error(f"Erro ao processar o arquivo: {e}")

# Executar o aplicativo
if __name__ == "__main__":
    main()
