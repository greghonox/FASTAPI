from passlib.context import CryptContext

CRIPTO:CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verificar_senha(senha:str, hash_senha:str) -> bool:
    """
        Verifica se a senha esta correta.
        Comparando a senha informada com o hash.
        Olhando para as senhas que estao no banco de dados.
    """
    return CRIPTO.verify(senha, hash_senha)


def gerar_hash(senha: str) -> str:
    """
        FUNCAO QUE GERA O HASH DA SENHA.
    """
    return CRIPTO.hash(senha)