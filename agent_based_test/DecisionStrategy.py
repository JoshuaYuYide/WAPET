
class REINFORCE():
    def __init__(self, model, optimizer, gamma=0.99):
        self.model = model
        self.optimizer = optimizer
        self.gamma = gamma

    def decide(self, state):
        return self.model(state).sample()

    def learn(self, state, action, reward, next_state):
        self.optimizer.zero_grad()
        loss = self.model.loss(state, action, reward, next_state, self.gamma)
        loss.backward()
        self.optimizer.step()

class RandomStrategy():
    def decide(self, state):
        return random.choice(state.actions)


class ChatGPT():
    def __init__(self, model, tokenizer, device):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device

    def decide(self, state):
        input_ids = self.tokenizer.encode(state, return_tensors="pt").to(self.device)
        output = self.model.generate(input_ids, max_length=50, num_return_sequences=1)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)




