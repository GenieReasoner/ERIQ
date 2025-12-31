# ERIQ Benchmark: Embodied Reasoning Intelligence Quotient

[![arXiv](https://img.shields.io/badge/arXiv-2501.XXXXX-b31b1b.svg)](https://arxiv.org/abs/2501.XXXXX)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Dataset-yellow)](https://huggingface.co/datasets/YOUR_ORG/ERIQ)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## Overview

ERIQ is a large-scale embodied reasoning benchmark for robotic manipulation, comprising **6,052** question-answer pairs across **15 fine-grained sub-tasks** organized into **4 major reasoning dimensions**. This benchmark decouples cognitive reasoning from motor control, enabling independent evaluation of embodied reasoning capabilities without confounding action execution errors.

## Benchmark Structure

### Four Major Reasoning Dimensions

1. **Spatial Perception & Grounding**
   - Scene Understanding
   - Dualview Matching
   - Task Grounding
   - Relative Position Grounding

2. **Planning & Monitoring**
   - Action Understanding
   - Success Detection
   - Subtask Planning
   - Fine-grained Planning
   - Trajectory Understanding
   - Task Progress

3. **Error Detection & Recovery**
   - Mistake Existence
   - Mistake Classification
   - Mistake Recovery

4. **Human Intent Understanding**
   - Human Intention Comprehension
   - Human-Robot Interaction

## Dataset Characteristics

- **Total QA Pairs**: 6,052
- **Task Scenarios**: 100+ distinct scenarios across 5 domains
  - Household (35%)
  - Restaurant (20%)
  - Supermarket (20%)
  - Industrial (15%)
  - Office (10%)
- **Modalities**:
  - Single Image (53%)
  - Sequential Images (26%)
  - Interleaved Image-Text Sequences (21%)
- **Data Source**: Real-world robotic trials with first-person (Robo View) perspective
- **Evaluation Format**: Multiple Choice (MC) and Binary (Yes/No) for deterministic, reproducible evaluation

## Dataset Files
```
Embodied_Reasoning_Intelligence_Quotient/
├── images/                              # Visual data for all questions
├── QA_ACTION_UNDERSTANDING.json         # Action understanding tasks
├── QA_DUALVIEW_MATCHING.json           # Multi-view spatial reasoning
├── QA_FINE_GRAINED_PLAN.json           # Detailed planning tasks
├── QA_HUMAN_INTENTION.json             # Human intention comprehension
├── QA_HUMAN_INTERACTION.json           # Human-robot collaboration
├── QA_MISTAKE_RECOVERY.json            # Error recovery strategies
├── QA_MISTAKE_CLASSIFY.json            # Error classification tasks
├── QA_MISTAKE_EXISTENCE.json           # Error detection tasks
├── QA_RELATIVE_POS_GROUNDING.json      # Relative position understanding
├── QA_SCENE_UNDERSTANDING.json         # Scene comprehension
├── QA_SUBTASK_PLANNING.json            # High-level task decomposition
├── QA_SUCCESS_DETECTION.json           # Task completion verification
├── QA_TASK_GROUNDING.json              # Task-relevant object grounding
├── QA_TASK_PROGRESS.json               # Progress monitoring
└── QA_TRAJ_UNDERSTANDING.json          # Trajectory reasoning
```

## Data Format

Each JSON file contains a list of question-answer pairs with the following structure:
```json
[
    {
        "id": "QA_ACTION_UNDERSTANDING:1",
        "image": [
            "path/to/image1.jpg",
            "path/to/image2.jpg"
        ],
        "conversations": [
            {
                "from": "human",
                "value": "<image>\n<image>\nQuestion text with options..."
            },
            {
                "from": "gpt",
                "value": "C"
            }
        ],
        "gt_answer": "C"
    }
]
```

### Field Descriptions

- `id`: Unique identifier in format `CATEGORY:INDEX`
- `image`: List of image paths (single or multiple images depending on the question type)
- `conversations`: Dialog format containing the question and ground truth answer
  - `from: "human"`: Question with `<image>` placeholders and multiple choice options
  - `from: "gpt"`: Ground truth answer
- `gt_answer`: Ground truth answer (letter for MC questions, "Yes"/"No" for binary questions)

## Key Features

- ✅ **Full Coverage**: Only benchmark providing comprehensive support across all four reasoning dimensions
- ✅ **Real-World Data**: All data from authentic robotic trials
- ✅ **Deterministic Evaluation**: Standardized MC format eliminates subjective scoring
- ✅ **Reasoning-Execution Decoupling**: Isolates cognitive capabilities from motor control
- ✅ **Predictive Value**: Strong positive correlation with end-to-end VLA generalization performance

---

## Evaluation Toolkit

Please use this toolkit for a fair comparison with published baselines.

### Step 1: Format Your Results

Format your model's predictions as a JSON list following this structure:
```json
[
    {
        "id": "QA_ACTION_UNDERSTANDING:1",
        "image": [...],
        "conversations": [...],
        "prediction": "C",
        "gt_answer": "C"
    },
    {
        "id": "QA_MISTAKE_EXISTENCE:1",
        "image": [...],
        "conversations": [...],
        "prediction": "No",
        "gt_answer": "No"
    }
]
```

**Required fields**:
- `id`: Must match the original question ID
- `prediction`: Your model's predicted answer (letter or "Yes"/"No")
- `gt_answer`: Ground truth answer (copy from original data)

**Optional fields** (can be included for reference):
- `image`: Image paths from original data
- `conversations`: Original question-answer pairs

### Step 2: Run the Evaluation Script
```bash
python eval_code/eval_hf.py eval_code/example.json
```

The script will automatically:
- Load your prediction file
- Calculate per-category accuracy for each sub-task
- Compute the weighted average accuracy across all categories
- Display results in a formatted table

### Example Output
```bash
python eval_code/eval_hf.py eval_code/example.json

Successfully read JSON file: eval_code/example.json
Total entries: 3
+--------------------------+-----------------+------------+------------------+
| Test Subset              | Total Samples   | Correct    | Accuracy         |
+==========================+=================+============+==================+
| QA_ACTION_UNDERSTANDING  | 1               | 1          | 1.0000 (100.00%) |
+--------------------------+-----------------+------------+------------------+
| QA_MISTAKE_EXISTENCE     | 2               | 1          | 0.5000 (50.00%)  |
+--------------------------+-----------------+------------+------------------+
| ----------               | ----------      | ---------- | ----------       |
+--------------------------+-----------------+------------+------------------+
| Total / Weighted Average | 3               | N/A        | 0.6667 (66.67%)  |
+--------------------------+-----------------+------------+------------------+

Detailed Statistics:
Total samples: 3
Number of test subsets: 2
Weighted average accuracy: 0.6667 (66.67%)
```

### Understanding the Results

- **Test Subset**: The category of questions (e.g., QA_ACTION_UNDERSTANDING, QA_MISTAKE_EXISTENCE)
- **Total Samples**: Number of questions in this category
- **Correct**: Number of correctly predicted answers
- **Accuracy**: Category-specific accuracy as both decimal and percentage
- **Weighted Average**: Overall performance across all categories, weighted by the number of samples in each category

---

## Baseline Results

| Model | Overall ERIQ Score |
|-------|-------------------|
| Qwen2.5-VL-3B | 58.64% |
| Qwen2.5-VL-7B | 66.69% |
| InternVL-3.5-8B | 66.72% |
| RoboBrain2.0-7B | 67.38% |
| Cosmos-Reason1-7B | 67.99% |
| Claude-Sonnet-4 | 65.66% |
| Qwen3-VL-8B | 75.53% |
| GPT-4o-mini | 77.61% |
| Gemini-2.5-pro | 80.55% |
| **GenieReasoner-3B (Ours)** | **82.72%** |

---

## Citation

If you use the ERIQ benchmark in your research, please cite:
```bibtex
@article{liu2025geniereasoner,
  title={Unified Embodied VLM Reasoning with Robotic Action via Autoregressive Discretized Pre-training},
  author={Liu, Yi and Wang, Sukai and Wei, Dafeng and Cai, Xiaowei and Zhong, Linqing and Yang, Jiange and Ren, Guanghui and Zhang, Jinyu and Yao, Maoqing and Li, Chuankang and He, Xindong and Chen, Liliang and Luo, Jianlan},
  journal={arXiv preprint arXiv:submit/7120983},
  year={2025}
}
```

---

## License

### Code (Evaluation Scripts)
MIT License - see [LICENSE-CODE](LICENSE-CODE)

### Dataset (ERIQ Benchmark)
Creative Commons Attribution 4.0 International (CC BY 4.0) - see [LICENSE-DATA](LICENSE-DATA)

© 2025 AgiBot Research. All Rights Reserved.

**Contact**: For commercial licensing inquiries, please contact [licensing@agibot.com](mailto:licensing@agibot.com)