from flask import Flask, request, render_template, redirect
app = Flask(__name__)


@app.route('/')

def index():
    return render_template('index.html')


@app.route('/cs_tv', methods=['post'])

def cs_tv():
    valor = int(request.form['opcoes'])
    if valor == 0:
        return redirect('/')
    else:
        from playwright.sync_api import sync_playwright
        from time import sleep
        with sync_playwright() as pw:
            navegador = pw.chromium.launch()
            email_temporario = navegador.new_page()
            email_temporario.set_default_timeout(120000)  # Esperar no máximo 2 minutos
            email_temporario.goto('https://pt.emailfake.com/')  # Acessar o Site
            pegar_dados_email = str(email_temporario.content())
            pegar_email = pegar_dados_email.split('<span id="email_ch_text">')
            separar_email = pegar_email[1]
            caracteres = separar_email.find('<')
            email = separar_email[0:caracteres]
            cs_goias = navegador.new_page()
            cs_goias.goto('http://superpainel.mine.nu/painel/formulario_testes.php?r=SGJtd0pmNXd1TTlzRUNtT25JK0lTallkL1RQVnBTMkFBQXMrWnlsZXEvdz0,')  # Teste 48H Cs
            cs_goias.fill('xpath=/html/body/div/div/form/div[1]/input', 'User')  # Preencher Nome
            cs_goias.fill('xpath=/html/body/div/div/form/div[2]/input', f'{email}')  # Preencher Email
            cs_goias.locator(f'xpath=/html/body/div/div/form/div[3]/div[{valor}]/input').click()  # Claro Tv Hd / Sky
            cs_goias.locator('xpath=/html/body/div/div/form/div[4]/button').click()  # Enviar
            sleep(5)
            email_temporario.reload()
            dados = str(email_temporario.content())
            separar_vencimento = dados.split('Vencimento: ')
            vencimento = separar_vencimento[1]
            separar_usuario = dados.split('login / usuario:&nbsp;')
            usuario = separar_usuario[1]
            fim_usuario = usuario.find('<')
            separar_senha = dados.split('Senha / password: ')
            senha = separar_senha[1]
        return render_template('cs_tv.html', valor=valor, data_vencimento=vencimento[0:19], user='User', usuario=usuario[0:fim_usuario], senha=senha[0:3])


if __name__ == '__main__':
    app.run(debug=True)
