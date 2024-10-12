from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message
import os

app = Flask(__name__)  # Aqui você instancia o Flask app

# Configurações de email usando variáveis de ambiente
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', '1']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

# Configurar o Flask-Mail
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    print("Início da função contact")  # Verifica se a função foi chamada

    if request.method == 'POST':
        # Lógica para tratar o envio de e-mail
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        print(f"Dados recebidos: {name}, {email}, {subject}, {message}")  # Exibe os dados no terminal

        if not name or not email or not message:
            print("Campos obrigatórios não preenchidos")  # Verifica se algum campo está faltando
            flash('Preencha todos os campos', 'error')
            return render_template('index.html')

        try:
            msg = Message(subject,
                          sender=app.config['MAIL_USERNAME'],
                          recipients=['seu-email@gmail.com'])
            msg.body = f"Mensagem de: {name}\nEmail: {email}\n\n{message}"

            print("Tentando enviar o e-mail...")  # Verifica se o e-mail está sendo preparado

            mail.send(msg)
            print("E-mail enviado com sucesso!")  # Se o e-mail for enviado com sucesso

            flash('Mensagem enviada com sucesso!', 'success')
        except Exception as e:
            print(f"Erro ao enviar e-mail: {str(e)}")  # Mostra o erro no terminal
            flash(f'Erro ao enviar mensagem: {str(e)}', 'error')

        return render_template('index.html')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
