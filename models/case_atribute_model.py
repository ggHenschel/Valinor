from PyQt5.QtCore import qDebug
import csv
from models.case_model import CaseModel
from sklearn import tree, model_selection, metrics, preprocessing, cluster
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

def tree_to_j48(clf, feature_names, class_names):
    tree_ = clf.tree_
    string = ""
    feature_name = [
        feature_names[i] if i != tree._tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    string+="Output ({}):\n".format(", ".join(feature_names))

    def recurse(node, depth):
        indent = "|    " * depth
        stri = ""
        if tree_.feature[node] != tree._tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            stri +="\n{} {} <= {}".format(indent, name, threshold)
            stri +=recurse(tree_.children_left[node], depth + 1)
            stri +="\n{} {} > {}".format(indent, name, threshold)
            stri +=recurse(tree_.children_right[node], depth + 1)
        else:
            stri +=" : {} ({})".format(class_names[np.argmax(tree_.value[node][0])],tree_.weighted_n_node_samples[node])
        return stri

    string+=recurse(0, 0)

    return string

class CaseAttributeModel(CaseModel):

    def __init__(self,name='A Case has no name'):
        super().__init__(name)
        self.clf = None
        self.cluster = None

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
        for i in list_of_itens[1:]:
            self.legend.extend(ilegend[i])

        for case, attr in self.cases.items():
            iitems = newModel.cases[case]
            for i in list_of_itens[1:]:
                attr[0].append(iitems[i-1])

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



    def generate_tree(self,params):
        index_of_class = params["class_index"]
        perct_of_test = params["perct_of_test"]
        list_of_ignored_attributes = params["ignored_attributes"]

        attribute_types = self.define_attribute_type_list()
        #Start Slicing
        data = []
        target = []
        list_of_strings = []
        feature_names = []
        class_name = []


        for case, attr in self.cases.items():
            attributes = []
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
                                list_of_strings.append(str(attr[0][i]))
                                value = list_of_strings.index(str(attr[0][i]))
                        else:
                            list_of_ignored_attributes.append(i)
                            continue

                    if i != index_of_class:
                        attributes.append(value)
                    else:
                        target.append(value)
            if len(attributes)+len(list_of_ignored_attributes)+2!=len(self.legend):
                print("Failed")
            data.append(attributes)

        #legend
        for item in range(1,len(self.legend)):
            if item-1!=index_of_class and not item-1 in list_of_ignored_attributes:
                feature_names.append(self.legend[item])
            elif not item-1 in list_of_ignored_attributes:
                class_name.append(self.legend[item])

        #training data e test data
        X_train, X_test, y_train, y_test = model_selection.train_test_split(data,target, test_size = perct_of_test, random_state=100)

        self.clf = tree.DecisionTreeClassifier(criterion = params["criterion"],
                                               splitter=params["splitter"],
                                               max_depth=params["max_depth"],
                                               min_samples_split=params["min_sample_split"],
                                               min_samples_leaf=params["min_sample_leafs"],
                                               min_weight_fraction_leaf = params["min_weight_fraction_leaf"],
                                               max_features=params["max_features"],
                                               random_state = params["random_state"],
                                               max_leaf_nodes=params["max_leaf_nodes"],
                                               min_impurity_split=params["min_impurity_split"])

        self.clf.fit(X_train,y_train)

        if params["code_type"]=="python":
            code = tree_to_code(self.clf,feature_names,list_of_strings)
        else:
            code = tree_to_j48(self.clf, feature_names, list_of_strings)

        dot_data = tree.export_graphviz(self.clf,out_file=None,feature_names=feature_names,class_names=list_of_strings,filled=True,rounded=True,special_characters=True)

        y_pred = self.clf.predict(X_test)

        accuracy = metrics.accuracy_score(y_test,y_pred)

        return (code, accuracy, dot_data, list_of_ignored_attributes)

    def clustering_algorithm(self,params):
        data = []
        attribute_types = self.define_attribute_type_list()
        list_of_ignored_attributes = params["ignored_attributes"]
        for case, attr in self.cases.items():
            attributes = []
            for i in range(0, len(attr[0])):
                if not i in list_of_ignored_attributes:
                    if attribute_types[i]== 0:
                        value = bool(attr[0][i])
                    elif (attribute_types[i]== 1 or attribute_types[i]== 2):
                        value = attr[0][i]
                    else:
                        list_of_ignored_attributes.append(i)
                        continue

                    attributes.append(value)

            data.append(attributes)


        k_clusters = params["number_of_clusters"]
        init = params["mode"]
        n_init=params["n_init"]
        max_iter=params["max_iter"]
        tolerance=params["tolerance"]
        if params["random_state"]:
            rnd = np.random.random_integers(0,99999)
        else:
            rnd = None
        algorithm = params["algorithm"]

        self.clusters = cluster.KMeans(init=init,n_clusters=k_clusters,n_init=n_init,max_iter=max_iter,tol=tolerance,random_state=rnd,algorithm=algorithm)

        self.clusters.fit(data)

        centers = self.clusters.cluster_centers_

        return_cluster = []
        for key, item in self.cases.items():
            datan = item[0].copy()
            dataf = []
            for i in list_of_ignored_attributes[::-1]:
                datan.pop(i)
            for value in datan:
                try:
                    dataf.append(float(value))
                except:
                    dataf.append(bool(value))
            dataf = np.array(dataf)
            return_cluster.append((key,self.clusters.predict([dataf])))

        return (centers,return_cluster)

    def define_attribute_type_list(self):
        fline = next(iter(self.cases.values()))
        list = []
        type = "string"
        for item in fline[0]:
            try:
                float(item)
                list.append(1)
            except:
                if item!='True' and item!='False' and item!='true' and item!='false':
                    list.append(3)
                else:
                    try:
                        bool(item)
                        list.append(0)
                    except ValueError:
                        list.append(3)

        return list
