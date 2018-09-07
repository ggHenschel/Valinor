from PyQt5.QtCore import qDebug
import csv
from models.case_model import CaseModel
from sklearn import tree, model_selection, metrics, preprocessing
import numpy as np


def tree_to_code(clf, feature_names, class_names):
    tree_ = clf.tree_
    string = ""
    feature_name = [
        feature_names[i] if i != tree._tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    string+="def tree({}):\n".format(", ".join(feature_names))

    def recurse(node, depth):
        indent = "  " * depth
        stri = ""
        if tree_.feature[node] != tree._tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            stri +="{}if {} <= {}:\n".format(indent, name, threshold)
            stri +=recurse(tree_.children_left[node], depth + 1)
            stri +="{}else:  # if {} > {}\n".format(indent, name, threshold)
            stri +=recurse(tree_.children_right[node], depth + 1)
        else:
            stri +="{}return {}\n".format(indent, class_names[np.argmax(tree_.value[node][0])])
        return stri

    string+=recurse(0, 1)

    return string

class CaseAttributeModel(CaseModel):
    def details(self):
        name = self.name
        n_cases = len(self.cases)
        n_atributes = len(self.legend)
        return (name, n_cases, n_atributes)

    def create_from_file(self,origin_path,has_legend=False,delimiter=";"):
        self.name = str(origin_path).split("/")[-1]
        file = open(origin_path)
        read = csv.reader(file, delimiter=delimiter)
        rows = []

        for row in read:
            rows.append(row)

        if has_legend:
            self.legend=rows[0]
            n=1
        else:
            n=0

        for row in rows[n:]:
            case = str(row[0])
            others = row[1:]
            self.attribute_size = len(others)
            self.cases[case] = [others]

    def add_legend(self,legend):
        self.legend = legend

    def merge(self,newModel,list_of_itens):
        ilegend = newModel.legend
        for i in list_of_itens:
            self.legend.append(ilegend[i+1])

        for case, attr in self.cases.items():
            iitems = newModel.cases[case]
            for i in list_of_itens:
                attr[0].append(iitems[i])

    def export(self,file_path,progress_dialog=None,keep_legend_bool=True,delimiter=";"):
        with open(file_path,mode='w') as file:
            writer = csv.writer(file,delimiter=delimiter)
            if keep_legend_bool:
                writer.writerow(self.legend)

            progress_dialog.setMaximum(len(self.cases))
            n = 0
            progress_dialog.setValue(n)
            for case, attributes in self.cases.items():
                l = [case]
                for attribute in attributes[0]:
                    l.append(attribute)
                writer.writerow(l)
                n+=1



    def generate_tree(self,attribute_types,params):
        index_of_class = params["class_index"]
        case_is_attribute = params["id_is_class"]
        perct_of_test = params["perct_of_test"]
        list_of_ignored_attributes = params["ignored_attributes"]


        #Start Slicing
        data = []
        target = []
        list_of_strings = []
        feature_names = []
        class_name = []
        if case_is_attribute:
            feature_names.append("Case")


        for case, attr in self.cases.items():
            attributes = []
            if case_is_attribute:
                attributes.append(str(case))
            for i in range(0, len(attr[0])):
                #Type Conversion
                if not i in list_of_ignored_attributes:
                    if attribute_types[i]== 0 and i != index_of_class:
                        value = bool(attr[0][i])
                    elif (attribute_types[i]== 1 or attribute_types[i]== 2)  and i != index_of_class:
                        value = attr[0][i]
                    else:
                        if i == index_of_class:
                            if str(attr[0][i]) in list_of_strings:
                                value = list_of_strings.index(str(attr[0][i]))
                            else:
                                list_of_strings.append(attr[0][i])
                                value = list_of_strings.index(str(attr[0][i]))
                        else:
                            #AVISAR ABORT
                            list_of_ignored_attributes.append(i)
                            return ;

                    if i != index_of_class:
                        attributes.append(value)
                    else:
                        target.append(value)
            data.append(attributes)

        #legend
        for item in range(1,len(self.legend)):
            if item-1!=index_of_class and not item-1 in list_of_ignored_attributes:
                feature_names.append(self.legend[item])
            elif not item-1 in list_of_ignored_attributes:
                class_name.append(self.legend[item])

        #training data e test data
        X_train, X_test, y_train, y_test = model_selection.train_test_split(data,target, test_size = perct_of_test, random_state=100)

        clf = tree.DecisionTreeClassifier(criterion = params["criterion"],splitter=params["splitter"],max_depth=params["max_depth"],
                                          min_samples_split=params["min_sample_split"],min_samples_leaf=params["min_sample_leafs"],
                                          min_weight_fraction_leaf = params["min_weight_fraction_leaf"],max_features=params["max_features"],
                                          random_state = params["random_state"],max_leaf_nodes=params["max_leaf_nodes"],
                                          min_impurity_split=params["min_impurity_split"])

        clf.fit(X_train,y_train)

        code = tree_to_code(clf,feature_names,list_of_strings)
        

