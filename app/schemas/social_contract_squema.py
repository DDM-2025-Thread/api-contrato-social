from pydantic import BaseModel
from typing import Optional, List, Any

class Empresa(BaseModel):
    nome: Optional[str] = None
    nome_fantasia: Optional[str] = None
    cnpj: Optional[str] = None
    nire: Optional[str] = None

class Contrato(BaseModel):
    tipo: Optional[str] = None
    data: Optional[str] = None
    versao: Optional[str] = None
    alteracoes: List[Any] = []

class SocioPessoaFisica(BaseModel):
    tipo: str
    nome: Optional[str] = None
    cpf: Optional[str] = None
    rg: Optional[str] = None
    nascimento: Optional[str] = None
    participacao: Optional[str] = None
    quotas: Optional[int] = None
    valor_total: Optional[float] = None

class RepresentanteLegal(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    cargo: Optional[str] = None

class SocioPessoaJuridica(BaseModel):
    tipo: str
    razao_social: Optional[str] = None
    cnpj: Optional[str] = None
    nire: Optional[str] = None
    representante_legal: RepresentanteLegal
    participacao: Optional[str] = None
    quotas: Optional[int] = None
    valor_total: Optional[float] = None

class Socios(BaseModel):
    atuais: List[Any]
    retirados: List[Any] = []

class Enderecos(BaseModel):
    sede_atual: Optional[str] = None
    sedes_anteriores: List[str] = []

class Porte(BaseModel):
    atual: Optional[str] = None
    anteriores: List[str] = []

class CapitalSocial(BaseModel):
    valor_total: Optional[float] = None
    quantidade_quotas: Optional[int] = None
    valor_quota: Optional[float] = None

class CNAE(BaseModel):
    codigo: Optional[str] = None
    descricao: Optional[str] = None

class AdministracaoResponsavel(BaseModel):
    nome: Optional[str] = None
    tipo: str
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    poderes: Optional[str] = None
    restricoes: List[str] = []

class Administracao(BaseModel):
    responsaveis: List[AdministracaoResponsavel]

class Disposicoes(BaseModel):
    foro: Optional[str] = None
    prazo_duracao: Optional[str] = None
    exercicio_social: Optional[str] = None
    pro_labore: Optional[str] = None
    herdeiros: Optional[str] = None
    outros: List[str] = []

class Assinatura(BaseModel):
    nome: Optional[str] = None
    cpf_cnpj: Optional[str] = None
    cargo: Optional[str] = None
    tipo_assinatura: str

class Testemunha(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    rg: Optional[str] = None

class CertificacaoDigital(BaseModel):
    orgao: Optional[str] = None
    data: Optional[str] = None
    protocolo: Optional[str] = None
    numero_registro: Optional[str] = None
    codigo_verificacao: Optional[str] = None

class CertificacaoFisica(BaseModel):
    orgao: Optional[str] = None
    livro: Optional[str] = None
    folha: Optional[str] = None
    numero_registro: Optional[str] = None
    data: Optional[str] = None

class CertificacaoRegistro(BaseModel):
    digital: CertificacaoDigital
    fisico: CertificacaoFisica

class ContratoSocial(BaseModel):
    empresa: Empresa
    contrato: Contrato
    socios: Socios
    enderecos: Enderecos
    porte: Porte
    capital_social: CapitalSocial
    cnaes: List[CNAE]
    objeto_social: List[str] = []
    administracao: Administracao
    disposicoes: Disposicoes
    assinaturas: List[Assinatura]
    testemunhas: List[Testemunha]
    certificacao_registro: CertificacaoRegistro