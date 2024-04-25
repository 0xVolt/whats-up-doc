from transformers import BertForSequenceClassification, BertTokenizer, AdamW
import torch
import numpy.random as random

# Load pre-trained BERT model and tokenizer
model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2) # 2 for binary classification

# Prepare data
# Generating example data
num_samples = 250

# Example sentences
train_texts = ["The cat is on the mat.", "The dog barks loudly.", "Birds chirp in the morning.", "Sunsets are beautiful."]

# Generating random binary labels (0 or 1) for each sentence
train_labels = [random.choice([0, 1]) for _ in range(num_samples)]

# train_texts = ["example sentence 1", "example sentence 2", ...]
# train_labels = [1, 0, ...] # binary labels for each sentence

input_ids = []
attention_masks = []

for text in train_texts:
    encoded_dict = tokenizer.encode_plus(
                        text,
                        add_special_tokens=True,
                        max_length=64,
                        pad_to_max_length=True,
                        return_attention_mask=True,
                        return_tensors='pt'
                    )

    input_ids.append(encoded_dict['input_ids'])
    attention_masks.append(encoded_dict['attention_mask'])

input_ids = torch.cat(input_ids, dim=0)
attention_masks = torch.cat(attention_masks, dim=0)
train_labels = torch.tensor(train_labels)

# Create data loader
batch_size = 32
train_data = torch.utils.data.TensorDataset(input_ids, attention_masks, train_labels)
train_sampler = torch.utils.data.RandomSampler(train_data)
train_dataloader = torch.utils.data.DataLoader(train_data, sampler=train_sampler, batch_size=batch_size)

# Set device to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Set optimizer and learning rate
optimizer = AdamW(model.parameters(), lr=1e-5)

# Training loop
num_epochs = 5

for epoch in range(num_epochs):
    total_loss = 0

    for batch in train_dataloader:
        batch = tuple(t.to(device) for t in batch)
        input_ids, attention_masks, labels = batch

        model.zero_grad()

        outputs = model(input_ids, attention_mask=attention_masks, labels=labels)
        loss = outputs.loss
        total_loss += loss.item()

        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

        optimizer.step()

    averageLoss = total_loss / len(train_dataloader)
    print(f"Epoch {epoch + 1} / {num_epochs}, Loss: {averageLoss}")