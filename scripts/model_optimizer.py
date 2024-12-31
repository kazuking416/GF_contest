import warnings
warnings.filterwarnings('ignore')

import optuna
from sklearn.svm import SVR
import xgboost as xgb
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C, Matern, DotProduct
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt

# Optunaのログ出力を抑制
optuna.logging.set_verbosity(optuna.logging.WARNING)

def plot_optimization_history(study):
    trials_df = study.trials_dataframe()
    trials_df['best_value'] = trials_df['value'].cummax()
    
    plt.figure(figsize=(14, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(trials_df['number'], trials_df['best_value'], label='Best R2')
    plt.xlabel('Trial')
    plt.ylabel('Best R2')
    plt.title('Optimization History (R2)')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(trials_df['number'], -trials_df['best_value'], label='Best MSE')  # R2の最大化はMSEの最小化に対応
    plt.xlabel('Trial')
    plt.ylabel('Best MSE')
    plt.title('Optimization History (MSE)')
    plt.legend()
    
    plt.show()

def check_data_consistency(X_train, y_train):
    if len(X_train) != len(y_train):
        raise ValueError(f"Inconsistent number of samples: {len(X_train)} in X_train, {len(y_train)} in y_train")

def optimize_svr(X_train, y_train):
    check_data_consistency(X_train, y_train)
    
    def objective(trial):
        C = trial.suggest_loguniform('C', 1e-3, 1e3)
        epsilon = trial.suggest_loguniform('epsilon', 1e-3, 1e1)
        model = SVR(C=C, epsilon=epsilon)
        score = cross_val_score(model, X_train, y_train, cv=3, scoring='r2').mean()
        return score
    
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=100, callbacks=[lambda study, trial: print(f"Best R2: {study.best_value}")])
    best_params = study.best_params
    best_model = SVR(**best_params)
    best_model.fit(X_train, y_train)
    
    plot_optimization_history(study)
    
    return best_model

def optimize_xgb(X_train, y_train):
    check_data_consistency(X_train, y_train)
    
    def objective(trial):
        param = {
            'verbosity': 0,  # 出力を抑制
            'objective': 'reg:squarederror',
            'booster': 'gbtree',
            'max_depth': trial.suggest_int('max_depth', 3, 9),
            'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
            'eta': trial.suggest_loguniform('eta', 1e-8, 1.0),
            'gamma': trial.suggest_loguniform('gamma', 1e-8, 1.0),
            'grow_policy': trial.suggest_categorical('grow_policy', ['depthwise', 'lossguide'])
        }
        model = xgb.XGBRegressor(**param)
        score = cross_val_score(model, X_train, y_train, cv=3, scoring='r2').mean()
        return score
    
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=100, callbacks=[lambda study, trial: print(f"Best R2: {study.best_value}")])
    best_params = study.best_params
    best_model = xgb.XGBRegressor(**best_params)
    best_model.fit(X_train, y_train)
    
    plot_optimization_history(study)
    
    return best_model

def optimize_gpr(X_train, y_train):
    check_data_consistency(X_train, y_train)
    
    def objective(trial):
        kernel_choice = trial.suggest_categorical('kernel', ['RBF', 'Matern3', 'Matern5'])
        if kernel_choice == 'RBF':
            kernel = C(1.0, (1e-3, 1e3)) * RBF(trial.suggest_loguniform('length_scale', 1e-2, 1e2))
        elif kernel_choice == 'Matern3':
            kernel = C(1.0, (1e-3, 1e3)) * Matern(length_scale=trial.suggest_loguniform('length_scale', 1e-2, 1e2), nu=1.5)
        elif kernel_choice == 'Matern5':
            kernel = C(1.0, (1e-3, 1e3)) * Matern(length_scale=trial.suggest_loguniform('length_scale', 1e-2, 1e2), nu=2.5)
        
        
        model = GaussianProcessRegressor(kernel=kernel, alpha=1e-10, n_restarts_optimizer=trial.suggest_int('n_restarts_optimizer', 0, 10))
        score = cross_val_score(model, X_train, y_train, cv=3, scoring='r2', n_jobs=-1, error_score='raise').mean()
        return score
    
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=10, callbacks=[lambda study, trial: print(f"Best R2: {study.best_value}")])
    best_params = study.best_params
    if best_params['kernel'] == 'RBF':
        best_kernel = C(1.0, (1e-3, 1e3)) * RBF(best_params['length_scale'])
    elif best_params['kernel'] == 'Matern3':
        best_kernel = C(1.0, (1e-3, 1e3)) * Matern(length_scale=best_params['length_scale'], nu=1.5)
    elif best_params['kernel'] == 'Matern5':
        best_kernel = C(1.0, (1e-3, 1e3)) * Matern(length_scale=best_params['length_scale'], nu=2.5)
    
    best_model = GaussianProcessRegressor(kernel=best_kernel, alpha=1e-10, n_restarts_optimizer=best_params['n_restarts_optimizer'])
    best_model.fit(X_train, y_train)
    
    plot_optimization_history(study)
    
    return best_model