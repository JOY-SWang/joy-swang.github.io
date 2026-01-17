---
title: "Speak With Dual Reasoning: Audio Perceptual Understanding with Explicit Reflection and Latent Reasoning"
collection: publications
category: manuscripts
permalink: /publication/ConfAudio
excerpt: 'This paper is going to submitted to ACL2026.'
date: 2025-09-01
venue: 'ICLR2026 (under review)'
paperurl: 'http://academicpages.github.io/files/RepresentitivePaper_Think_Out_LoudPause_in_Silence.pdf'
slidesurl: 'https://github.com/JOY-SWang/R1-AQA-Omni'
citation: 'Wang J., Niu Y., Xu D. \&  Wei Z. We proposed an adaptive framework that couples perceptual grounding with reasoning for LALMs, ConfAudio, which unifies explicit, reflective reasoning (fine-tuned on our novel dataset) with implicit, pause-driven latent  GRPO training, via a controller monitors lowest-group-confidence and a composite reward function.'
---
The failures of Large Audio Language Models (LALMs) primarily stem from two categories of errors: perceptual errors, such as misidentifying background sounds or speaker turns, and reasoning errors, where the generated rationale becomes decoupled from the acoustic evidence.
To address these challenges, we propose an adaptive framework that couples perceptual grounding with computational resources that expand only when necessary.
First, we constructed a perceptually-grounded Audio QA (Audio QA) dataset comprising 16,000 multiple-choice questions, pairing of audio—rich with background noise and multiple speakers. Then, we introduce PauseAudio. This model unifies two modes of reasoning: explicit, reflective reasoning, fine-tuned on the dataset, and implicit, pause-driven latent computation, trained via GRPO, distinguished by lowest-group-confidence" (LGC). To stabilize the training process, we designed a composite reward function that balances answer correctness, reasoning-answer consistency, perceptual robustness, and output format. Our findings demonstrate that this confidence-guided, adaptive reasoning approach, grounded in verifiable acoustic evidence, effectively mitigates the dominant perceptual and reasoning failure modes in Audio-QA.