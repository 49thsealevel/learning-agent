from math import prod

import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence


class LSTMEncoder(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(
            input_size=prod(input_size),
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
        )

    def forward(self, x, hidden=None, cell=None):
        hx = None
        if hidden is not None:
            hx = (hidden, cell)
        output, (hidden, cell) = self.lstm(x, hx)
        return output, hidden, cell


class LSTMDecoder(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.lstm = nn.LSTM(
            input_size=prod(input_size),
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
        )
        self.linear = nn.Linear(
            in_features=hidden_size,
            out_features=prod(input_size),
        )

    def forward(self, x, hidden=None, cell=None):
        hx = None
        if hidden is not None:
            hx = (hidden, cell)
        output, (hidden, cell) = self.lstm(x, hx)
        output = self.linear(output)
        return output, hidden, cell


class LSTMAutoencoder(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super().__init__()
        self.input_size = input_size
        self.encoder = LSTMEncoder(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
        )
        self.decoder = LSTMDecoder(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
        )

        self.loss_1 = nn.MSELoss()

        self.optimizer = torch.optim.Adam(self.parameters(), lr=1e-2)

    def forward(self, x, seq_len):
        """
        Autoencoder needs the sequence lengths for the inputs, so that it can pack the sequences
        for batching
        Inputs should be size (batch_size, max_seq_len, action_size)
        """
        # Get the input shape
        s = x.size()
        batch_size, max_seq_len = s[0], s[1]

        # Pack the inputs to ignore outside length
        packed_input = pack_padded_sequence(x, seq_len, batch_first=True, enforce_sorted=False)

        # Run the packed input through the encoder
        # The input to the decoder is the hidden and cell state from the last
        # sequence item
        _, hidden, cell = self.encoder(packed_input)

        # The inputs start with zeros for action_size, and all following actions should
        # match the actions taken.
        dec_input = torch.zeros((batch_size, 1, *self.input_size), dtype=torch.float32)

        dec_input = dec_input + (0.1**0.5) * torch.randn(*dec_input.size())

        # Predictions are per timestep, we want results to line up with batch,
        # So we append to the batch's list, and concat at the end.
        dec_outputs = [[] for _ in range(batch_size)]
        for i in range(max(seq_len)):
            # One element slice on sequence for entire batch
            # Cache hidden and cell for next time step
            dec_input, hidden, cell = self.decoder(dec_input, hidden, cell)
            for j in range(batch_size):
                dec_outputs[j].append(dec_input[j, :, :])
            dec_input = dec_input + (0.1 ** 0.5) * torch.randn(*dec_input.size())

        # Create
        outputs = torch.cat([torch.cat(o) for o in dec_outputs])
        return outputs.view(batch_size, max_seq_len, *self.input_size)

    def train_iter(self, batched_padded_inputs, sequence_lengths) -> None:
        mask = torch.arange(0, len(batched_padded_inputs) + 1).unsqueeze(0) < sequence_lengths.unsqueeze(1)

        output = self.forward(batched_padded_inputs, sequence_lengths)

        self.optimizer.zero_grad()
        # Output is shape (batch_size, max_sequence_len, prediction)
        # Need to mask the unwanted elements in output and padded input
        loss = self.loss_1(output[mask], batched_padded_inputs[mask])
        loss.backward()
        self.optimizer.step()
