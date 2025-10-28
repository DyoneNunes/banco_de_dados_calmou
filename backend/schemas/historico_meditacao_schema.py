"""Schema de validação para histórico de meditações"""
from marshmallow import Schema, fields, validate


class HistoricoMeditacaoSchema(Schema):
    """Schema para registrar histórico de meditação"""
    usuario_id = fields.Int(
        required=True,
        error_messages={'required': 'ID do usuário é obrigatório'}
    )

    meditacao_id = fields.Int(
        required=True,
        error_messages={'required': 'ID da meditação é obrigatório'}
    )

    duracao_real_minutos = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=300),
        error_messages={
            'required': 'Duração real em minutos é obrigatória',
            'min': 'Duração deve ser no mínimo 1 minuto',
            'max': 'Duração não pode exceder 300 minutos (5 horas)'
        }
    )
