--
-- PostgreSQL database dump
--

\restrict IF87Bf5lchoGJDg6FSmPdf4RGMwBiFX5eSgB1GzZZAVe1HRLton9M0odJu1Y6Uy

-- Dumped from database version 15.17 (Debian 15.17-1.pgdg13+1)
-- Dumped by pg_dump version 15.17 (Debian 15.17-1.pgdg13+1)

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
-- Name: parts_inventory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.parts_inventory (
    id integer NOT NULL,
    oem_number character varying(50) NOT NULL,
    part_name character varying(255) NOT NULL,
    photo_url text,
    brand character varying(50),
    model character varying(100),
    body_code character varying(20),
    year_start integer,
    year_end integer,
    address text,
    store_name character varying(100),
    phone character varying(20),
    quantity integer DEFAULT 0,
    price numeric(10,2) NOT NULL,
    condition character varying(10) NOT NULL,
    updated_at timestamp without time zone DEFAULT now(),
    CONSTRAINT parts_inventory_condition_check CHECK ((upper((condition)::text) = ANY (ARRAY['NEW'::text, 'USED'::text]))),
    CONSTRAINT parts_inventory_quantity_check CHECK ((quantity >= 0))
);


--
-- Name: parts_inventory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.parts_inventory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: parts_inventory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.parts_inventory_id_seq OWNED BY public.parts_inventory.id;


--
-- Name: parts_inventory id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parts_inventory ALTER COLUMN id SET DEFAULT nextval('public.parts_inventory_id_seq'::regclass);


--
-- Data for Name: parts_inventory; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.parts_inventory (id, oem_number, part_name, photo_url, brand, model, body_code, year_start, year_end, address, store_name, phone, quantity, price, condition, updated_at) FROM stdin;
1	12345-S12-123	╨á╨░╨╝╨░ ╨║╤â╨╖╨╛╨▓╨░	\N	Honda	CR-V	RD1	1996	2001	╨ó╨₧╨Ñ╨ó╨É 12\\1	╨Ü╨ó╨ô╨£	\N	3	5000.00	used	2026-03-19 14:42:22.843591
2	43512-30360	╨ó╨╛╤Ç╨╝╨╛╨╖╨╜╨╛╨╣ ╨┤╨╕╤ü╨║ ╨┐╨╡╤Ç╨╡╨┤╨╜╨╕╨╣	https://example.com/brake-disc.jpg	Lexus	IS250	GSE20	2005	2013	╤â╨╗. ╨¢╨╡╨╜╨╕╨╜╨░ 42	╨É╨▓╤é╨╛╨¢╤Ä╨║╤ü ╨ª╨╡╨╜╤é╤Ç	+7-495-111-22-33	4	8500.00	NEW	2026-04-04 05:14:46.006806
3	04465-53320	╨Ü╨╛╨╗╨╛╨┤╨║╨╕ ╤é╨╛╤Ç╨╝╨╛╨╖╨╜╤ï╨╡ ╨┐╨╡╤Ç╨╡╨┤╨╜╨╕╨╡	https://example.com/front-pads.jpg	Lexus	IS250	GSE20	2005	2013	╤â╨╗. ╨¢╨╡╨╜╨╕╨╜╨░ 42	╨É╨▓╤é╨╛╨¢╤Ä╨║╤ü ╨ª╨╡╨╜╤é╤Ç	+7-495-111-22-33	8	4200.00	NEW	2026-04-04 05:14:46.006806
4	04466-48180	╨Ü╨╛╨╗╨╛╨┤╨║╨╕ ╤é╨╛╤Ç╨╝╨╛╨╖╨╜╤ï╨╡ ╨╖╨░╨┤╨╜╨╕╨╡	https://example.com/rear-pads.jpg	Lexus	IS250	GSE20	2005	2013	╤â╨╗. ╨ƒ╤Ç╨╛╨╝╤ï╤ê╨╗╨╡╨╜╨╜╨░╤Å 15	JapParts ╨£╨í╨Ü	+7-495-444-55-66	6	3100.00	NEW	2026-04-04 05:14:46.006806
5	90915-YZZD2	╨ñ╨╕╨╗╤î╤é╤Ç ╨╝╨░╤ü╨╗╤Å╨╜╤ï╨╣		Lexus	IS250	GSE20	2005	2013	╤â╨╗. ╨ƒ╤Ç╨╛╨╝╤ï╤ê╨╗╨╡╨╜╨╜╨░╤Å 15	JapParts ╨£╨í╨Ü	+7-495-444-55-66	15	650.00	NEW	2026-04-04 05:14:46.006806
6	17801-31090	╨ñ╨╕╨╗╤î╤é╤Ç ╨▓╨╛╨╖╨┤╤â╤ê╨╜╤ï╨╣	https://example.com/air-filter.jpg	Lexus	IS250	GSE20	2005	2013	╨┐╤Ç. ╨£╨╕╤Ç╨░ 88	╨ñ╨╕╨╗╤î╤é╤Ç-╨¿╨╛╨┐	+7-812-777-88-99	10	1800.00	NEW	2026-04-04 05:14:46.006806
7	48820-53010	╨É╨╝╨╛╤Ç╤é╨╕╨╖╨░╤é╨╛╤Ç ╨╖╨░╨┤╨╜╨╕╨╣ ╨┐╤Ç╨░╨▓╤ï╨╣		Lexus	IS250	GSE20	2005	2013	╤â╨╗. ╨í╨║╨╗╨░╨┤╤ü╨║╨░╤Å 3	╨á╨░╨╖╨▒╨╛╤Ç╨║╨░ ╨ó╨╛╨╣╨╛╤é╨░	+7-903-123-45-67	2	5500.00	USED	2026-04-04 05:14:46.006806
8	48510-59455	╨í╤é╨╛╨╣╨║╨░ ╨░╨╝╨╛╤Ç╤é╨╕╨╖╨░╤é╨╛╤Ç╨░ ╨┐╨╡╤Ç╨╡╨┤╨╜╤Å╤Å ╨╗╨╡╨▓╨░╤Å		Lexus	IS250	GSE20	2005	2013	╤â╨╗. ╨í╨║╨╗╨░╨┤╤ü╨║╨░╤Å 3	╨á╨░╨╖╨▒╨╛╤Ç╨║╨░ ╨ó╨╛╨╣╨╛╤é╨░	+7-903-123-45-67	1	7200.00	USED	2026-04-04 05:14:46.006806
9	90919-02250	╨Ü╨░╤é╤â╤ê╨║╨░ ╨╖╨░╨╢╨╕╨│╨░╨╜╨╕╤Å	https://example.com/coil.jpg	Lexus	IS250	GSE20	2005	2013	╤â╨╗. ╨¢╨╡╨╜╨╕╨╜╨░ 42	╨É╨▓╤é╨╛╨¢╤Ä╨║╤ü ╨ª╨╡╨╜╤é╤Ç	+7-495-111-22-33	12	2900.00	NEW	2026-04-04 05:14:46.006806
10	11210-31071	╨ƒ╨╛╨┤╤â╤ê╨║╨░ ╨┤╨▓╨╕╨│╨░╤é╨╡╨╗╤Å ╨┐╨╡╤Ç╨╡╨┤╨╜╤Å╤Å ╨┐╤Ç╨░╨▓╨░╤Å	https://example.com/mount.jpg	Lexus	IS250	GSE20	2005	2013	╤â╨╗. ╨É╨▓╤é╨╛╨╖╨░╨▓╨╛╨┤╤ü╨║╨░╤Å 21	Lexus-╨ö╨╡╤é╨░╨╗╨╕	+7-495-333-22-11	3	6800.00	NEW	2026-04-04 05:14:46.006806
11	43410-59426	╨á╤â╨╗╨╡╨▓╨░╤Å ╤é╤Å╨│╨░ ╨▓ ╤ü╨▒╨╛╤Ç╨╡		Lexus	IS250	GSE20	2005	2013	╤â╨╗. ╨í╨║╨╗╨░╨┤╤ü╨║╨░╤Å 3	╨á╨░╨╖╨▒╨╛╤Ç╨║╨░ ╨ó╨╛╨╣╨╛╤é╨░	+7-903-123-45-67	2	3400.00	USED	2026-04-04 05:14:46.006806
\.


--
-- Name: parts_inventory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.parts_inventory_id_seq', 11, true);


--
-- Name: parts_inventory parts_inventory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parts_inventory
    ADD CONSTRAINT parts_inventory_pkey PRIMARY KEY (id);


--
-- Name: idx_brand_model; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_brand_model ON public.parts_inventory USING btree (brand, model);


--
-- Name: idx_oem_number; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_oem_number ON public.parts_inventory USING btree (oem_number);


--
-- Name: idx_store; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_store ON public.parts_inventory USING btree (store_name);


--
-- Name: idx_years; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_years ON public.parts_inventory USING btree (year_start, year_end);


--
-- PostgreSQL database dump complete
--

\unrestrict IF87Bf5lchoGJDg6FSmPdf4RGMwBiFX5eSgB1GzZZAVe1HRLton9M0odJu1Y6Uy

