import os
try:
    from hyperopt import hp,Trials,fmin,tpe,STATUS_OK
    from sklearn.model_selection import train_test_split
    from sklearn import metrics
    import joblib
    import xgboost
    from sklearn import svm
    from sklearn.ensemble import BaggingClassifier,BaggingRegressor
except ModuleNotFoundError:
    for x in ['scikit-learn','xgboost','hyperopt','joblib','pandas','numpy']:
        os.system('pip install '+ x)

class MlT:
    """Clase para hacerme la vida mas facil"""

    def __init__(self,features,target,size=2,rs=0):
        """Splitea chama y guarda variables generales para ser usadas por otras funciones"""
        self.model,self.params = '',''
        self.X_train,self.X_test,self.y_train,self.y_test = train_test_split(features,
                                                        target,
                                                        test_size=int(size)/10,
                                                        random_state= int(rs))
  
    def __str__(self):
        """Para printear los parametros con los que se entreno el modelo"""
        return str(self.params) if self.params else 'No parametros todavia monina'

    def salver(self,nombre):
        """Para salvar el modelo"""
        direccion = r'D:\Programacion\Proyectos\Modelos'
        joblib.dump(self.model,(direccion + os.sep + nombre +'.joblib'))

    def metricas(self,y_test,y_pred):
        """Funcion para printear las metricas el modelo fitteado"""
        if self.tipo=='c':
            print(f'\nAccuracy: {metrics.accuracy_score(y_test,y_pred)}\nPrecision: {metrics.precision_score(y_test,y_pred,average=self.avg)}\nRecall: {metrics.recall_score(y_test,y_pred,average=self.avg)}\nF1: {metrics.f1_score(y_test,y_pred,average=self.avg)}')
        else:
            print(f'\nMSE: {metrics.mean_squared_error(y_test,y_pred)}\nMAE: {metrics.mean_absolute_error(y_test,y_pred)}\nR2: {metrics.r2_score(y_test,y_pred)}')

    def objective(self,space):
        """Para tunniear el modelo dependiendo si es para regression o classificacion 
        que es llamado por el modelo escogido como parte de hyperopt"""
        #testeando
        exec(self.string)
        self.model.fit(self.X_train, self.y_train)
        pred = self.model.predict(self.X_test)
        self.puntuacion = ''
        if self.tipo == 'c' : 
            tiza = 1 
            exec('self.puntuacion = tiza*(metrics.' + self.scorer + '(self.y_test, pred,average=self.avg))')
        else: 
            tiza = -1
            exec('self.puntuacion = tiza*(metrics.' + self.scorer + '(self.y_test, pred))')
        return {'loss': -self.puntuacion, 'status': STATUS_OK }
    
    def hyper_opt(self,iter):
        """Funcion que llama a objective y va optimizando"""
        trials = Trials()
        best_hyperparams = fmin(fn = self.objective,
                        space = self.space,
                        algo = tpe.suggest,
                        max_evals = iter,
                        trials = trials)
        return best_hyperparams

    def std(self):
        """Para standarizar"""
        from sklearn.preprocessing import StandardScaler
        std = StandardScaler()
        self.X_train = std.fit_transform(self.X_train)
        self.X_test = std.transform(self.X_test)

    def bparams(self,tipo,scorer,avg):
        """Para definir parametros y en caso normal ya elige solo"""
        self.tipo = tipo
        if scorer : self.scorer = scorer
        elif tipo == 'c' : self.scorer = 'f1_score' 
        else : self.scorer = 'mean_absolute_error'
        
        if avg == 'w':
            self.avg = 'weighted'
        else : self.avg = avg

class XGBs(MlT):
    """Clase especializada en decision trees del modulo xgboost para tener algunas cosas generales"""
        
    def xgbs(self,tipo,scorer=None,iter=50,avg='binary'):
        """Si tipo c clasificacion else regression, crea el modelo lo entrena con hyperopt, guarda parametros y
        printea resultados, se decide solo el tipo de arbol a utilizar"""
        #estableciendo tipo de problema(clasificacion o regresion,escorer(con defaults) y tipo de average por si no es binary
        self.bparams(tipo,scorer,avg)
        
        self.space = {'n_estimators': hp.quniform('n_estimators',10,150,1),
                      'max_depth':hp.quniform('max_depth',1,20,1),
                      'learning_rate': hp.uniform('learning_rate',0.001,1),
                      'subsample': hp.uniform('subsample',0,1),
                      'reg_lambda': hp.quniform('reg_lambda',0,20,1),
                      'reg_alpha': hp.quniform('reg_alpha',0,20,1),
                      'seed': hp.quniform('seed',0,50,1)}
        if self.tipo == 'c':
            self.string = "self.model = xgboost.XGBClassifier(n_estimators=int(space['n_estimators']),max_depth=int(space['max_depth']),learning_rate=space['learning_rate'],subsample=space['subsample'],reg_alpha= int(space['reg_alpha']),reg_lambda=int(space['reg_lambda']),seed=int(space['seed']))"
        else:
            self.string = "self.model = xgboost.XGBRegressor(n_estimators=int(space['n_estimators']),max_depth=int(space['max_depth']),learning_rate=space['learning_rate'],subsample=space['subsample'],reg_alpha= int(space['reg_alpha']),reg_lambda=int(space['reg_lambda']),seed=int(space['seed']))"
        
        #hyperopt
        best_hyperparams = self.hyper_opt(iter)

        #Fittenado y printeando modelo con los mejores parametros
        if self.tipo == 'c':
            xgb = xgboost.XGBClassifier(n_estimators=int(best_hyperparams['n_estimators']),max_depth=int(best_hyperparams['max_depth']),learning_rate=best_hyperparams['learning_rate'],subsample=best_hyperparams['subsample'],seed=int(best_hyperparams['seed']))
        else:
            xgb = xgboost.XGBRegressor(n_estimators=int(best_hyperparams['n_estimators']),max_depth=int(best_hyperparams['max_depth']),learning_rate=best_hyperparams['learning_rate'],subsample=best_hyperparams['subsample'],seed=int(best_hyperparams['seed']))
        xgb.fit(self.X_train,self.y_train)
        y_pred = xgb.predict(self.X_test)
        self.metricas(self.y_test,y_pred)
        #guardando datos del modelo
        self.params = best_hyperparams
        self.model = xgb

class Svms(MlT):
    """Clase especializada en LinearSVM del modulo sklaear.svm para tener algunas cosas generales"""

    def __init__(self,features,target,size=2,rs=0):
        MlT.__init__(self,features,target,size=2,rs=0)
        self.std()
    
    def lsvms(self,tipo,scorer=None,iter=50,avg='binary'):
        """Si tipo c clasificacion else regression, crea el modelo lo entrena con hyperopt, guarda parametros y
        printea resultados, se decide solo el tipo de linearsvm a utilizar"""
        #estableciendo tipo de problema(clasificacion o regresion,escorer(con defaults).
        self.bparams(tipo,scorer,avg)

        self.space = {'n_estimators': hp.quniform('n_estimators',10,150,1),'C': hp.quniform('C',1,30,1)}

        if self.tipo == 'c':
            self.string = "self.model = BaggingClassifier(svm.LinearSVC(dual=False,C=int(space['C'])),n_estimators=int(space['n_estimators']))"
        else:
            self.string = "self.model = BaggingRegressor(svm.LinearSVR(dual=False,C=int(space['C'])),n_estimators=int(space['n_estimators']))"

        #hyperopt
        best_hyperparams = self.hyper_opt(iter)

        #Fittenado y printeando modelo con los mejores parametros
        if self.tipo == 'c':
            lsvms = BaggingClassifier(svm.LinearSVC(dual=False,C=int(best_hyperparams['C'])),n_estimators=int(best_hyperparams['n_estimators']))
        else:
            lsvms = BaggingRegressor(svm.LinearSVR(dual=False,C=int(best_hyperparams['C'])),n_estimators=int(best_hyperparams['n_estimators']))
        lsvms.fit(self.X_train,self.y_train)
        y_pred = lsvms.predict(self.X_test)
        self.metricas(self.y_test,y_pred)
        #guardando datos del modelo
        self.params = best_hyperparams
        self.model = lsvms

    def nsvms(self,tipo,scorer=None,iter=50,avg='binary'):
        """Si tipo c clasificacion else regression, crea el modelo lo entrena con hyperopt, guarda parametros y
        printea resultados, se decide solo el tipo de svm a utilizar, la stands for normal"""
        #estableciendo tipo de problema(clasificacion o regresion,escorer(con defaults).
        self.bparams(tipo,scorer,avg)

        self.space = {'n_estimators': hp.quniform('n_estimators',10,150,1),'C': hp.quniform('C',1,30,1)}

        if self.tipo == 'c':
            self.string = "self.model = BaggingClassifier(svm.SVC(C=int(space['C'])),n_estimators=int(space['n_estimators']))"
        else:
            self.string = "self.model = BaggingRegressor(svm.SVR(C=int(space['C'])),n_estimators=int(space['n_estimators']))"

        #hyperopt
        best_hyperparams = self.hyper_opt(iter)

        #Fittenado y printeando modelo con los mejores parametros
        if self.tipo == 'c':
            nsvms = BaggingClassifier(svm.SVC(C=int(best_hyperparams['C'])),n_estimators=int(best_hyperparams['n_estimators']))
        else:
            nsvms = BaggingRegressor(svm.SVR(C=int(best_hyperparams['C'])),n_estimators=int(best_hyperparams['n_estimators']))
        nsvms.fit(self.X_train,self.y_train)
        y_pred = nsvms.predict(self.X_test)
        self.metricas(self.y_test,y_pred)
        #guardando datos del modelo
        self.params = best_hyperparams
        self.model = nsvms

if __name__ == '__main__':
    import pandas as pd 
    #df = pd.read_csv(r'D:\Programacion\Datasets\red-wine.csv')
    #X = df.drop(['quality'],axis=1)
    #y = df.quality
    df = pd.read_csv(r'D:\Programacion\Datasets\mobiles\train.csv')
    X = df.drop(['price_range'],axis=1)
    y = df.price_range
    



    #XGB
    test= XGBs(X,y)
    test.xgbs('c',iter=30,avg='w')
    #print(test)

    #LinearSVM
    #test= Svms(X,y)
    #test.lsvms(tipo='r',iter=10)
    #print(test)

    #NSVM
    #test= Svms(X,y)
    #print(test.X_train)
    #test.nsvms('r',iter=50)
    
    print(test)





    

    