--
-- PostgreSQL database dump
--

\restrict fasxmdEsAaAzRb3DaMoFg8SwYGJMTPurpV00ew0Tibqf0iAxUFnDLYEsbNgH64y

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
    shop_url character varying(500) DEFAULT ''::character varying NOT NULL,
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

COPY public.parts_inventory (id, oem_number, part_name, photo_url, brand, model, body_code, year_start, year_end, address, store_name, phone, shop_url, quantity, price, condition, updated_at) FROM stdin;
81	12305-AA020	Масляный поддон Toyota Land Cruiser 200	https://static.baza.drom.ru/drom/1770873318866_bulletin	Toyota	Land Cruiser 200	\N	2012	2020	г. Казань, ул. Транспортная, 64	Автоопт	+7-971-551-40-94	https://baza.drom.ru/g17981539075.html	19	3346.00	new	2026-04-07 09:58:00.967234
3	17801-24054	Воздушный фильтр Mitsubishi Pajero Sport	https://static.baza.drom.ru/drom/1717038538306_bulletin	Mitsubishi	Pajero Sport	\N	1999	2004	г. Новокузнецк, ул. Транспортная, 42	Exist	+7-985-400-91-97	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-vozdushnyj-cena-aktualna-dlja-vseh-avto-v-objavlenii-119881525.html	9	1973.00	used	2026-04-07 09:48:18.384505
5	22401-AA560	Свечи зажигания (4 шт) Honda Accord	https://static.baza.drom.ru/drom/1772175679281_bulletin	Honda	Accord	\N	2015	2022	г. Санкт-Петербург, ул. Кирова, 33	Автозапчасти24	+7-988-750-63-37	https://baza.drom.ru/g17707630243.html	16	1038.00	used	2026-04-07 09:48:23.609488
6	16400-32519	Радиатор Subaru Outback	https://static.baza.drom.ru/drom/1715051547311_bulletin	Subaru	Outback	\N	1998	2008	г. Казань, ул. Курако, 35	Автозапчасти24	+7-969-870-69-55	https://baza.drom.ru/novosibirsk/sell_spare_parts/radiator-toyota-avensis-119272506.html	2	11834.00	new	2026-04-07 09:48:26.196909
7	27060-56730	Генератор Nissan Qashqai	https://static.baza.drom.ru/drom/1770642186414_bulletin	Nissan	Qashqai	\N	2006	2015	г. Санкт-Петербург, ул. Ленина, 88	Автодок	+7-943-359-18-64	https://baza.drom.ru/novosibirsk/sell_spare_parts/generator-caterpillar-d9r-d6r-133649208.html	13	13356.00	used	2026-04-07 09:48:28.941838
9	48520-28974	Амортизатор задний Mitsubishi Lancer	https://static.baza.drom.ru/drom/1716529840985_bulletin	Mitsubishi	Lancer	\N	2000	2007	г. Кемерово, ул. Курако, 21	Авторазбор №1	+7-990-233-89-11	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	4	6921.00	new	2026-04-07 09:48:34.283658
11	22401-98444	Свечи зажигания (4 шт) Mitsubishi Lancer	https://static.baza.drom.ru/drom/1772175679281_bulletin	Mitsubishi	Lancer	\N	2006	2011	г. Санкт-Петербург, ул. Кирова, 97	Дром Запчасти	+7-990-687-13-53	https://baza.drom.ru/g17707630243.html	5	1103.00	new	2026-04-07 09:48:41.996949
12	04465-0W020	Тормозные колодки передние Nissan Qashqai	https://static.baza.drom.ru/drom/1729247023243_bulletin	Nissan	Qashqai	\N	2008	2018	г. Москва, ул. Транспортная, 5	Автоопт	+7-962-582-68-59	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	22	3102.00	used	2026-04-07 09:48:45.220617
14	23300-0W010	Топливный фильтр Kia Ceed	https://static.baza.drom.ru/drom/1770873353904_bulletin	Kia	Ceed	\N	2007	2016	г. Кемерово, ул. Транспортная, 98	Exist	+7-915-662-20-24	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-separator-s-podogrevom-howo-t5g-sitrak-t-j-g17981540458.html	7	1473.00	used	2026-04-07 09:48:50.065334
16	04465-93827	Тормозные колодки передние Mazda 6	https://static.baza.drom.ru/drom/1729247023243_bulletin	Mazda	6	\N	2005	2014	г. Новосибирск, ул. Ленина, 42	Дром Запчасти	+7-960-345-48-20	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	7	2275.00	new	2026-04-07 09:48:55.021251
17	27060-14085	Генератор Kia Optima	https://static.baza.drom.ru/drom/1770642186414_bulletin	Kia	Optima	\N	2009	2017	г. Казань, ул. Кирова, 45	Exist	+7-990-262-23-75	https://baza.drom.ru/novosibirsk/sell_spare_parts/generator-caterpillar-d9r-d6r-133649208.html	21	15646.00	used	2026-04-07 09:48:57.445984
19	90916-03089	Термостат Subaru Impreza	https://static.baza.drom.ru/drom/1670769850835_bulletin	Subaru	Impreza	\N	2009	2017	г. Москва, ул. Ленина, 59	АвтоМир	+7-984-635-89-46	https://baza.drom.ru/novosibirsk/sell_spare_parts/termostat-bmw-7-series-f01-n54b30-106879755.html	10	2125.00	used	2026-04-07 09:49:02.308663
21	04466-49495	Тормозные колодки задние Mazda CX-5	https://static.baza.drom.ru/drom/1729247023243_bulletin	Mazda	CX-5	\N	2000	2008	г. Новокузнецк, ул. Кирова, 8	Exist	+7-903-933-44-20	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	8	1488.00	new	2026-04-07 09:49:06.884735
23	28100-0W030	Стартер Mitsubishi Lancer	https://static.baza.drom.ru/drom/1772175678828_bulletin	Mitsubishi	Lancer	\N	1999	2006	г. Санкт-Петербург, ул. Ленина, 64	Автоопт	+7-975-924-50-46	https://baza.drom.ru/novosibirsk/sell_spare_parts/starter-mitsubishi-pajero-challenger-delica-delica-spacegear-l200-strada-md164977-g17707629212.html	1	14593.00	new	2026-04-07 09:49:14.07848
25	48510-10186	Амортизатор передний Hyundai Tucson	https://static.baza.drom.ru/drom/1716529840985_bulletin	Hyundai	Tucson	\N	2008	2014	г. Екатеринбург, ул. Курако, 43	Дром Запчасти	+7-940-944-59-40	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	24	3211.00	used	2026-04-07 09:49:19.333936
27	27060-31852	Генератор Mazda MX-5	https://static.baza.drom.ru/drom/1770642186414_bulletin	Mazda	MX-5	\N	1999	2009	г. Москва, ул. Транспортная, 79	Авторазбор №1	+7-905-103-64-48	https://baza.drom.ru/novosibirsk/sell_spare_parts/generator-caterpillar-d9r-d6r-133649208.html	14	9880.00	used	2026-04-07 09:49:24.489164
28	28100-89005	Стартер Toyota Camry	https://static.baza.drom.ru/drom/1772175678828_bulletin	Toyota	Camry	\N	2012	2021	г. Москва, ул. Кирова, 92	Автоопт	+7-916-926-92-39	https://baza.drom.ru/novosibirsk/sell_spare_parts/starter-mitsubishi-pajero-challenger-delica-delica-spacegear-l200-strada-md164977-g17707629212.html	9	14091.00	used	2026-04-07 09:49:27.124605
30	12305-AA020	Масляный поддон Mazda CX-9	https://static.baza.drom.ru/drom/1770873318866_bulletin	Mazda	CX-9	\N	1996	2004	г. Красноярск, ул. Кирова, 52	Авторазбор №1	+7-976-748-11-19	https://baza.drom.ru/g17981539075.html	21	2146.00	used	2026-04-07 09:49:31.917506
31	48520-09L85	Амортизатор задний Nissan Patrol	https://static.baza.drom.ru/drom/1716529840985_bulletin	Nissan	Patrol	\N	2002	2012	г. Новосибирск, ул. Ленина, 56	Автоопт	+7-937-346-57-46	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	8	5874.00	new	2026-04-07 09:49:34.651848
34	12305-AA020	Масляный поддон Mazda CX-9	https://static.baza.drom.ru/drom/1770873318866_bulletin	Mazda	CX-9	\N	2000	2006	г. Москва, ул. Транспортная, 75	АвтоМир	+7-955-803-90-42	https://baza.drom.ru/g17981539075.html	24	2081.00	new	2026-04-07 09:49:44.863838
37	04465-0W020	Тормозные колодки передние Honda Fit	https://static.baza.drom.ru/drom/1729247023243_bulletin	Honda	Fit	\N	2011	2019	г. Москва, ул. Курако, 77	АвтоМир	+7-934-391-70-27	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	13	3538.00	new	2026-04-07 09:49:52.125667
39	23300-47154	Топливный фильтр Subaru WRX	https://static.baza.drom.ru/drom/1770873353904_bulletin	Subaru	WRX	\N	2003	2010	г. Кемерово, ул. Транспортная, 75	Авторазбор №1	+7-930-416-35-14	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-separator-s-podogrevom-howo-t5g-sitrak-t-j-g17981540458.html	19	770.00	used	2026-04-07 09:49:57.275552
40	16400-0W210	Радиатор Mitsubishi Pajero Sport	https://static.baza.drom.ru/drom/1715051547311_bulletin	Mitsubishi	Pajero Sport	\N	2005	2010	г. Москва, ул. Курако, 78	АвтоМир	+7-992-585-41-37	https://baza.drom.ru/novosibirsk/sell_spare_parts/radiator-toyota-avensis-119272506.html	20	8397.00	used	2026-04-07 09:52:43.488259
42	15208-AA100	Масляный фильтр Subaru Forester	https://static.baza.drom.ru/drom/1716531250287_bulletin	Subaru	Forester	\N	2014	2021	г. Санкт-Петербург, ул. Ленина, 44	Авторазбор №1	+7-977-409-13-10	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-masljanyj-kartridzh-cena-aktualna-dlja-vseh-avto-v-objavlenii-119730121.html	14	888.00	new	2026-04-07 09:52:48.915259
44	22401-AA560	Свечи зажигания (4 шт) Mazda CX-9	https://static.baza.drom.ru/drom/1772175679281_bulletin	Mazda	CX-9	\N	2001	2009	г. Санкт-Петербург, ул. Курако, 32	Автоопт	+7-987-613-63-96	https://baza.drom.ru/g17707630243.html	6	1195.00	new	2026-04-07 09:52:55.430716
46	04466-34588	Тормозные колодки задние Subaru WRX	https://static.baza.drom.ru/drom/1729247023243_bulletin	Subaru	WRX	\N	2013	2020	г. Екатеринбург, ул. Курако, 26	Автоопт	+7-908-130-22-83	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	1	2446.00	used	2026-04-07 09:53:01.85368
48	27060-0W070	Генератор Honda Fit	https://static.baza.drom.ru/drom/1770642186414_bulletin	Honda	Fit	\N	2006	2016	г. Санкт-Петербург, ул. Курако, 86	Автодок	+7-920-840-68-27	https://baza.drom.ru/novosibirsk/sell_spare_parts/generator-caterpillar-d9r-d6r-133649208.html	12	11837.00	new	2026-04-07 09:53:07.259015
49	90916-03089	Термостат Honda CR-V	https://static.baza.drom.ru/drom/1670769850835_bulletin	Honda	CR-V	\N	2004	2013	г. Москва, ул. Ленина, 86	Автодок	+7-959-938-59-12	https://baza.drom.ru/novosibirsk/sell_spare_parts/termostat-bmw-7-series-f01-n54b30-106879755.html	12	1261.00	used	2026-04-07 09:53:10.09338
51	31210-61506	Ступица передняя Hyundai Solaris	https://static.baza.drom.ru/drom/1684953011971_bulletin	Hyundai	Solaris	\N	2010	2020	г. Красноярск, ул. Курако, 74	Exist	+7-986-281-14-40	https://baza.drom.ru/novosibirsk/sell_spare_parts/stupica-pravaja-perednjaja-w212-110869688.html	4	5461.00	used	2026-04-07 09:53:16.01426
53	48520-09L85	Амортизатор задний Mitsubishi Outlander	https://static.baza.drom.ru/drom/1716529840985_bulletin	Mitsubishi	Outlander	\N	2005	2014	г. Екатеринбург, ул. Курако, 14	ЗапчастиКузбасс	+7-920-959-99-53	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	8	4842.00	used	2026-04-07 09:53:21.277972
54	17801-24890	Воздушный фильтр Honda Civic	https://static.baza.drom.ru/drom/1717038538306_bulletin	Honda	Civic	\N	2008	2015	г. Кемерово, ул. Ленина, 94	Exist	+7-990-504-38-77	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-vozdushnyj-cena-aktualna-dlja-vseh-avto-v-objavlenii-119881525.html	23	1464.00	new	2026-04-07 09:53:25.385797
56	15208-23414	Масляный фильтр Kia Optima	https://static.baza.drom.ru/drom/1716531250287_bulletin	Kia	Optima	\N	1999	2005	г. Кемерово, ул. Кирова, 22	Авторазбор №1	+7-959-110-66-62	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-masljanyj-kartridzh-cena-aktualna-dlja-vseh-avto-v-objavlenii-119730121.html	19	1263.00	new	2026-04-07 09:53:30.858376
58	04466-10920	Тормозные колодки задние Kia Sportage	https://static.baza.drom.ru/drom/1729247023243_bulletin	Kia	Sportage	\N	2001	2010	г. Новокузнецк, ул. Ленина, 97	ЗапчастиКузбасс	+7-929-573-46-79	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	5	1470.00	new	2026-04-07 09:53:36.683353
60	13568-88125	Ремень ГРМ Mitsubishi Pajero	https://static.baza.drom.ru/drom/1741949867079_bulletin	Mitsubishi	Pajero	\N	2001	2010	г. Кемерово, ул. Транспортная, 22	Автоопт	+7-928-907-40-18	https://baza.drom.ru/novosibirsk/sell_spare_parts/komplekt-grm-subaru-s-originalnym-remnem-13028aa240-13028aa250-104867105.html	18	1802.00	new	2026-04-07 09:53:42.847285
62	17801-0V010	Воздушный фильтр Mazda MX-5	https://static.baza.drom.ru/drom/1717038538306_bulletin	Mazda	MX-5	\N	2013	2018	г. Новокузнецк, ул. Кирова, 34	Автодок	+7-925-623-22-94	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-vozdushnyj-cena-aktualna-dlja-vseh-avto-v-objavlenii-119881525.html	19	885.00	new	2026-04-07 09:53:48.334474
64	23300-0W010	Топливный фильтр Nissan Qashqai	https://static.baza.drom.ru/drom/1770873353904_bulletin	Nissan	Qashqai	\N	1997	2002	г. Санкт-Петербург, ул. Кирова, 37	ЗапчастиКузбасс	+7-933-155-37-37	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-separator-s-podogrevom-howo-t5g-sitrak-t-j-g17981540458.html	19	1118.00	used	2026-04-07 09:53:54.283052
65	28100-83766	Стартер Toyota Camry	https://static.baza.drom.ru/drom/1772175678828_bulletin	Toyota	Camry	\N	2001	2006	г. Казань, ул. Ленина, 42	Автоопт	+7-978-425-77-46	https://baza.drom.ru/novosibirsk/sell_spare_parts/starter-mitsubishi-pajero-challenger-delica-delica-spacegear-l200-strada-md164977-g17707629212.html	18	13540.00	used	2026-04-07 09:53:58.989023
67	16400-0W210	Радиатор Kia Ceed	https://static.baza.drom.ru/drom/1715051547311_bulletin	Kia	Ceed	\N	2012	2021	г. Санкт-Петербург, ул. Транспортная, 50	Автозапчасти24	+7-991-493-76-34	https://baza.drom.ru/novosibirsk/sell_spare_parts/radiator-toyota-avensis-119272506.html	13	10826.00	new	2026-04-07 09:54:06.999691
69	23300-0W010	Топливный фильтр Honda CR-V	https://static.baza.drom.ru/drom/1770873353904_bulletin	Honda	CR-V	\N	2007	2012	г. Москва, ул. Транспортная, 21	Автодок	+7-983-635-15-93	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-separator-s-podogrevom-howo-t5g-sitrak-t-j-g17981540458.html	14	1250.00	used	2026-04-07 09:54:13.636682
80	15208-AA100	Масляный фильтр Honda Accord	https://static.baza.drom.ru/drom/1716531250287_bulletin	Honda	Accord	\N	1998	2003	г. Кемерово, ул. Курако, 32	Дром Запчасти	+7-913-953-18-20	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-masljanyj-kartridzh-cena-aktualna-dlja-vseh-avto-v-objavlenii-119730121.html	23	1006.00	used	2026-04-07 09:57:53.718091
82	15208-23039	Масляный фильтр Nissan Patrol	https://static.baza.drom.ru/drom/1716531250287_bulletin	Nissan	Patrol	\N	2008	2017	г. Новосибирск, ул. Транспортная, 37	ЗапчастиКузбасс	+7-978-343-63-60	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-masljanyj-kartridzh-cena-aktualna-dlja-vseh-avto-v-objavlenii-119730121.html	9	1347.00	new	2026-04-07 09:58:14.082532
84	04465-91664	Тормозные колодки передние Nissan Qashqai	https://static.baza.drom.ru/drom/1729247023243_bulletin	Nissan	Qashqai	\N	2015	2023	г. Новосибирск, ул. Транспортная, 25	ЗапчастиКузбасс	+7-917-600-78-37	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	4	3366.00	new	2026-04-07 09:58:31.083698
85	12305-AA020	Масляный поддон Subaru Impreza	https://static.baza.drom.ru/drom/1770873318866_bulletin	Subaru	Impreza	\N	2012	2022	г. Казань, ул. Кирова, 22	Авторазбор №1	+7-982-356-86-39	https://baza.drom.ru/g17981539075.html	10	2990.00	new	2026-04-07 09:58:36.499607
86	12305-AA020	Масляный поддон Kia Ceed	https://static.baza.drom.ru/drom/1770873318866_bulletin	Kia	Ceed	\N	2005	2013	г. Кемерово, ул. Ленина, 3	Автодок	+7-987-408-25-96	https://baza.drom.ru/g17981539075.html	20	3243.00	new	2026-04-07 09:58:43.680939
88	12305-33679	Масляный поддон Hyundai Elantra	https://static.baza.drom.ru/drom/1770873318866_bulletin	Hyundai	Elantra	\N	1999	2005	г. Кемерово, ул. Ленина, 82	Автодок	+7-930-979-18-96	https://baza.drom.ru/g17981539075.html	15	3442.00	used	2026-04-07 09:58:58.304637
90	22401-AA560	Свечи зажигания (4 шт) Honda CR-V	https://static.baza.drom.ru/drom/1772175679281_bulletin	Honda	CR-V	\N	2013	2021	г. Красноярск, ул. Курако, 42	Автоопт	+7-901-369-88-51	https://baza.drom.ru/g17707630243.html	19	674.00	used	2026-04-07 09:59:11.651224
91	16400-0W210	Радиатор Kia Sorento	https://static.baza.drom.ru/drom/1715051547311_bulletin	Kia	Sorento	\N	2009	2018	г. Кемерово, ул. Транспортная, 85	Дром Запчасти	+7-937-190-45-87	https://baza.drom.ru/novosibirsk/sell_spare_parts/radiator-toyota-avensis-119272506.html	19	8546.00	new	2026-04-07 09:59:19.013476
92	12305-37357	Масляный поддон Honda CR-V	https://static.baza.drom.ru/drom/1770873318866_bulletin	Honda	CR-V	\N	2009	2018	г. Новосибирск, ул. Кирова, 16	Автодок	+7-996-398-80-96	https://baza.drom.ru/g17981539075.html	23	3016.00	new	2026-04-07 09:59:25.037152
94	17801-48885	Воздушный фильтр Honda Fit	https://static.baza.drom.ru/drom/1717038538306_bulletin	Honda	Fit	\N	1996	2005	г. Санкт-Петербург, ул. Кирова, 72	ЗапчастиКузбасс	+7-937-843-68-30	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-vozdushnyj-cena-aktualna-dlja-vseh-avto-v-objavlenii-119881525.html	11	1924.00	used	2026-04-07 09:59:39.203482
98	15208-AA100	Масляный фильтр Kia Rio	\N	Kia	Rio	\N	2002	2010	г. Москва, ул. Ленина, 26	Автоопт	+7-915-183-76-19		5	1421.00	new	2026-04-07 09:38:12.808409
99	15208-AA100	Масляный фильтр Mazda CX-5	\N	Mazda	CX-5	\N	2011	2017	г. Екатеринбург, ул. Транспортная, 27	Exist	+7-978-827-45-47		7	1144.00	new	2026-04-07 09:38:12.808409
100	27060-0W070	Генератор Honda Pilot	\N	Honda	Pilot	\N	1995	2001	г. Кемерово, ул. Курако, 66	ЗапчастиКузбасс	+7-989-296-97-36		11	18323.00	used	2026-04-07 09:38:12.808409
1	48510-17023	Амортизатор передний Nissan Patrol	https://static.baza.drom.ru/drom/1716529840985_bulletin	Nissan	Patrol	\N	2013	2018	г. Казань, ул. Кирова, 34	Дром Запчасти	+7-982-184-94-29	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	25	6980.00	new	2026-04-07 09:48:13.843797
71	13568-09070	Ремень ГРМ Toyota Corolla	https://static.baza.drom.ru/drom/1741949867079_bulletin	Toyota	Corolla	\N	2015	2020	г. Екатеринбург, ул. Транспортная, 62	Автоопт	+7-965-553-89-23	https://baza.drom.ru/novosibirsk/sell_spare_parts/komplekt-grm-subaru-s-originalnym-remnem-13028aa240-13028aa250-104867105.html	14	1652.00	used	2026-04-07 09:54:19.376906
72	22401-AA560	Свечи зажигания (4 шт) Toyota Camry	https://static.baza.drom.ru/drom/1772175679281_bulletin	Toyota	Camry	\N	2005	2010	г. Кемерово, ул. Транспортная, 97	Exist	+7-971-307-87-14	https://baza.drom.ru/g17707630243.html	25	953.00	new	2026-04-07 09:54:22.367998
74	12305-AA020	Масляный поддон Toyota Land Cruiser 200	https://static.baza.drom.ru/drom/1770873318866_bulletin	Toyota	Land Cruiser 200	\N	2007	2012	г. Кемерово, ул. Курако, 33	Дром Запчасти	+7-903-459-33-68	https://baza.drom.ru/g17981539075.html	20	4375.00	new	2026-04-07 09:54:29.282706
75	90916-49696	Термостат Kia Optima	https://static.baza.drom.ru/drom/1670769850835_bulletin	Kia	Optima	\N	2012	2020	г. Красноярск, ул. Транспортная, 86	Дром Запчасти	+7-955-563-12-24	https://baza.drom.ru/novosibirsk/sell_spare_parts/termostat-bmw-7-series-f01-n54b30-106879755.html	13	1106.00	new	2026-04-07 09:54:32.41336
77	12305-AA020	Масляный поддон Toyota Highlander	https://static.baza.drom.ru/drom/1770873318866_bulletin	Toyota	Highlander	\N	2010	2018	г. Москва, ул. Транспортная, 46	Автодок	+7-933-851-18-97	https://baza.drom.ru/g17981539075.html	19	3788.00	new	2026-04-07 09:54:38.034729
78	13568-19225	Ремень ГРМ Toyota Highlander	https://static.baza.drom.ru/drom/1741949867079_bulletin	Toyota	Highlander	\N	2001	2007	г. Кемерово, ул. Транспортная, 4	Авторазбор №1	+7-946-169-63-41	https://baza.drom.ru/novosibirsk/sell_spare_parts/komplekt-grm-subaru-s-originalnym-remnem-13028aa240-13028aa250-104867105.html	25	1543.00	new	2026-04-07 09:54:40.454343
96	15208-AA100	Масляный фильтр Mitsubishi Lancer	https://static.baza.drom.ru/drom/1716531250287_bulletin	Mitsubishi	Lancer	\N	2012	2020	г. Москва, ул. Курако, 97	Автоопт	+7-912-887-38-68	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-masljanyj-kartridzh-cena-aktualna-dlja-vseh-avto-v-objavlenii-119730121.html	19	1359.00	used	2026-04-07 09:59:53.528822
97	16400-0W210	Радиатор Hyundai Tucson	https://baza.drom.ru/resources/img/drom-240.png	Hyundai	Tucson	\N	2014	2023	г. Москва, ул. Курако, 72	АвтоМир	+7-960-165-88-66	https://baza.drom.ru/novosibirsk/sell_spare_parts/radiator-toyota-avensis-119272506.html	8	9512.00	new	2026-04-07 10:00:01.742486
2	13568-09070	Ремень ГРМ Nissan X-Trail	https://static.baza.drom.ru/drom/1741949867079_bulletin	Nissan	X-Trail	\N	2000	2010	г. Санкт-Петербург, ул. Транспортная, 60	Автодок	+7-985-800-12-41	https://baza.drom.ru/novosibirsk/sell_spare_parts/komplekt-grm-subaru-s-originalnym-remnem-13028aa240-13028aa250-104867105.html	21	2619.00	new	2026-04-07 09:48:16.000342
4	04466-77137	Тормозные колодки задние Honda Civic	https://static.baza.drom.ru/drom/1729247023243_bulletin	Honda	Civic	\N	2014	2020	г. Новокузнецк, ул. Транспортная, 99	Exist	+7-968-294-61-49	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	10	1417.00	new	2026-04-07 09:48:21.231915
8	28100-0W030	Стартер Nissan Juke	https://static.baza.drom.ru/drom/1772175678828_bulletin	Nissan	Juke	\N	1996	2006	г. Екатеринбург, ул. Транспортная, 93	ЗапчастиКузбасс	+7-917-299-51-85	https://baza.drom.ru/novosibirsk/sell_spare_parts/starter-mitsubishi-pajero-challenger-delica-delica-spacegear-l200-strada-md164977-g17707629212.html	7	8766.00	used	2026-04-07 09:48:31.426469
10	17801-0V010	Воздушный фильтр Mitsubishi Outlander	https://static.baza.drom.ru/drom/1717038538306_bulletin	Mitsubishi	Outlander	\N	2009	2015	г. Новокузнецк, ул. Ленина, 53	Автодок	+7-988-304-99-14	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-vozdushnyj-cena-aktualna-dlja-vseh-avto-v-objavlenii-119881525.html	5	1777.00	used	2026-04-07 09:48:38.84662
13	13568-82619	Ремень ГРМ Nissan Patrol	https://static.baza.drom.ru/drom/1741949867079_bulletin	Nissan	Patrol	\N	1996	2005	г. Красноярск, ул. Кирова, 81	ЗапчастиКузбасс	+7-944-154-41-43	https://baza.drom.ru/novosibirsk/sell_spare_parts/komplekt-grm-subaru-s-originalnym-remnem-13028aa240-13028aa250-104867105.html	16	1264.00	new	2026-04-07 09:48:47.75005
15	16400-80365	Радиатор Mazda MX-5	https://static.baza.drom.ru/drom/1715051547311_bulletin	Mazda	MX-5	\N	2008	2014	г. Екатеринбург, ул. Ленина, 70	Автодок	+7-921-961-94-68	https://baza.drom.ru/novosibirsk/sell_spare_parts/radiator-toyota-avensis-119272506.html	22	6136.00	used	2026-04-07 09:48:52.341622
18	28100-0W030	Стартер Toyota Highlander	https://static.baza.drom.ru/drom/1772175678828_bulletin	Toyota	Highlander	\N	2002	2012	г. Санкт-Петербург, ул. Ленина, 47	Автозапчасти24	+7-971-140-31-27	https://baza.drom.ru/novosibirsk/sell_spare_parts/starter-mitsubishi-pajero-challenger-delica-delica-spacegear-l200-strada-md164977-g17707629212.html	10	14549.00	used	2026-04-07 09:49:00.01306
20	12305-AA020	Масляный поддон Mitsubishi Outlander	https://static.baza.drom.ru/drom/1770873318866_bulletin	Mitsubishi	Outlander	\N	2001	2007	г. Казань, ул. Транспортная, 14	АвтоМир	+7-962-949-53-35	https://baza.drom.ru/g17981539075.html	1	4822.00	used	2026-04-07 09:49:04.506046
22	48520-09L85	Амортизатор задний Hyundai Tucson	https://static.baza.drom.ru/drom/1716529840985_bulletin	Hyundai	Tucson	\N	2006	2015	г. Казань, ул. Кирова, 36	Автодок	+7-918-847-64-18	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	9	5350.00	new	2026-04-07 09:49:11.480718
24	04466-0W020	Тормозные колодки задние Honda Civic	https://static.baza.drom.ru/drom/1729247023243_bulletin	Honda	Civic	\N	2007	2013	г. Москва, ул. Курако, 45	ЗапчастиКузбасс	+7-987-579-38-81	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	17	2260.00	new	2026-04-07 09:49:16.814734
26	48510-09L85	Амортизатор передний Mazda MX-5	https://static.baza.drom.ru/drom/1716529840985_bulletin	Mazda	MX-5	\N	2005	2013	г. Казань, ул. Транспортная, 52	Авторазбор №1	+7-931-689-46-38	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	4	3666.00	used	2026-04-07 09:49:22.317433
29	13568-09070	Ремень ГРМ Hyundai Creta	https://static.baza.drom.ru/drom/1741949867079_bulletin	Hyundai	Creta	\N	2002	2008	г. Кемерово, ул. Курако, 43	АвтоМир	+7-947-633-22-68	https://baza.drom.ru/novosibirsk/sell_spare_parts/komplekt-grm-subaru-s-originalnym-remnem-13028aa240-13028aa250-104867105.html	15	1595.00	used	2026-04-07 09:49:29.603277
32	16400-37634	Радиатор Mazda 3	https://static.baza.drom.ru/drom/1715051547311_bulletin	Mazda	3	\N	2009	2016	г. Новосибирск, ул. Ленина, 49	Автодок	+7-902-652-23-60	https://baza.drom.ru/novosibirsk/sell_spare_parts/radiator-toyota-avensis-119272506.html	5	11835.00	new	2026-04-07 09:49:37.136197
33	48510-48545	Амортизатор передний Hyundai Tucson	https://static.baza.drom.ru/drom/1716529840985_bulletin	Hyundai	Tucson	\N	2006	2011	г. Санкт-Петербург, ул. Транспортная, 47	Автодок	+7-915-571-78-24	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	1	4179.00	new	2026-04-07 09:49:42.403063
35	48510-77853	Амортизатор передний Nissan Juke	https://static.baza.drom.ru/drom/1716529840985_bulletin	Nissan	Juke	\N	2009	2019	г. Новосибирск, ул. Транспортная, 78	Автоопт	+7-971-718-11-87	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	9	7148.00	new	2026-04-07 09:49:47.150722
36	12305-AA020	Масляный поддон Honda Fit	https://static.baza.drom.ru/drom/1770873318866_bulletin	Honda	Fit	\N	2003	2012	г. Екатеринбург, ул. Кирова, 46	Exist	+7-944-317-14-81	https://baza.drom.ru/g17981539075.html	7	4178.00	new	2026-04-07 09:49:49.624938
38	48520-09L85	Амортизатор задний Subaru Forester	https://static.baza.drom.ru/drom/1716529840985_bulletin	Subaru	Forester	\N	1997	2006	г. Новокузнецк, ул. Транспортная, 7	Автоопт	+7-905-865-83-86	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	10	4967.00	new	2026-04-07 09:49:54.790378
41	22401-AA560	Свечи зажигания (4 шт) Nissan Juke	https://static.baza.drom.ru/drom/1772175679281_bulletin	Nissan	Juke	\N	2014	2019	г. Красноярск, ул. Кирова, 16	Автодок	+7-965-380-89-97	https://baza.drom.ru/g17707630243.html	6	474.00	used	2026-04-07 09:52:46.070758
43	13568-79880	Ремень ГРМ Nissan Juke	https://static.baza.drom.ru/drom/1741949867079_bulletin	Nissan	Juke	\N	2003	2010	г. Москва, ул. Курако, 50	АвтоМир	+7-984-389-33-29	https://baza.drom.ru/novosibirsk/sell_spare_parts/komplekt-grm-subaru-s-originalnym-remnem-13028aa240-13028aa250-104867105.html	17	1998.00	used	2026-04-07 09:52:53.066549
45	28100-0W030	Стартер Mitsubishi Lancer	https://static.baza.drom.ru/drom/1772175678828_bulletin	Mitsubishi	Lancer	\N	1996	2003	г. Новокузнецк, ул. Ленина, 59	Exist	+7-972-396-92-74	https://baza.drom.ru/novosibirsk/sell_spare_parts/starter-mitsubishi-pajero-challenger-delica-delica-spacegear-l200-strada-md164977-g17707629212.html	21	13814.00	used	2026-04-07 09:52:58.488927
47	48510-09L85	Амортизатор передний Subaru Forester	https://static.baza.drom.ru/drom/1716529840985_bulletin	Subaru	Forester	\N	2014	2020	г. Кемерово, ул. Транспортная, 38	Автозапчасти24	+7-935-849-26-10	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	15	6038.00	new	2026-04-07 09:53:04.635682
50	27060-0W070	Генератор Mazda 3	https://static.baza.drom.ru/drom/1770642186414_bulletin	Mazda	3	\N	1999	2008	г. Новосибирск, ул. Курако, 96	Автодок	+7-984-774-56-47	https://baza.drom.ru/novosibirsk/sell_spare_parts/generator-caterpillar-d9r-d6r-133649208.html	17	17510.00	used	2026-04-07 09:53:13.028341
52	31210-71263	Ступица передняя Hyundai Elantra	https://static.baza.drom.ru/drom/1684953011971_bulletin	Hyundai	Elantra	\N	2009	2017	г. Красноярск, ул. Ленина, 6	Авторазбор №1	+7-925-255-87-63	https://baza.drom.ru/novosibirsk/sell_spare_parts/stupica-pravaja-perednjaja-w212-110869688.html	18	3776.00	new	2026-04-07 09:53:18.711365
55	16400-0W210	Радиатор Mitsubishi ASX	https://static.baza.drom.ru/drom/1715051547311_bulletin	Mitsubishi	ASX	\N	2002	2007	г. Екатеринбург, ул. Кирова, 47	АвтоМир	+7-928-635-54-79	https://baza.drom.ru/novosibirsk/sell_spare_parts/radiator-toyota-avensis-119272506.html	19	6196.00	used	2026-04-07 09:53:28.098017
57	15208-AA100	Масляный фильтр Nissan X-Trail	https://static.baza.drom.ru/drom/1716531250287_bulletin	Nissan	X-Trail	\N	2007	2013	г. Новосибирск, ул. Ленина, 19	Автодок	+7-999-374-45-51	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-masljanyj-kartridzh-cena-aktualna-dlja-vseh-avto-v-objavlenii-119730121.html	12	672.00	new	2026-04-07 09:53:33.420752
59	48520-09L85	Амортизатор задний Honda Accord	https://static.baza.drom.ru/drom/1716529840985_bulletin	Honda	Accord	\N	1995	2003	г. Казань, ул. Курако, 4	Дром Запчасти	+7-964-228-69-44	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	16	5424.00	used	2026-04-07 09:53:39.564016
61	28100-22563	Стартер Honda Fit	https://static.baza.drom.ru/drom/1772175678828_bulletin	Honda	Fit	\N	2000	2008	г. Новокузнецк, ул. Ленина, 13	АвтоМир	+7-980-996-83-37	https://baza.drom.ru/novosibirsk/sell_spare_parts/starter-mitsubishi-pajero-challenger-delica-delica-spacegear-l200-strada-md164977-g17707629212.html	20	8311.00	used	2026-04-07 09:53:45.626544
63	15208-AA100	Масляный фильтр Toyota Highlander	https://static.baza.drom.ru/drom/1716531250287_bulletin	Toyota	Highlander	\N	2015	2020	г. Санкт-Петербург, ул. Курако, 47	Exist	+7-916-582-71-74	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-masljanyj-kartridzh-cena-aktualna-dlja-vseh-avto-v-objavlenii-119730121.html	19	1420.00	new	2026-04-07 09:53:51.035812
66	28100-0W030	Стартер Hyundai Elantra	https://static.baza.drom.ru/drom/1772175678828_bulletin	Hyundai	Elantra	\N	2003	2013	г. Екатеринбург, ул. Кирова, 92	АвтоМир	+7-965-826-93-22	https://baza.drom.ru/novosibirsk/sell_spare_parts/starter-mitsubishi-pajero-challenger-delica-delica-spacegear-l200-strada-md164977-g17707629212.html	1	8731.00	used	2026-04-07 09:54:02.220706
68	17801-0V010	Воздушный фильтр Toyota Land Cruiser 200	https://static.baza.drom.ru/drom/1717038538306_bulletin	Toyota	Land Cruiser 200	\N	2005	2012	г. Казань, ул. Курако, 94	Авторазбор №1	+7-960-835-19-93	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-vozdushnyj-cena-aktualna-dlja-vseh-avto-v-objavlenii-119881525.html	19	1617.00	used	2026-04-07 09:54:10.600103
70	15208-AA100	Масляный фильтр Nissan X-Trail	https://static.baza.drom.ru/drom/1716531250287_bulletin	Nissan	X-Trail	\N	2001	2006	г. Новокузнецк, ул. Кирова, 60	Авторазбор №1	+7-988-348-40-57	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-masljanyj-kartridzh-cena-aktualna-dlja-vseh-avto-v-objavlenii-119730121.html	12	683.00	new	2026-04-07 09:54:16.535042
73	31210-0W010	Ступица передняя Mazda CX-5	https://static.baza.drom.ru/drom/1684953011971_bulletin	Mazda	CX-5	\N	2005	2013	г. Екатеринбург, ул. Ленина, 36	Дром Запчасти	+7-969-467-93-39	https://baza.drom.ru/novosibirsk/sell_spare_parts/stupica-pravaja-perednjaja-w212-110869688.html	7	7653.00	used	2026-04-07 09:54:24.822375
76	27060-0W070	Генератор Kia Sorento	https://static.baza.drom.ru/drom/1770642186414_bulletin	Kia	Sorento	\N	2003	2010	г. Екатеринбург, ул. Транспортная, 1	Автозапчасти24	+7-981-986-83-69	https://baza.drom.ru/novosibirsk/sell_spare_parts/generator-caterpillar-d9r-d6r-133649208.html	4	8703.00	new	2026-04-07 09:54:35.162861
79	27060-83364	Генератор Kia Sportage	https://static.baza.drom.ru/drom/1770642186414_bulletin	Kia	Sportage	\N	2015	2021	г. Новокузнецк, ул. Ленина, 8	Автодок	+7-964-288-30-79	https://baza.drom.ru/novosibirsk/sell_spare_parts/generator-caterpillar-d9r-d6r-133649208.html	1	8043.00	used	2026-04-07 09:54:43.297665
83	27060-47657	Генератор Nissan Patrol	https://static.baza.drom.ru/drom/1770642186414_bulletin	Nissan	Patrol	\N	2010	2018	г. Кемерово, ул. Курако, 75	Дром Запчасти	+7-984-957-46-56	https://baza.drom.ru/novosibirsk/sell_spare_parts/generator-caterpillar-d9r-d6r-133649208.html	2	16136.00	new	2026-04-07 09:58:19.574429
87	90916-03089	Термостат Subaru Legacy	https://static.baza.drom.ru/drom/1670769850835_bulletin	Subaru	Legacy	\N	2009	2015	г. Новосибирск, ул. Кирова, 42	Автозапчасти24	+7-909-751-30-91	https://baza.drom.ru/novosibirsk/sell_spare_parts/termostat-bmw-7-series-f01-n54b30-106879755.html	1	1043.00	used	2026-04-07 09:58:50.49733
89	48520-09L85	Амортизатор задний Nissan Qashqai	https://static.baza.drom.ru/drom/1716529840985_bulletin	Nissan	Qashqai	\N	2006	2016	г. Казань, ул. Транспортная, 83	Дром Запчасти	+7-996-577-27-57	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	4	5766.00	used	2026-04-07 09:59:04.486154
93	31210-0W010	Ступица передняя Hyundai Santa Fe	https://static.baza.drom.ru/drom/1684953011971_bulletin	Hyundai	Santa Fe	\N	2005	2010	г. Новокузнецк, ул. Транспортная, 96	Автоопт	+7-990-172-44-53	https://baza.drom.ru/novosibirsk/sell_spare_parts/stupica-pravaja-perednjaja-w212-110869688.html	11	6767.00	used	2026-04-07 09:59:32.869941
95	04465-0W020	Тормозные колодки передние Toyota Camry	https://static.baza.drom.ru/drom/1729247023243_bulletin	Toyota	Camry	\N	1997	2002	г. Санкт-Петербург, ул. Курако, 60	Автодок	+7-900-452-92-53	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	24	2866.00	new	2026-04-07 09:59:47.073416
\.


--
-- Name: parts_inventory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.parts_inventory_id_seq', 100, true);


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
-- Name: idx_shop_url; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_shop_url ON public.parts_inventory USING btree (shop_url);


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

\unrestrict fasxmdEsAaAzRb3DaMoFg8SwYGJMTPurpV00ew0Tibqf0iAxUFnDLYEsbNgH64y

