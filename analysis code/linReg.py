import networkx as nx
import numpy as np
import analysis as analysis
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm


def fit_model(df, filename):
    f = open(filename + ".txt", "w")

    #fit model
    res = smf.ols(formula='CD ~ (std_d + std_rs + std_rw) ** 2', data=df).fit()
    f.write(str(res.summary()))
    f.write(str(anova_lm(res)))
    
    #fit SPL model
    res2 = smf.ols(formula='SPL ~ (std_d + std_rs + std_rw) ** 2', data=df).fit()
    f.write(str(res2.summary()))
    f.write(str(anova_lm(res2)))
    
    f.close()