--
-- PostgreSQL database dump
--

\restrict yT9Pycu829rLWwbajUwFHhhfbsNbHrYnqPkR2TsaOt1gdT5WzWD0SeKkwtY1pNH

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
3	90916-03089	Термостат Subaru Outback	https://static.baza.drom.ru/drom/1670769850835_bulletin	Subaru	Outback	\N	2015	2020	г. Екатеринбург, ул. Транспортная, 1	Авторазбор №1	+7-931-796-57-49	https://baza.drom.ru/novosibirsk/sell_spare_parts/termostat-bmw-7-series-f01-n54b30-106879755.html	25	2100.00	used	2026-04-06 11:39:02.631553
4	17801-0V010	Воздушный фильтр Nissan X-Trail	https://static.baza.drom.ru/drom/1717038538306_bulletin	Nissan	X-Trail	\N	2011	2020	г. Красноярск, ул. Курако, 14	Автодок	+7-980-383-25-50	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-vozdushnyj-cena-aktualna-dlja-vseh-avto-v-objavlenii-119881525.html	20	822.00	used	2026-04-06 11:39:06.637954
6	48520-09L85	Амортизатор задний Hyundai Tucson	https://static.baza.drom.ru/drom/1716529840985_bulletin	Hyundai	Tucson	\N	1996	2005	г. Москва, ул. Кирова, 46	Автодок	+7-912-164-69-61	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	6	6578.00	new	2026-04-06 11:39:11.289489
8	04466-0W020	Тормозные колодки задние Nissan Teana	https://static.baza.drom.ru/drom/1729247023243_bulletin	Nissan	Teana	\N	2001	2009	г. Казань, ул. Транспортная, 66	Авторазбор №1	+7-991-369-72-13	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	13	1429.00	new	2026-04-06 11:39:15.403439
10	12305-AA020	Масляный поддон Toyota RAV4	https://static.baza.drom.ru/drom/1770873318866_bulletin	Toyota	RAV4	\N	2010	2020	г. Красноярск, ул. Курако, 12	Exist	+7-916-956-13-94	https://baza.drom.ru/g17981539075.html	3	4139.00	new	2026-04-06 11:39:19.55425
11	17801-0V010	Воздушный фильтр Kia Sorento	https://static.baza.drom.ru/drom/1717038538306_bulletin	Kia	Sorento	\N	2012	2019	г. Новосибирск, ул. Курако, 30	Автоопт	+7-956-281-45-12	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-vozdushnyj-cena-aktualna-dlja-vseh-avto-v-objavlenii-119881525.html	10	1095.00	used	2026-04-06 11:39:21.684632
13	15208-AA100	Масляный фильтр Hyundai Solaris	https://static.baza.drom.ru/drom/1722525962328_bulletin	Hyundai	Solaris	\N	1997	2002	г. Москва, ул. Кирова, 71	Exist	+7-942-102-42-89	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-masljanyj-s-5816-121720260.html	17	1379.00	new	2026-04-06 11:39:25.85307
14	27060-0W070	Генератор Hyundai Elantra	https://static.baza.drom.ru/drom/1770642186414_bulletin	Hyundai	Elantra	\N	2002	2008	г. Новосибирск, ул. Ленина, 5	Автозапчасти24	+7-985-978-44-96	https://baza.drom.ru/novosibirsk/sell_spare_parts/generator-caterpillar-d9r-d6r-133649208.html	20	18510.00	used	2026-04-06 11:39:27.78487
16	48510-09L85	Амортизатор передний Kia Rio	https://static.baza.drom.ru/drom/1716529840985_bulletin	Kia	Rio	\N	2000	2010	г. Москва, ул. Кирова, 8	АвтоМир	+7-934-506-59-64	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	25	3674.00	new	2026-04-06 11:39:32.296936
18	12305-AA020	Масляный поддон Toyota Camry	https://baza.drom.ru/resources/img/drom-240.png	Toyota	Camry	\N	1998	2003	г. Екатеринбург, ул. Транспортная, 69	Дром Запчасти	+7-934-434-38-70	https://baza.drom.ru/g17981539075.html	14	3375.00	used	2026-04-06 11:39:38.232476
19	12305-39336	Масляный поддон Subaru Legacy	https://static.baza.drom.ru/drom/1770873318866_bulletin	Subaru	Legacy	\N	2014	2021	г. Санкт-Петербург, ул. Курако, 65	Автоопт	+7-989-873-41-60	https://baza.drom.ru/g17981539075.html	12	3648.00	used	2026-04-06 11:43:10.94913
21	13568-91707	Ремень ГРМ Honda Fit	https://static.baza.drom.ru/drom/1741949867079_bulletin	Honda	Fit	\N	2013	2023	г. Москва, ул. Ленина, 45	ЗапчастиКузбасс	+7-964-187-59-36	https://baza.drom.ru/novosibirsk/sell_spare_parts/komplekt-grm-subaru-s-originalnym-remnem-13028aa240-13028aa250-104867105.html	24	2591.00	used	2026-04-06 11:43:15.04828
23	04465-79227	Тормозные колодки передние Honda CR-V	https://static.baza.drom.ru/drom/1729247023243_bulletin	Honda	CR-V	\N	2004	2014	г. Екатеринбург, ул. Кирова, 13	Автозапчасти24	+7-986-344-47-37	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	17	3365.00	used	2026-04-06 11:43:21.505681
24	04465-77793	Тормозные колодки передние Mazda 3	https://static.baza.drom.ru/drom/1729247023243_bulletin	Mazda	3	\N	1995	2003	г. Новосибирск, ул. Ленина, 23	Авторазбор №1	+7-973-351-79-21	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	14	2002.00	used	2026-04-06 11:43:23.972224
26	27060-0W070	Генератор Toyota Highlander	https://static.baza.drom.ru/drom/1770642186414_bulletin	Toyota	Highlander	\N	2014	2023	г. Кемерово, ул. Ленина, 74	Автозапчасти24	+7-936-610-35-75	https://baza.drom.ru/novosibirsk/sell_spare_parts/generator-caterpillar-d9r-d6r-133649208.html	11	10444.00	used	2026-04-06 11:43:28.005553
28	48520-09L85	Амортизатор задний Nissan X-Trail	https://static.baza.drom.ru/drom/1716529840985_bulletin	Nissan	X-Trail	\N	2006	2014	г. Санкт-Петербург, ул. Транспортная, 47	Автоопт	+7-932-281-73-36	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	4	5650.00	used	2026-04-06 11:43:32.330272
29	27060-0W070	Генератор Nissan Teana	https://static.baza.drom.ru/drom/1770642186414_bulletin	Nissan	Teana	\N	2004	2009	г. Кемерово, ул. Кирова, 76	Автодок	+7-990-341-89-14	https://baza.drom.ru/novosibirsk/sell_spare_parts/generator-caterpillar-d9r-d6r-133649208.html	2	12211.00	used	2026-04-06 11:43:34.262208
31	04465-81702	Тормозные колодки передние Nissan X-Trail	https://static.baza.drom.ru/drom/1729247023243_bulletin	Nissan	X-Trail	\N	2002	2011	г. Кемерово, ул. Ленина, 40	Автоопт	+7-967-245-71-54	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	18	2101.00	new	2026-04-06 11:43:38.612865
33	04466-0W020	Тормозные колодки задние Mitsubishi Lancer	https://static.baza.drom.ru/drom/1729247023243_bulletin	Mitsubishi	Lancer	\N	2007	2016	г. Казань, ул. Ленина, 41	Автоопт	+7-902-768-93-63	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	24	2121.00	new	2026-04-06 11:43:42.972554
62	12305-37333	Масляный поддон Mazda MX-5	\N	Mazda	MX-5	\N	2003	2010	г. Москва, ул. Транспортная, 73	Дром Запчасти	+7-917-345-58-51		22	2381.00	used	2026-04-06 11:38:31.711536
63	31210-0W010	Ступица передняя Honda Pilot	\N	Honda	Pilot	\N	2000	2008	г. Санкт-Петербург, ул. Транспортная, 80	Автоопт	+7-932-118-33-29		13	7144.00	new	2026-04-06 11:38:31.711536
64	12305-AA020	Масляный поддон Subaru Forester	\N	Subaru	Forester	\N	2004	2014	г. Екатеринбург, ул. Курако, 1	Авторазбор №1	+7-960-637-86-71		1	3279.00	used	2026-04-06 11:38:31.711536
65	17801-0V010	Воздушный фильтр Subaru Legacy	\N	Subaru	Legacy	\N	2011	2019	г. Казань, ул. Кирова, 43	Автозапчасти24	+7-953-752-58-33		1	1987.00	new	2026-04-06 11:38:31.711536
66	22401-AA560	Свечи зажигания (4 шт) Mazda 3	\N	Mazda	3	\N	2009	2016	г. Кемерово, ул. Транспортная, 65	Дром Запчасти	+7-969-488-58-41		17	430.00	used	2026-04-06 11:38:31.711536
67	16400-0W210	Радиатор Subaru Legacy	\N	Subaru	Legacy	\N	2014	2019	г. Москва, ул. Ленина, 18	ЗапчастиКузбасс	+7-941-397-53-35		6	5386.00	used	2026-04-06 11:38:31.711536
68	28100-24819	Стартер Honda Civic	\N	Honda	Civic	\N	2004	2012	г. Санкт-Петербург, ул. Транспортная, 74	Автодок	+7-920-596-94-52		20	10004.00	new	2026-04-06 11:38:31.711536
37	04466-0W020	Тормозные колодки задние Toyota RAV4	https://baza.drom.ru/resources/img/drom-240.png	Toyota	RAV4	\N	2008	2018	г. Казань, ул. Ленина, 60	Автоопт	+7-913-592-41-61	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	11	3020.00	new	2026-04-06 11:43:53.941823
38	16400-0W210	Радиатор Kia Sorento	https://static.baza.drom.ru/drom/1772004553725_bulletin	Kia	Sorento	\N	2009	2015	г. Красноярск, ул. Кирова, 66	Авторазбор №1	+7-973-363-25-55	https://baza.drom.ru/novosibirsk/sell_spare_parts/radiator-ohlazhdenija-133989706.html	10	9729.00	used	2026-04-06 15:41:12.010819
40	48510-79619	Амортизатор передний Mazda 6	https://static.baza.drom.ru/drom/1716529840985_bulletin	Mazda	6	\N	2009	2018	г. Красноярск, ул. Транспортная, 88	Автозапчасти24	+7-920-263-41-45	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	2	7208.00	new	2026-04-06 15:41:16.304759
42	15208-AA100	Масляный фильтр Mazda 3	https://static.baza.drom.ru/drom/1722525962328_bulletin	Mazda	3	\N	2000	2006	г. Казань, ул. Курако, 62	Автодок	+7-921-119-37-12	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-masljanyj-s-5816-121720260.html	19	513.00	used	2026-04-06 15:41:20.551442
44	04465-0W020	Тормозные колодки передние Toyota Camry	https://static.baza.drom.ru/drom/1729247023243_bulletin	Toyota	Camry	\N	1997	2004	г. Красноярск, ул. Кирова, 56	Автоопт	+7-921-540-71-85	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	17	2328.00	new	2026-04-06 15:41:27.100188
45	13568-09070	Ремень ГРМ Subaru Legacy	https://static.baza.drom.ru/drom/1741949867079_bulletin	Subaru	Legacy	\N	1999	2009	г. Казань, ул. Ленина, 18	ЗапчастиКузбасс	+7-928-469-82-96	https://baza.drom.ru/novosibirsk/sell_spare_parts/komplekt-grm-subaru-s-originalnym-remnem-13028aa240-13028aa250-104867105.html	5	2812.00	used	2026-04-06 15:41:29.138763
47	31210-0W010	Ступица передняя Hyundai Creta	https://static.baza.drom.ru/drom/1684953011971_bulletin	Hyundai	Creta	\N	2014	2022	г. Казань, ул. Транспортная, 59	ЗапчастиКузбасс	+7-923-717-15-24	https://baza.drom.ru/novosibirsk/sell_spare_parts/stupica-pravaja-perednjaja-w212-110869688.html	15	7562.00	used	2026-04-06 15:41:33.517154
49	15208-AA100	Масляный фильтр Toyota RAV4	https://static.baza.drom.ru/drom/1722525962328_bulletin	Toyota	RAV4	\N	2012	2022	г. Кемерово, ул. Транспортная, 80	Дром Запчасти	+7-927-931-82-52	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-masljanyj-s-5816-121720260.html	19	913.00	used	2026-04-07 02:19:56.412255
50	16400-91419	Радиатор Toyota Corolla	https://static.baza.drom.ru/drom/1772004553725_bulletin	Toyota	Corolla	\N	2011	2017	г. Кемерово, ул. Ленина, 60	Автодок	+7-945-972-76-54	https://baza.drom.ru/novosibirsk/sell_spare_parts/radiator-ohlazhdenija-133989706.html	8	7198.00	new	2026-04-07 02:20:00.420254
52	15208-AA100	Масляный фильтр Subaru Legacy	https://static.baza.drom.ru/drom/1722525962328_bulletin	Subaru	Legacy	\N	2001	2011	г. Кемерово, ул. Транспортная, 96	Автоопт	+7-911-623-15-91	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-masljanyj-s-5816-121720260.html	13	1221.00	used	2026-04-07 02:20:04.653542
54	22401-82506	Свечи зажигания (4 шт) Toyota Land Cruiser 200	https://static.baza.drom.ru/drom/1772175679281_bulletin	Toyota	Land Cruiser 200	\N	2006	2011	г. Новокузнецк, ул. Ленина, 87	АвтоМир	+7-900-622-19-25	https://baza.drom.ru/g17707630243.html	25	939.00	used	2026-04-07 02:20:08.917657
55	12305-89228	Масляный поддон Toyota Camry	https://static.baza.drom.ru/drom/1770873318866_bulletin	Toyota	Camry	\N	2009	2014	г. Красноярск, ул. Транспортная, 76	Дром Запчасти	+7-953-891-12-83	https://baza.drom.ru/g17981539075.html	8	3258.00	used	2026-04-07 02:20:10.730001
57	48520-60811	Амортизатор задний Honda Fit	https://static.baza.drom.ru/drom/1716529840985_bulletin	Honda	Fit	\N	2002	2012	г. Екатеринбург, ул. Транспортная, 81	Exist	+7-948-661-20-21	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	23	6553.00	used	2026-04-07 02:20:14.938461
58	28100-0W030	Стартер Kia Ceed	https://static.baza.drom.ru/drom/1772175678828_bulletin	Kia	Ceed	\N	1996	2003	г. Екатеринбург, ул. Ленина, 9	Автодок	+7-939-424-68-83	https://baza.drom.ru/novosibirsk/sell_spare_parts/starter-mitsubishi-pajero-challenger-delica-delica-spacegear-l200-strada-md164977-g17707629212.html	4	6474.00	used	2026-04-07 02:20:17.248387
60	16400-0W210	Радиатор Mazda MX-5	https://static.baza.drom.ru/drom/1772004553725_bulletin	Mazda	MX-5	\N	1996	2006	г. Новокузнецк, ул. Кирова, 11	Автозапчасти24	+7-978-322-27-91	https://baza.drom.ru/novosibirsk/sell_spare_parts/radiator-ohlazhdenija-133989706.html	25	11453.00	new	2026-04-07 02:20:21.185918
69	22401-AA560	Свечи зажигания (4 шт) Mazda 6	\N	Mazda	6	\N	2005	2015	г. Казань, ул. Ленина, 17	АвтоМир	+7-900-103-20-99		12	920.00	new	2026-04-06 11:38:31.711536
70	04465-18610	Тормозные колодки передние Toyota Camry	\N	Toyota	Camry	\N	1998	2006	г. Казань, ул. Транспортная, 15	АвтоМир	+7-986-696-30-31		19	3291.00	used	2026-04-06 11:38:31.711536
71	31210-0W010	Ступица передняя Nissan X-Trail	\N	Nissan	X-Trail	\N	2000	2009	г. Новокузнецк, ул. Кирова, 81	ЗапчастиКузбасс	+7-998-975-25-43		8	4431.00	new	2026-04-06 11:38:31.711536
72	28100-0W030	Стартер Mazda MX-5	\N	Mazda	MX-5	\N	2006	2016	г. Казань, ул. Ленина, 14	Авторазбор №1	+7-969-165-83-39		8	13407.00	new	2026-04-06 11:38:31.711536
73	04465-19921	Тормозные колодки передние Toyota Camry	\N	Toyota	Camry	\N	2009	2016	г. Кемерово, ул. Курако, 10	ЗапчастиКузбасс	+7-972-923-57-26		8	2385.00	used	2026-04-06 11:38:31.711536
74	13568-09070	Ремень ГРМ Nissan Juke	\N	Nissan	Juke	\N	2014	2024	г. Кемерово, ул. Курако, 31	Автоопт	+7-976-144-69-12		22	1603.00	used	2026-04-06 11:38:31.711536
75	90916-03089	Термостат Honda Fit	\N	Honda	Fit	\N	1999	2008	г. Москва, ул. Транспортная, 5	Автоопт	+7-997-413-93-80		20	1451.00	new	2026-04-06 11:38:31.711536
76	16400-0W210	Радиатор Nissan Qashqai	\N	Nissan	Qashqai	\N	2004	2013	г. Казань, ул. Ленина, 97	Авторазбор №1	+7-960-707-28-63		7	6633.00	new	2026-04-06 11:38:31.711536
77	28100-0W030	Стартер Hyundai Creta	\N	Hyundai	Creta	\N	2015	2024	г. Новосибирск, ул. Курако, 45	Автоопт	+7-908-950-94-97		13	7010.00	used	2026-04-06 11:38:31.711536
78	28100-18990	Стартер Nissan Patrol	\N	Nissan	Patrol	\N	2007	2012	г. Новосибирск, ул. Кирова, 22	Автодок	+7-983-881-89-60		25	7819.00	used	2026-04-06 11:38:31.711536
79	31210-0W010	Ступица передняя Honda Civic	\N	Honda	Civic	\N	2002	2012	г. Москва, ул. Курако, 76	Дром Запчасти	+7-964-818-27-15		15	7118.00	new	2026-04-06 11:38:31.711536
80	31210-0W010	Ступица передняя Kia Optima	\N	Kia	Optima	\N	2003	2012	г. Кемерово, ул. Курако, 8	Автозапчасти24	+7-901-439-99-69		23	6095.00	new	2026-04-06 11:38:31.711536
81	16400-0W210	Радиатор Honda Accord	\N	Honda	Accord	\N	2009	2015	г. Красноярск, ул. Курако, 7	Автодок	+7-922-816-28-34		6	7770.00	new	2026-04-06 11:38:31.711536
82	90916-03089	Термостат Honda Pilot	\N	Honda	Pilot	\N	1999	2006	г. Кемерово, ул. Курако, 64	Автозапчасти24	+7-914-445-65-93		14	2257.00	used	2026-04-06 11:38:31.711536
83	48520-09L85	Амортизатор задний Nissan Qashqai	\N	Nissan	Qashqai	\N	2003	2012	г. Москва, ул. Кирова, 58	Автоопт	+7-914-985-23-67		3	5534.00	new	2026-04-06 11:38:31.711536
84	16400-14450	Радиатор Honda Fit	\N	Honda	Fit	\N	1999	2005	г. Екатеринбург, ул. Курако, 77	Exist	+7-979-776-30-51		17	6233.00	new	2026-04-06 11:38:31.711536
85	23300-13968	Топливный фильтр Mazda MX-5	\N	Mazda	MX-5	\N	1997	2006	г. Красноярск, ул. Транспортная, 68	Exist	+7-977-332-78-73		6	700.00	used	2026-04-06 11:38:31.711536
86	22401-AA560	Свечи зажигания (4 шт) Mitsubishi ASX	\N	Mitsubishi	ASX	\N	1998	2007	г. Екатеринбург, ул. Кирова, 46	Exist	+7-983-481-23-58		1	729.00	new	2026-04-06 11:38:31.711536
87	12305-61671	Масляный поддон Mazda CX-5	\N	Mazda	CX-5	\N	2004	2013	г. Москва, ул. Ленина, 45	ЗапчастиКузбасс	+7-914-152-10-11		17	4882.00	used	2026-04-06 11:38:31.711536
88	04465-0W020	Тормозные колодки передние Mazda 3	\N	Mazda	3	\N	1999	2005	г. Красноярск, ул. Ленина, 33	ЗапчастиКузбасс	+7-961-441-71-82		1	3901.00	used	2026-04-06 11:38:31.711536
89	23300-75620	Топливный фильтр Toyota Land Cruiser 200	\N	Toyota	Land Cruiser 200	\N	1995	2002	г. Санкт-Петербург, ул. Курако, 50	Автозапчасти24	+7-937-849-13-74		15	1320.00	new	2026-04-06 11:38:31.711536
90	12305-AA020	Масляный поддон Honda Pilot	\N	Honda	Pilot	\N	2002	2011	г. Новосибирск, ул. Курако, 77	Автозапчасти24	+7-977-904-27-69		10	4921.00	used	2026-04-06 11:38:31.711536
91	28100-0W030	Стартер Hyundai Creta	\N	Hyundai	Creta	\N	2006	2014	г. Новосибирск, ул. Кирова, 47	Дром Запчасти	+7-904-472-31-22		18	9778.00	new	2026-04-06 11:38:31.711536
92	04466-0W020	Тормозные колодки задние Kia Rio	\N	Kia	Rio	\N	2012	2022	г. Екатеринбург, ул. Транспортная, 17	ЗапчастиКузбасс	+7-989-124-51-52		25	1696.00	used	2026-04-06 11:38:31.711536
93	23300-0W010	Топливный фильтр Mazda 6	\N	Mazda	6	\N	2012	2017	г. Красноярск, ул. Транспортная, 53	ЗапчастиКузбасс	+7-972-283-79-84		6	1126.00	used	2026-04-06 11:38:31.711536
94	48510-43702	Амортизатор передний Honda Civic	\N	Honda	Civic	\N	2007	2016	г. Казань, ул. Кирова, 5	Дром Запчасти	+7-974-405-23-77		13	6102.00	new	2026-04-06 11:38:31.711536
95	22401-AA560	Свечи зажигания (4 шт) Kia Rio	\N	Kia	Rio	\N	2012	2020	г. Екатеринбург, ул. Транспортная, 45	Exist	+7-979-650-84-24		20	961.00	new	2026-04-06 11:38:31.711536
96	13568-26510	Ремень ГРМ Mazda MX-5	\N	Mazda	MX-5	\N	2002	2008	г. Новосибирск, ул. Кирова, 51	Автозапчасти24	+7-988-993-12-28		20	2336.00	used	2026-04-06 11:38:31.711536
97	48520-09L85	Амортизатор задний Hyundai Elantra	\N	Hyundai	Elantra	\N	2014	2020	г. Екатеринбург, ул. Ленина, 59	Автодок	+7-919-159-76-86		15	7289.00	new	2026-04-06 11:38:31.711536
98	28100-33112	Стартер Mitsubishi ASX	\N	Mitsubishi	ASX	\N	2000	2009	г. Москва, ул. Кирова, 2	Автозапчасти24	+7-918-725-33-19		23	13643.00	used	2026-04-06 11:38:31.711536
99	23300-0W010	Топливный фильтр Nissan X-Trail	\N	Nissan	X-Trail	\N	2011	2018	г. Кемерово, ул. Транспортная, 27	АвтоМир	+7-959-132-49-16		14	1210.00	new	2026-04-06 11:38:31.711536
100	22401-AA560	Свечи зажигания (4 шт) Hyundai Santa Fe	\N	Hyundai	Santa Fe	\N	2000	2006	г. Санкт-Петербург, ул. Транспортная, 19	ЗапчастиКузбасс	+7-927-108-24-57		15	922.00	used	2026-04-06 11:38:31.711536
101	48520-09L85	Амортизатор задний Nissan Patrol	\N	Nissan	Patrol	\N	2002	2011	г. Новосибирск, ул. Транспортная, 22	Exist	+7-934-493-84-69		25	6091.00	new	2026-04-06 11:38:31.711536
102	16400-0W210	Радиатор Subaru WRX	\N	Subaru	WRX	\N	1998	2007	г. Кемерово, ул. Ленина, 91	ЗапчастиКузбасс	+7-930-674-52-52		24	7373.00	used	2026-04-06 11:38:31.711536
103	12305-22016	Масляный поддон Toyota Camry	\N	Toyota	Camry	\N	2013	2018	г. Новокузнецк, ул. Ленина, 13	Exist	+7-942-673-21-90		22	3061.00	used	2026-04-06 11:38:31.711536
104	16400-59949	Радиатор Toyota Corolla	\N	Toyota	Corolla	\N	2009	2014	г. Красноярск, ул. Курако, 30	АвтоМир	+7-997-657-26-16		22	5956.00	new	2026-04-06 11:38:31.711536
105	90916-58799	Термостат Hyundai Creta	\N	Hyundai	Creta	\N	2012	2020	г. Кемерово, ул. Транспортная, 96	Дром Запчасти	+7-981-124-12-79		18	1400.00	new	2026-04-06 11:38:31.711536
106	48520-09L85	Амортизатор задний Hyundai Santa Fe	\N	Hyundai	Santa Fe	\N	1996	2002	г. Москва, ул. Кирова, 60	Автозапчасти24	+7-998-465-30-91		1	6171.00	new	2026-04-06 11:38:31.711536
107	48510-09L85	Амортизатор передний Hyundai Creta	\N	Hyundai	Creta	\N	2013	2020	г. Новосибирск, ул. Кирова, 17	Дром Запчасти	+7-919-575-33-92		25	7394.00	new	2026-04-06 11:38:31.711536
108	48520-94527	Амортизатор задний Mazda CX-9	\N	Mazda	CX-9	\N	2015	2025	г. Новокузнецк, ул. Ленина, 88	Дром Запчасти	+7-948-985-31-39		9	3419.00	used	2026-04-06 11:38:31.711536
109	22401-42335	Свечи зажигания (4 шт) Hyundai Santa Fe	\N	Hyundai	Santa Fe	\N	2000	2007	г. Казань, ул. Транспортная, 12	ЗапчастиКузбасс	+7-981-514-96-39		8	548.00	new	2026-04-06 11:38:31.711536
110	17801-0V010	Воздушный фильтр Mitsubishi Pajero	\N	Mitsubishi	Pajero	\N	2011	2020	г. Москва, ул. Курако, 49	Exist	+7-943-251-11-65		7	1686.00	new	2026-04-06 11:38:31.711536
111	17801-0V010	Воздушный фильтр Toyota Camry	\N	Toyota	Camry	\N	1996	2004	г. Санкт-Петербург, ул. Кирова, 54	Автозапчасти24	+7-908-396-26-99		8	1179.00	used	2026-04-06 11:38:31.711536
112	27060-0W070	Генератор Toyota Land Cruiser 200	\N	Toyota	Land Cruiser 200	\N	2000	2010	г. Казань, ул. Транспортная, 36	Автозапчасти24	+7-944-486-77-26		8	10646.00	used	2026-04-06 11:38:31.711536
113	28100-54757	Стартер Toyota RAV4	\N	Toyota	RAV4	\N	1998	2006	г. Москва, ул. Курако, 94	Авторазбор №1	+7-911-913-68-29		22	9381.00	used	2026-04-06 11:38:31.711536
114	12305-95718	Масляный поддон Honda Pilot	\N	Honda	Pilot	\N	1999	2004	г. Санкт-Петербург, ул. Кирова, 55	Автозапчасти24	+7-936-564-14-12		4	4461.00	new	2026-04-06 11:38:31.711536
115	31210-0W010	Ступица передняя Hyundai Creta	\N	Hyundai	Creta	\N	2003	2009	г. Новосибирск, ул. Кирова, 50	ЗапчастиКузбасс	+7-959-531-23-17		6	5654.00	new	2026-04-06 11:38:31.711536
116	48520-96940	Амортизатор задний Hyundai Solaris	\N	Hyundai	Solaris	\N	2004	2009	г. Казань, ул. Курако, 72	Автоопт	+7-963-723-64-62		25	6795.00	new	2026-04-06 11:38:31.711536
117	27060-0W070	Генератор Subaru Outback	\N	Subaru	Outback	\N	2006	2015	г. Новосибирск, ул. Кирова, 36	Автодок	+7-968-595-64-63		5	18646.00	used	2026-04-06 11:38:31.711536
118	27060-13243	Генератор Mazda 3	\N	Mazda	3	\N	2010	2015	г. Новокузнецк, ул. Транспортная, 46	Автодок	+7-963-662-31-21		6	10119.00	new	2026-04-06 11:38:31.711536
119	15208-AA100	Масляный фильтр Toyota Camry	\N	Toyota	Camry	\N	2013	2022	г. Санкт-Петербург, ул. Транспортная, 60	Авторазбор №1	+7-939-126-89-43		23	576.00	new	2026-04-06 11:38:31.711536
120	90916-03089	Термостат Kia Sorento	\N	Kia	Sorento	\N	2000	2010	г. Красноярск, ул. Транспортная, 79	Авторазбор №1	+7-957-830-48-91		12	1925.00	used	2026-04-06 11:38:31.711536
121	22401-AA560	Свечи зажигания (4 шт) Toyota Camry	\N	Toyota	Camry	\N	2006	2014	г. Новокузнецк, ул. Кирова, 30	Exist	+7-940-959-87-31		16	1054.00	new	2026-04-06 11:38:31.711536
122	27060-0W070	Генератор Toyota Highlander	\N	Toyota	Highlander	\N	1997	2007	г. Екатеринбург, ул. Ленина, 68	Автодок	+7-917-342-96-22		14	17431.00	new	2026-04-06 11:38:31.711536
123	48510-27217	Амортизатор передний Honda Fit	\N	Honda	Fit	\N	2006	2013	г. Санкт-Петербург, ул. Транспортная, 52	АвтоМир	+7-964-731-25-53		8	5569.00	new	2026-04-06 11:38:31.711536
124	90916-64824	Термостат Hyundai Tucson	\N	Hyundai	Tucson	\N	2009	2018	г. Новокузнецк, ул. Кирова, 83	Авторазбор №1	+7-982-217-54-20		22	2156.00	new	2026-04-06 11:38:31.711536
125	22401-AA560	Свечи зажигания (4 шт) Nissan Teana	\N	Nissan	Teana	\N	2008	2017	г. Кемерово, ул. Кирова, 63	Exist	+7-965-477-61-79		25	939.00	used	2026-04-06 11:38:31.711536
126	48510-09L85	Амортизатор передний Kia Sportage	\N	Kia	Sportage	\N	2007	2016	г. Москва, ул. Ленина, 85	Exist	+7-901-732-71-81		9	7451.00	new	2026-04-06 11:38:31.711536
127	31210-0W010	Ступица передняя Kia Sportage	\N	Kia	Sportage	\N	1995	2003	г. Новокузнецк, ул. Ленина, 19	Авторазбор №1	+7-901-129-93-15		13	6697.00	new	2026-04-06 11:38:31.711536
128	12305-32260	Масляный поддон Kia Sportage	\N	Kia	Sportage	\N	2006	2011	г. Екатеринбург, ул. Ленина, 82	Exist	+7-939-606-90-24		18	2997.00	new	2026-04-06 11:38:31.711536
129	28100-0W030	Стартер Subaru Legacy	\N	Subaru	Legacy	\N	2005	2013	г. Кемерово, ул. Курако, 32	Авторазбор №1	+7-958-120-81-66		2	13760.00	used	2026-04-06 11:38:31.711536
130	90916-03089	Термостат Subaru WRX	\N	Subaru	WRX	\N	1999	2007	г. Новосибирск, ул. Ленина, 21	АвтоМир	+7-914-706-65-47		3	1472.00	new	2026-04-06 11:38:31.711536
131	27060-0W070	Генератор Kia Rio	\N	Kia	Rio	\N	2003	2008	г. Москва, ул. Ленина, 99	Дром Запчасти	+7-939-606-35-82		16	18721.00	new	2026-04-06 11:38:31.711536
132	31210-0W010	Ступица передняя Subaru Outback	\N	Subaru	Outback	\N	2010	2015	г. Казань, ул. Курако, 92	Дром Запчасти	+7-983-378-12-55		22	5420.00	new	2026-04-06 11:38:31.711536
133	04466-0W020	Тормозные колодки задние Toyota Highlander	\N	Toyota	Highlander	\N	2013	2020	г. Красноярск, ул. Курако, 69	Авторазбор №1	+7-927-918-17-92		12	1602.00	used	2026-04-06 11:38:31.711536
134	17801-0V010	Воздушный фильтр Mitsubishi Pajero Sport	\N	Mitsubishi	Pajero Sport	\N	2004	2014	г. Новокузнецк, ул. Ленина, 66	АвтоМир	+7-950-985-38-62		14	1175.00	new	2026-04-06 11:38:31.711536
135	31210-82299	Ступица передняя Kia Sorento	\N	Kia	Sorento	\N	2007	2012	г. Новосибирск, ул. Транспортная, 52	АвтоМир	+7-905-901-85-28		8	5499.00	new	2026-04-06 11:38:31.711536
136	04465-0W020	Тормозные колодки передние Mitsubishi Outlander	\N	Mitsubishi	Outlander	\N	2006	2015	г. Санкт-Петербург, ул. Кирова, 77	Автоопт	+7-961-948-78-27		25	2653.00	new	2026-04-06 11:38:31.711536
137	28100-0W030	Стартер Subaru Legacy	\N	Subaru	Legacy	\N	2013	2022	г. Новокузнецк, ул. Кирова, 29	АвтоМир	+7-992-636-50-81		25	13803.00	used	2026-04-06 11:38:31.711536
138	16400-0W210	Радиатор Mazda MX-5	\N	Mazda	MX-5	\N	2001	2010	г. Новокузнецк, ул. Ленина, 66	Дром Запчасти	+7-954-816-81-84		14	5426.00	new	2026-04-06 11:38:31.711536
139	90916-03089	Термостат Mitsubishi Pajero Sport	\N	Mitsubishi	Pajero Sport	\N	1997	2003	г. Москва, ул. Курако, 29	Авторазбор №1	+7-960-814-46-17		19	1415.00	new	2026-04-06 11:38:31.711536
140	31210-0W010	Ступица передняя Nissan X-Trail	\N	Nissan	X-Trail	\N	2009	2014	г. Новокузнецк, ул. Кирова, 60	Автоопт	+7-957-926-76-77		25	4672.00	used	2026-04-06 11:38:31.711536
141	16400-96022	Радиатор Subaru Legacy	\N	Subaru	Legacy	\N	2001	2008	г. Екатеринбург, ул. Курако, 6	Exist	+7-952-134-43-79		3	8303.00	new	2026-04-06 11:38:31.711536
142	23300-0W010	Топливный фильтр Hyundai Tucson	\N	Hyundai	Tucson	\N	2003	2008	г. Новосибирск, ул. Кирова, 33	ЗапчастиКузбасс	+7-911-813-12-62		4	1128.00	new	2026-04-06 11:38:31.711536
143	13568-09070	Ремень ГРМ Toyota Corolla	\N	Toyota	Corolla	\N	2005	2010	г. Кемерово, ул. Кирова, 33	Автодок	+7-910-325-74-89		18	2697.00	used	2026-04-06 11:38:31.711536
144	28100-0W030	Стартер Honda Pilot	\N	Honda	Pilot	\N	2008	2014	г. Санкт-Петербург, ул. Курако, 40	Автодок	+7-941-259-63-31		23	8388.00	new	2026-04-06 11:38:31.711536
145	13568-09070	Ремень ГРМ Nissan X-Trail	\N	Nissan	X-Trail	\N	2009	2016	г. Новосибирск, ул. Кирова, 75	Автозапчасти24	+7-938-203-50-92		11	2408.00	new	2026-04-06 11:38:31.711536
146	15208-AA100	Масляный фильтр Kia Sorento	\N	Kia	Sorento	\N	2000	2009	г. Красноярск, ул. Ленина, 32	ЗапчастиКузбасс	+7-978-860-59-94		6	884.00	used	2026-04-06 11:38:31.711536
147	04465-18988	Тормозные колодки передние Toyota Corolla	\N	Toyota	Corolla	\N	2002	2011	г. Казань, ул. Курако, 76	Авторазбор №1	+7-903-745-39-24		5	3785.00	new	2026-04-06 11:38:31.711536
148	31210-0W010	Ступица передняя Subaru Outback	\N	Subaru	Outback	\N	2004	2010	г. Казань, ул. Транспортная, 5	Автозапчасти24	+7-907-430-99-37		3	5524.00	used	2026-04-06 11:38:31.711536
149	13568-09070	Ремень ГРМ Hyundai Creta	\N	Hyundai	Creta	\N	2003	2012	г. Санкт-Петербург, ул. Транспортная, 73	Автодок	+7-970-326-16-51		5	2959.00	used	2026-04-06 11:38:31.711536
150	48520-09L85	Амортизатор задний Nissan Qashqai	\N	Nissan	Qashqai	\N	1998	2004	г. Казань, ул. Транспортная, 48	Exist	+7-946-455-63-12		7	3928.00	new	2026-04-06 11:38:31.711536
151	17801-64573	Воздушный фильтр Subaru Outback	\N	Subaru	Outback	\N	2002	2010	г. Красноярск, ул. Курако, 34	Авторазбор №1	+7-985-271-93-33		10	1050.00	used	2026-04-06 11:38:31.711536
152	04466-0W020	Тормозные колодки задние Nissan X-Trail	\N	Nissan	X-Trail	\N	2002	2007	г. Красноярск, ул. Курако, 91	АвтоМир	+7-970-106-22-61		2	3341.00	used	2026-04-06 11:38:31.711536
153	90916-68188	Термостат Mazda CX-5	\N	Mazda	CX-5	\N	2013	2022	г. Красноярск, ул. Транспортная, 13	Автодок	+7-902-944-55-96		10	1810.00	used	2026-04-06 11:38:31.711536
154	22401-AA560	Свечи зажигания (4 шт) Nissan Juke	\N	Nissan	Juke	\N	1998	2008	г. Новокузнецк, ул. Ленина, 91	Автозапчасти24	+7-983-801-79-22		5	1000.00	new	2026-04-06 11:38:31.711536
155	04466-0W020	Тормозные колодки задние Kia Sorento	\N	Kia	Sorento	\N	1998	2006	г. Новосибирск, ул. Транспортная, 91	Exist	+7-975-654-86-75		3	2754.00	used	2026-04-06 11:38:31.711536
156	27060-0W070	Генератор Honda CR-V	\N	Honda	CR-V	\N	2014	2020	г. Санкт-Петербург, ул. Кирова, 64	Exist	+7-945-970-66-23		16	15459.00	used	2026-04-06 11:38:31.711536
157	90916-03089	Термостат Nissan Patrol	\N	Nissan	Patrol	\N	2014	2019	г. Новокузнецк, ул. Транспортная, 46	ЗапчастиКузбасс	+7-916-250-12-26		13	1858.00	new	2026-04-06 11:38:31.711536
158	12305-AA020	Масляный поддон Mitsubishi Pajero Sport	\N	Mitsubishi	Pajero Sport	\N	2010	2016	г. Кемерово, ул. Транспортная, 78	Дром Запчасти	+7-950-687-84-83		22	3220.00	new	2026-04-06 11:38:31.711536
159	22401-AA560	Свечи зажигания (4 шт) Hyundai Creta	\N	Hyundai	Creta	\N	2000	2009	г. Новокузнецк, ул. Ленина, 57	АвтоМир	+7-931-660-51-27		17	1065.00	used	2026-04-06 11:38:31.711536
160	90916-03089	Термостат Kia Optima	\N	Kia	Optima	\N	2010	2019	г. Екатеринбург, ул. Курако, 78	Авторазбор №1	+7-956-319-93-67		3	2491.00	new	2026-04-06 11:38:31.711536
161	04465-57683	Тормозные колодки передние Mitsubishi ASX	\N	Mitsubishi	ASX	\N	2014	2023	г. Екатеринбург, ул. Курако, 40	Автозапчасти24	+7-926-468-96-96		16	2583.00	new	2026-04-06 11:38:31.711536
162	48510-09L85	Амортизатор передний Nissan Juke	\N	Nissan	Juke	\N	2000	2009	г. Красноярск, ул. Кирова, 87	Exist	+7-994-818-50-58		8	3037.00	new	2026-04-06 11:38:31.711536
163	28100-35863	Стартер Kia Rio	\N	Kia	Rio	\N	1997	2007	г. Санкт-Петербург, ул. Кирова, 71	АвтоМир	+7-978-636-63-19		9	12014.00	new	2026-04-06 11:38:31.711536
164	90916-03089	Термостат Nissan Qashqai	\N	Nissan	Qashqai	\N	2004	2014	г. Красноярск, ул. Транспортная, 14	ЗапчастиКузбасс	+7-917-294-56-94		16	843.00	new	2026-04-06 11:38:31.711536
165	31210-0W010	Ступица передняя Kia Optima	\N	Kia	Optima	\N	2006	2016	г. Кемерово, ул. Кирова, 74	ЗапчастиКузбасс	+7-930-948-66-60		1	6976.00	used	2026-04-06 11:38:31.711536
166	27060-0W070	Генератор Kia Sorento	\N	Kia	Sorento	\N	2005	2014	г. Екатеринбург, ул. Транспортная, 13	Автозапчасти24	+7-974-447-20-21		1	16325.00	new	2026-04-06 11:38:31.711536
167	04465-89339	Тормозные колодки передние Mitsubishi Outlander	\N	Mitsubishi	Outlander	\N	2008	2013	г. Новосибирск, ул. Транспортная, 50	Авторазбор №1	+7-971-921-11-42		9	3282.00	new	2026-04-06 11:38:31.711536
168	23300-0W010	Топливный фильтр Kia Rio	\N	Kia	Rio	\N	1995	2005	г. Кемерово, ул. Транспортная, 35	Автозапчасти24	+7-968-982-45-32		12	778.00	new	2026-04-06 11:38:31.711536
169	12305-50829	Масляный поддон Hyundai Creta	\N	Hyundai	Creta	\N	2008	2016	г. Санкт-Петербург, ул. Кирова, 24	Дром Запчасти	+7-919-763-57-50		20	4697.00	used	2026-04-06 11:38:31.711536
170	13568-70122	Ремень ГРМ Toyota Highlander	\N	Toyota	Highlander	\N	1999	2006	г. Новосибирск, ул. Ленина, 41	АвтоМир	+7-957-465-23-77		8	1263.00	new	2026-04-06 11:38:31.711536
171	48520-09L85	Амортизатор задний Kia Sportage	\N	Kia	Sportage	\N	1999	2009	г. Кемерово, ул. Транспортная, 93	ЗапчастиКузбасс	+7-935-999-19-17		1	4125.00	new	2026-04-06 11:38:31.711536
172	15208-AA100	Масляный фильтр Honda Civic	\N	Honda	Civic	\N	2003	2011	г. Новосибирск, ул. Транспортная, 51	ЗапчастиКузбасс	+7-962-721-17-56		21	852.00	new	2026-04-06 11:38:31.711536
173	31210-47558	Ступица передняя Honda CR-V	\N	Honda	CR-V	\N	1999	2008	г. Красноярск, ул. Транспортная, 61	Дром Запчасти	+7-984-354-44-70		21	4484.00	new	2026-04-06 11:38:31.711536
174	13568-09070	Ремень ГРМ Mazda CX-9	\N	Mazda	CX-9	\N	2011	2021	г. Екатеринбург, ул. Курако, 74	Автозапчасти24	+7-912-574-32-91		10	2767.00	new	2026-04-06 11:38:31.711536
175	90916-03089	Термостат Toyota Corolla	\N	Toyota	Corolla	\N	2001	2006	г. Екатеринбург, ул. Курако, 80	Автозапчасти24	+7-928-766-46-18		5	1124.00	new	2026-04-06 11:38:31.711536
176	90916-03089	Термостат Mitsubishi Outlander	\N	Mitsubishi	Outlander	\N	2009	2018	г. Красноярск, ул. Ленина, 10	Автоопт	+7-906-683-57-89		21	1154.00	new	2026-04-06 11:38:31.711536
177	15208-41759	Масляный фильтр Toyota Land Cruiser 200	\N	Toyota	Land Cruiser 200	\N	2011	2021	г. Москва, ул. Кирова, 86	Авторазбор №1	+7-917-345-81-68		1	1079.00	used	2026-04-06 11:38:31.711536
178	28100-0W030	Стартер Mazda 3	\N	Mazda	3	\N	1995	2003	г. Екатеринбург, ул. Ленина, 59	Автодок	+7-958-632-10-25		24	8438.00	new	2026-04-06 11:38:31.711536
179	04465-0W020	Тормозные колодки передние Mazda CX-5	\N	Mazda	CX-5	\N	2002	2007	г. Москва, ул. Ленина, 67	АвтоМир	+7-981-528-34-96		25	2947.00	used	2026-04-06 11:38:31.711536
180	27060-0W070	Генератор Toyota Land Cruiser 200	\N	Toyota	Land Cruiser 200	\N	2013	2019	г. Кемерово, ул. Кирова, 26	Автоопт	+7-913-156-81-26		17	7865.00	new	2026-04-06 11:38:31.711536
181	31210-0W010	Ступица передняя Mazda CX-9	\N	Mazda	CX-9	\N	1996	2004	г. Новосибирск, ул. Курако, 42	Автодок	+7-942-928-20-61		21	7629.00	new	2026-04-06 11:38:31.711536
182	48520-09L85	Амортизатор задний Mazda 3	\N	Mazda	3	\N	2005	2014	г. Новокузнецк, ул. Ленина, 62	ЗапчастиКузбасс	+7-931-788-69-90		13	6351.00	new	2026-04-06 11:38:31.711536
183	27060-0W070	Генератор Subaru Legacy	\N	Subaru	Legacy	\N	1998	2006	г. Красноярск, ул. Ленина, 19	Exist	+7-921-159-74-63		8	13138.00	used	2026-04-06 11:38:31.711536
184	90916-18808	Термостат Mazda MX-5	\N	Mazda	MX-5	\N	2003	2008	г. Санкт-Петербург, ул. Ленина, 52	Автодок	+7-965-534-32-59		1	1742.00	new	2026-04-06 11:38:31.711536
185	16400-0W210	Радиатор Honda Fit	\N	Honda	Fit	\N	1998	2006	г. Екатеринбург, ул. Ленина, 73	ЗапчастиКузбасс	+7-931-183-64-33		25	10964.00	new	2026-04-06 11:38:31.711536
186	27060-0W070	Генератор Nissan X-Trail	\N	Nissan	X-Trail	\N	2012	2019	г. Екатеринбург, ул. Кирова, 95	Автозапчасти24	+7-973-891-86-35		13	16458.00	used	2026-04-06 11:38:31.711536
187	23300-0W010	Топливный фильтр Mazda CX-5	\N	Mazda	CX-5	\N	2005	2013	г. Екатеринбург, ул. Транспортная, 60	Exist	+7-993-251-43-63		16	1348.00	new	2026-04-06 11:38:31.711536
188	13568-09070	Ремень ГРМ Nissan Patrol	\N	Nissan	Patrol	\N	2013	2020	г. Новокузнецк, ул. Транспортная, 55	Автодок	+7-932-776-33-79		8	3182.00	used	2026-04-06 11:38:31.711536
189	15208-AA100	Масляный фильтр Hyundai Creta	\N	Hyundai	Creta	\N	2013	2020	г. Красноярск, ул. Кирова, 68	Exist	+7-911-413-51-43		10	750.00	new	2026-04-06 11:38:31.711536
190	23300-0W010	Топливный фильтр Kia Sportage	\N	Kia	Sportage	\N	2008	2018	г. Санкт-Петербург, ул. Курако, 85	ЗапчастиКузбасс	+7-906-369-34-64		14	1445.00	new	2026-04-06 11:38:31.711536
191	23300-0W010	Топливный фильтр Mitsubishi Outlander	\N	Mitsubishi	Outlander	\N	2010	2016	г. Екатеринбург, ул. Кирова, 20	Авторазбор №1	+7-988-973-84-50		19	1456.00	new	2026-04-06 11:38:31.711536
192	13568-09070	Ремень ГРМ Toyota Highlander	\N	Toyota	Highlander	\N	1997	2006	г. Санкт-Петербург, ул. Ленина, 42	Автодок	+7-940-999-71-57		22	3373.00	used	2026-04-06 11:38:31.711536
193	31210-0W010	Ступица передняя Mitsubishi Outlander	\N	Mitsubishi	Outlander	\N	2005	2015	г. Новосибирск, ул. Транспортная, 70	Exist	+7-958-318-58-46		13	5265.00	new	2026-04-06 11:38:31.711536
194	16400-0W210	Радиатор Nissan Teana	\N	Nissan	Teana	\N	2002	2012	г. Новокузнецк, ул. Транспортная, 12	Exist	+7-900-146-98-67		24	5389.00	new	2026-04-06 11:38:31.711536
195	16400-12586	Радиатор Subaru Forester	\N	Subaru	Forester	\N	1999	2006	г. Екатеринбург, ул. Кирова, 22	АвтоМир	+7-981-925-15-48		7	7046.00	used	2026-04-06 11:38:31.711536
196	48510-09L85	Амортизатор передний Nissan Patrol	\N	Nissan	Patrol	\N	2005	2014	г. Москва, ул. Курако, 65	Exist	+7-999-883-70-34		16	7624.00	used	2026-04-06 11:38:31.711536
197	17801-0V010	Воздушный фильтр Subaru Impreza	\N	Subaru	Impreza	\N	2005	2012	г. Новокузнецк, ул. Ленина, 75	Автозапчасти24	+7-900-306-98-64		22	1716.00	used	2026-04-06 11:38:31.711536
198	12305-AA020	Масляный поддон Honda Pilot	\N	Honda	Pilot	\N	2013	2023	г. Кемерово, ул. Курако, 42	Авторазбор №1	+7-943-863-32-33		12	3807.00	new	2026-04-06 11:38:31.711536
199	17801-98751	Воздушный фильтр Toyota Land Cruiser 200	\N	Toyota	Land Cruiser 200	\N	2011	2016	г. Новосибирск, ул. Курако, 42	Exist	+7-969-846-18-27		14	1073.00	used	2026-04-06 11:38:31.711536
200	04466-68124	Тормозные колодки задние Hyundai Santa Fe	\N	Hyundai	Santa Fe	\N	2007	2014	г. Новосибирск, ул. Транспортная, 56	Автоопт	+7-935-621-10-60		5	2161.00	new	2026-04-06 11:38:31.711536
1	22401-AA560	Свечи зажигания (4 шт) Toyota RAV4	https://static.baza.drom.ru/drom/1772175679281_bulletin	Toyota	RAV4	\N	2007	2016	г. Казань, ул. Транспортная, 46	Автодок	+7-969-491-40-62	https://baza.drom.ru/g17707630243.html	8	753.00	used	2026-04-06 11:38:58.355931
2	04465-0W020	Тормозные колодки передние Kia Sorento	https://static.baza.drom.ru/drom/1729247023243_bulletin	Kia	Sorento	\N	1996	2006	г. Москва, ул. Кирова, 52	Exist	+7-943-339-75-48	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	7	1943.00	used	2026-04-06 11:39:00.654356
5	04465-0W020	Тормозные колодки передние Mazda CX-9	https://static.baza.drom.ru/drom/1729247023243_bulletin	Mazda	CX-9	\N	2009	2018	г. Санкт-Петербург, ул. Кирова, 69	Автодок	+7-984-290-61-30	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	15	2447.00	new	2026-04-06 11:39:09.037127
7	27060-0W070	Генератор Nissan Patrol	https://static.baza.drom.ru/drom/1770642186414_bulletin	Nissan	Patrol	\N	2003	2013	г. Москва, ул. Транспортная, 35	Автоопт	+7-985-493-71-81	https://baza.drom.ru/novosibirsk/sell_spare_parts/generator-caterpillar-d9r-d6r-133649208.html	2	16501.00	new	2026-04-06 11:39:13.294598
9	48520-59036	Амортизатор задний Subaru Legacy	https://static.baza.drom.ru/drom/1716529840985_bulletin	Subaru	Legacy	\N	2014	2023	г. Новокузнецк, ул. Ленина, 25	ЗапчастиКузбасс	+7-906-897-38-34	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	17	2925.00	new	2026-04-06 11:39:17.711151
12	13568-09070	Ремень ГРМ Toyota RAV4	https://static.baza.drom.ru/drom/1741949867079_bulletin	Toyota	RAV4	\N	2010	2018	г. Новосибирск, ул. Курако, 75	ЗапчастиКузбасс	+7-971-407-76-86	https://baza.drom.ru/novosibirsk/sell_spare_parts/komplekt-grm-subaru-s-originalnym-remnem-13028aa240-13028aa250-104867105.html	10	3319.00	used	2026-04-06 11:39:23.715896
15	31210-91625	Ступица передняя Mitsubishi ASX	https://static.baza.drom.ru/drom/1684953011971_bulletin	Mitsubishi	ASX	\N	2008	2014	г. Екатеринбург, ул. Курако, 96	Exist	+7-911-633-73-55	https://baza.drom.ru/novosibirsk/sell_spare_parts/stupica-pravaja-perednjaja-w212-110869688.html	2	6306.00	used	2026-04-06 11:39:30.012702
17	22401-AA560	Свечи зажигания (4 шт) Subaru Outback	https://static.baza.drom.ru/drom/1772175679281_bulletin	Subaru	Outback	\N	2010	2018	г. Казань, ул. Ленина, 12	Дром Запчасти	+7-970-478-95-22	https://baza.drom.ru/g17707630243.html	9	1148.00	used	2026-04-06 11:39:34.354769
20	16400-13598	Радиатор Mitsubishi Pajero Sport	https://static.baza.drom.ru/drom/1772004553725_bulletin	Mitsubishi	Pajero Sport	\N	2015	2022	г. Новосибирск, ул. Транспортная, 84	ЗапчастиКузбасс	+7-935-272-49-72	https://baza.drom.ru/novosibirsk/sell_spare_parts/radiator-ohlazhdenija-133989706.html	19	6389.00	new	2026-04-06 11:43:12.98315
22	48510-09L85	Амортизатор передний Toyota Highlander	https://static.baza.drom.ru/drom/1716529840985_bulletin	Toyota	Highlander	\N	1996	2001	г. Казань, ул. Курако, 77	АвтоМир	+7-997-858-83-92	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	23	6043.00	new	2026-04-06 11:43:17.339312
25	28100-0W030	Стартер Toyota Camry	https://static.baza.drom.ru/drom/1679668980786_bulletin	Toyota	Camry	\N	2001	2009	г. Кемерово, ул. Кирова, 89	Автодок	+7-975-875-43-29	https://baza.drom.ru/novosibirsk/sell_spare_parts/starter-nissan-elgrand-murano-teana-x-trail-23300-et80a-g17707629160.html	1	8965.00	new	2026-04-06 11:43:26.044102
27	17801-0V010	Воздушный фильтр Honda CR-V	https://static.baza.drom.ru/drom/1717038538306_bulletin	Honda	CR-V	\N	1996	2001	г. Новокузнецк, ул. Ленина, 68	Автозапчасти24	+7-913-912-54-69	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-vozdushnyj-cena-aktualna-dlja-vseh-avto-v-objavlenii-119881525.html	25	1936.00	new	2026-04-06 11:43:30.153041
30	16400-30148	Радиатор Mitsubishi Outlander	https://static.baza.drom.ru/drom/1772004553725_bulletin	Mitsubishi	Outlander	\N	2008	2018	г. Москва, ул. Курако, 6	АвтоМир	+7-991-545-32-24	https://baza.drom.ru/novosibirsk/sell_spare_parts/radiator-ohlazhdenija-133989706.html	7	7597.00	new	2026-04-06 11:43:36.239735
32	28100-0W030	Стартер Toyota Corolla	https://static.baza.drom.ru/drom/1679668980786_bulletin	Toyota	Corolla	\N	2010	2016	г. Новокузнецк, ул. Транспортная, 65	Дром Запчасти	+7-934-450-88-12	https://baza.drom.ru/novosibirsk/sell_spare_parts/starter-nissan-elgrand-murano-teana-x-trail-23300-et80a-g17707629160.html	13	13364.00	used	2026-04-06 11:43:40.702362
34	28100-14136	Стартер Hyundai Creta	https://static.baza.drom.ru/drom/1679668980786_bulletin	Hyundai	Creta	\N	2013	2018	г. Красноярск, ул. Ленина, 7	АвтоМир	+7-950-918-63-21	https://baza.drom.ru/novosibirsk/sell_spare_parts/starter-nissan-elgrand-murano-teana-x-trail-23300-et80a-g17707629160.html	14	7792.00	new	2026-04-06 11:43:45.289095
35	48520-09L85	Амортизатор задний Nissan Juke	https://static.baza.drom.ru/drom/1716529840985_bulletin	Nissan	Juke	\N	2006	2015	г. Санкт-Петербург, ул. Курако, 60	Автоопт	+7-975-729-83-35	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	12	3111.00	new	2026-04-06 11:43:47.485961
36	04465-0W020	Тормозные колодки передние Toyota RAV4	https://static.baza.drom.ru/drom/1729247023243_bulletin	Toyota	RAV4	\N	2015	2023	г. Красноярск, ул. Ленина, 5	Авторазбор №1	+7-936-157-15-96	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	23	1848.00	new	2026-04-06 11:43:49.78197
39	22401-AA560	Свечи зажигания (4 шт) Kia Sportage	https://static.baza.drom.ru/drom/1772175679281_bulletin	Kia	Sportage	\N	2002	2007	г. Кемерово, ул. Курако, 38	Exist	+7-971-368-17-64	https://baza.drom.ru/g17707630243.html	8	503.00	new	2026-04-06 15:41:13.935907
41	17801-73688	Воздушный фильтр Honda Accord	https://static.baza.drom.ru/drom/1717038538306_bulletin	Honda	Accord	\N	2008	2015	г. Казань, ул. Ленина, 24	Авторазбор №1	+7-947-669-14-93	https://baza.drom.ru/novosibirsk/sell_spare_parts/filtr-vozdushnyj-cena-aktualna-dlja-vseh-avto-v-objavlenii-119881525.html	18	1532.00	new	2026-04-06 15:41:18.52078
43	48510-09L85	Амортизатор передний Mitsubishi Pajero	https://static.baza.drom.ru/drom/1716529840985_bulletin	Mitsubishi	Pajero	\N	1996	2003	г. Санкт-Петербург, ул. Кирова, 17	ЗапчастиКузбасс	+7-910-900-70-13	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	24	7888.00	used	2026-04-06 15:41:22.702585
46	48510-09L85	Амортизатор передний Hyundai Tucson	https://static.baza.drom.ru/drom/1716529840985_bulletin	Hyundai	Tucson	\N	2001	2008	г. Казань, ул. Кирова, 27	Автозапчасти24	+7-905-869-42-62	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	10	7427.00	used	2026-04-06 15:41:31.292532
48	48520-09L85	Амортизатор задний Subaru Impreza	https://static.baza.drom.ru/drom/1716529840985_bulletin	Subaru	Impreza	\N	1998	2004	г. Новокузнецк, ул. Транспортная, 4	Exist	+7-940-359-12-54	https://baza.drom.ru/novosibirsk/sell_spare_parts/stojka-perednjaja-cena-aktualna-dlja-vseh-avto-v-objavlenii-119729361.html	13	5834.00	used	2026-04-06 15:41:35.623819
51	31210-0W010	Ступица передняя Kia Rio	https://static.baza.drom.ru/drom/1684953011971_bulletin	Kia	Rio	\N	2002	2009	г. Новосибирск, ул. Кирова, 28	Автоопт	+7-929-672-20-85	https://baza.drom.ru/novosibirsk/sell_spare_parts/stupica-pravaja-perednjaja-w212-110869688.html	20	5074.00	new	2026-04-07 02:20:02.628416
53	04466-0W020	Тормозные колодки задние Hyundai Solaris	https://static.baza.drom.ru/drom/1729247023243_bulletin	Hyundai	Solaris	\N	2003	2012	г. Казань, ул. Ленина, 29	АвтоМир	+7-910-135-93-12	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	16	3477.00	used	2026-04-07 02:20:06.896921
56	28100-0W030	Стартер Subaru Impreza	https://static.baza.drom.ru/drom/1772175678828_bulletin	Subaru	Impreza	\N	2015	2023	г. Екатеринбург, ул. Кирова, 94	Автодок	+7-985-812-30-93	https://baza.drom.ru/novosibirsk/sell_spare_parts/starter-mitsubishi-pajero-challenger-delica-delica-spacegear-l200-strada-md164977-g17707629212.html	5	7767.00	new	2026-04-07 02:20:12.716208
59	13568-76860	Ремень ГРМ Mazda CX-9	https://static.baza.drom.ru/drom/1741949867079_bulletin	Mazda	CX-9	\N	1995	2003	г. Красноярск, ул. Курако, 17	Дром Запчасти	+7-942-809-82-64	https://baza.drom.ru/novosibirsk/sell_spare_parts/komplekt-grm-subaru-s-originalnym-remnem-13028aa240-13028aa250-104867105.html	15	3172.00	used	2026-04-07 02:20:19.160551
61	04465-0W020	Тормозные колодки передние Hyundai Creta	https://static.baza.drom.ru/drom/1729247023243_bulletin	Hyundai	Creta	\N	1995	2005	г. Кемерово, ул. Курако, 97	Дром Запчасти	+7-938-819-92-10	https://baza.drom.ru/novosibirsk/sell_spare_parts/kolodki-tormoznye-perednie-cena-dlja-vseh-avto-v-objavlenii-123654254.html	22	2445.00	new	2026-04-07 02:20:23.414446
\.


--
-- Name: parts_inventory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.parts_inventory_id_seq', 201, true);


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

\unrestrict yT9Pycu829rLWwbajUwFHhhfbsNbHrYnqPkR2TsaOt1gdT5WzWD0SeKkwtY1pNH

