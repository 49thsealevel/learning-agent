import torch
import torch.nn as nn
from torch.nn.utils.rnn import pad_sequence

from app.agents.sequence_encoder import LSTMAutoencoder


def test_seq_to_seq_training():
    # Instantiate the autoencoder
    input_size = (4,)
    hidden_size = 8
    num_layers = 1
    autoencoder = LSTMAutoencoder(input_size, hidden_size, num_layers)

    # Define the training data with variable-length sequences
    data = [
        torch.tensor([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]], dtype=torch.float32),
        torch.tensor([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=torch.float32),
        torch.tensor([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]], dtype=torch.float32)
    ]
    # Get the sequence lengths
    seq_len = torch.tensor([len(d) for d in data], dtype=torch.int)
    # Pad to max sequence length
    padded_data = pad_sequence(data, batch_first=True)

    # Train the autoencoder for some number of epochs
    num_epochs = 1000
    for epoch in range(num_epochs):
        autoencoder.train_iter(padded_data, seq_len)

    for i in range(padded_data.size()[0]):
        input_batch = padded_data[i, 0:seq_len[i].item(), :]
        output, hidden, cell = autoencoder.encoder(input_batch)
        output = torch.zeros(1, 4)
        for j in range(seq_len[i].item()):
            output, hidden, cell = autoencoder.decoder(output, hidden, cell)
            assert torch.allclose(input_batch[j:j+1, :], output, atol=2e-2)
