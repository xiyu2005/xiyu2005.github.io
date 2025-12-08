#!/usr/bin/python
import io
from experiment import Example
from experiment import Experiment

def any_redundant_records(experiment):
    set_size = len(experiment.training_set)
    for i in range(set_size):
        for j in range(i+1, set_size):
            flag_compound = experiment.training_set[i].compound_id == experiment.training_set[j].compound_id
            flag_assay = experiment.training_set[i].assay_id == experiment.training_set[j].assay_id
            if flag_assay and flag_compound:
                print('redundant')

def read_example(line, compounds):
    strings = line.split(',')
    compound_id = str(strings[0])
    pic50_exp = float(strings[1])
    pic50_pred = float(strings[2])
    assay_id = int(strings[3])
    smiles = strings[4]

    if compound_id not in compounds:
        compounds[compound_id] = smiles

    example = Example(compound_id, assay_id, pic50_exp, pic50_pred)

    return example

def read_txt(filename, mode='random'):
    file = open(filename, 'r', encoding='UTF-8', errors='ignore')
    lines = file.readlines()
    file.close()

    num_lines = len(lines)

    assay_ids = []
    compounds = {}

    rand_train = {}
    real_train = {}
    rand_test = {}
    real_test = {}

    read_assay = False
    read_rand_train = False
    read_real_train = False
    read_rand_test = False
    read_real_test = False

    for i in range(num_lines):
        lines[i] = str(lines[i].strip())
        if lines[i] == 'ChEMBL':
            read_assay = True

        if read_assay:
            try:
                assay_id = int(lines[i])
                if assay_id not in assay_ids:
                    assay_ids.append(assay_id)
            except:
                print(lines[i])

        if 'PubChem' in lines[i]:
            read_assay = False

        if 'Random training' in lines[i]:
            read_rand_train = True

        if read_rand_train:
            try:
                tmp_exp = read_example(lines[i], compounds)
                if tmp_exp.assay_id not in rand_train:
                    rand_train[tmp_exp.assay_id] = []
                    rand_train[tmp_exp.assay_id].append(tmp_exp)
                else:
                    rand_train[tmp_exp.assay_id].append(tmp_exp)
            except:
                print(lines[i])

        if 'Realistic training' in lines[i]:
            read_rand_train = False
            read_real_train = True

        if read_real_train:
            try:
                tmp_exp = read_example(lines[i], compounds)
                if tmp_exp.assay_id not in real_train:
                    real_train[tmp_exp.assay_id] = []
                    real_train[tmp_exp.assay_id].append(tmp_exp)
                else:
                    real_train[tmp_exp.assay_id].append(tmp_exp)
            except:
                print(lines[i])

        if 'Random test' in lines[i]:
            read_real_train = False
            read_rand_test = True

        if read_rand_test:
            try:
                tmp_exp = read_example(lines[i], compounds)
                if tmp_exp.assay_id not in rand_test:
                    rand_test[tmp_exp.assay_id] = []
                    rand_test[tmp_exp.assay_id].append(tmp_exp)
                else:
                    rand_test[tmp_exp.assay_id].append(tmp_exp)
            except:
                print(lines[i])

        if 'Realistic test' in lines[i]:
            read_rand_test = False
            read_real_test = True


        if read_real_test:
            try:
                tmp_exp = read_example(lines[i], compounds)
                if tmp_exp.assay_id not in real_test:
                    real_test[tmp_exp.assay_id] = []
                    real_test[tmp_exp.assay_id].append(tmp_exp)
                else:
                    real_test[tmp_exp.assay_id].append(tmp_exp)
            except:
                print(lines[i])


    # construct the experiment set thereby
    if mode == 'random':
        experiment = Experiment(rand_train, rand_test, assay_ids, compounds, mode)
    else:
        experiment = Experiment(real_train, real_test, assay_ids, compounds, mode)

    return experiment