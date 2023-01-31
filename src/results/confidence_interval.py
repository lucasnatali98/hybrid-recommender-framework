from src.results.results import AbstractResults
from scipy.stats import t, norm, ttest_1samp, ttest_ind, ttest_ind_from_stats, ttest_rel
from src.utils import process_parameters
from scipy import stats
import numpy as np


class ConfidenceInterval(AbstractResults):

    def __init__(self, parameters: dict) -> None:
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

        self.loc = parameters.get('loc')
        self.sigma = parameters.get('sigma')
        self.scale = parameters.get('scale')
        self.type = parameters.get('type')
        self.alpha = parameters.get('alpha')

    def get_results(self, sample_data, **kwargs):
        """

        @return:
        """
        if self.type == "norm":
            return norm.interval()

        if self.type == "t":
            return norm.interval()

        return None


class ConfidenceIntervalMean(ConfidenceInterval):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def get_results(self, sample_data, **kwargs):
        return stats.t.interval(
            alpha=0.95,
            loc=np.mean(sample_data),
            df=len(sample_data) - 1,
            scale=stats.sem(sample_data)
        )


class ConfidenceIntervalBinomial(ConfidenceInterval):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def get_results(self, sample_data, **kwargs):
        return stats.binom.interval(
            alpha=0.99,
            n=len(sample_data) - 1,
            loc=np.mean(sample_data),
            p=stats.sem(sample_data)
        )


class ConfidenceIntervalLinearDifference(ConfidenceInterval):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def get_results(self, sample_data, **kwargs):
        sample_data = np.array(sample_data)
        sample_data2 = np.array(kwargs.get('sample_data2'))

        diffsamp = sample_data - sample_data2
        len_no_obs = len(sample_data)
        diffmean = np.mean(diffsamp)
        diffvar = np.var(diffsamp, ddof=1)
        criticalvalue = stats.t.ppf(q=1 - alp / 2, df=len_no_obs - 1)
        rad = criticalvalue * np.sqrt(diffvar) / np.sqrt(len_no_obs)

        return [diffmean - rad, diffmean + rad]
