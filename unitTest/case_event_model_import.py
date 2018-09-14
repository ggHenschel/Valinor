from models.case_atribute_model import CaseAttributeModel


c = CaseAttributeModel()

c.create_from_file("../Data/AttrLog.csv",";")

#print(c.details())

params = {"class_index": 169,
          "id_is_class": False,
          "perct_of_test": 0.3,
          "criterion":"gini",
          "splitter": "best",
          "max_features": None,
          "max_depth": 10,
          "min_sample_split": 2,
          "min_sample_leafs": 1,
          "min_weight_fraction_leaf": 0.0,
          "random_state": None,
          "max_leaf_nodes": None,
          "min_impurity_split": None,
          "ignored_attributes": [167,168]
          }
attribute_types = [1 for i in range(0,len(c.legend)-1)]
attribute_types.append(3)
print(c.define_attribute_type_list())
#(code, acc, dot) = c.generate_tree(attribute_types,params)

#print(code, acc, dot)
