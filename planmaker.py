import numpy as np
import scipy as sp
import scipy.linalg as lng
import scipy.optimize as opt
import sys
import multiprocessing as mp
from scipy.spatial import distance
import pickle
from core import fmaker
# Поиск информационной матрицы для известного плана
def Meps():
    global plan
    global f
    global m
    M=np.zeros((m,m))
    for i in range(len(plan[0])):
        fu=f.make(plan[0][i])
        M+=plan[1][i]*fu*fu.T
    return M

# phi(x,eps) = f.T * d(psi)d(M) * f = [ в случае psi == ln|M| (D-оптимальный план)]=
# = tr(M.inv(eps) * M(x))
# M.inv - это матрица M в -1 степени
def phi (x):
    global plan
    global f
    global Mep
    fux=f.make(x)
    Mx=fux*fux.T
    return -np.trace(np.dot(lng.inv(Mep),Mx))

# Создание нового в соответствии с алгоритмом
def make_new_plan(alpha,x):
    global plan
    for i in range(len(plan[0])):
        plan[1][i]=(1-alpha)*plan[1][i]
    plan[0].append(x)
    plan[1].append(alpha)    

# Жутко неэффективно, зато не запарно
# Просто отменяет действие функции make_new_plan
def return_old_plan(alpha):
    global plan
    for i in range(len(plan[0])):
        plan[1][i]=plan[1][i]/(1-alpha)
    plan[0].pop()
    plan[1].pop()

# Процедура очистки 
# необходима для того, что окончательный спектр не содержал
# огромного числа близко расположенных точек.
# Точки объеденяются по группам в зависимости от близости
# к точкам изначального спектра
def clear(plan: list, threshold: int = 1e-2) -> list:
    clear_plan = [[],[]]
    # ДАЖЕ НЕ ПЫТАЙТЕСЬ ПОНЯТЬ ОЧИСТКУ
    free_p = 0
    while len(plan[0])>0:
        que = [plan[0][0]]
        amount = 1
        middle_point = plan[0][0]
        sump = plan[1][0]
        del plan[1][0]
        del plan[0][0]
        while len(que)>0:
            j = 0
            while j < len(plan[0]):
                dist = distance.euclidean(que[0],plan[0][j])
                if dist < threshold:
                    que.append(plan[0][j])
                    middle_point += plan[0][j]
                    sump += plan[1][j]
                    del plan[1][j]
                    del plan[0][j]
                    amount += 1
                    j -= 1
                j += 1        
            del que[0]
        if amount > 1:
            clear_plan[0].append(middle_point / amount)
            clear_plan[1].append(sump)
        else:
            free_p+=sump
            
    # Перераспределение весов свободных точек
    len_cp = len(clear_plan[0])
    free_p /= len_cp
    for i in range(len_cp):
        clear_plan[1][i]+=free_p
    return clear_plan   
plan=[]
m = 0
Mep = 0
f = 0
'''
fmake - объект класса fmaker (подробнее в определение класса)

button - кнопка, на которой планируется выводить число итераций алгоритма

iters_to_update - количество итераций алгоритма, которые должны пройти,
чтобы на интерфейсе обновился счетчик

threshold - расстояние между точками, которого достаточно, чтобы сказать,
что точки можно считать одной точкой
'''
def make_plan(fmake: fmaker, button, precision: float = 1e-4,
              maxiter: int = 1000, iters_to_update: int = 10,
              threshold:float = 5e-2) -> list:
    global f
    global plan
    global m
    global Mep
    
    f = fmake
    m = f.get_m( )
    start_points = list(np.linspace(-1,1, m))
    startn = len(start_points)
    # Создание изначального спектра
    # В plan[0] хранятся точки плана
    # В plan[1] хранятся веса точек плана
    plan = []
    plan.append([])
    plan[0] = start_points.copy()
    # Задание весов плана
    plan.append([])
    for i in range(startn):
        plan[1].append(1.0/startn)
        
        
    # ПОдготовка к циклу
    Mep=Meps()
    psiold=np.log(lng.det(Mep))
    gamma=2
    iter_=1  
    while True:
        #2 Поиск глобального максимума
        res = opt.differential_evolution(phi,bounds=[(-1,1)])
        point = res.x
        val = -res.fun
        #3 Проверка необходимых и достаточных условий выхода из алгоритма
        if abs(-val+m)<precision or iter_>maxiter:
            break    
        # Инициализация alpha в соответствии с советами в методичке
        alpha=2.0/(len(plan[0]))  
        while True:
            #4 Создание нового плана
            make_new_plan(alpha, point[0])
            #5 Проверка допустимости плана
            Mep=Meps()
            psinew=np.log(lng.det(Mep))
            # В отличии от оригинального алгоритма добавлена проверка значимости alpha
            # Для избежания ситуаций зацикливания
            if psinew<=psiold and alpha>1e-10:
                return_old_plan(alpha)
                alpha=alpha/gamma
            else:
                break
        
        if iter_ % iters_to_update == 0:  
            button.setText('Iteration: '+str(iter_))
            
        if iter_ % (m*40) == 0: 
            plan = clear(plan,threshold = threshold)
            
        iter_=iter_+1
        psiold=psinew  
    button.setText('Clearing...')
     
    plan = clear(plan,threshold = threshold)
    plan.append(lng.det(Meps()))
    return plan

#make_plan(iters_to_update = 10)