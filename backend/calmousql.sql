--
-- PostgreSQL database dump
--

\restrict jWmYsHvHUelfN6L70qFef3F59C1WjpiLcmSFI2Ul63MMka0iI2WAhrJ5WlHgcin

-- Dumped from database version 16.10
-- Dumped by pg_dump version 18.0

-- Started on 2025-10-23 09:15:40 -03

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE meu_banco;
--
-- TOC entry 3496 (class 1262 OID 16384)
-- Name: meu_banco; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE meu_banco WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


\unrestrict jWmYsHvHUelfN6L70qFef3F59C1WjpiLcmSFI2Ul63MMka0iI2WAhrJ5WlHgcin
\connect meu_banco
\restrict jWmYsHvHUelfN6L70qFef3F59C1WjpiLcmSFI2Ul63MMka0iI2WAhrJ5WlHgcin

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 853 (class 1247 OID 16391)
-- Name: tipo_avaliacao; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.tipo_avaliacao AS ENUM (
    'ansiedade',
    'depressao',
    'estresse',
    'burnout',
    'Avaliação de Estresse',
    'Questionário de Burnout'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 222 (class 1259 OID 16538)
-- Name: classificacoes_humor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.classificacoes_humor (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    nivel_humor integer,
    sentimento_principal character varying(100),
    notas text,
    data_classificacao timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 221 (class 1259 OID 16537)
-- Name: classificacoes_humor_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.classificacoes_humor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3497 (class 0 OID 0)
-- Dependencies: 221
-- Name: classificacoes_humor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.classificacoes_humor_id_seq OWNED BY public.classificacoes_humor.id;


--
-- TOC entry 220 (class 1259 OID 16524)
-- Name: enderecos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.enderecos (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    pais character varying(100),
    estado character varying(100),
    cidade character varying(100),
    rua character varying(255),
    numero character varying(20),
    complemento character varying(100),
    cep character varying(20)
);


--
-- TOC entry 219 (class 1259 OID 16523)
-- Name: enderecos_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.enderecos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3498 (class 0 OID 0)
-- Dependencies: 219
-- Name: enderecos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.enderecos_id_seq OWNED BY public.enderecos.id;


--
-- TOC entry 226 (class 1259 OID 16568)
-- Name: historico_meditacoes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.historico_meditacoes (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    meditacao_id integer NOT NULL,
    data_conclusao timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    duracao_real_minutos integer
);


--
-- TOC entry 225 (class 1259 OID 16567)
-- Name: historico_meditacoes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.historico_meditacoes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3499 (class 0 OID 0)
-- Dependencies: 225
-- Name: historico_meditacoes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.historico_meditacoes_id_seq OWNED BY public.historico_meditacoes.id;


--
-- TOC entry 218 (class 1259 OID 16515)
-- Name: meditacoes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.meditacoes (
    id integer NOT NULL,
    titulo character varying(255) NOT NULL,
    descricao text,
    duracao_minutos integer,
    url_audio text,
    tipo character varying(100),
    categoria character varying(100),
    imagem_capa text
);


--
-- TOC entry 217 (class 1259 OID 16514)
-- Name: meditacoes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.meditacoes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3500 (class 0 OID 0)
-- Dependencies: 217
-- Name: meditacoes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.meditacoes_id_seq OWNED BY public.meditacoes.id;


--
-- TOC entry 228 (class 1259 OID 16586)
-- Name: notificacoes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notificacoes (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    titulo character varying(255) NOT NULL,
    mensagem text,
    data_envio timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    lida boolean DEFAULT false
);


--
-- TOC entry 227 (class 1259 OID 16585)
-- Name: notificacoes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.notificacoes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3501 (class 0 OID 0)
-- Dependencies: 227
-- Name: notificacoes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.notificacoes_id_seq OWNED BY public.notificacoes.id;


--
-- TOC entry 224 (class 1259 OID 16553)
-- Name: resultados_avaliacoes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.resultados_avaliacoes (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    tipo public.tipo_avaliacao NOT NULL,
    respostas jsonb,
    resultado_score integer,
    resultado_texto text,
    data_avaliacao timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 223 (class 1259 OID 16552)
-- Name: resultados_avaliacoes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.resultados_avaliacoes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3502 (class 0 OID 0)
-- Dependencies: 223
-- Name: resultados_avaliacoes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.resultados_avaliacoes_id_seq OWNED BY public.resultados_avaliacoes.id;


--
-- TOC entry 216 (class 1259 OID 16503)
-- Name: usuarios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    nome character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password_hash text NOT NULL,
    config jsonb,
    data_cadastro timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    cpf character varying(14),
    data_nascimento date,
    tipo_sanguineo character varying(3),
    alergias text,
    foto_perfil text
);


--
-- TOC entry 215 (class 1259 OID 16502)
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3503 (class 0 OID 0)
-- Dependencies: 215
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- TOC entry 3301 (class 2604 OID 16541)
-- Name: classificacoes_humor id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.classificacoes_humor ALTER COLUMN id SET DEFAULT nextval('public.classificacoes_humor_id_seq'::regclass);


--
-- TOC entry 3300 (class 2604 OID 16527)
-- Name: enderecos id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enderecos ALTER COLUMN id SET DEFAULT nextval('public.enderecos_id_seq'::regclass);


--
-- TOC entry 3305 (class 2604 OID 16571)
-- Name: historico_meditacoes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historico_meditacoes ALTER COLUMN id SET DEFAULT nextval('public.historico_meditacoes_id_seq'::regclass);


--
-- TOC entry 3299 (class 2604 OID 16518)
-- Name: meditacoes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meditacoes ALTER COLUMN id SET DEFAULT nextval('public.meditacoes_id_seq'::regclass);


--
-- TOC entry 3307 (class 2604 OID 16589)
-- Name: notificacoes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notificacoes ALTER COLUMN id SET DEFAULT nextval('public.notificacoes_id_seq'::regclass);


--
-- TOC entry 3303 (class 2604 OID 16556)
-- Name: resultados_avaliacoes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resultados_avaliacoes ALTER COLUMN id SET DEFAULT nextval('public.resultados_avaliacoes_id_seq'::regclass);


--
-- TOC entry 3297 (class 2604 OID 16506)
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- TOC entry 3484 (class 0 OID 16538)
-- Dependencies: 222
-- Data for Name: classificacoes_humor; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.classificacoes_humor VALUES (2, 2, 3, 'Feliz', 'Dia produtivo!', '2025-10-23 08:27:43.679313+00');


--
-- TOC entry 3482 (class 0 OID 16524)
-- Dependencies: 220
-- Data for Name: enderecos; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 3488 (class 0 OID 16568)
-- Dependencies: 226
-- Data for Name: historico_meditacoes; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 3480 (class 0 OID 16515)
-- Dependencies: 218
-- Data for Name: meditacoes; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 3490 (class 0 OID 16586)
-- Dependencies: 228
-- Data for Name: notificacoes; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 3486 (class 0 OID 16553)
-- Dependencies: 224
-- Data for Name: resultados_avaliacoes; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 3478 (class 0 OID 16503)
-- Dependencies: 216
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.usuarios VALUES (2, 'Teste Usuario', 'teste@email.com', '$2b$12$sT9I/WWp5qZ5udAvu/hccePptbI1MYD3Q8qj648i9zxjRy7xX3PzK', NULL, '2025-10-23 07:19:54.683785+00', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.usuarios VALUES (3, 'Usuário', 'calmou@calmou.app', '$2b$12$y/0CKM0uxRGpT7756MlXjORI7FD76dLHUZvPRk4InH0FQ/XHuDUh6', '{}', '2025-10-23 07:52:44.770624+00', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.usuarios VALUES (5, 'Dyone', 'dyone', '$2b$12$RpP73ADiAP0..VaK6L/tdudn7vDMRwBvMc9G0RKMCp7TkOH4yC3OO', NULL, '2025-10-23 08:03:50.164797+00', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.usuarios VALUES (6, 'Maria Souza', 'maria@test.com', '$2b$12$S784NU6Pdd.hy9t7Kdd2TO8xP9AE9VqTzm/Am5lrVyfN7XF37NL.i', NULL, '2025-10-23 08:37:16.156574+00', NULL, NULL, NULL, NULL, NULL, NULL);


--
-- TOC entry 3504 (class 0 OID 0)
-- Dependencies: 221
-- Name: classificacoes_humor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.classificacoes_humor_id_seq', 2, true);


--
-- TOC entry 3505 (class 0 OID 0)
-- Dependencies: 219
-- Name: enderecos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.enderecos_id_seq', 1, false);


--
-- TOC entry 3506 (class 0 OID 0)
-- Dependencies: 225
-- Name: historico_meditacoes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.historico_meditacoes_id_seq', 1, false);


--
-- TOC entry 3507 (class 0 OID 0)
-- Dependencies: 217
-- Name: meditacoes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.meditacoes_id_seq', 1, false);


--
-- TOC entry 3508 (class 0 OID 0)
-- Dependencies: 227
-- Name: notificacoes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.notificacoes_id_seq', 1, false);


--
-- TOC entry 3509 (class 0 OID 0)
-- Dependencies: 223
-- Name: resultados_avaliacoes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.resultados_avaliacoes_id_seq', 1, false);


--
-- TOC entry 3510 (class 0 OID 0)
-- Dependencies: 215
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 7, true);


--
-- TOC entry 3321 (class 2606 OID 16546)
-- Name: classificacoes_humor classificacoes_humor_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.classificacoes_humor
    ADD CONSTRAINT classificacoes_humor_pkey PRIMARY KEY (id);


--
-- TOC entry 3319 (class 2606 OID 16531)
-- Name: enderecos enderecos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enderecos
    ADD CONSTRAINT enderecos_pkey PRIMARY KEY (id);


--
-- TOC entry 3325 (class 2606 OID 16574)
-- Name: historico_meditacoes historico_meditacoes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historico_meditacoes
    ADD CONSTRAINT historico_meditacoes_pkey PRIMARY KEY (id);


--
-- TOC entry 3317 (class 2606 OID 16522)
-- Name: meditacoes meditacoes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meditacoes
    ADD CONSTRAINT meditacoes_pkey PRIMARY KEY (id);


--
-- TOC entry 3327 (class 2606 OID 16595)
-- Name: notificacoes notificacoes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notificacoes
    ADD CONSTRAINT notificacoes_pkey PRIMARY KEY (id);


--
-- TOC entry 3323 (class 2606 OID 16561)
-- Name: resultados_avaliacoes resultados_avaliacoes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resultados_avaliacoes
    ADD CONSTRAINT resultados_avaliacoes_pkey PRIMARY KEY (id);


--
-- TOC entry 3311 (class 2606 OID 16602)
-- Name: usuarios usuarios_cpf_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_cpf_key UNIQUE (cpf);


--
-- TOC entry 3313 (class 2606 OID 16513)
-- Name: usuarios usuarios_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_email_key UNIQUE (email);


--
-- TOC entry 3315 (class 2606 OID 16511)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- TOC entry 3329 (class 2606 OID 16547)
-- Name: classificacoes_humor classificacoes_humor_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.classificacoes_humor
    ADD CONSTRAINT classificacoes_humor_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id) ON DELETE CASCADE;


--
-- TOC entry 3328 (class 2606 OID 16532)
-- Name: enderecos enderecos_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enderecos
    ADD CONSTRAINT enderecos_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id) ON DELETE CASCADE;


--
-- TOC entry 3331 (class 2606 OID 16580)
-- Name: historico_meditacoes historico_meditacoes_meditacao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historico_meditacoes
    ADD CONSTRAINT historico_meditacoes_meditacao_id_fkey FOREIGN KEY (meditacao_id) REFERENCES public.meditacoes(id);


--
-- TOC entry 3332 (class 2606 OID 16575)
-- Name: historico_meditacoes historico_meditacoes_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historico_meditacoes
    ADD CONSTRAINT historico_meditacoes_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id) ON DELETE CASCADE;


--
-- TOC entry 3333 (class 2606 OID 16596)
-- Name: notificacoes notificacoes_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notificacoes
    ADD CONSTRAINT notificacoes_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id) ON DELETE CASCADE;


--
-- TOC entry 3330 (class 2606 OID 16562)
-- Name: resultados_avaliacoes resultados_avaliacoes_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resultados_avaliacoes
    ADD CONSTRAINT resultados_avaliacoes_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id) ON DELETE CASCADE;


-- Completed on 2025-10-23 09:15:40 -03

--
-- PostgreSQL database dump complete
--

\unrestrict jWmYsHvHUelfN6L70qFef3F59C1WjpiLcmSFI2Ul63MMka0iI2WAhrJ5WlHgcin

