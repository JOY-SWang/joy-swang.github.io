---
title: "SpeechMedAssist: Efficiently and Effectively Adapting Speech Language Model for Medical Consultation"
collection: publications
category: manuscripts
permalink: /publication/SpeechMedAssist
excerpt: 'A **SpeechLM** natively capable of conducting multi-turn speech-based interactions with patients, with modality alignment, satefy and efficiency check.'
date: 2025-09-01
venue: 'ICLR2026 (under review)'
slidesurl: 'https://sirrychen.github.io/share/2025-09-22-SpeechMedAssist.html'
paperurl: 'https://anonymous.4open.science/r/SpeechMedAssist-Anonymous/'
citation: 'Chen S., Wang J., Chen W., \&  Wei Z. A **SpeechLM** natively capable of conducting multi-turn speech-based interactions with patients, with modality alignment, satefy and efficiency check.'
---

Medical consultations are inherently speech-based, yet current works focus on fine-tuning large language models (LLMs) to perform patient-unfriendly long-text interaction. While existing speech language models (SpeechLMs) enable efficient speech-based interaction, the scarcity of speech data in medical domain prevents them from being directly fine-tuned for practical applications. In this paper, we propose SpeechMedAssist, a SpeechLM natively capable of conducting multi-turn speech-based interactions with patients. To mitigate data scarcity, we mathematically analyze the architecture of SpeechLMs and decouple one-stage training that requires a large corpus of medical speech data into a two-stage training paradigm. (1) Knowledge&Capability injection: train the LLM core with rewritten and filtered medical text data to inject medical knowledge and endow it with diagnostic and treatment capabilities. (2) Modality alignment: train the SpeechLM using a small amount of synthetic medical speech data that matches patient characteristics to realign the speech and text modalities. After two-stage training, SpeechMedAssist performs excellent on our designed speech-based medical benchmark. Experiments further show that the second stage only requires 2k speech dialogue samples to achieve modality alignment, allowing the knowledge and capabilities acquired in the text modality during the first stage to generalize to the speech modality, which demonstrates the effectiveness and efficiency of our approach.