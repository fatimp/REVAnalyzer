def _delta(a, b):
    if (a+b != 0):
        return 2*abs((a-b)/((a+b)))
    else:
        return 0


def get_sREV_size(sigmas_n, threshold):
    sigmas_n = {key: val for key, val in sigmas_n.items() if val != 0.0}
    sizes = list(sigmas_n.keys())
    sizes.sort(reverse=True)
    for i, l in enumerate(sizes):
        if sigmas_n[l] > threshold:
            if i == 0:
                return None
            else:
                return sizes[i-1]
    return sizes[-1]


def get_dREV_size_1_scalar(values, threshold):
    sizes = list(values.keys())
    sizes.sort(reverse=True)
    for i in range(len(sizes)-1):
        if _delta(values[sizes[i]], values[sizes[i+1]]) > threshold:
            if i == 0:
                return None
            else:
                return sizes[i]
    return sizes[-1]


def get_dREV_size_1_scalar_dimensional(values, threshold):
    sizes = list(values.keys())
    sizes.sort(reverse=True)
    result = []
    for k in range(3):
        label = 0
        for i in range(len(sizes)-1):
            if _delta(values[sizes[i]][k], values[sizes[i+1]][k]) > threshold:
                if i == 0:
                    return None
                else:
                    result.append(sizes[i])
                    label = 1
        if (label == 0):
            result.append(sizes[-1])
    return max(result)


def get_dREV_size_2_scalar(values, threshold):
    sizes = list(values.keys())
    sizes.sort(reverse=True)
    value0 = values[sizes[0]]
    for i in range(1, len(sizes)):
        if _delta(values[sizes[i]], value0) > threshold:
            if i == 1:
                return None
            else:
                return sizes[i-1]
    return sizes[-1]


def get_dREV_size_2_scalar_dimensional(values, threshold):
    sizes = list(values.keys())
    sizes.sort(reverse=True)
    result = []
    for k in range(3):
        value0 = values[sizes[0]][k]
        label = 0
        for i in range(len(sizes)-1):
            if _delta(values[sizes[i]][k], value0) > threshold:
                if i == 0:
                    return None
                else:
                    result.append(sizes[i])
                    label = 1
        if label == 0:
            result.append(sizes[-1])
    return max(result)


def get_dREV_size_1_vector(values, threshold):
    sizes = list(values.keys())
    sizes.sort(reverse=True)
    for i in range(len(sizes)):
        if values[sizes[i]] > threshold:
            if i == 0:
                return None
            else:
                return sizes[i-1]
    return sizes[-1]
