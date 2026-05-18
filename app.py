"""
Jogo de Adivinhação de Palavras para Estudo de Programação
Versão com Streamlit

Objetivo:
O jogador deve descobrir palavras relacionadas à programação.

Funcionalidades:
- Sistema de vidas
- Tentativas de letras
- Tentativa de palavra completa
- Exibição de significado e exemplo
- Palavras não repetidas
"""

import streamlit as st
import random


# Configuração da página
st.set_page_config(
    page_title="Jogo de Adivinhação",
    layout="centered"
)


# Dicionário com palavras, exemplos e significados
palavras = {
    "variavel": [
        "x = 5",
        "Um local de armazenamento de dados em um programa"
    ],
    "funcao": [
        "def minha_funcao():",
        "Um bloco de código reutilizável que realiza uma tarefa específica"
    ],
    "lista": [
        "minha_lista = [1, 2, 3]",
        "Uma coleção ordenada e mutável de elementos"
    ],
    "dicionario": [
        "meu_dicionario = {'chave': 'valor'}",
        "Uma coleção de pares chave-valor"
    ],
    "tupla": [
        "minha_tupla = (1, 2, 3)",
        "Uma coleção ordenada e imutável de elementos"
    ],
    "conjunto": [
        "meu_conjunto = {1, 2, 3}",
        "Uma coleção não ordenada e sem elementos duplicados"
    ],
    "classe": [
        "class MinhaClasse:",
        "Um modelo para criar objetos"
    ],
    "objeto": [
        "meu_objeto = MinhaClasse()",
        "Uma instância de uma classe"
    ],
    "metodo": [
        "def meu_metodo(self):",
        "Uma função definida dentro de uma classe"
    ],
    "atributo": [
        "self.meu_atributo = valor",
        "Uma variável que pertence a um objeto"
    ]
}


# Inicialização do session_state
if "palavras_utilizadas" not in st.session_state:
    st.session_state.palavras_utilizadas = []

if "vidas" not in st.session_state:
    st.session_state.vidas = 3

if "tentativas" not in st.session_state:
    st.session_state.tentativas = 0

if "letras_tentadas" not in st.session_state:
    st.session_state.letras_tentadas = []

if "fim_jogo" not in st.session_state:
    st.session_state.fim_jogo = False

if "palavra_rodada" not in st.session_state:
    st.session_state.palavra_rodada = None

if "palavra_oculta" not in st.session_state:
    st.session_state.palavra_oculta = []

if "mensagem_resultado" not in st.session_state:
    st.session_state.mensagem_resultado = ""

if "tipo_mensagem" not in st.session_state:
    st.session_state.tipo_mensagem = ""


def escolher_palavra():
    """
    Escolhe uma palavra aleatória que ainda
    não foi utilizada anteriormente.

    Returns:
        str | None:
        Retorna a palavra sorteada ou None
        caso todas as palavras já tenham sido usadas.
    """

    if len(st.session_state.palavras_utilizadas) == len(palavras):
        return None

    palavra = random.choice(
        list(palavras.keys())
    )

    while (
        palavra
        in st.session_state.palavras_utilizadas
    ):
        palavra = random.choice(
            list(palavras.keys())
        )

    st.session_state.palavras_utilizadas.append(
        palavra
    )

    return palavra


def iniciar_novo_jogo():
    """
    Reinicia todos os dados da rodada atual.

    A função:
    - escolhe uma nova palavra
    - cria a palavra oculta
    - redefine vidas
    - redefine tentativas
    - limpa letras utilizadas
    """

    nova_palavra = escolher_palavra()

    st.session_state.palavra_rodada = (
        nova_palavra
    )

    if nova_palavra is not None:

        st.session_state.palavra_oculta = [
            "_" for _ in nova_palavra
        ]

    st.session_state.vidas = 3

    st.session_state.tentativas = 0

    st.session_state.letras_tentadas = []

    st.session_state.fim_jogo = False

    st.session_state.mensagem_resultado = ""

    st.session_state.tipo_mensagem = ""


def validar_letra(letra):
    """
    Valida a letra digitada pelo usuário.

    Regras:
    - Deve conter apenas um caractere
    - Deve ser uma letra do alfabeto

    Args:
        letra (str):
        Letra digitada pelo usuário.

    Returns:
        tuple:
        (True, "") se válida.
        (False, mensagem) se inválida.
    """

    if len(letra) != 1:
        return False, (
            "Digite apenas UMA letra."
        )

    if not letra.isalpha():
        return False, (
            "Digite apenas letras."
        )

    return True, ""


def verificar_vitoria():
    """
    Verifica se o jogador completou
    toda a palavra.

    Returns:
        bool:
        True se venceu.
        False caso contrário.
    """

    return (
        "_"
        not in st.session_state.palavra_oculta
    )


# Inicia primeira rodada
if st.session_state.palavra_rodada is None:
    iniciar_novo_jogo()


# Interface principal
st.title("🎮 Jogo de Adivinhação de Palavras")

st.write(
    "Descubra palavras relacionadas à programação e seus significados."
)


# Verifica se acabaram as palavras
if st.session_state.palavra_rodada is None:

    st.success(
        "Todas as palavras já foram utilizadas."
    )

else:

    palavra_rodada = (
        st.session_state.palavra_rodada
    )

    # Exibe palavra oculta
    st.subheader("Palavra")

    st.markdown(
        f"# {' '.join(st.session_state.palavra_oculta)}"
    )

    # Resultado da palavra revelada
    if verificar_vitoria():

        st.session_state.fim_jogo = True

        st.success(
            "Parabéns! Você descobriu a palavra!"
        )

        st.subheader("Significado")
        st.write(
            palavras[palavra_rodada][1]
        )

        st.subheader("Exemplo")
        st.code(
            palavras[palavra_rodada][0]
        )

        if st.button(
            "Jogar Novamente"
        ):

            iniciar_novo_jogo()

            st.rerun()

        st.stop()

    st.write(
        f"Quantidade de letras: "
        f"{len(palavra_rodada)}"
    )

    st.markdown(
        f"<p style='color: red;'>Vidas restantes: "
        f"{st.session_state.vidas}</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<p style='color: red;'>Tentativas: "
        f"{st.session_state.tentativas}</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='color: red;'>Letras tentadas: "
        + ", ".join(
            st.session_state.letras_tentadas
        )
        + "</p>",
        unsafe_allow_html=True
    )

    # Campo de letra
    letra = st.text_input(
        "Digite uma letra"
    )

    # Botão verificar letra
    if st.button("Verificar Letra"):

        letra = letra.lower().strip()

        valido, mensagem = validar_letra(
            letra
        )

        if not valido:

            st.warning(mensagem)

        elif (
            letra
            in st.session_state.letras_tentadas
        ):

            st.warning(
                "Você já tentou essa letra."
            )

        else:

            st.session_state.letras_tentadas.append(
                letra
            )

            st.session_state.tentativas += 1

            lista_letras = list(
                palavra_rodada
            )

            # Verifica acerto da letra
            if letra in lista_letras:

                for i in range(
                    len(lista_letras)
                ):

                    if (
                        lista_letras[i]
                        == letra
                    ):
                        st.session_state.palavra_oculta[i] = letra

                st.session_state.mensagem_resultado = (
                    "Você acertou uma letra!"
                )

                st.session_state.tipo_mensagem = (
                    "success"
                )

            # Erro da letra
            else:

                st.session_state.vidas -= 1

                st.session_state.mensagem_resultado = (
                    "Letra incorreta!"
                )

                st.session_state.tipo_mensagem = (
                    "error"
                )

            st.rerun()

    # Exibe mensagens
    if st.session_state.mensagem_resultado:

        if (
            st.session_state.tipo_mensagem
            == "success"
        ):

            st.success(
                st.session_state.mensagem_resultado
            )

        elif (
            st.session_state.tipo_mensagem
            == "error"
        ):

            st.error(
                st.session_state.mensagem_resultado
            )

    # Campo aparece após primeira tentativa
    if (
        st.session_state.tentativas > 0
        and not st.session_state.fim_jogo
    ):

        st.subheader(
            "Tentar adivinhar a palavra"
        )

        palavra_tentativa = st.text_input(
            "Digite a palavra completa"
        )

        # Botão verificar palavra
        if st.button("Verificar Palavra"):

            st.session_state.tentativas += 1

            if (
                palavra_tentativa
                .lower()
                .strip()
                == palavra_rodada
            ):

                st.session_state.palavra_oculta = list(
                    palavra_rodada
                )

                st.session_state.mensagem_resultado = (
                    "Parabéns! Você acertou a palavra!"
                )

                st.session_state.tipo_mensagem = (
                    "success"
                )

                st.session_state.fim_jogo = True

            else:

                st.session_state.vidas -= 1

                st.session_state.mensagem_resultado = (
                    "Palavra incorreta!"
                )

                st.session_state.tipo_mensagem = (
                    "error"
                )

            st.rerun()

    # Game Over
    if st.session_state.vidas <= 0:

        st.error("Game Over!")

        st.write(
            f"A palavra era: "
            f"{palavra_rodada}"
        )

        st.subheader("Significado")

        st.write(
            palavras[palavra_rodada][1]
        )

        st.subheader("Exemplo")

        st.code(
            palavras[palavra_rodada][0]
        )

        st.session_state.fim_jogo = True

    # Reiniciar jogo
    if st.session_state.fim_jogo:

        if st.button(
            "Jogar Novamente"
        ):

            iniciar_novo_jogo()

            st.rerun()
