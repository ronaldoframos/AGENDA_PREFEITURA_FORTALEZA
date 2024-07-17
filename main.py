#%%
from dotenv import load_dotenv # type: ignore
import polars as pl # type:ignore
import time
from tqdm import tqdm
#
from langchain_openai import ChatOpenAI, OpenAI # type: ignore
from langchain.prompts import PromptTemplate # type: ignore
from langchain_core.output_parsers import StrOutputParser # type: ignore
from langchain_core.output_parsers import JsonOutputParser # type: ignore
#%%
# variaveis globais
#
load_dotenv()
arquivo_csv = './dados/orgaos_prefeitura_fortaleza.csv'
saida = './dados/agenda_fortaleza.csv'

#%%
# carregando o csv
# 
df = pl.read_csv(arquivo_csv,separator=';')
#%%
# preparar o prompt e o llm 
#
gabarito = """ você deve agir como um serviço de informação da prefeitura de fortaleza ceará.
Dado o órgão abaixo retorne um arquivo no formato json contendo endereço do órgão, telefone do órgão e 
nome do responsável pelo órgão no seguinte formato:
{{
    "endereco": endereço do órgao
    "telefone": telefone do órgão
    "responsavel" : nome do responsável pelo órgão

}}.
Não inclua nenhuma informação adicional.
O nome do órgão é:
<órgão>
{orgao}
</órgão>
"""
prompt_template = PromptTemplate.from_template(gabarito)
llm = ChatOpenAI()
parser = JsonOutputParser()
cadeia = prompt_template | llm | parser
#%%
# main

linhas = []
for linha in df.to_dicts():
    nome_orgao = linha['orgao']
    try:
        res = cadeia.invoke({'orgao':nome_orgao})
    except Exception as e:
        print(f"Erro de Invokação {nome_orgao}  \nMensagem : {e} ")
        time.sleep(5)
        continue
    try:
        linha['endereco'] = res['endereco']
        linha['telefone'] = res['telefone']
        linha['responsavel'] = res['responsavel']
        linhas.append(linha)
    except Exception as e:
        print(f"Erro no resulado de  {nome_orgao} \nMensagem : {e} ")
        time.sleep(5)
        continue
    time.sleep(5)

#%%
# gravar resultado
ndf = pl.from_dicts(linhas)

#%%

ndf.write_csv(saida)


# %%
