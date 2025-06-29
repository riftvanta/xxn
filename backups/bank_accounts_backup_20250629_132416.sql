--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9 (Ubuntu 16.9-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.9 (Ubuntu 16.9-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: bank_account; Type: TABLE; Schema: public; Owner: bankuser
--

CREATE TABLE public.bank_account (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    starting_balance numeric(12,2) NOT NULL,
    current_balance numeric(12,2) NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.bank_account OWNER TO bankuser;

--
-- Name: bank_account_id_seq; Type: SEQUENCE; Schema: public; Owner: bankuser
--

CREATE SEQUENCE public.bank_account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bank_account_id_seq OWNER TO bankuser;

--
-- Name: bank_account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bankuser
--

ALTER SEQUENCE public.bank_account_id_seq OWNED BY public.bank_account.id;


--
-- Name: corresponding_account; Type: TABLE; Schema: public; Owner: bankuser
--

CREATE TABLE public.corresponding_account (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    type character varying(50) NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.corresponding_account OWNER TO bankuser;

--
-- Name: corresponding_account_id_seq; Type: SEQUENCE; Schema: public; Owner: bankuser
--

CREATE SEQUENCE public.corresponding_account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.corresponding_account_id_seq OWNER TO bankuser;

--
-- Name: corresponding_account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bankuser
--

ALTER SEQUENCE public.corresponding_account_id_seq OWNED BY public.corresponding_account.id;


--
-- Name: transaction; Type: TABLE; Schema: public; Owner: bankuser
--

CREATE TABLE public.transaction (
    id integer NOT NULL,
    bank_account_id integer NOT NULL,
    corresponding_account_id integer NOT NULL,
    amount numeric(12,2) NOT NULL,
    transaction_type character varying(10) NOT NULL,
    transaction_date date NOT NULL,
    notes text,
    created_at timestamp without time zone
);


ALTER TABLE public.transaction OWNER TO bankuser;

--
-- Name: transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: bankuser
--

CREATE SEQUENCE public.transaction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.transaction_id_seq OWNER TO bankuser;

--
-- Name: transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bankuser
--

ALTER SEQUENCE public.transaction_id_seq OWNED BY public.transaction.id;


--
-- Name: bank_account id; Type: DEFAULT; Schema: public; Owner: bankuser
--

ALTER TABLE ONLY public.bank_account ALTER COLUMN id SET DEFAULT nextval('public.bank_account_id_seq'::regclass);


--
-- Name: corresponding_account id; Type: DEFAULT; Schema: public; Owner: bankuser
--

ALTER TABLE ONLY public.corresponding_account ALTER COLUMN id SET DEFAULT nextval('public.corresponding_account_id_seq'::regclass);


--
-- Name: transaction id; Type: DEFAULT; Schema: public; Owner: bankuser
--

ALTER TABLE ONLY public.transaction ALTER COLUMN id SET DEFAULT nextval('public.transaction_id_seq'::regclass);


--
-- Data for Name: bank_account; Type: TABLE DATA; Schema: public; Owner: bankuser
--

COPY public.bank_account (id, name, starting_balance, current_balance, created_at) FROM stdin;
\.


--
-- Data for Name: corresponding_account; Type: TABLE DATA; Schema: public; Owner: bankuser
--

COPY public.corresponding_account (id, name, type, created_at) FROM stdin;
\.


--
-- Data for Name: transaction; Type: TABLE DATA; Schema: public; Owner: bankuser
--

COPY public.transaction (id, bank_account_id, corresponding_account_id, amount, transaction_type, transaction_date, notes, created_at) FROM stdin;
\.


--
-- Name: bank_account_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bankuser
--

SELECT pg_catalog.setval('public.bank_account_id_seq', 1, false);


--
-- Name: corresponding_account_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bankuser
--

SELECT pg_catalog.setval('public.corresponding_account_id_seq', 1, false);


--
-- Name: transaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bankuser
--

SELECT pg_catalog.setval('public.transaction_id_seq', 1, false);


--
-- Name: bank_account bank_account_pkey; Type: CONSTRAINT; Schema: public; Owner: bankuser
--

ALTER TABLE ONLY public.bank_account
    ADD CONSTRAINT bank_account_pkey PRIMARY KEY (id);


--
-- Name: corresponding_account corresponding_account_pkey; Type: CONSTRAINT; Schema: public; Owner: bankuser
--

ALTER TABLE ONLY public.corresponding_account
    ADD CONSTRAINT corresponding_account_pkey PRIMARY KEY (id);


--
-- Name: transaction transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: bankuser
--

ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT transaction_pkey PRIMARY KEY (id);


--
-- Name: transaction transaction_bank_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bankuser
--

ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT transaction_bank_account_id_fkey FOREIGN KEY (bank_account_id) REFERENCES public.bank_account(id);


--
-- Name: transaction transaction_corresponding_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bankuser
--

ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT transaction_corresponding_account_id_fkey FOREIGN KEY (corresponding_account_id) REFERENCES public.corresponding_account(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO bankuser;


--
-- PostgreSQL database dump complete
--

