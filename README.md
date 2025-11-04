# Projeto de Banco de Dados com PostgreSQL

O *Calmou* é um aplicativo para *monitorar o estresse e prevenir burnout*, ajudando o usuário a acompanhar 
seu humor diário, registrar emoções e acessar meditações guiadas.

Projeto desenvolvido na disciplina **Projeto Integrador II**, sob orientação do professor **Leonardo Pereira 
Valadão Lopes**, e na disciplina de **Banco de Dados**, com o professor **Howard Cruz Roatti**, no curso de 
**Tecnologia em Análise e Desenvolvimento de Sistemas - FAESA**.

Este README é para um projeto cujo foco principal é o banco de dados PostgreSQL.

Markdown
<img width="4002" height="1983" alt="diagrama_calmou" src="https://github.com/user-attachments/assets/95fd3d9e-d9f2-4e5d-a647-782b8a671177" />

##  Descrição

Este projeto é dedicado à criação, modelagem e manutenção de um banco de dados PostgreSQL. 
Ele serve como a fonte central de dados para o aplicativo calmou. A estrutura é gerenciada 
através de scripts SQL e o ambiente é containerizado com Docker para facilitar a replicação 
e o desenvolvimento.

---

##  Tecnologias Utilizadas
-   **PostgreSQL**: Gerenciamento de Banco de Dados Relacional.
-   **Docker**: Plataforma de containerização para criação do ambiente.
-   **Python**: Linguagem de programaca para estrutura do backend.
-   **React Native**: Para multiplataforma mobile IOS/ANDROID.
-   **Typescript**: Framework de desenvolvimento mobile.

###  Pré-requisitos
-   ** Docker**: [Link para instalação do Docker](https://www.docker.com/products/docker-desktop/)
-   ** Um cliente SQL** (Opcional, mas recomendado): DBeaver, pgAdmin, etc.
-   ** Node **: Para execução do react native.
-   ** Python**:  Para construcao do backend.

###  Instalação e Execução
1.  **Clone o repositório:**
    ```bash ssh
    git clone git@github.com:DyoneNunes/banco_de_dados_calmou.git
    cd banco_de_dados_calmou
    ```

2.  **Execucao do backend e frontend**
    Na raiz de cada ambiente existe um readme com as instrucoes de cada ambiente.
    Recomendações do Dyone: Executar cada ambiente em um vs code (ou ide de preferencia) para execução do projetos.
    

5.  **Execute os Scripts SQL:**
    Use seu cliente SQL preferido para se conectar ao banco de dados com as
    credenciais username: "postgres", senha: "postgres", db: "meu_banco" conectando
    ao localhost na porta 5432.

---

##  Colaboradores

-   **Derek Cobain**
-   **Dyone Andrade**
