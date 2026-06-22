import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'claudia_rocha.settings')
django.setup()

from blog.models import Artigo

artigos = [
    {
        'titulo': 'Horas extras não pagas: saiba quando você tem direito à reparação',
        'resumo': 'Trabalhar além do contratado sem receber por isso é uma das violações mais comuns no Direito do Trabalho. Entenda os limites legais, como calcular o que é devido e o que fazer para garantir sua reparação.',
        'conteudo': 'A jornada de trabalho no Brasil é regulada pela CLT e pela Constituição Federal, que fixam o limite de 8 horas diárias e 44 horas semanais. Horas trabalhadas além desse limite devem ser remuneradas com acréscimo mínimo de 50% sobre o valor da hora normal.\n\nO que muitos trabalhadores não sabem é que esse direito não desaparece com o tempo. A prescrição trabalhista permite reivindicar horas extras dos últimos 5 anos (se ainda empregado) ou 2 anos após o desligamento.\n\nA prova mais comum são os registros de ponto. Mas quando o empregador adultera esses registros — prática mais comum do que se imagina — é possível recorrer a testemunhas, e-mails e mensagens.\n\nSe você percebe que trabalha sistematicamente além da jornada sem receber, consulte um advogado especializado. O primeiro passo é reunir qualquer registro que documente sua rotina de trabalho real.',
        'publicado': True,
    },
    {
        'titulo': 'Assédio moral no trabalho — como identificar e o que fazer',
        'resumo': 'Humilhações repetidas, isolamento, sobrecarga deliberada e exposição vexatória configuram assédio moral. Esse tipo de violência deixa marcas profundas e gera direito à indenização.',
        'conteudo': 'O assédio moral é a exposição do trabalhador a situações humilhantes ou constrangedoras de forma repetida e prolongada. Diferente de um conflito pontual, o assédio tem caráter sistemático — é uma prática deliberada que visa desestabilizar emocionalmente o trabalhador.\n\nExemplos comuns: gritos em público, tarefas impossíveis ou degradantes, isolamento proposital, vigilância excessiva e desqualificação constante do trabalho realizado.\n\nAs consequências para a saúde são graves. Ansiedade, depressão e burnout são diagnósticos frequentes entre vítimas. Esses adoecimentos, quando causados pelo ambiente de trabalho, podem caracterizar doença ocupacional — gerando direitos adicionais.\n\nDocumente tudo. Guarde e-mails, mensagens, anote datas e testemunhas. A indenização por danos morais pode ser substancial, proporcional à gravidade e às consequências do assédio.',
        'publicado': True,
    },
    {
        'titulo': 'Rescisão indireta: quando o empregado pode pedir demissão e receber tudo',
        'resumo': 'Poucas pessoas conhecem a rescisão indireta — o mecanismo que permite ao trabalhador encerrar o contrato por culpa do empregador e receber todas as verbas rescisórias integralmente.',
        'conteudo': 'A rescisão indireta, prevista no artigo 483 da CLT, permite que o próprio empregado encerre o vínculo quando o empregador comete falta grave — e receba todos os direitos como se tivesse sido demitido sem justa causa.\n\nIsso inclui: aviso prévio indenizado, saldo de salário, 13º proporcional, férias com 1/3, FGTS com multa de 40% e habilitação ao seguro-desemprego.\n\nCasos comuns que justificam a rescisão indireta: salários atrasados de forma reiterada, rebaixamento de função sem justificativa, supressão de benefícios essenciais e assédio moral praticado ou tolerado pelo empregador.\n\nO trabalhador pode continuar trabalhando enquanto o processo tramita — estratégia financeiramente mais segura. Com o reconhecimento judicial, recebe as verbas integrais.',
        'publicado': True,
    },
    {
        'titulo': 'FGTS e multa rescisória: o que seu empregador é obrigado a pagar',
        'resumo': 'O Fundo de Garantia é um direito garantido constitucionalmente. Muitos trabalhadores não sabem quanto devem receber nem como verificar se os depósitos foram feitos corretamente.',
        'conteudo': 'O FGTS é um direito de todo empregado regido pela CLT. Todo mês, o empregador deve depositar em conta vinculada do trabalhador o equivalente a 8% do salário bruto. Esse valor pertence ao empregado.\n\nPelo aplicativo FGTS ou pelo site da Caixa Econômica Federal, qualquer trabalhador pode consultar o extrato de sua conta vinculada. Depósitos ausentes ou valores incorretos são irregularidades que geram ação de cobrança.\n\nQuando o empregador demite sem justa causa, é obrigado a pagar uma multa equivalente a 40% de todo o saldo do FGTS acumulado. Esse valor não vem da conta do trabalhador — é um encargo do empregador.\n\nEmpregadores que não depositam o FGTS corretamente cometem infração passível de autuação. O prazo para cobrar irregularidades é de 30 anos — um dos mais longos do Direito do Trabalho.',
        'publicado': True,
    },
    {
        'titulo': 'Trabalho sem carteira assinada: quais direitos você ainda tem',
        'resumo': 'A ausência do registro formal não cancela seus direitos trabalhistas. O vínculo empregatício existe na prática e a Justiça do Trabalho pode reconhecê-lo integralmente.',
        'conteudo': 'Um dos equívocos mais perigosos no Direito do Trabalho é acreditar que, sem carteira assinada, não há direitos. Essa crença beneficia apenas quem descumpre a lei.\n\nO que define o vínculo empregatício são quatro elementos: prestação de serviço por pessoa física, pessoalidade, não eventualidade e subordinação. Se esses elementos existem, o vínculo existe — independentemente de qualquer formalidade.\n\nCom o reconhecimento judicial, o trabalhador tem direito ao registro em carteira, FGTS com multa de 40%, 13º salário, férias com 1/3, aviso prévio, horas extras e todas as verbas do período.\n\nServem como prova: mensagens com ordens do empregador, e-mails, fotos de uniforme, comprovantes de pagamento e extratos bancários com transferências regulares. Informalidade não é ausência de direitos — é ausência de registro. E isso tem solução.',
        'publicado': True,
    },
    {
        'titulo': 'Acidente de trabalho e doença ocupacional — direitos e indenizações',
        'resumo': 'Acidente no trabalho ou doença causada pelo trabalho gera direitos previdenciários e pode gerar indenização civil. Saiba o que muda quando há culpa do empregador.',
        'conteudo': 'Acidente de trabalho é aquele que ocorre pelo exercício do trabalho a serviço do empregador, causando lesão corporal ou doença que resulte em morte ou redução da capacidade laboral. A definição inclui acidentes no trajeto e doenças causadas pelas condições de trabalho.\n\nA partir do 16º dia de afastamento, o trabalhador recebe auxílio-doença acidentário pelo INSS — benefício que garante estabilidade no emprego por 12 meses após o retorno. O FGTS continua sendo depositado durante o afastamento.\n\nO benefício previdenciário não exclui a indenização civil. Quando o acidente decorre de culpa ou negligência do empregador — ambiente insalubre, ausência de equipamentos de proteção, jornadas abusivas — o trabalhador tem direito a indenização por danos materiais, morais e estéticos.\n\nO primeiro passo após um acidente: registre a Comunicação de Acidente de Trabalho (CAT), busque atendimento médico imediatamente e guarde toda a documentação.',
        'publicado': True,
    },
]

for dados in artigos:
    obj, criado = Artigo.objects.get_or_create(titulo=dados['titulo'], defaults=dados)
    status = 'Criado' if criado else 'Ja existe'
    print(f'{status}: {dados["titulo"][:60]}')

print('Concluido.')
