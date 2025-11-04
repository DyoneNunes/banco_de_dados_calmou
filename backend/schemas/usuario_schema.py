"""Schemas de validação para usuários"""
from marshmallow import Schema, fields, validate, validates, ValidationError
import re


def validate_cpf(cpf):
    """Valida formato de CPF (apenas formato, não valida dígitos)"""
    if not cpf:
        return True  # CPF é opcional

    # Remove caracteres não numéricos
    cpf_limpo = re.sub(r'\D', '', cpf)

    if len(cpf_limpo) != 11:
        raise ValidationError('CPF deve ter 11 dígitos')

    return True


def validate_email_format(email):
    """Valida formato de email"""
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise ValidationError('Formato de email inválido')
    return True


class LoginSchema(Schema):
    """Schema para validação de login"""
    email = fields.Email(required=True, error_messages={
        'required': 'Email é obrigatório',
        'invalid': 'Email inválido'
    })
    password = fields.Str(required=True, validate=validate.Length(min=1), error_messages={
        'required': 'Senha é obrigatória'
    })


class UsuarioCreateSchema(Schema):
    """Schema para criação de usuário"""
    nome = fields.Str(required=True, validate=validate.Length(min=3, max=255), error_messages={
        'required': 'Nome é obrigatório',
        'min': 'Nome deve ter no mínimo 3 caracteres',
        'max': 'Nome deve ter no máximo 255 caracteres'
    })

    email = fields.Email(required=True, error_messages={
        'required': 'Email é obrigatório',
        'invalid': 'Email inválido'
    })

    password = fields.Str(required=True, validate=validate.Length(min=8, max=100), error_messages={
        'required': 'Senha é obrigatória',
        'min': 'Senha deve ter no mínimo 8 caracteres',
        'max': 'Senha deve ter no máximo 100 caracteres'
    })

    config = fields.Dict(required=False, load_default=None)

    @validates('email')
    def validate_email(self, value):
        validate_email_format(value)


class UsuarioUpdateSchema(Schema):
    """Schema para atualização de usuário"""
    nome = fields.Str(validate=validate.Length(min=3, max=255))
    email = fields.Email()
    password = fields.Str(validate=validate.Length(min=8, max=100))
    config = fields.Dict()

    @validates('email')
    def validate_email(self, value):
        if value:
            validate_email_format(value)


class PerfilUpdateSchema(Schema):
    """Schema para atualização de perfil"""
    nome = fields.Str(validate=validate.Length(min=3, max=255))
    cpf = fields.Str(validate=validate_cpf)
    data_nascimento = fields.Date()
    tipo_sanguineo = fields.Str(validate=validate.OneOf(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']))
    alergias = fields.Str()
    foto_perfil = fields.Str()


class UsuarioSchema(Schema):
    """Schema completo de usuário (para resposta)"""
    id = fields.Int()
    nome = fields.Str()
    email = fields.Email()
    cpf = fields.Str(allow_none=True)
    data_nascimento = fields.Date(allow_none=True)
    tipo_sanguineo = fields.Str(allow_none=True)
    alergias = fields.Str(allow_none=True)
    data_cadastro = fields.DateTime(allow_none=True)
    foto_perfil = fields.Str(allow_none=True)
