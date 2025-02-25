{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyM94YQaL7AR7uPFNuvmEpFR"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "QsO766U8D9Jf"
      },
      "outputs": [],
      "source": [
        "class ABTestAnalyser:\n",
        "\n",
        "  def __init__(self,A_group, B_group):\n",
        "    self.A_group = A_group\n",
        "    self.B_group = B_group\n",
        "\n",
        "  def getData(self):\n",
        "    return A_group,B_group\n",
        "  \n",
        "  def setData(self,new_A, new_B):\n",
        "    self.A_group = new_A\n",
        "    self.B_group = new_B\n",
        "\n",
        "  def checkAdversarialLabel(self,\n",
        "                    covariates,\n",
        "                    sample_frac = 1.0,\n",
        "                    thr_max = 0.51,\n",
        "                    thr_min = 0.49,\n",
        "                    verbose = False\n",
        "                    ):\n",
        "  \"\"\"\n",
        "  Check if the group variants were stratified correctly using adverserial strategy\n",
        "\n",
        "  Parameters:\n",
        "  * covariates: List of covariates\n",
        "  * sample_frac: Sample of fraction % for faster validation (default 1)\n",
        "  * thr_max: Max threshold for ROC (default 0.51)\n",
        "  * thr_min: Min threshold for ROC (default 0.49)\n",
        "  * verbose: if True then print all step status\n",
        "\n",
        "  Returns: True / False\n",
        "  \"\"\" \n",
        "  from sklearn.ensemble import RandomForestClassifier\n",
        "  from sklearn.model_selection import cross_val_predict\n",
        "  from sklearn.metrics import roc_auc_score\n",
        "\n",
        "  if verbose == True:\n",
        "    print(\"Adverserial validation started...\")\n",
        "  if len(covariates) < 1:\n",
        "    return False\n",
        "  \n",
        "  A_group = self.A_group.copy(deep = True)\n",
        "  B_group = self.B_group.copy(deep = True)\n",
        "\n",
        "  # if sample fraction is specified, extract the subsets randomly\n",
        "  if (sample_frac < 1.0) and (sample_frac > 0.0):\n",
        "    if verbose == True:\n",
        "      print(\"Sampling {} of both datasets\".format(sample_frac))\n",
        "\n",
        "    A_group = A_group.sample(frac = sample_frac)\n",
        "    B_group = B_group.sample(frac = sample_frac)\n",
        "    \n",
        "  # Prepare a dataset by combining A & B and put labels of the groups - 2 classes\n",
        "  if verbose == True:\n",
        "    print(\"Combine A & B groups and create group label for each\")\n",
        "  X = A_group.append(B_group) \n",
        "  y = [0]*len(A_group) + [1]*len(B_group) # put a pseudolabel\n",
        "\n",
        "  # convert all categorical variables to binary \n",
        "  X = pd.get_dummies(X,columns = covariates)\n",
        "\n",
        "  if verbose == True:\n",
        "    print(\"Run a classifier to distinguish between the 2 datasets\")\n",
        "  model = RandomForestClassifier() # use RandomForest here but could be any classifier\n",
        "  \n",
        "  # do cross-val and output prediction of pseudo-label\n",
        "  cv_preds = cross_val_predict(model, \n",
        "                               X, \n",
        "                               y, \n",
        "                               cv=2, \n",
        "                               n_jobs = None,\n",
        "                               method = \"predict_proba\",\n",
        "                               verbose = verbose)\n",
        "  \n",
        "  roc_score = roc_auc_score(y_true = y, y_score = cv_preds[:,1])\n",
        "  if verbose == True:\n",
        "    print (\"ROC Score = {}\".format(roc_score))\n",
        "    print (\"Adverserial validation finished.\")\n",
        "\n",
        "  return thr_min <= roc_score <= thr_max"
      ]
    }
  ]
}