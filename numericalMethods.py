import numpy as np

np.random.seed(4949)


def basic_monte_carlo(x_0, time_steps, paths, step_calc_fun):
    t_size = np.size(time_steps)
    X = np.zeros((1, t_size), int)
    for j in range(0, paths):
        Z = np.random.normal(loc=0, scale=1, size=t_size)
        x_j = np.array([x_0])

        for i in range(1, t_size):
            h = time_steps[i] - time_steps[i - 1]
            x_next = step_calc_fun(x_j[i - 1], h, Z[i])
            x_j = np.append(x_j, x_next)

        X = np.vstack((X, [x_j]))
    return X[1:]

def longstaff_schwarz_method(sim_paths, cash_flows, discont_values):
    n = len(sim_paths)
    m = len(sim_paths[0])
    # disconting cash flows
    for i in range(0, n):
        for j in range(0, m):
            if cash_flows[i][j] > 0.0:
                cash_flows[i][j] = discont_values[m-1]*cash_flows[i][j]
            else:
                cash_flows[i][j] = 0.0

    for m in range(m - 2, 0, -1):
        # print(m)
        X = []
        Y = []
        j = []
        for i in range(0, n):
            if cash_flows[i][m] > 0.0:
                j.append(i)
                x = sim_paths[i][m]
                X.append([np.exp(-x / 2), np.exp(-x / 2) * -2 * x, np.exp(-x / 2) * ((x * x) / 2)])
                # X.append([1,x,x*x]) #kleinste quadrate
                # B_t=np.exp(-mü*T[t_pay[m+1]])
                Y.append(cash_flows[i][m + 1])

        # lösen des Regressionsproblem mit QR Verfahren (Minimierung)
        Q, R = np.linalg.qr(X)
        p = np.dot(Q.T, Y)
        a = np.dot(np.linalg.pinv(R), p)

        C = np.dot(X, a)

        # print(C)
        V = []
        for i in j:
            V.append(cash_flows[i][m])

        for i in range(len(V)):
            if V[i] >= C[i]:
                cash_flows[j[i]][m + 1] = 0.0
            else:
                cash_flows[j[i]][m] = 0.0
    return cash_flows

