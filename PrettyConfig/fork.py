import copy

from numpy import prod

from .hyperparameters import HyperParameters


class ChoiceList(list):
    pass


def _get_bounds(rep_dict):
    result = list()
    for (recursive, k), v in sorted(rep_dict.items()):
        if recursive:
            result += _get_bounds(v)
        elif type(v) is not ChoiceList:
            continue
        else:
            result.append(len(v))
    return result


def _get_next_hp_recursive(values, rep_dict, start_idx):
    idx = 0
    for (recursive, k), v in sorted(rep_dict.items()):
        if recursive:
            rep_dict[(True, k)], jump = _get_next_hp_recursive(values, v, start_idx + idx)
            idx += jump
        elif type(v) is not ChoiceList:
            continue
        else:
            rep_dict[(False, k)] = v[values[start_idx + idx]]
            idx += 1
    return rep_dict, idx


def _get_next_hp(values, rep_dict):
    result = copy.deepcopy(rep_dict)
    _get_next_hp_recursive(values, result, 0)
    return result


def _next_values(values, bounds):
    n = len(values)
    values[0] += 1

    idx = 0
    while values[idx] == bounds[idx]:
        values[idx] = 0
        idx = (idx + 1) % n
        values[idx] += 1

    return values


def get_possible_hyper_parameters(hp):
    result = list()
    rep_dict = hp.representation()
    bounds = _get_bounds(rep_dict)
    n_parameters = len(bounds)
    values = [0] * n_parameters

    for _ in range(prod(bounds)):
        result.append(HyperParameters(inp_rep=_get_next_hp(values, rep_dict)))
        _next_values(values, bounds)

    return result
