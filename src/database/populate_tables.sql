INSERT INTO usuario (id, email, senha, nickname, nome, sobrenome)
VALUES
('U001', 'user1@example.com', 'Senha@123', 'user1nick', 'Alice', 'Silva'),
('U002', 'user2@example.com', 'Senha@456', 'user2nick', 'Bob', 'Souza'),
('U003', 'user3@example.com', 'Senha@789', 'user3nick', 'Clara', 'Pereira'),
('U004', 'user4@example.com', 'Senha@101', 'user4nick', 'David', 'Oliveira'),
('U005', 'user5@example.com', 'Senha@102', 'user5nick', 'Eva', 'Moura'),
('U006', 'user6@example.com', 'Senha@103', 'user6nick', 'Felipe', 'Almeida'),
('U007', 'user7@example.com', 'Senha@104', 'user7nick', 'Gabi', 'Ferreira'),
('U008', 'user8@example.com', 'Senha@105', 'user8nick', 'Hugo', 'Costa'),
('U009', 'user9@example.com', 'Senha@106', 'user9nick', 'Inês', 'Martins'),
('U010', 'user10@example.com', 'Senha@107', 'user10nick', 'Jorge', 'Nunes'),
('U011', 'user11@example.com', 'Senha@108', 'user11nick', 'Karina', 'Rodrigues'),
('U012', 'user12@example.com', 'Senha@109', 'user12nick', 'Lucas', 'Barros'),
('U013', 'user13@example.com', 'Senha@110', 'user13nick', 'Marina', 'Santos'),
('U014', 'user14@example.com', 'Senha@111', 'user14nick', 'Nina', 'Batista'),
('U015', 'user15@example.com', 'Senha@112', 'user15nick', 'Otávio', 'Pinto'),
('U016', 'user16@example.com', 'Senha@113', 'user16nick', 'Paula', 'Lima'),
('U017', 'user17@example.com', 'Senha@114', 'user17nick', 'Ricardo', 'Fonseca'),
('U018', 'user18@example.com', 'Senha@115', 'user18nick', 'Sofia', 'Vaz'),
('U019', 'user19@example.com', 'Senha@116', 'user19nick', 'Tiago', 'Ramos'),
('U020', 'user20@example.com', 'Senha@117', 'user20nick', 'Valéria', 'Castro');

INSERT INTO livro (id, autor, nome, genero, descricao)
VALUES
('L016', 'José de Alencar', 'Iracema', 'Romance', 'Um clássico do romantismo brasileiro, narrando a história de amor entre Iracema e Martim.'),
('L017', 'Machado de Assis', 'Dom Casmurro', 'Romance', 'A famosa história de Bentinho e Capitu, abordando temas de ciúmes e traição.'),
('L018', 'Machado de Assis', 'Memórias Póstumas de Brás Cubas', 'Romance', 'Uma narrativa inovadora sobre a vida e morte de Brás Cubas, contada por ele mesmo.'),
('L019', 'Aluísio Azevedo', 'O Cortiço', 'Naturalismo', 'Uma representação da vida num cortiço carioca, com ênfase em críticas sociais.'),
('L020', 'Graciliano Ramos', 'Vidas Secas', 'Romance', 'A luta de uma família sertaneja pela sobrevivência em um cenário de seca.'),
('L021', 'Guimarães Rosa', 'Grande Sertão: Veredas', 'Romance', 'Uma complexa e épica narrativa sobre a vida no sertão brasileiro.'),
('L022', 'Jorge Amado', 'Capitães da Areia', 'Romance', 'A história dos meninos de rua de Salvador e suas aventuras e desventuras.'),
('L023', 'Jorge Amado', 'Gabriela, Cravo e Canela', 'Romance', 'Uma narrativa que retrata a vida em uma cidade da Bahia e o impacto de uma mulher livre e apaixonada.'),
('L024', 'Raquel de Queiroz', 'O Quinze', 'Romance', 'Um relato sobre a grande seca de 1915 e suas consequências para o povo nordestino.'),
('L025', 'Joaquim Manuel de Macedo', 'A Moreninha', 'Romance', 'Uma história de amor juvenil em um cenário idílico.'),
('L026', 'José de Alencar', 'O Guarani', 'Romance', 'A aventura de Peri e Cecília no Brasil colonial.'),
('L027', 'Joaquim Nabuco', 'O Abolicionismo', 'História', 'Uma obra importante sobre a luta pela abolição da escravatura no Brasil.'),
('L028', 'Euclides da Cunha', 'Os Sertões', 'Ensaios', 'Um relato detalhado sobre a Guerra de Canudos e a vida no sertão brasileiro.'),
('L029', 'Clarice Lispector', 'A Hora da Estrela', 'Romance', 'A trajetória de Macabéa, uma jovem nordestina em busca de um sentido para sua vida.'),
('L030', 'Lima Barreto', 'Triste Fim de Policarpo Quaresma', 'Romance', 'A história de um patriota ingênuo e suas desilusões.');

INSERT INTO participa (usuario_id, clube_id)
VALUES
('U001', 'C001'),
('U002', 'C001'),
('U003', 'C002'),
('U004', 'C002'),
('U005', 'C003'),
('U006', 'C003'),
('U007', 'C001'),
('U008', 'C002'),
('U009', 'C003'),
('U010', 'C001'),
('U010', 'C002'),
('U010', 'C003');

INSERT INTO adiciona (usuario_id, clube_id, livro_id, data_adicao)
VALUES
('U001', 'C001', 'L016', '2024-11-01'),
('U002', 'C001', 'L017', '2024-11-02'),
('U003', 'C002', 'L018', '2024-11-03'),
('U004', 'C002', 'L019', '2024-11-04'),
('U005', 'C003', 'L020', '2024-11-05'),
('U006', 'C003', 'L021', '2024-11-06'),
('U007', 'C001', 'L022', '2024-11-07'),
('U008', 'C002', 'L023', '2024-11-08'),
('U009', 'C003', 'L024', '2024-11-09'),
('U010', 'C001', 'L025', '2024-11-10');

INSERT INTO avaliacao (avaliador_id, livro_id, descricao, estrelas, data_avaliacao)
VALUES
('U001', 'L016', 'Iracema é uma obra poética e tocante, representando o encontro de culturas.', 5, '2024-11-11 10:00:00'),
('U002', 'L017', 'Dom Casmurro é intrigante e mantém o leitor em dúvida até o fim.', 5, '2024-11-12 11:00:00'),
('U003', 'L018', 'Memórias Póstumas é uma narrativa genial, repleta de ironia.', 5, '2024-11-13 12:00:00'),
('U004', 'L019', 'O Cortiço é uma crítica social brilhante e realista.', 4, '2024-11-14 13:00:00'),
('U005', 'L020', 'Vidas Secas é profundamente comovente e realista.', 5, '2024-11-15 14:00:00'),
('U006', 'L021', 'Grande Sertão: Veredas é desafiador e recompensador.', 5, '2024-11-16 15:00:00'),
('U007', 'L022', 'Capitães da Areia é uma leitura envolvente e emocionante.', 4, '2024-11-17 16:00:00'),
('U008', 'L023', 'Gabriela, Cravo e Canela traz um charme único à literatura.', 4, '2024-11-18 17:00:00'),
('U009', 'L024', 'O Quinze é uma obra que ilustra a força do sertanejo.', 5, '2024-11-19 18:00:00'),
('U010', 'L025', 'A Moreninha é uma história leve e encantadora.', 3, '2024-11-20 19:00:00');