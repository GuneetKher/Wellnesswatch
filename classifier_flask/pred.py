import torch



class ClassPredictor:
  def __init__(self,model,tokenizer):
    self.model = model
    self.tokenizer = tokenizer
    # self.model.load_state_dict(torch.load('/content/drive/MyDrive/roberta_model.pt'))
    # self.model.load_state_dict(torch.load(model_state))
    self.model.eval()

  def __call__(self, text, prob=True):
    if isinstance(text, str):
      text = [text]
      unpack = True
    else:
      unpack = False

    tokenized_text = [self.tokenizer.encode(t, add_special_tokens=True) for t in text]
    # Pad the tokenized input text to the same length
    max_length = max(len(t) for t in tokenized_text)
    padded_text = [t + [0] * (max_length - len(t)) for t in tokenized_text]
    # Convert the padded input text to PyTorch tensor
    input_ids = torch.tensor(padded_text)
    # Make predictions with the model
    with torch.no_grad():
      logits = self.model(input_ids).logits
      probs = torch.softmax(logits, dim=1)
        

    if prob:
      if unpack:
        return (probs[0,1].tolist())
      else:
        return (bool(logits.argmax()),probs[:,1].tolist())
    else:
      return bool(logits.argmax())

