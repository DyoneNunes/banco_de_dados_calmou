"""Schemas de validação para a API Calmou"""
from .usuario_schema import UsuarioSchema, LoginSchema, UsuarioCreateSchema, UsuarioUpdateSchema
from .humor_schema import ClassificacaoHumorSchema
from .avaliacao_schema import ResultadoAvaliacaoSchema
from .historico_meditacao_schema import HistoricoMeditacaoSchema

__all__ = [
    'UsuarioSchema',
    'LoginSchema',
    'UsuarioCreateSchema',
    'UsuarioUpdateSchema',
    'ClassificacaoHumorSchema',
    'ResultadoAvaliacaoSchema',
    'HistoricoMeditacaoSchema'
]
