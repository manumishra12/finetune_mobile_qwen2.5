# finetune_mobile_qwen2.5

tier_1_fintune: https://drive.google.com/drive/folders/1_qKCt362SAwuC46BvnwF47B3URSBncCD?usp=sharing
final vesion: https://drive.google.com/file/d/18j5QvXynqm1aKqBjzeoFMhMBSa0HUOLj/view?usp=sharing

```
*final_version folder summary:*

Contains two complete models:
> Qwen 2.5 – 1.5B and Qwen 2.5 – 3B

For each model (1.5B & 3B):
* Fine-tuning notebook (finetune_*.ipynb)
* Training outputs (all_training_outputs*.zip)
* Final HuggingFace model (finetuned_model*.zip)
* GGUF conversion notebook (model_to_gguf*.ipynb)

Final GGUF models:
> *_f16.gguf (full precision)
> *_Q4_K_M.gguf (quantized, mobile-friendly)

Root folder:
> Common GGUF conversion notebooks
> final_version.zip (full backup)
```

*Dataset Creation Scripts:*

> *Tier_1* : `generate_dataset.py`
> *Tier_2* : `generate_dataset_reasoning.py`
