import numpy as np

'''
Возможные функции принадлежности для нечетких моделей.
Выбраны в соответствием заданием курсового проекта
'''
def mu1(x: float) -> float:
    if x<-0.75:
        return 1
    if x<-0.25:
        return -0.5-2*x
    return 0

def mu2(x: float) -> float:
    if x<-0.75:
        return 0
    if x<-0.25:
        return 1.5+2*x
    if x<0.25:
        return 1
    if x<0.75:
        return 1.5-2*x
    return 0

def mu3(x: float) -> float:
    if x<0.25:
        return 0
    if x<0.75:
        return 2*x-0.5
    return 1

'''
Методы генерации векторов f в соответствии с моделью, определенной
на нечетком множестве
'''
def flin(x):
    return np.array([1, x])
    
def fquad(x):
    return np.array([1, x, x**2])

'''
Класс содержит соответствия между нечеткими множествами и определенными в них
функциями принадлежности.
Позволяет строить общий вектор f.
'''
class fmaker:	
	# Доступные для использования модели
    models_avlb = {'lin': flin,'quad':fquad}
	
	# Функции для вычиления вектора f
	# и используемые для этого функции принадлежности
    models_used = [{'type':'quad', 'mu':mu1},
				{'type':'quad', 'mu':mu2},
				{'type':'quad', 'mu':mu3}]
    def __init__(self):
        return
    
    def get_avlb_models(self):
        return self.models_avlb.keys()

    def get_m(self):
        return len(self.make(1))
    
    def change_model(self,index: int, type_: str, muf = None):
        self.models_used[index]['type'] = type_
        if muf!= None:
            self.models_used[index]['mu'] = muf
    
    def make(self,x: float) -> float:
        fs = []
        for fparam in self.models_used:
            fs.append(fparam['mu'](x) * self.models_avlb[fparam['type']](x))
        fs = np.concatenate(fs)
        return fs[np.newaxis].T
    
if __name__ == '__main__':
    fm = fmaker()
    fm.change_model(0,'lin')
    fm.change_model(1,'lin')
    fm.change_model(2,'lin')
    a = fm.make(0.5)
    print(a, fm.get_m())