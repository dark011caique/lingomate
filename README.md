# LingoMate - Chatbot para Aprendizado de Inglês

**LingoMate** é um chatbot desenvolvido para ajudar usuários a melhorar suas habilidades em inglês por meio de conversas interativas e adaptáveis ao nível do usuário. O sistema é projetado para ser flexível, permitindo a inclusão de imagens para esclarecer dúvidas e personalizar a experiência de aprendizado com diferentes personalidades do chatbot.

## Funcionalidades

- **Conversação em Inglês**: Interaja com o chatbot para praticar e melhorar suas habilidades no idioma.
- **Níveis de Personalidade**: O chatbot adapta suas respostas conforme o humor e estilo do usuário:
  - **Positiva**: Encoraja e celebra cada conquista com entusiasmo.
  - **Neutra**: Focada em explicações técnicas e objetivas.
  - **Negativa (Acolhedora)**: Empática, ideal para quem enfrenta dificuldades e precisa de apoio emocional durante o aprendizado.
- **Imagens Interativas**: Adicione imagens para ajudar a esclarecer dúvidas ou fazer perguntas relacionadas ao aprendizado de inglês.
  
## Tecnologias Utilizadas

- **Python** 🐍: Linguagem de programação principal do projeto.
- **Gemini AI (Google)** 💡: Tecnologia de inteligência artificial utilizada para processamento e geração das respostas do chatbot.
- **Flask** ⚙️: Framework web utilizado para criar a aplicação backend.
- **JavaScript** 🌐: Para interatividade no frontend.
- **HTML/CSS**: Para a estruturação e estilização da interface do usuário.

## Como Rodar o Projeto

### Pré-requisitos

Antes de rodar o projeto, você precisa ter os seguintes itens instalados no seu computador:

- **Python 3.x**: Para rodar o backend.
- **Node.js**: Para rodar o frontend (caso precise de interatividade extra).
- **Pip**: Para instalar as dependências Python.

### Passos para Iniciar

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/dark011caique/lingomate.git
   cd lingomate

2. **Instale as dependências do Python:**
    pip install -r requirements.txt

3. **Carregue as variáveis de ambiente do .env:**
    Adicione a chave de API do Google Gemini no arquivo .env:
        GEMINI_API_KEY="sua-chave-da-api-aqui"

4. **Rodando o Servidor:**
    Rodando o Servidor:
        python app.py
