

class throughput():
    def __init__(self):
        # h5 ILP data  15s begin
        self.y1 = [
            0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
            0.00, 0.00, 0.00, 0.00, 0.00,
            7.76, 7.97, 7.79, 7.83, 7.77, 7.79, 7.77, 7.77, 7.79,
            7.77, 7.77, 7.79, 7.77, 7.77, 7.79
        ]
        # h6 data  5s begin
        self.y2 = [
            0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
            6.28, 6.01, 6.00, 6.00, 6.00, 6.01, 6.00, 6.00, 6.00,
            6.00, 6.01, 6.00, 6.00, 6.00, 6.00, 6.01, 6.00, 6.00, 6.00,
            6.00, 6.01, 6.00, 6.00, 6.00, 6.00
        ]
        # h7 data  10s begin
        self.y3 = [
            0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
            4.99, 5.00, 5.01, 5.00, 5.00, 4.97,
            3.85, 3.87, 3.88, 3.86, 3.87, 3.89, 3.86, 3.86, 3.86, 3.88,
            3.85, 3.85, 3.85, 3.85
        ]
        # h8 data  0s begin
        self.y4 = [
            0.00, 4.01, 4.00, 4.00, 4.00, 4.00, 4.02, 4.01, 4.00,
            4.02, 4.01, 4.01, 4.00, 3.99, 4.02, 3.96, 4.03,
            4.00, 0.341, 0.329, 0.341, 0.353, 0.329, 0.329, 0.353, 0.341,
            0.341, 0.341, 0.341, 0.341, 0.341
        ]

class throughput2():
    def __init__(self):
        # h5 CWSP data  15s begin
        self.y1 = [
            0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
            0.00, 0.00, 0.00, 0.00, 0.00,
            6.81, 6.52, 6.51, 6.51, 6.52, 6.52, 6.42, 6.52, 6.53,
            6.51, 6.52, 6.53, 6.52, 6.51, 6.52
        ]
        # h6 data  5s begin
        self.y2 = [
            0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
            6.32, 6.01, 6.00, 6.00, 6.00, 6.00, 6.01, 6.00, 6.00,
            6.00, 6.00, 6.01, 6.00, 6.00, 6.00, 6.01, 6.00, 6.00, 6.00,
            6.00, 6.01, 6.00, 6.00, 6.00, 6.00
        ]
        # h7 data  10s begin
        self.y3 = [
            0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
            5.00, 5.01, 5.00, 5.00, 5.01, 3.33, 3.34,
            3.32, 3.31, 3.54, 3.35, 3.33, 3.34, 3.32, 3.21, 3.33, 3.32,
            3.32, 3.31, 3.31
        ]
        # h8 data  0s begin
        self.y4 = [
            0.00, 3.86, 4.00, 4.00, 4.01, 4.00, 4.00, 4.00, 4.00, 4.01,
            4.02, 3.95, 4.06, 3.99, 4.00, 3.97, 3.99, 4.05, 3.99, 3.97,
            4.03, 4.01, 4.00, 4.00, 3.99, 3.99, 4.02, 4.00, 4.01, 4.00,
            3.99
        ]

class sender():
    def __init__(self):
        self.y1 = [
            0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00
            , 0.00, 0.00, 0.00, 0.00, 0.00, 8.00, 8.00, 8.00, 8.00,
            8.00, 8.00, 8.00, 8.00, 8.00, 8.00, 8.00, 8.00, 8.00, 8.00,
            8.00
        ]
        # h6 data  5s begin
        self.y2 = [
            0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 6.00, 6.00, 6.00, 6.00, 6.00
            , 6.00, 6.00, 6.00, 6.00, 6.00, 6.00, 6.00, 6.00, 6.00,
            6.00, 6.00, 6.00, 6.00, 6.00, 6.00, 6.00, 6.00, 6.00, 6.00,
            6.00
        ]
        # h7 data  10s begin
        self.y3 = [
            0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
            5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00,
            5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00,
            5.00
        ]
        # h8 data  0s begin
        self.y4 = [
            0.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00,
            4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00,
            4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00,
            4.00
        ]

sender_throughput = sender()
CWSP_throughput = throughput2()
ILP_throughput = throughput()