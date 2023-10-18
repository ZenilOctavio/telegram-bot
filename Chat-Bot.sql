CREATE TABLE `Usuario` (
  `id` bigint PRIMARY KEY,
  `nombres` varchar(100),
  `apellidos` varchar(150),
  `chat_id` bigint
);

CREATE TABLE `Nota` (
  `id` bigint PRIMARY KEY,
  `id_usuario` bigint,
  `titulo` varchar(50),
  `descripcion` varchar(300)
);

ALTER TABLE `Nota` ADD FOREIGN KEY (`id_usuario`) REFERENCES `Usuario` (`id`);
