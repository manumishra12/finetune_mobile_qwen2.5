# finetune_mobile_qwen2.5

Fine-tuned **Qwen 2.5** models (1.5B & 3B) optimized for on-device mobile inference. Built for **Arny** — a multi-agent AI assistant that runs a dual-tier architecture entirely on mobile devices using GGUF quantized models via `llama.cpp`.

---

## Architecture Overview

The system uses a **two-tier routing architecture** where a lightweight always-on router classifies queries and an on-demand reasoner handles complex tasks:

```
User Query
    │
    ▼
┌──────────────────────────────┐
│  Tier-1: Router Model        │  ◄── Always loaded in memory
│  Qwen 2.5 - 1.5B (Q4_K_M)  │      (~941 MB)
│                              │
│  • Intent classification     │
│  • Agent/domain routing      │
│  • Complexity scoring        │
│  • Missing field detection   │
│  • Outputs strict JSON       │
└──────────┬───────────────────┘
           │
     ┌─────┴──────────────────────────────┐
     │              │                     │
     ▼              ▼                     ▼
 Simple Query   Complex Query        Needs Live Data
 (score < 60)   (score ≥ 60)         (execution)
     │              │                     │
     ▼              ▼                     ▼
 Direct Answer  ┌────────────────┐   Cloud APIs
 from Tier-1    │ Tier-2 Reasoner│   (flights,
                │ Qwen 2.5 - 3B │    hotels,
                │ (Q4_K_M)      │    payments)
                │ (~1.8 GB)     │
                │               │
                │ • Deep reason  │
                │ • Step-by-step │
                │ • NL generation│
                └────────────────┘
                  Loaded on-demand,
                  unloaded after use
```

**Architecture Diagrams:**
- [flow_basic.jpeg](flow_and_architecture/flow_basic.jpeg) — High-level routing flow
- [flow_revised.jpeg](flow_and_architecture/flow_revised.jpeg) — Detailed three-mode deployment diagram

---

## Repository Structure

```
finetune_mobile_qwen2.5/
│
├── README.md
│
├── dataset/                            # Training datasets (JSONL)
│   ├── tier_1/
│   │   ├── dataset.jsonl                  # 6,107 router training samples
│   │   ├── dataset_fixed.jsonl            # 6,106 samples (encoding-fixed)
│   │   ├── TIER1_ROUTER.jsonl             # 2,077 curated samples
│   │   └── tier1_router_unsloth_format.*  # 2,000 samples (Unsloth-ready)
│   │
│   └── tier_2/
│       ├── tier2_reasoning_dataset_2k.jsonl   # 2,000 reasoning samples
│       └── tier2_reasoning_dataset_3k.jsonl   # 3,000 reasoning samples
│
├── dataset_creation/                   # Dataset generation scripts
│   ├── generate_dataset_tier_1.py         # Tier-1 router dataset generator
│   ├── generate_dataset_reasoning_tier_2.py  # Tier-2 reasoning dataset generator
│   └── format.json                        # Output schema specification
│
├── flow_and_architecture/              # Architecture docs & diagrams
│   ├── flow_basic.jpeg                    # Basic architecture diagram
│   ├── flow_revised.jpeg                  # Revised multi-mode diagram
│   └── device_run_mobile.md               # Full Flutter integration guide
│
├── Tier-1 & Tier-2 Ai Architecture Implementation Report.pdf
│
├── finetuned/                          # (Google Drive — see links below)
│   ├── qwen_2_5_1_5B/
│   │   ├── finetune_qwen2_5_1_5b_mobile.ipynb   # Training notebook
│   │   ├── model_to_gguf_1_5b.ipynb              # GGUF conversion notebook
│   │   ├── qwen2_5_1_5b_f16.gguf                 # Full precision (2.9 GB)
│   │   ├── qwen2_5_1_5b_Q4_K_M.gguf              # Quantized mobile (941 MB)
│   │   ├── finetuned_model.zip                    # HuggingFace checkpoint
│   │   └── all_training_outputs.zip               # Logs, losses, metrics
│   │
│   └── qwen_2_5_3B/
│       ├── finetune_qwen2_5_3b_mobile.ipynb       # Training notebook
│       ├── model_to_gguf_3b.ipynb                 # GGUF conversion notebook
│       ├── qwen2_5_3b_f16.gguf                    # Full precision (5.8 GB)
│       ├── qwen2_5_3b_Q4_K_M.gguf                # Quantized mobile (1.8 GB)
│       ├── finetuned_model_3b_bitbyte.zip         # HuggingFace checkpoint
│       └── all_training_outputs_bitbyte.zip       # Logs, losses, metrics
```

---

## Model Variants

| Model | Role | Full Precision (F16) | Quantized (Q4_K_M) | Use Case |
|-------|------|---------------------|---------------------|----------|
| Qwen 2.5 — 1.5B | Tier-1 Router | `qwen2_5_1_5b_f16.gguf` (2.9 GB) | `qwen2_5_1_5b_Q4_K_M.gguf` (941 MB) | Intent classification, routing, JSON output |
| Qwen 2.5 — 3B | Tier-2 Reasoner | `qwen2_5_3b_f16.gguf` (5.8 GB) | `qwen2_5_3b_Q4_K_M.gguf` (1.8 GB) | Deep reasoning, explanations, NL generation |

**Q4_K_M** is the recommended format for mobile deployment — it uses 4-bit quantization with K-means clustering, offering near-full-precision quality at a fraction of the size and RAM usage.

---

## Download Links

| Asset | Link |
|-------|------|
| Tier-1 Fine-tuning Folder (all artifacts) | [Google Drive](https://drive.google.com/drive/folders/1_qKCt362SAwuC46BvnwF47B3URSBncCD?usp=sharing) |
| Final Version (models + notebooks + outputs) | [Google Drive](https://drive.google.com/file/d/18j5QvXynqm1aKqBjzeoFMhMBSa0HUOLj/view?usp=sharing) |

---

## Fine-Tuning Pipeline

### Training Setup

Both models are fine-tuned using [Unsloth](https://github.com/unslothai/unsloth) for 2x faster LoRA training with 4-bit quantization.

| Parameter | Tier-1 (1.5B Router) | Tier-2 (3B Reasoner) |
|-----------|----------------------|----------------------|
| Base Model | `unsloth/Qwen2.5-1.5B-bnb-4bit` | `unsloth/Qwen2.5-3B-bnb-4bit` |
| LoRA Rank (r) | 16 | 16 |
| LoRA Alpha | 16 | 16 |
| Dropout | 0 | 0 |
| Batch Size | 4 | 2 |
| Gradient Accumulation | 4 steps | 4 steps |
| Effective Batch Size | 16 | 8 |
| Epochs | 4 | 4 |
| Learning Rate | 2e-4 | 1e-4 |
| Warmup Steps | 5 | 10 |
| Max Sequence Length | 2048 | 2048 |
| Packing | Disabled | Enabled |
| Optimizer | AdamW 8-bit | AdamW 8-bit |
| Weight Decay | 0.01 | 0.01 |

Training was performed on a Tesla T4 GPU (~1.2 hours per model).

### Conversion Pipeline

```
Qwen 2.5 Base (HuggingFace)
    │
    ▼  LoRA fine-tuning (Unsloth + bitsandbytes 4-bit)
LoRA Adapters
    │
    ▼  Merge adapters into base model
Full Fine-tuned Model (SafeTensors)
    │
    ▼  Dequantize NF4 → FP16
FP16 Model Weights
    │
    ▼  llama.cpp convert_hf_to_gguf.py
model_f16.gguf
    │
    ▼  llama-quantize Q4_K_M
model_Q4_K_M.gguf  ← Ready for mobile deployment
```

---

## Dataset Creation

### Tier-1 Router Dataset

**Script:** [`generate_dataset_tier_1.py`](dataset_creation/generate_dataset_tier_1.py)

Generates structured JSON routing decisions across **16 agent domains**:

`youtube` · `flight` · `hotel` · `uber` · `wellness` · `financial_wellness` · `family_care` · `value_assurance` · `tech_connectivity` · `logistics_coordination` · `math_solver` · `transit_planning` · `events_discovery` · `calendar` · `sports` · `god_mode`

**Distribution:** 70% domain-specific queries + 30% simple QA (facts, greetings, math)

**Output schema:**
```json
{
  "intent": "hotel_search",
  "primary_journey": "hotel",
  "journeys": ["hotel", "value_assurance"],
  "direct_answer": null,
  "missing_fields": ["check_in_date", "budget"],
  "needs_clarification": true,
  "clarification": "What are your check-in dates and budget range?",
  "needs_execution": true,
  "execution_type": "cloud_agent",
  "complexity_score": 45,
  "routing_confidence": 0.88,
  "formatting_style": "list"
}
```

### Tier-2 Reasoning Dataset

**Script:** [`generate_dataset_reasoning_tier_2.py`](dataset_creation/generate_dataset_reasoning_tier_2.py)

Generates multi-paragraph natural language responses across **44 diverse topics**:

- **Technology:** quantum computing, machine learning, blockchain, cybersecurity, cloud computing, edge computing
- **Science:** neuroscience, immunology, dark matter, quantum entanglement, ocean acidification
- **Business:** digital transformation, cryptocurrency, supply chain management, behavioral economics
- **Social:** climate change, renewable energy, mental health, online learning, AR/VR in education

**10 question types:** explanation, comparison, application, history, challenges, future predictions, societal impact, technical deep-dive, ethical considerations, limitations

---

## Tier-1 Router — How It Works

The router model receives a user query and outputs a strict JSON control signal that determines the next action:

**Example — Simple factual query:**
```
User: "What is the capital of France?"

Router Output:
{
  "intent": "fact_lookup",
  "primary_journey": "general",
  "direct_answer": "Paris",
  "complexity_score": 5,
  "routing_confidence": 0.97,
  "needs_clarification": false,
  "needs_execution": false
}
→ Action: Respond directly (no Tier-2 needed)
```

**Example — Complex query requiring reasoning:**
```
User: "Compare the economic impact of renewable vs fossil fuels over the next decade"

Router Output:
{
  "intent": "economic_comparison",
  "primary_journey": "financial_wellness",
  "complexity_score": 72,
  "routing_confidence": 0.91,
  "needs_clarification": false,
  "needs_execution": false
}
→ Action: Load Tier-2 reasoner (complexity > 60)
```

**Example — Query needing clarification:**
```
User: "Book me a flight"

Router Output:
{
  "intent": "flight_booking",
  "primary_journey": "flight",
  "missing_fields": ["origin", "destination", "date"],
  "needs_clarification": true,
  "clarification": "Where are you flying from, to which city, and on what date?",
  "needs_execution": true,
  "execution_type": "cloud_agent"
}
→ Action: Ask clarification before proceeding
```

---

## Mobile Deployment

### Device RAM Requirements

| Device RAM | Mode | Models Loaded |
|-----------|------|---------------|
| 3–4 GB | Lite (Tier-1 only) | 1.5B Q4_K_M (~941 MB) |
| 6–8 GB | Full Local | 1.5B always-on + 3B on-demand |
| 8–12+ GB | Both Resident | Both models kept in memory |

### Supported Platforms

- **Android:** [ChatterUI](https://github.com/Mobile-Artificial-Intelligence/chatterui), [PocketPal AI](https://github.com/nicbarker/PocketPal-AI)
- **iOS:** LLM Farm, PocketPal AI
- **Desktop:** [ollama](https://ollama.ai), llama.cpp CLI
- **Flutter:** Native integration via `llama_cpp_dart` FFI bindings (see [device_run_mobile.md](flow_and_architecture/device_run_mobile.md))

### ChatML Prompt Format

Both models use the Qwen ChatML format:

```
<|im_start|>system
You are Arny's Tier-1 Router Model...
<|im_end|>
<|im_start|>user
Book a hotel in Paris under $200
<|im_end|>
<|im_start|>assistant
{"intent": "hotel_booking", ...}
<|im_end|>
```

### Quick Test with llama.cpp

```bash
# Test Tier-1 Router
./llama-cli -m qwen2_5_1_5b_Q4_K_M.gguf \
  -p "<|im_start|>system\nYou are Arny's Tier-1 Router Model. Output strict JSON only.\n<|im_end|>\n<|im_start|>user\nWhat is 25 * 4?\n<|im_end|>\n<|im_start|>assistant\n" \
  -n 256 --temp 0.3

# Test Tier-2 Reasoner
./llama-cli -m qwen2_5_3b_Q4_K_M.gguf \
  -p "<|im_start|>system\nYou are Arny's Tier-2 Reasoning Model. Provide thorough explanations.\n<|im_end|>\n<|im_start|>user\nExplain quantum entanglement in simple terms.\n<|im_end|>\n<|im_start|>assistant\n" \
  -n 512 --temp 0.7
```

---

## GGUF Quantization Formats

| Format | Bits/Weight | Size (1.5B) | Size (3B) | Quality | Speed | Use Case |
|--------|------------|-------------|-----------|---------|-------|----------|
| F16 | 16 | 2.9 GB | 5.8 GB | Maximum | Slower | Desktop / cloud |
| Q8_0 | 8 | ~1.6 GB | ~3.2 GB | Near-lossless | Medium | High-end mobile |
| Q5_K_M | ~5.5 | ~1.2 GB | ~2.1 GB | Very good | Fast | Mid-range mobile |
| **Q4_K_M** | **~4.5** | **941 MB** | **1.8 GB** | **Good** | **Fast** | **Recommended for mobile** |

---

## Tech Stack

| Component | Tool |
|-----------|------|
| Fine-tuning | [Unsloth](https://github.com/unslothai/unsloth) + [TRL](https://github.com/huggingface/trl) |
| LoRA | [PEFT](https://github.com/huggingface/peft) |
| Quantization (training) | [bitsandbytes](https://github.com/TimDettmers/bitsandbytes) (4-bit NF4) |
| Quantization (deployment) | [llama.cpp](https://github.com/ggerganov/llama.cpp) (Q4_K_M) |
| Model Format | SafeTensors → GGUF |
| Base Models | [Qwen 2.5](https://huggingface.co/Qwen) (1.5B, 3B) |
| Mobile Inference | llama.cpp via FFI / Flutter bindings |

---

## Reproducing the Fine-Tune

1. **Generate datasets**
   ```bash
   python dataset_creation/generate_dataset_tier_1.py       # → 3,000 Tier-1 samples
   python dataset_creation/generate_dataset_reasoning_tier_2.py  # → 3,000 Tier-2 samples
   ```

2. **Run fine-tuning notebooks** (Google Colab with T4 GPU recommended)
   - `finetuned/qwen_2_5_1_5B/finetune_qwen2_5_1_5b_mobile.ipynb`
   - `finetuned/qwen_2_5_3B/finetune_qwen2_5_3b_mobile.ipynb`

3. **Convert to GGUF**
   - `finetuned/qwen_2_5_1_5B/model_to_gguf_1_5b.ipynb`
   - `finetuned/qwen_2_5_3B/model_to_gguf_3b.ipynb`

4. **Deploy** — Copy `*_Q4_K_M.gguf` files to device and load via llama.cpp

---

## License

This project fine-tunes [Qwen 2.5](https://huggingface.co/Qwen) models. Please refer to the [Qwen License](https://huggingface.co/Qwen/Qwen2.5-1.5B/blob/main/LICENSE) for model usage terms.
