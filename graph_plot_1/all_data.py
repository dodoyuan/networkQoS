

class throughput():
    def __init__(self):
        # h5 ILP data  15s begin
        self.y1 = [
            0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
            0.00, 0.00, 0.00, 0.00, 0.00,
            8.56, 7.97, 7.79, 7.83, 7.77, 7.79, 7.77, 7.77, 7.79,
            7.77, 7.77, 7.79, 7.77, 7.77, 7.79
        ]
        # h6 data  5s begin
        self.y2 = [
            0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
            6.58, 6.01, 6.00, 6.00, 6.00, 6.01, 6.00, 6.00, 6.00,
            6.00, 6.01, 6.00, 6.00, 6.00, 6.00, 6.01, 6.00, 6.00, 6.00,
            6.00, 6.01, 6.00, 6.00, 6.00, 6.00
        ]
        # h7 data  10s begin
        self.y3 = [
            0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
            5.49, 5.00, 5.01, 5.00, 5.00, 4.97,
            3.85, 3.87, 3.88, 3.86, 3.87, 3.89, 3.86, 3.86, 3.86, 3.88,
            3.85, 3.85, 3.85, 3.85
        ]
        # h8 data  0s begin
        # self.y4 = [
        #     0.00, 4.31, 4.00, 4.00, 4.00, 4.00, 4.02, 4.01, 4.00,
        #     4.02, 4.01, 4.01, 4.00, 3.99, 4.02, 3.96, 4.03,
        #     4.00, 0.341, 0.329, 0.341, 0.353, 0.329, 0.329, 0.353, 0.341,
        #     0.341, 0.341, 0.341, 0.341, 0.341
        # ]

        self.y4 = [
            0.00, 4.31, 4.00, 4.00, 4.00, 4.00, 4.02, 4.01, 4.00,
            4.02, 4.01, 4.01, 4.00, 3.99, 4.02, 3.96, 4.03,
            4.00, 2.141, 2.129, 2.141, 2.153, 2.129, 2.129, 2.153, 2.141,
            2.141, 2.141, 2.141, 2.141, 2.141
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
            5.40, 5.01, 5.00, 5.00, 5.01, 3.33, 3.34,
            3.32, 3.31, 3.54, 3.35, 3.33, 3.34, 3.32, 3.21, 3.33, 3.32,
            3.32, 3.31, 3.31
        ]
        # h8 data  0s begin
        self.y4 = [
            0.00, 4.36, 4.00, 4.00, 4.01, 4.00, 4.00, 4.00, 4.00, 4.01,
            4.02, 3.95, 4.06, 3.99, 4.00, 3.97, 3.99, 4.05, 3.99, 3.97,
            4.03, 4.01, 4.00, 4.00, 3.99, 3.99, 4.02, 4.00, 4.01, 4.00,
            3.99
        ]


class throughput3():
    def __init__(self):
        # h5 SP data  15s begin  8M  35%

        self.y1 = [
            0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
            0.00, 0.00, 0.00, 0.00, 0.00, 4.80, 4.55, 4.25, 4.36,
            4.27, 4.19, 4.20, 4.20, 4.28, 4.25, 4.23, 4.20, 4.29, 4.22, 4.21
        ]
        # h6 data  5s begin   6M  25%
        self.y2 = [
            0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 6.51, 6.00, 6.00, 6.00, 6.00,
            5.11, 5.48, 5.55, 5.57, 5.57, 3.22, 3.36, 3.79, 3.74,
            3.70, 3.79, 3.75, 3.80, 3.76, 3.77, 3.79, 3.81, 3.79, 3.81, 3.80

        ]
        # h7 data  10s begin   5M  40%
        self.y3 = [
            # 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 5.74, 5.01, 5.00, 5.00, 5.00,
            # 3.23, 2.86, 3.05, 3.35, 3.23, 3.39, 3.39, 3.26, 3.36,
            # 3.36, 3.52, 3.36, 3.45, 3.56, 3.29, 3.36, 3.35, 3.35, 3.38, 3.34

            0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
            4.70, 4.65, 4.63, 4.63, 4.62, 2.45, 2.29, 2.15, 2.16,
            2.14, 2.26, 2.26, 2.28, 2.18, 2.22, 2.15, 2.27, 2.14, 2.20, 2.19
        ]

        # h8 data  0s begin   4M  61%
        self.y4 = [
            0.00, 4.00, 4.00, 4.00, 4.00, 4.00, 3.58, 4.05, 4.09, 4.02, 4.06,
            1.46, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01

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
SP_throughput = throughput3()
