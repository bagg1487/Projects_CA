--
-- PostgreSQL database dump
--

\restrict 3r8Fh4oqerqTVBHE8JilZc0am3YI78r28SFhQk33DBsYXaO1Mzp7PEyzBKWzDcM

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
-- Name: car_models; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.car_models (
    id integer NOT NULL,
    brand character varying(50) NOT NULL,
    model character varying(100) NOT NULL,
    year_start integer,
    year_end integer,
    body_code character varying(20)
);


ALTER TABLE public.car_models OWNER TO myuser;

--
-- Name: car_models_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.car_models_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.car_models_id_seq OWNER TO myuser;

--
-- Name: car_models_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.car_models_id_seq OWNED BY public.car_models.id;


--
-- Name: inventory; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.inventory (
    id integer NOT NULL,
    part_id integer NOT NULL,
    location_id integer NOT NULL,
    quantity integer DEFAULT 0,
    price numeric(10,2) NOT NULL,
    condition character varying(10) NOT NULL,
    updated_at timestamp without time zone DEFAULT now(),
    CONSTRAINT inventory_condition_check CHECK ((upper((condition)::text) = ANY (ARRAY['NEW'::text, 'USED'::text]))),
    CONSTRAINT inventory_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.inventory OWNER TO myuser;

--
-- Name: inventory_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.inventory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.inventory_id_seq OWNER TO myuser;

--
-- Name: inventory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.inventory_id_seq OWNED BY public.inventory.id;


--
-- Name: locations; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.locations (
    id integer NOT NULL,
    address text NOT NULL,
    store_name character varying(100),
    phone character varying(20)
);


ALTER TABLE public.locations OWNER TO myuser;

--
-- Name: locations_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.locations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.locations_id_seq OWNER TO myuser;

--
-- Name: locations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.locations_id_seq OWNED BY public.locations.id;


--
-- Name: part_compatibility; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.part_compatibility (
    part_id integer NOT NULL,
    model_id integer NOT NULL
);


ALTER TABLE public.part_compatibility OWNER TO myuser;

--
-- Name: parts; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.parts (
    id integer NOT NULL,
    oem_number character varying(50) NOT NULL,
    part_name character varying(255) NOT NULL,
    photo_url text
);


ALTER TABLE public.parts OWNER TO myuser;

--
-- Name: parts_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.parts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.parts_id_seq OWNER TO myuser;

--
-- Name: parts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.parts_id_seq OWNED BY public.parts.id;


--
-- Name: car_models id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.car_models ALTER COLUMN id SET DEFAULT nextval('public.car_models_id_seq'::regclass);


--
-- Name: inventory id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.inventory ALTER COLUMN id SET DEFAULT nextval('public.inventory_id_seq'::regclass);


--
-- Name: locations id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.locations ALTER COLUMN id SET DEFAULT nextval('public.locations_id_seq'::regclass);


--
-- Name: parts id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.parts ALTER COLUMN id SET DEFAULT nextval('public.parts_id_seq'::regclass);


--
-- Data for Name: car_models; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.car_models (id, brand, model, year_start, year_end, body_code) FROM stdin;
1	Honda	CR-V	1995	2001	RD1
\.


--
-- Data for Name: inventory; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.inventory (id, part_id, location_id, quantity, price, condition, updated_at) FROM stdin;
\.


--
-- Data for Name: locations; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.locations (id, address, store_name, phone) FROM stdin;
\.


--
-- Data for Name: part_compatibility; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.part_compatibility (part_id, model_id) FROM stdin;
1	1
\.


--
-- Data for Name: parts; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.parts (id, oem_number, part_name, photo_url) FROM stdin;
1	51220-S04-003	╨¿╨░╤Ç╨╛╨▓╨░╤Å ╨╛╨┐╨╛╤Ç╨░	\N
\.


--
-- Name: car_models_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.car_models_id_seq', 1, true);


--
-- Name: inventory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.inventory_id_seq', 1, false);


--
-- Name: locations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.locations_id_seq', 1, false);


--
-- Name: parts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.parts_id_seq', 1, true);


--
-- Name: car_models car_models_brand_model_body_code_key; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.car_models
    ADD CONSTRAINT car_models_brand_model_body_code_key UNIQUE (brand, model, body_code);


--
-- Name: car_models car_models_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.car_models
    ADD CONSTRAINT car_models_pkey PRIMARY KEY (id);


--
-- Name: inventory inventory_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_pkey PRIMARY KEY (id);


--
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (id);


--
-- Name: part_compatibility part_compatibility_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.part_compatibility
    ADD CONSTRAINT part_compatibility_pkey PRIMARY KEY (part_id, model_id);


--
-- Name: parts parts_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.parts
    ADD CONSTRAINT parts_pkey PRIMARY KEY (id);


--
-- Name: idx_model_years; Type: INDEX; Schema: public; Owner: myuser
--

CREATE INDEX idx_model_years ON public.car_models USING btree (year_start, year_end);


--
-- Name: idx_oem; Type: INDEX; Schema: public; Owner: myuser
--

CREATE INDEX idx_oem ON public.parts USING btree (oem_number);


--
-- Name: inventory inventory_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.locations(id) ON DELETE CASCADE;


--
-- Name: inventory inventory_part_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_part_id_fkey FOREIGN KEY (part_id) REFERENCES public.parts(id) ON DELETE CASCADE;


--
-- Name: part_compatibility part_compatibility_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.part_compatibility
    ADD CONSTRAINT part_compatibility_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.car_models(id) ON DELETE CASCADE;


--
-- Name: part_compatibility part_compatibility_part_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.part_compatibility
    ADD CONSTRAINT part_compatibility_part_id_fkey FOREIGN KEY (part_id) REFERENCES public.parts(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict 3r8Fh4oqerqTVBHE8JilZc0am3YI78r28SFhQk33DBsYXaO1Mzp7PEyzBKWzDcM

