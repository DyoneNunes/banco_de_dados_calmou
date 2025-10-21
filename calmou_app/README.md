# Calmou App 👋

Este é um projeto [Expo](https://expo.dev) para o aplicativo Calmou, desenvolvido com React Native.

## 1. Pré-requisitos

Antes de começar, você precisa ter as seguintes ferramentas instaladas em seu sistema.

- **Node.js (versão LTS):** Essencial para rodar o ambiente JavaScript.
- **Git:** Para clonar e gerenciar o versionamento do código.
- **Watchman (para macOS e Linux):** Recomendado pelo React Native para observar mudanças no sistema de arquivos.
- **Um editor de código:** Como [VS Code](https://code.visualstudio.com/).

## 2. Configuração do Ambiente por Sistema Operacional

Siga as instruções correspondentes ao seu sistema operacional para configurar o ambiente de desenvolvimento nativo.

---

### Ruindows

No Windows, você pode desenvolver para Android. O desenvolvimento para iOS não é suportado.

1.  **Instale o Node.js e o Git:**
    *   Baixe e instale a versão LTS do [Node.js](https://nodejs.org/en/).
    *   Baixe e instale o [Git para Windows](https://git-scm.com/download/win).

2.  **Configure o ambiente Android:**
    *   Siga o guia oficial do React Native para **"React Native CLI Quickstart"** na aba **"Windows"** e **"Android"**.
    *   O guia irá instruí-lo a instalar o **Android Studio**, o **JDK** (Java Development Kit) e a configurar as variáveis de ambiente (`ANDROID_HOME`).
    *   **Link:** [Guia de Configuração do React Native](https://reactnative.dev/docs/environment-setup?platform=android&os=windows)

---

###  macOS

No macOS, você pode desenvolver para iOS e Android.

1.  **Instale o Homebrew, Node.js, Watchman e Git:**
    *   Abra o Terminal e instale o [Homebrew](https://brew.sh/index_pt-br) (gerenciador de pacotes).
    *   Use o Homebrew para instalar as ferramentas:
        ```bash
        brew install node
        brew install watchman
        brew install git
        ```

2.  **Configure o ambiente iOS:**
    *   Instale o **Xcode** através da [Mac App Store](https://apps.apple.com/us/app/xcode/id497799835?mt=12).
    *   Abra o Xcode, vá em **Settings...** > **Locations** e instale o **Command Line Tools** na lista suspensa.

3.  **Configure o ambiente Android:**
    *   Siga o guia oficial do React Native para **"React Native CLI Quickstart"** na aba **"macOS"** e **"Android"**.
    *   O guia irá instruí-lo a instalar o **Android Studio** e configurar as variáveis de ambiente.
    *   **Link:** [Guia de Configuração do React Native](https://reactnative.dev/docs/environment-setup?platform=android&os=macos)

---

### 🐧 Linux

No Linux, você pode desenvolver para Android. O desenvolvimento para iOS não é suportado.

1.  **Instale o Node.js e o Git:**
    *   Recomenda-se usar o `nvm` (Node Version Manager) para gerenciar as versões do Node.js.
    *   Siga as instruções de instalação do `nvm` [aqui](https://github.com/nvm-sh/nvm#installing-and-updating).
    *   Para distribuições baseadas em Debian/Ubuntu, você pode instalar o Git com:
        ```bash
        sudo apt-get update && sudo apt-get install -y git
        ```

2.  **Configure o ambiente Android:**
    *   Siga o guia oficial do React Native para **"React Native CLI Quickstart"** na aba **"Linux"** e **"Android"**.
    *   O guia irá instruí-lo a instalar o **Android Studio**, o **JDK** e a configurar as variáveis de ambiente.
    *   **Link:** [Guia de Configuração do React Native](https://reactnative.dev/docs/environment-setup?platform=android&os=linux)

## 3. Executando o Projeto

Após configurar o ambiente, clone o repositório e execute os seguintes comandos no terminal, dentro da pasta do projeto:

**1. Instale as dependências:**
```bash
npm install
npx expo install(Depende da dependencia do expo)
```

**2. Inicie o aplicativo:**

Você pode iniciar o Metro Bundler e escolher a plataforma (Android/iOS/Web) no terminal, ou usar um dos comandos específicos abaixo.

**Para iniciar o Metro Bundler:**
```bash
npm start
npx expo start
```

**Para iniciar diretamente em uma plataforma (requer o ambiente nativo configurado):**
```bash
# Android
npm run android

# iOS (apenas no macOS)
npm run ios

# Web (para desenvolvimento no navegador)
npm run web

# Expo 
npx expo start
```
