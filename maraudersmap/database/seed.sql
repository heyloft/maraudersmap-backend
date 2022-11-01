--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5 (Debian 14.5-2.pgdg110+2)
-- Dumped by pg_dump version 14.5 (Debian 14.5-2.pgdg110+2)

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

--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.events (id, active_from, active_to) FROM stdin;
cc0d3b66-3edf-4259-a5f4-09e1ee32ffd3	2022-10-18 22:55:30.074	2022-10-18 22:55:30.074
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, location) FROM stdin;
c7c99df4-c49e-4c44-8911-450e6774b3f6	hans	\N
5f507915-8f2a-42a4-8880-a5f506016f3b	johnny	\N
\.


--
-- Data for Name: eventParticipation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."eventParticipation" (user_id, status, event_id) FROM stdin;
c7c99df4-c49e-4c44-8911-450e6774b3f6	0	cc0d3b66-3edf-4259-a5f4-09e1ee32ffd3
\.


--
-- Data for Name: items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.items (id, title, description, icon, item_type) FROM stdin;
ef9a8c98-182b-466f-b8ab-d4f771b58ad9	The Great Beak	Kind of a skeleton key but more alive	great_beak	KEY
841beda8-0849-43ae-9885-f4f8212e7f1b	Goodie Bag	Wow, such great job!	iguess	VOUCHER
46777a2d-dc7a-4309-8c9e-60182f20b324	Shiny Shoes	Enjoy them while they last	shoes	COLLECTIBLE
\.


--
-- Data for Name: itemOwnerships; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."itemOwnerships" (id, obtained_at, item_id, owner_id) FROM stdin;
\.


--
-- Data for Name: quests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.quests (id, title, description, active_from, active_to, event_id, unlock_method, location) FROM stdin;
01c438c0-cc65-4823-9d90-f6a2997f6bb1	The forgotten flamingo	It is really pink!	2022-10-18 22:56:44.592	2023-02-18 22:56:44.592	cc0d3b66-3edf-4259-a5f4-09e1ee32ffd3	QR_CODE	{63.43153,10.400901}
\.


--
-- Data for Name: questDependencies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."questDependencies" (quest_to_finish_before_id, quest_to_finish_after_id) FROM stdin;
\.


--
-- Data for Name: questItems; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."questItems" (id, quest_id, item_id, location, unlock_method) FROM stdin;
27c5aee7-584b-4a88-9089-a43523aba9a2	01c438c0-cc65-4823-9d90-f6a2997f6bb1	ef9a8c98-182b-466f-b8ab-d4f771b58ad9	{63.43137186651732,10.401065453445952}	QR_CODE
873ef02c-f59f-4e6d-8b37-37d6ea5acc01	01c438c0-cc65-4823-9d90-f6a2997f6bb1	841beda8-0849-43ae-9885-f4f8212e7f1b	\N	QUEST_COMPLETION
aeef001e-e29f-4b8a-9bcb-3c427cd8a9a6	01c438c0-cc65-4823-9d90-f6a2997f6bb1	46777a2d-dc7a-4309-8c9e-60182f20b324	\N	QUEST_COMPLETION
\.


--
-- Data for Name: questParticipations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."questParticipations" (user_id, status, quest_id) FROM stdin;
\.


--
-- PostgreSQL database dump complete
--

