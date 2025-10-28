"""Schemas de validação para classificação de humor"""
from marshmallow import Schema, fields, validate


class ClassificacaoHumorSchema(Schema):
    """Schema para classificação de humor"""
    usuario_id = fields.Int(required=True, error_messages={
        'required': 'ID do usuário é obrigatório'
    })

    nivel_humor = fields.Int(
        required=True,
        validate=validate.Range(min=0, max=10),
        error_messages={
            'required': 'Nível de humor é obrigatório',
            'min': 'Nível de humor deve ser entre 0 e 10',
            'max': 'Nível de humor deve ser entre 0 e 10'
        }
    )

    sentimento_principal = fields.Str(
        validate=validate.Length(max=100),
        allow_none=True
    )

    notas = fields.Str(allow_none=True)
