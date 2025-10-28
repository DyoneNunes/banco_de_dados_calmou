"""Schemas de validação para avaliações"""
from marshmallow import Schema, fields, validate


class ResultadoAvaliacaoSchema(Schema):
    """Schema para resultado de avaliação"""
    usuario_id = fields.Int(required=True, error_messages={
        'required': 'ID do usuário é obrigatório'
    })

    tipo = fields.Str(
        required=True,
        validate=validate.OneOf([
            'ansiedade',
            'depressao',
            'estresse',
            'burnout',
            'Avaliação de Estresse',
            'Questionário de Burnout'
        ]),
        error_messages={
            'required': 'Tipo de avaliação é obrigatório'
        }
    )

    respostas = fields.Dict(
        required=True,
        error_messages={
            'required': 'Respostas são obrigatórias'
        }
    )

    resultado_score = fields.Int(
        required=True,
        validate=validate.Range(min=0),
        error_messages={
            'required': 'Score do resultado é obrigatório'
        }
    )

    resultado_texto = fields.Str(allow_none=True)
