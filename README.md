# Corretor-DMED

Esse programa foi feito para ajudar na produtividade da empresa onde trabalho.

O objetivo do Corretor DMED é ajudar na hora de enviar arquivos fiscais para a receita federal, muitas vezes os arquivos vem com problemas de importação e o Corretor ajuda a ajustar esses problemas. Na versão atual (V0.2) o programa arruma o erro de um usuário dependente aparecer sem CPF, isso ajudou muito na hora de revisar os arquivos no meu setor.

Exemplo do erro:

TOP|090001|123456789|NOME DE UMA PESSOA X|01|000687|
TOP|090002|123456788|NOME DE UMA PESSOA X|01|000908|
DTOP|090067||NOME DE UMA PESSOA X|02|001002|
TOP|090056|123456125|NOME DE UMA PESSOA X|01|000176|

Exemplo da correção:

TOP|090001|123456789|NOME DE UMA PESSOA X|01|000687|
TOP|090002|123456788|NOME DE UMA PESSOA X|01|001910|
TOP|090056|123456125|NOME DE UMA PESSOA X|01|000176|
