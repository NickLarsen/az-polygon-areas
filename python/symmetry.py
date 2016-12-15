def canonicalHash(state):
    return min([
        hashState(state),
        hashState(symX(state)),
        hashState(symY(state)),
        hashState(symD1(state)),
        hashState(symD2(state)),
        hashState(symR90(state)),
        hashState(symR180(state)),
        hashState(symR270(state))
    ])

def hashState(state):
    return hash("-".join([str(i) for i in state]))

def symX(state):
    N = len(state)
    return [state[N - (i + 1)] for i in range(N)]

def symY(state):
    N = len(state)
    return [N - (state[i] + 1) for i in range(N)]

def symD1(state):
    return [state.index(i) for i in range(len(state))]

def symD2(state):
    N = len(state)
    return [N - (state.index(N-(i+1)) + 1) for i in range(N)]

def symR90(state):
    N = len(state)
    return [N - (state.index(i) + 1) for i in range(N)]

def symR180(state):
    N = len(state)
    return [N - (state[N-(i+1)] + 1) for i in range(N)]

def symR270(state):
    N = len(state)
    return [state.index(N-(i+1)) for i in range(N)]