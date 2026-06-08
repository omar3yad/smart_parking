COPY public.parking_camera (id, camera_id, zone_name, "row", col) FROM stdin;
1	CAM-01	entrance	0	0
2	CAM-02	zone-A1	    1	1
3	CAM-03	zone-A16	16	1
4	CAM-04	zone-A32	32	1
5	CAM-05	zone-D1	    1	4
6	CAM-06	zone-D16	16	4
7	CAM-07	zone-D32	32	4
8	CAM-08	exit	    45	1
\.

COPY public.parking_parkingslot (id, slot_number, status, slot_type, latitude, longitude, floor, "row", col, camera_id) FROM stdin;
17	B1	occupied	regular	\N	\N	1	1	2	2
19	C1	occupied	regular	\N	\N	1	1	3	2
9	D1	occupied	regular	\N	\N	1	1	5	2
2	A2	occupied	regular	\N	\N	1	2	0	2
18	B2	occupied	regular	\N	\N	1	2	2	2
20	C2	occupied	regular	\N	\N	1	2	3	2
10	D2	occupied	regular	\N	\N	1	2	5	2
3	A3	occupied	regular	\N	\N	1	3	0	2
27	A15	occupied	regular	\N	\N	1	15	0	3
52	C3	occupied	regular	\N	\N	1	3	3	5
11	D3	occupied	regular	\N	\N	1	3	5	2
4	A4	occupied	regular	\N	\N	1	4	0	2
58	B4	occupied	regular	\N	\N	1	4	2	5
53	C4	occupied	regular	\N	\N	1	4	3	5
12	D4	occupied	regular	\N	\N	1	4	5	2
5	A5	occupied	regular	\N	\N	1	5	0	2
59	B5	occupied	regular	\N	\N	1	5	2	5
54	C5	occupied	regular	\N	\N	1	5	3	5
13	D5	occupied	regular	\N	\N	1	5	5	2
6	A6	occupied	regular	\N	\N	1	6	0	2
60	B6	occupied	regular	\N	\N	1	6	2	5
55	C6	occupied	regular	\N	\N	1	6	3	5
14	D6	occupied	regular	\N	\N	1	6	5	2
7	A7	occupied	regular	\N	\N	1	7	0	2
61	B7	occupied	regular	\N	\N	1	7	2	5
56	C7	occupied	regular	\N	\N	1	7	3	5
15	D7	occupied	regular	\N	\N	1	7	5	2
8	A8	occupied	regular	\N	\N	1	8	0	2
77	B8	occupied	regular	\N	\N	1	8	2	6
72	C8	occupied	regular	\N	\N	1	8	3	6
16	D8	occupied	regular	\N	\N	1	8	5	2
21	A9	occupied	regular	\N	\N	1	9	0	3
78	B9	occupied	regular	\N	\N	1	9	2	6
73	C9	occupied	regular	\N	\N	1	9	3	6
42	D9	occupied	regular	\N	\N	1	9	5	5
22	A10	occupied	regular	\N	\N	1	10	0	3
79	B10	occupied	regular	\N	\N	1	10	2	6
74	C10	occupied	regular	\N	\N	1	10	3	6
43	D10	occupied	regular	\N	\N	1	10	5	5
23	A11	occupied	regular	\N	\N	1	11	0	3
80	B11	occupied	regular	\N	\N	1	11	2	6
75	C11	occupied	regular	\N	\N	1	11	3	6
44	D11	occupied	regular	\N	\N	1	11	5	5
24	A12	occupied	regular	\N	\N	1	12	0	3
49	D16	occupied	regular	\N	\N	1	16	5	5
76	C12	occupied	regular	\N	\N	1	12	3	6
45	D12	occupied	regular	\N	\N	1	12	5	5
25	A13	occupied	regular	\N	\N	1	13	0	3
96	B13	occupied	regular	\N	\N	1	13	2	7
92	C13	occupied	regular	\N	\N	1	13	3	7
46	D13	occupied	regular	\N	\N	1	13	5	5
81	B12	occupied	regular	\N	\N	1	12	2	6
97	B14	occupied	regular	\N	\N	1	14	2	7
93	C14	occupied	regular	\N	\N	1	14	3	7
47	D14	occupied	regular	\N	\N	1	14	5	5
26	A14	occupied	regular	\N	\N	1	14	0	3
94	C15	occupied	regular	\N	\N	1	15	3	7
30	A18	occupied	regular	\N	\N	1	18	0	3
51	D18	occupied	regular	\N	\N	1	18	5	5
48	D15	occupied	regular	\N	\N	1	15	5	5
57	B3	occupied	regular	\N	\N	1	3	2	5
28	A16	occupied	regular	\N	\N	1	16	0	3
95	C16	occupied	regular	\N	\N	1	16	3	7
29	A17	occupied	regular	\N	\N	1	17	0	3
50	D17	occupied	regular	\N	\N	1	17	5	5
31	A19	occupied	regular	\N	\N	1	19	0	3
32	D19	occupied	regular	\N	\N	1	19	5	4
62	A20	occupied	regular	\N	\N	1	20	0	6
33	D20	occupied	regular	\N	\N	1	20	5	4
63	A21	occupied	regular	\N	\N	1	21	0	6
34	D21	occupied	regular	\N	\N	1	21	5	4
64	A22	occupied	regular	\N	\N	1	22	0	6
35	D22	occupied	regular	\N	\N	1	22	5	4
65	A23	occupied	regular	\N	\N	1	23	0	6
36	D23	occupied	regular	\N	\N	1	23	5	4
37	D24	occupied	regular	\N	\N	1	24	5	4
67	A25	occupied	regular	\N	\N	1	25	0	6
38	D25	occupied	regular	\N	\N	1	25	5	4
68	A26	occupied	regular	\N	\N	1	26	0	6
39	D26	occupied	regular	\N	\N	1	26	5	4
69	A27	occupied	regular	\N	\N	1	27	0	6
40	D27	occupied	regular	\N	\N	1	27	5	4
70	A28	occupied	regular	\N	\N	1	28	0	6
41	D28	occupied	regular	\N	\N	1	28	5	4
71	A29	occupied	regular	\N	\N	1	29	0	6
82	A30	occupied	regular	\N	\N	1	30	0	7
83	A31	occupied	regular	\N	\N	1	31	0	7
84	A32	occupied	regular	\N	\N	1	32	0	7
85	A33	occupied	regular	\N	\N	1	33	0	7
86	A34	occupied	regular	\N	\N	1	34	0	7
87	A35	occupied	regular	\N	\N	1	35	0	7
88	A36	occupied	regular	\N	\N	1	36	0	7
89	A37	occupied	regular	\N	\N	1	37	0	7
90	A38	occupied	regular	\N	\N	1	38	0	7
91	A39	occupied	regular	\N	\N	1	39	0	7
98	B15	occupied	regular	\N	\N	1	15	2	7
100	A50	occupied	regular	15	12	1	1	1	3
99	B16	occupied	regular	\N	\N	1	16	2	7
66	A24	occupied	regular	\N	\N	1	24	0	6
1	A1	occupied	regular	\N	\N	1	1	0	2
\.