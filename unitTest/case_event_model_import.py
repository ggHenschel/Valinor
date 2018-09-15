from models.case_atribute_model import CaseAttributeModel


c = CaseAttributeModel()

#c.create_from_file("../Data/AttrLog.csv",";")
c.create_from_file("../Data/my_atributes.csv",";")

params = {
            "mode":"k-means++", #"random"
            "number_of_clusters":4,
            "n_init":10,
            "max_iter":300,
            "tolerance":float(1e-4),
            "random_state":True,
            "algorithm":"auto", #full, elkan,
            "ignored_attributes": []
        }

(code, ret) = c.clustering_algorithm(params)

print(code)
for item in ret[:100:]:
    print("Case:"+item[0]+"\t Att:"+str(c.cases[item[0]])+"\t defined as"+str(item[1]))
