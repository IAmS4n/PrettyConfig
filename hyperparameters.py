import inspect
import json


class HyperParameters:
    def __init__(self, path=None, inp_rep=None):

        if path is not None:
            assert inp_rep is None, "use one type of import"
            with open(path) as json_file:
                data = json.load(json_file)
            init_state = HyperParameters._dict2rep(data)
        elif inp_rep is not None:
            assert path is None, "use one type of import"
            init_state = inp_rep
        else:
            assert type(self) != HyperParameters, "You need inheritance from this class and define static attribute!"
            init_state = self.class_representation()

        self._load(init_state)
        self.__short_name_dict = {}
        self.__filename_categories = {}

    @staticmethod
    def filter_dict(inp_dict):
        # attribute by "__" prefix is not considered!
        res = {}
        for name, val in inp_dict.items():
            if inspect.isfunction(val) or inspect.ismethod(val):
                pass
            elif inspect.isclass(val):
                if issubclass(val, HyperParameters):
                    res[(True, name)] = val
                else:
                    raise NotImplementedError
            elif issubclass(type(val), HyperParameters):
                res[(True, name)] = val
            elif not name.startswith("_"):
                res[(False, name)] = val
        return res

    @classmethod
    def class_representation(cls):
        res = {}
        for details, val in HyperParameters.filter_dict(cls.__dict__).items():
            recursive, name = details
            res[details] = val.class_representation() if recursive else val
        return res

    def representation(self):
        rep = {}
        for details, val in HyperParameters.filter_dict(self.__dict__).items():
            recursive, name = details
            rep[details] = val.representation() if recursive else val
        return rep

    @staticmethod
    def rep2set(inp_rep):  # this function is for hash
        res = set()
        for details, val in inp_rep.items():
            recursive, name = details
            if recursive:
                res |= HyperParameters.rep2set(val)
            else:
                newval = val
                if type(val) is dict:
                    newval = frozenset(val.items())
                if type(val) is list:
                    newval = frozenset(enumerate(val))
                res.add((name, newval))
        return frozenset(res)

    def __hash__(self):
        return hash(HyperParameters.rep2set(self.representation()))

    def set_filename_shortnames(self, inp_dict):
        self.__short_name_dict = inp_dict

    def set_filename_category(self, name, name_set):
        self.__filename_categories[name] = frozenset(name_set)

    def get_filename_categories(self):
        return list(self.__filename_categories)

    def _file_name(self, rep, category=None):
        category_filter = lambda x: category is None or x[0][0] or x[0][1] in self.__filename_categories[category]
        res = []
        res_recursive = []
        for details, val in filter(category_filter, sorted(rep.items())):
            recursive, name = details

            if recursive:
                tmp = self._file_name(val, category)
                if len(tmp) > 0:
                    res_recursive.append("%s(%s)" % (name, "-".join(tmp)))
            else:
                if name in self.__short_name_dict:
                    name = self.__short_name_dict[name]
                res.append("%s%s" % (name, str(val)))
        return res + res_recursive

    def file_name(self, category=None):
        rep = self.representation()
        path = "-".join(self._file_name(rep, category))
        path = path.replace(".", "dot")
        path = path.replace(" ", "")
        path = path.replace("[", "(")
        path = path.replace("]", ")")
        path = path.replace(",", "-")
        return path

    @staticmethod
    def _rep2lines(inp_rep):
        fields = []
        sub_fields = []
        for details, val in inp_rep.items():
            recursive, name = details
            if recursive:
                tmp_lines = [name]
                tmp_lines.extend(HyperParameters._rep2lines(val))

                sub_fields.append(tmp_lines)
            else:
                fields.append(["> %s:%s" % (name, val)])
        all_fields = fields + sub_fields

        fields = None
        sub_fields = None

        res_lines = []

        for i, field in enumerate(all_fields):
            field = all_fields[i]
            if i < len(all_fields) - 1:
                pointer_char = "├"
                addtab = lambda x: "│  %s" % x
            else:
                pointer_char = "└"
                addtab = lambda x: "   %s" % x
            res_lines.append("%s──%s" % (pointer_char, field[0]))
            res_lines.extend(map(addtab, field[1:]))
        return res_lines

    def __str__(self):
        return "\n".join(HyperParameters._rep2lines(self.representation()))

    def save(self, path):
        with open(path, 'w') as outfile:
            data = HyperParameters._rep2dict(self.representation())
            json.dump(data, outfile)

    @staticmethod
    def _rep2dict(inp_rep):
        # rep type is for supporting dict in attribute
        res = {}
        for details, val in inp_rep.items():
            recursive, name = details
            details_str = "T" if recursive else "F"
            details_str += "_" + name
            res[details_str] = HyperParameters._rep2dict(val) if recursive else val
        return res

    @staticmethod
    def _dict2rep(inp_dict):
        res = {}
        for details_str, val in inp_dict.items():
            recursive = details_str[0] == "T"
            name = details_str[2:]
            res[(recursive, name)] = HyperParameters._dict2rep(val) if recursive else val
        return res

    def _load(self, inp_rep):
        for details, val in inp_rep.items():
            recursive, name = details
            set_val = HyperParameters(inp_rep=val) if recursive else val
            setattr(self, name, set_val)


if __name__ == "__main__":
    class ModelHyperParameters(HyperParameters):
        test1 = 5
        test2 = 6
        test_list = [1, 2, 3, 4]
        test_dict = {"first": 111, "second": 222}

        class subparam1(HyperParameters):
            a = 10
            b = 20

            class subsubparam(HyperParameters):
                g1 = 100
                g2 = 200

        class subparam2(HyperParameters):
            a = 1000
            b = "name"
            c = [1, 2, 3, 4]

            class subsubparam(HyperParameters):
                g1 = 1e-2
                g2 = 1e-3


    ######################################################
    print("=" * 10 + "default values" + "=" * 10)
    myparam = ModelHyperParameters()
    myparam.set_filename_shortnames({"a": "AX", "g1": "g1X"})
    myparam.set_filename_category("save", {"g1", "g2", "a", "b", "c"})
    myparam.set_filename_category("log", {"a", "b", "c"})
    print(myparam.file_name())
    print(myparam.file_name("save"))
    print(myparam.file_name("log"))
    print(myparam)
    ######################################################
    print("=" * 10 + "change some values" + "=" * 10)
    myparam.test1 = 66666
    myparam.subparam1.a = 66666
    print(myparam)
    ######################################################
    print("=" * 10 + "load values" + "=" * 10)
    myparam.save("/tmp/test")
    myparam.test1 = -1
    myparam.subparam1.a = -1
    myparam.subparam2.subsubparam.g1 = -1
    myparam.subparam2.subsubparam.g2 = -1
    myparam = None
    newmyparam = ModelHyperParameters("/tmp/test")
    print(newmyparam)
    ######################################################
    print("=" * 10 + "add values" + "=" * 10)
    newmyparam.newval1 = 321
    newmyparam.subparam2.newvalue2 = 123
    print(newmyparam)
    ######################################################
    print("=" * 10 + "checking hash" + "=" * 10)
    myparam = ModelHyperParameters()
    tmp = hash(myparam)
    myparam.test1 = 123456
    myparam.subparam2.c = [1]
    myparam.subparam2.b = "newname"
    assert hash(myparam) != tmp
    myparam.test1 = 5
    myparam.subparam2.b = "name"
    myparam.subparam2.c = [1, 2, 3, 4]
    assert hash(myparam) == tmp
