import numpy as np

np.random.seed(4444)


def basic_monte_carlo(x_0, time_steps, paths, step_calc_fun):
    t_size = np.size(time_steps)-1
    X = np.zeros((1, t_size), int)
    for j in range(0, paths):
        Z = np.random.normal(loc=0, scale=1, size=t_size)
        x_j = np.array([x_0])

        for i in range(1, t_size):
            x_next = step_calc_fun(x_j[i - 1], time_steps, i, Z[i])
            x_j = np.append(x_j, x_next)

        X = np.vstack((X, [x_j]))
    return X[1:]

def longstaff_schwarz_method(sim_paths, cash_flows, discont_values = None):
    n = len(sim_paths)
    m = len(sim_paths[0])
    # disconting cash flows
    # ONLY FOR STOCKS CHECK IF IS AN OPTION FOR SWAP
    """
    for i in range(0, n):
        for j in range(0, m):
            if cash_flows[i][j] > 0.0:
                cash_flows[i][j] = discont_values[j]*cash_flows[i][j]
            else:
                cash_flows[i][j] = 0.0
    """
    for k in range(m - 2, 0, -1):
        # print(m)
        X = []
        Y = []
        j = []
        for i in range(0, n):
            if cash_flows[i][k] > 0.0:
                j.append(i)
                x = sim_paths[i][k]
                #X.append([np.exp(-x / 2), np.exp(-x / 2) * -2 * x, np.exp(-x / 2) * ((x * x) / 2)])
                X.append([1, x, x*x]) #kleinste quadrate
                # B_t=np.exp(-mü*T[t_pay[m+1]])
                Y.append(cash_flows[i][k + 1])
            else:
                cash_flows[i][k] = 0.0
        # lösen des Regressionsproblem mit QR Verfahren (Minimierung)
        if Y:
            Q, R = np.linalg.qr(X)
            p = np.dot(Q.T, Y)
            a = np.dot(np.linalg.pinv(R), p)
            C = np.dot(X, a)

            # print(C)
            V = []
            for i in j:
                V.append(cash_flows[i][k])

            for i in range(len(V)):
                if V[i] >= C[i]:
                    cash_flows[j[i]][k + 1] = 0.0
                else:
                    cash_flows[j[i]][k] = 0.0
    return cash_flows

