Usar para o desenvolvimento
- Enunciado do trabalho 03
- Slides Pyro.pdf
- Tarefas abaixo

# Tarefas sugeridas pela professora (ClassRoom)

- [x] 1. Execute o serviço de nomes;
- [x] 2. Implemente o líder (seguindo o código do servidor dos slides - crie uma instância do daemon, registre o objeto no daemon, registra o nome Lider_Epoca1 e a URI no serviço de nomes);
- [x] 3. Implemente o votante e o observador - (sigam o código do cliente dos slides - crie o daemon, pois vão receber notificação do líder para buscar atualizações do tópico, busquem a URI do "Lider_Epoca1" no serviço de nomes);
- [ ] 4. Implemente os métodos do líder;
- [ ] 5. Implemente os métodos dos votantes e observador;
- [ ] 6. Implemente o publicador - só vai publicar mensagens no líder;
- [ ] 7. Implemente a troca de mensagens de replicação entre líder e demais brokers;
- [ ] 8. Implemente o envio de heartbeat e a verificação de falhas dos votantes;
- [ ] 9. Teste a falha de um votante e implemente a mudança de observador para votante;
- [ ] 10. Implemente o consumidor - só vai consumir mensagens do líder que estão commit.

Comandos:
```sh
pyro5-ns # Executa o servidor de nomes
pyro5-ns list # lista os objetos (apenas o ns e o lider devem aparecer)
```