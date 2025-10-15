---
title: "RedRAG: A RefinED RAG Framework Towards Complex Queries and Information Confliction in Generative Search Engines"
collection: publications
category: manuscripts
permalink: /publication/redrag
excerpt: ''
date: 2025-02-01
venue: 'ACL2024'
paperurl: 'https://aclanthology.org/2024.findings-acl.296.pdf'
citation: 'In this paper, we propose a new refined RAG system, **RedRAG**, which can more accurately understand complex user queries, reduce information conflicts, and improve the coherence and credibility of the generated answers, with four modules, Query Planning, Recalling and Retrieval, Machine Reading Comprehension (MRC) Extraction, Entity Clustering, Answer Verification and Summarization Module.'
---

Generative search engines have become a popular direction  with their core often relying on the RAG (Retrieval-Augmented Generation) architecture. However, existing RAG methods still face several issues: (1) Multi-layered requirements in complex queries: Complex user queries often involve multiple elements, and simple similarity-based retrieval may recall irrelevant documents; (2) Conflicting opinions in different documents: During the generation phase, opinions extracted from different documents may conflict, affecting the reliability of the final answer; (3) Shallow processing of answer aggregation: Current answer aggregation, which relies on direct refinement and compression of raw data, offers limited conciseness and struggles with complex queries. To address these issues, we propose a novel refined RAG system, RedRAG. Through modular collaboration, RedRAG can more accurately handle multiple requirements in complex queries, reduce information conflicts, and enhance the coherence and credibility of the generated answers. Additionally, to evaluate the effectiveness of the RedRAG framework in real-world scenarios, we collect a large number of user-generated queries from social media platforms and create a high-quality evaluation dataset. Extensive experimental results and positive online feedback validate the superiority of our system.