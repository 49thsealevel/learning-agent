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

    # Define the loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(autoencoder.parameters(), lr=1e-2)

    # Define the training data with variable-length sequences
    data = [
        torch.tensor([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]], dtype=torch.float32),
        torch.tensor([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=torch.float32),
        torch.tensor([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]], dtype=torch.float32)
    ]
    # Get the sequence lengths
    seq_len = torch.tensor([len(d) for d in data], dtype=torch.int)
    mask = torch.range(0, len(data)).unsqueeze(0) < seq_len.unsqueeze(1)
    # Pad to max sequence length
    padded_data = pad_sequence(data, batch_first=True)

    # Train the autoencoder for some number of epochs
    num_epochs = 1000
    for epoch in range(num_epochs):
        output = autoencoder(padded_data, seq_len)

        optimizer.zero_grad()
        # Output is shape (batch_size, max_sequence_len, prediction)
        # Need to mask the unwanted elements in output and padded input
        loss = criterion(output[mask], padded_data[mask])
        loss.backward()
        optimizer.step()

    for i in range(padded_data.size()[0]):
        input_batch = padded_data[i, 0:seq_len[i].item(), :]
        output, hidden, cell = autoencoder.encoder(input_batch)
        output = torch.zeros(1, 4)
        for j in range(seq_len[i].item()):
            output, hidden, cell = autoencoder.decoder(output, hidden, cell)
            assert torch.allclose(input_batch[j:j+1, :], output, atol=1e-2)
