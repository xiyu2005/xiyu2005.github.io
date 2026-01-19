#!/usr/bin/python

from sklearn.ensemble import RandomForestRegressor
import numpy as np
from rdkit.Chem import AllChem
from rdkit.Chem import DataStructs
from rdkit import Chem
from sklearn.metrics import r2_score
from sklearn.cross_decomposition import PLSRegression
import os
import pandas as pd
import pickle

class Example():
    """A simple data container for a single experimental data point."""
    def __init__(self, compound_id, assay_id, pic50_exp, pic50_pred=None):
        self.compound_id = compound_id
        self.assay_id = assay_id
        self.pic50_exp = pic50_exp
        self.pic50_pred = pic50_pred

class Experiment():
    """
    Encapsulates the entire pQSAR workflow, including RFR model building,
    feature profile generation, and the final PLS model training with Max2 optimization.
    """
    def __init__(self, training_set, test_set, assays, compounds, mode):
        self.training_set = training_set
        self.test_set = test_set
        self.assays = assays
        self.compounds = compounds
        self.mode = mode
        self.rfr_r2s = {}
        self.pls_r2s = {}
        self.assay_keys_for_features = [] # To store the order of features

    def build_rfr_models(self, store=False):
        """Step 1: Build an individual Random Forest Regressor for each assay."""
        self.rfr_models = {}
        cwd = os.getcwd()
        print("--- Building RFR Models (Step 1) ---")

        for assay_id in self.training_set.keys():
            # Prepare training data
            X_train, y_train = [], []
            for exp in self.training_set[assay_id]:
                smile = self.compounds.get(exp.compound_id)
                if not smile: continue
                mol = Chem.MolFromSmiles(smile)
                if not mol: continue
                fp = AllChem.GetMorganGenerator(radius=2, fpSize=1024).GetFingerprint(mol)
                arr = np.zeros((0,), dtype=np.int8)
                DataStructs.ConvertToNumpyArray(fp, arr)
                X_train.append(arr)
                y_train.append(exp.pic50_exp)

            if len(X_train) < 10: # Skip assays with too little data
                print(f"Skipping RFR for assay {assay_id}: only {len(X_train)} training points.")
                continue
            
            X_train, y_train = np.array(X_train), np.array(y_train)

            # Train the model
            regr = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
            regr.fit(X_train, y_train)

            # Prepare test data
            X_test, y_test = [], []
            for exp in self.test_set[assay_id]:
                smile = self.compounds.get(exp.compound_id)
                if not smile: continue
                mol = Chem.MolFromSmiles(smile)
                if not mol: continue
                fp = AllChem.GetMorganGenerator(radius=2, fpSize=1024).GetFingerprint(mol)
                arr = np.zeros((0,), dtype=np.int8)
                DataStructs.ConvertToNumpyArray(fp, arr)
                X_test.append(arr)
                y_test.append(exp.pic50_exp)

            if len(X_test) == 0:
                self.rfr_r2s[assay_id] = -999 # Indicate no test data
                continue

            # Evaluate and store results
            X_test, y_test = np.array(X_test), np.array(y_test)
            y_pred = regr.predict(X_test)
            r2 = r2_score(y_test, y_pred)
            self.rfr_r2s[assay_id] = r2
            print(f"RFR R^2 for Assay {assay_id}: {r2:.4f}")
            
            if store:
                model_dir = os.path.join(cwd, 'rfr_models')
                os.makedirs(model_dir, exist_ok=True)
                model_filename = os.path.join(model_dir, f'{assay_id}.sav')
                pickle.dump(regr, open(model_filename, 'wb'))

        if store:
            df = pd.DataFrame.from_dict(self.rfr_r2s, orient='index', columns=['R2_Score'])
            df.to_csv(os.path.join(cwd, 'rfr_r2_scores.csv'))

    def compound_rfr_features(self):
        """Step 2: Generate the 'activity profile' for all compounds using the RFR models."""
        print("--- Generating RFR Features (Activity Profile) ---")
        cwd = os.getcwd()
        rfr_models = {}
        model_dir = os.path.join(cwd, 'rfr_models')
        
        if not os.path.isdir(model_dir):
            print("Error: `rfr_models` directory not found. Please run `build_rfr_models` first.")
            return

        for file in os.listdir(model_dir):
            if file.endswith('.sav'):
                assay_id = int(file.split('.')[0])
                filename = os.path.join(model_dir, file)
                rfr_models[assay_id] = pickle.load(open(filename, 'rb'))
        
        # Sort assay keys to ensure consistent feature order
        self.assay_keys_for_features = sorted(rfr_models.keys())
        
        compounds_rfr_dict = {}
        for comp_id, smile in self.compounds.items():
            mol = Chem.MolFromSmiles(smile)
            if not mol: continue
            
            fp = AllChem.GetMorganGenerator(radius=2, fpSize=1024).GetFingerprint(mol)
            arr = np.zeros((0,), dtype=np.int8)
            DataStructs.ConvertToNumpyArray(fp, arr)
            feature_vector = [rfr_models[aid].predict(arr.reshape(1, -1))[0] for aid in self.assay_keys_for_features]
            compounds_rfr_dict[comp_id] = np.array(feature_vector)

        # Save the feature dictionary and the key mapping for robust loading
        data_to_save = {
            'assay_keys': self.assay_keys_for_features,
            'features': compounds_rfr_dict
        }
        filename = os.path.join(cwd, 'compound_rfr_features.pkl')
        with open(filename, 'wb') as f:
            pickle.dump(data_to_save, f)
        print("--- Activity Profile saved to compound_rfr_features.pkl ---")


    def _train_and_eval_pls(self, X_train, y_train, X_test, y_test):
        """Helper function to train and evaluate a single PLS model."""
        if X_train.shape[1] == 0 or X_test.shape[1] == 0: # No features selected
            return -999, None
        
        # n_components cannot be larger than the number of features or samples
        n_comp = min(10, X_train.shape[0], X_train.shape[1])
        if n_comp < 1:
            return -999, None

        try:
            pls = PLSRegression(n_components=n_comp)
            pls.fit(X_train, y_train)
            y_pred = pls.predict(X_test).flatten()
            return r2_score(y_test, y_pred), pls
        except Exception as e:
            print(f"    PLS failed: {e}")
            return -999, None

    def build_pls_models(self, load=True, store=False):
        """Step 3: Build final PLS models using the Max2 optimization for feature selection."""
        print("--- Building PLS Models with Max2 Optimization (Step 3) ---")
        cwd = os.getcwd()

        if load:
            feature_file = os.path.join(cwd, 'compound_rfr_features.pkl')
            if not os.path.exists(feature_file):
                print("Error: `compound_rfr_features.pkl` not found. Please run `compound_rfr_features` first.")
                return
            with open(feature_file, 'rb') as f:
                loaded_data = pickle.load(f)
            self.compounds_rfr = loaded_data['features']
            self.assay_keys_for_features = loaded_data['assay_keys']
        
        key_to_index = {key: i for i, key in enumerate(self.assay_keys_for_features)}

        for assay_id in self.training_set.keys():
            print(f"Processing PLS for Assay {assay_id}...")
            # Prepare full training and test sets for this assay
            train_compound_ids = [exp.compound_id for exp in self.training_set[assay_id]]
            test_compound_ids = [exp.compound_id for exp in self.test_set[assay_id]]
            
            X_full_train = np.array([self.compounds_rfr[cid] for cid in train_compound_ids if cid in self.compounds_rfr])
            y_train = np.array([exp.pic50_exp for exp in self.training_set[assay_id] if exp.compound_id in self.compounds_rfr])
            
            X_full_test = np.array([self.compounds_rfr[cid] for cid in test_compound_ids if cid in self.compounds_rfr])
            y_test = np.array([exp.pic50_exp for exp in self.test_set[assay_id] if exp.compound_id in self.compounds_rfr])

            if len(y_train) < 10 or len(y_test) == 0:
                print(f"  Skipping PLS for assay {assay_id}: Insufficient data.")
                continue

            # --- Max2 Feature Selection Logic ---
            correlations = []
            for i, other_assay_id in enumerate(self.assay_keys_for_features):
                if other_assay_id == assay_id: # Exclude self
                    continue
                y_pred_from_other_model = X_full_train[:, i]
                with np.errstate(all='ignore'): # Suppress warnings from poor correlations
                    corr = r2_score(y_train, y_pred_from_other_model)
                if np.isfinite(corr):
                    correlations.append({'corr': corr, 'index': i})

            # Get indices for the two thresholds
            indices_05 = [item['index'] for item in correlations if item['corr'] > 0.05]
            indices_02 = [item['index'] for item in correlations if item['corr'] > 0.20]
            print(f"  Found {len(indices_05)} features for r^2>0.05 and {len(indices_02)} for r^2>0.20")
            
            # --- Train and evaluate models for both thresholds ---
            # Model 1: r^2 > 0.05
            X_train_05 = X_full_train[:, indices_05]
            X_test_05 = X_full_test[:, indices_05]
            r2_05, pls_05 = self._train_and_eval_pls(X_train_05, y_train, X_test_05, y_test)
            
            # Model 2: r^2 > 0.20
            X_train_02 = X_full_train[:, indices_02]
            X_test_02 = X_full_test[:, indices_02]
            r2_02, pls_02 = self._train_and_eval_pls(X_train_02, y_train, X_test_02, y_test)
            
            # --- Max2: Select the best of the two models ---
            final_r2 = -999
            best_model = None
            if r2_02 > r2_05:
                final_r2 = r2_02
                best_model = pls_02
                print(f"  Selected model (r^2>0.20). Final R^2: {final_r2:.4f}")
            else:
                final_r2 = r2_05
                best_model = pls_05
                print(f"  Selected model (r^2>0.05). Final R^2: {final_r2:.4f}")
            
            self.pls_r2s[assay_id] = final_r2
            
            if store and best_model:
                model_dir = os.path.join(cwd, 'pls_models_max2')
                os.makedirs(model_dir, exist_ok=True)
                model_filename = os.path.join(model_dir, f'{assay_id}.sav')
                pickle.dump(best_model, open(model_filename, 'wb'))

        if store:
            df = pd.DataFrame.from_dict(self.pls_r2s, orient='index', columns=['R2_Score_Max2'])
            df.to_csv(os.path.join(cwd, 'pls_max2_r2_scores.csv'))

