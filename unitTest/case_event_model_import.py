from models.case_atribute_model import CaseAttributeModel

c = CaseAttributeModel()

c.create_from_file("../Data/my_atributes.csv",";")

print(c.details())