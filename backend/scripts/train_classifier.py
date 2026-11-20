"""
Usage (backend folder se):
    python scripts/train_classifier.py --hf-user your-hf-username

Do models banata hai: category aur urgency. Hugging Face Hub par push karta hai.

NOTE: This script requires PyTorch and training-specific packages.
      Install them via:  pip install -r requirements-train.txt
"""
import argparse

import numpy as np
import pandas as pd
from datasets import Dataset
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)

BASE_MODEL = "distilbert-base-uncased"


def compute_metrics(eval_pred):
    preds = np.argmax(eval_pred.predictions, axis=-1)
    return {
        "accuracy": accuracy_score(eval_pred.label_ids, preds),
        "f1": f1_score(eval_pred.label_ids, preds, average="macro"),
    }


def train_one(df: pd.DataFrame, label_col: str, repo_id: str):
    labels = sorted(df[label_col].unique())
    label2id = {l: i for i, l in enumerate(labels)}
    id2label = {i: l for l, i in label2id.items()}
    y = df[label_col].map(label2id).values

    train_x, test_x, train_y, test_y = train_test_split(
        df["text"].tolist(), y, test_size=0.2, stratify=y, random_state=42
    )

    tok = AutoTokenizer.from_pretrained(BASE_MODEL)

    def tokenize(examples):
        return tok(examples["text"], truncation=True, max_length=256, padding=True)

    train_ds = Dataset.from_dict({"text": train_x, "labels": train_y.tolist()}).map(tokenize, batched=True)
    test_ds = Dataset.from_dict({"text": test_x, "labels": test_y.tolist()}).map(tokenize, batched=True)

    model = AutoModelForSequenceClassification.from_pretrained(
        BASE_MODEL, num_labels=len(labels), id2label=id2label, label2id=label2id
    )

    args = TrainingArguments(
        output_dir=f"./out-{label_col}",
        num_train_epochs=4,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        learning_rate=2e-5,
        weight_decay=0.01,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        logging_steps=20,
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        eval_dataset=test_ds,
        compute_metrics=compute_metrics,
    )
    trainer.train()
    print(f"[{label_col}] eval:", trainer.evaluate())

    model.push_to_hub(repo_id)
    tok.push_to_hub(repo_id)
    print(f"[{label_col}] pushed to {repo_id}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hf-user", required=True)
    parser.add_argument("--data", default="data/tickets.csv")
    args = parser.parse_args()

    df = pd.read_csv(args.data).dropna(subset=["text", "category", "urgency"])
    print(f"Rows: {len(df)}")
    print(df["category"].value_counts())

    train_one(df, "category", f"{args.hf_user}/smarttriage-category")
    train_one(df, "urgency", f"{args.hf_user}/smarttriage-urgency")


if __name__ == "__main__":
    main()
