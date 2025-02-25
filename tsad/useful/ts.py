# косяк, мой подсчет метрик не работает если там нет трушных 1
"""
CDSDSDS
"""

from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def ts_train_test_split(df, len_seq, 
                     points_ahead=1, gap=0, shag=1, intersection=True,
                     test_size=None,train_size=None, random_state=None, shuffle=True, shuffle_target='only_train'):
    """
    Функция которая разбивает временной ряд на трейн и тест выборки 
    
    Временной ряд здесь это вообще вся история
    Функционал позволяет разбивать ....

    Parameters
    ----------
    df : pd.DataFrame
        Array of shape (n_samples, n_features) with timestamp index.
    
    points_ahead : int, default=0
        Сколько точек вперед прогнозируем, отражается в y
         
    gap :  int, default=0
        Сколько точек между трейном и тестом. Условно говоря,
        если крайняя точка train а это t, то первая точка теста t + gap +1.
        Параметр создан, чтобы можно было прогнозировать одну точку через большой 
        дополнительный интервал времени. 
    
    shag :  int, default=1.
        Шаг генерации выборки. Если первая точка была t у 1-ого сэмпла трейна,
        то у 2-ого сэмла трейна она будет t + shag, если intersection=True, иначе 
        тоже самое но без пересечений значений ряда. 

    intersection :  bool, default=True
        Наличие значений ряда (одного момента времени) в различных сэмплах выборки. 
    
    test_size : float or int or timestamp for df, or list of timestamps, default=0.25. 
        Может быть 0, тогда вернет значения X,y
        If float, should be between 0.0 and 1.0 and represent the proportion
        of the dataset to include in the test split. 
        If int, represents the
        absolute number of test samples. If None, the value is set to the
        complement of the train size. If ``train_size`` is also None, it will
        be set to 0.25. *
        *https://github.com/scikit-learn/scikit-learn/blob/95119c13a/sklearn/model_selection/_split.py#L2076 
        If timestamp for df, for X_test we will use set from df[t:] **
        If list of timestamps [t1,t2], for X_test we will use set from df[t1:t2] **
        !!! Важно, если timestamp мы всегда захватываем и слева и српава.
        
    
    train_size : float or int, default=None
        If float, should be between 0.0 and 1.0 and represent the
        proportion of the dataset to include in the train split. If
        int, represents the absolute number of train samples. If None,
        the value is automatically set to the complement of the test size. *
        *https://github.com/scikit-learn/scikit-learn/blob/95119c13a/sklearn/model_selection/_split.py#L2076
        If timestamp for df, for X_train we will use set for train from df[:t] **
        If list of timestamps [t1,t2], for X_train we will use set for train from df[t1:t2] **
    
    random_state : int, RandomState instance or None, default=None
        Controls the shuffling applied to the data before applying the split.
        Pass an int for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.*
        *https://github.com/scikit-learn/scikit-learn/blob/95119c13a/sklearn/model_selection/_split.py#L2076
        
    
    shuffle : bool, default=True
        Whether or not to shuffle the data before splitting. If shuffle=False
        then stratify must be None. *
        
    shuffle_target: {'only_train', 'all'}, str. Default = only_train. 
        In the case of 'only_train' we random shuffle only X_train, and y_train. 
            Test samples are unused for the shuffle. Any sample from X_test is later 
            than any sample from X_train. This is also true for respectively
        In case of 'all' in analogy with sklearn.model_selection.train_test_split

    Returns
    -------
    (X_train, X_test, y_train, y_test) : tuple 
        Tuple containing train-test split of inputs
    
    TODO
    --------
    t-test of timestamp
    ** todo реализовать
    ошибка прогнозирует через одну.
    туда же через точки пробывать модели. 
    
    Examples
    --------
    >>> X = np.ones((4, 3))
    >>> y = np.ones(4)
    >>> sklearn_template(X, y)
    (z, xmin, xmax)  # this should match the actual output
    """

#    """
#	df - требование, но если тебе не хочется то просто сделай np.array на выходе и все
#    Разбить временные ряды на трейн и тест
#    len_seq- количество времменых точек в трейн
#    points_ahead - количество времменых точек в прогнозе
#    gap - расстояние между концом трейна и началом теста
#    intersection - если нет, то в выборке нет перескающих множеств (временнызх моментов)
#    shag - через сколько прыгаем
#    train_size - float от 0 до 1
#    
#    return list of dfs
#    
#    """
    #TODO требования к входным данным прописать
    #TODO переписать энергоэффективно чтобы было
    #TODO пока временные характеристики int_ами пора бы в pd.TimdDelta
    # нет индексов 
    assert len_seq + points_ahead + gap + 1 <= len(df)
    how='seq to seq'   

# -------------------------------------------------------  
#             
# -------------------------------------------------------     


    x_start=0
    x_end= x_start + len_seq
    y_start = x_end + gap +1
    y_end = y_start + points_ahead
    
    if intersection:
        # ради вычислительной нагрузки такой кастыль
        def compute_new_x_start(x_start,y_end,shag):
            return x_start + shag
    else:
        def compute_new_x_start(x_start,y_end,shag):
            return y_end + shag -1
    
    X = []
    y = []
    while y_end <= len(df):
        X.append(df[x_start:x_end])
        y.append(df[y_start:y_end])
        
        x_start= compute_new_x_start(x_start,y_end,shag)
        x_end= x_start + len_seq
        y_start = x_end + gap +1
        y_end = y_start + points_ahead
          
    
    if (test_size==0) | (len(X)==1):
        indices = np.array(range(len(X)))
        np.random.seed(random_state)
        if shuffle:
            print(indices)
            np.random.shuffle(indices)
            print(indices)
        X = [X[i] for i in indices]
        y = [y[i] for i in indices]
        return X,[],y,[]
    else:
        return train_test_split(X,y, 
                                test_size=test_size, 
                                train_size=train_size, 
                                random_state=random_state, 
                                shuffle=shuffle, 
                               )
        
def split_by_repeated(series,df=None):
    """
    retrun dict with lists of ts whwre keys is unique values
    ts[ts.diff()!=0]  побыстрее будет
    """
    series = series.copy().dropna()
    if len(series.unique())==1:
        result = {series.unique()[0]:series}
    elif len(series.unique())>1:
        result = {uni:[] for uni in series.unique()}
        recent_i=0
        recent_val=series.values[0]
        for i in range(len(series)):
            val = series.values[i]
            if (recent_val == val):
                continue
            else:
                result[recent_val].append(series[recent_i:i])
                recent_i=i
                recent_val = val

        if i == len(series)-1:
            if (recent_val == val):
                result[recent_val].append(series[recent_i:i+1])
            else:
                result[recent_val].append(series[recent_i:i+1])
    else:
        raise NameError('0 series')


    if df is not None:
        new_result = {uni:[] for uni in series.unique()}
        for key in result:
            for i in range(len(result[key])):
                if len(result[key][i]) <=1:
                    continue
                else:
                    new_result[key].append(df.loc[result[key][i].index])
        return new_result
    else:
        return result
        
        
def df2dfs(df,  # Авторы не рекомендуют так делать,
            resample_freq = None, # требования
            thereshold_gap = None, 
            koef_freq_of_gap = 1.2, # 1.2 проблема которая возникает которую 02.09.2021 я написал в ИИ 
            plot = False,
            col = None):
    """
    Функция которая преообратает raw df до требований к входу на DL_AD    
    то есть разбивает df на лист of dfs by gaps 
    
    Не ресемлирует так как это тяжелая задача, но если частота реже чем 
    koef_freq_of_gap of thereshold_gap то это воспринимается как пропуск. 
    Основной посыл: если сигнал приходит чаще, то он не уползает сильно, 
    а значит не приводит к аномалии, а если редко то приводит, поэтому воспри-
    нимается как пропуск. 
    
    plot - очень долго
    
    Parameters
    ----------   
    df : pd.DataFrame
        Исходный временной ряд полностью за всю историю   
        
    resample_freq: pd.TimeDelta (optional, default=None)
        Частота дискретизации временного ряда. 
        Если default то самая частая частота дискретизации. При этом, 
        если нет выраженной частоты вылетит ошибка. 
    thereshold_gap : pd.TimeDelta (optional, default=None)
        Порог периода, превышая который функция будет воспринимать
        данный период как пропуск. 
    koef_freq_of_gap : float or int (optional if thereshold_gap==None,
        default=1.2)  
        thereshold_gap = koef_freq_of_gap * resample_freq
    plot : bool (optional, default=True)
        If true, then отрисуется нарезка
        If false, then не отрисуется нарезка   
    col : int of str (optional, default=True)
        Название или номер колонки для отрисовки
        Если None первая колонка
    Returns
    -------
    dfs : list of pd.DataFrame
        Список времменных рядов без пропусков с относительно стабильной 
        частотой дискретизации. 
    """

    df = df.dropna(how='all').dropna(1,how='all')
    dts  = df.dropna(how='all').index.to_series().diff()
    if resample_freq is None:
        dts_dist = dts.value_counts()
        if dts_dist[0] > dts_dist[1:].sum():
            resample_freq  = dts_dist.index[0]
        else: 
            print(dts_dist)
            raise Exception("Необходимо самостоятельно обработать функцию так как нет преобладающей частоты дискретизации")
    thereshold_gap = resample_freq*koef_freq_of_gap if thereshold_gap is None else thereshold_gap
    gaps = (dts > thereshold_gap).astype(int).cumsum()
    dfs = [df.loc[gaps[gaps==stage].index] for stage in gaps.unique()]
    
    if plot:
        f, ax = plt.subplots()
        if col is None:
            col = df.columns[0]
        else:
            if type(col)==type(int):
                col = df.columns[col]
        for df in dfs:
            df[col].plot(ax=ax)
    return dfs

    