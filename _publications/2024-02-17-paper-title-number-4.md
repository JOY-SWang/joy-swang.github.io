---
title: "Think Out Loud, Pause in Silence: Confidence-Guided Reflect–Pause–Abort for Robust Audio Perceptual Understanding"
collection: publications
category: manuscripts
permalink: /publication/ConfAudio
excerpt: 'This paper is submitted to ICLR2026.'
date: 2025-09-01
paperurl: 'http://academicpages.github.io/files/RepresentitivePaper_Think_Out_LoudPause_in_Silence.pdf'
slidesurl: 'https://github.com/JOY-SWang/R1-AQA-Omni'
citation: 'Wang J., Niu Y., Xu D. \&  Wei Z. We proposed an adaptive framework that couples **perceptual** grounding with reasoning for **LALMs**, ConfAudio, which unifies explicit, reflective reasoning (**fine-tuned** on our novel dataset) with implicit, **pause-driven latent  GRPO** training, via a controller monitors **lowest-group-confidence** and a **composite reward function**.'
---
Large Audio Language Models (LALMs) mainly fail for two errors: perceptual errors misidentifying background sounds or speaker turns, and reasoning errors drifting rationales that decouple from acoustic evidence. To address these issues, we propose an adaptive framework that couples perceptual grounding with computation that expands only when needed. First, we introduce PAQA, a Perceptually grounded Audio QA dataset of 7,470 multiple-choice items that pairs multi-speaker, background-rich audio with stepwise reasoning and reflection annotations, enabling supervision of verifiable audio-grounded rationales. On the modeling side, we propose ConfAudio, which unifies explicit, reflective reasoning (fine-tuned on PAQA) with implicit, pause-driven latent computation trained via GRPO. A confidence-aware controller monitors lowest-group-confidence (LGC) during decoding to insert pauses when uncertainty rises and to abort unstable trajectories, thereby reallocating compute toward hard perceptual segments. To stabilize the training process, we design a composite reward function that balances answer correctness, reasoning–answer consistency with perceptual robustness, and output format. Across PAQA, MMAU-mini, and MMAR, ConfAudio consistently improves both accuracy and consistency, particularly in noisy, multi-speaker conditions. Our results demonstrate that confidence-guided, adaptive reasoning—grounded in verifiable acoustic evidence—mitigates the dominant perceptual and reasoning failure modes in Audio-QA.


![Overview](/images/paper/ICLRoverview.png)

![Sample](/images/paper/ICLRsample.png)

![Latent](/images/paper/ICLRlatent.png)

