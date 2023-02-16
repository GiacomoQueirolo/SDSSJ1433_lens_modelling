import pickle
from lenstronomy.Sampling.parameters import Param

from Utils.tools import * 
from Utils.get_res import get_mcmc_prm
from Data.input_data import get_kwargs_model, get_kwargs_constraints

def _get_Param(setting):
    setting = get_setting_module(setting,1)
    kwargs_lens_init, kwargs_lens_sigma, kwargs_fixed_lens, kwargs_lower_lens, kwargs_upper_lens = setting.lens_params
    kwargs_ps_init, kwargs_ps_sigma, kwargs_fixed_ps, kwargs_lower_ps, kwargs_upper_ps = setting.ps_params
    kwargs_lens_light_init, kwargs_lens_light_sigma, kwargs_fixed_lens_light, kwargs_lower_lens_light, kwargs_upper_lens_light = setting.lens_light_params
    if not setting.WS:
        kwargs_source_init, kwargs_source_sigma, kwargs_fixed_source, kwargs_lower_source, kwargs_upper_source = setting.source_params
    else:
        kwargs_source_init, kwargs_source_sigma, kwargs_fixed_source, kwargs_lower_source, kwargs_upper_source = None,None,None,None,None
    
    kwargs_model       = get_kwargs_model(setting)
    kwargs_constraints = get_kwargs_constraints(setting)
    param_class = Param(kwargs_model, kwargs_fixed_lens=kwargs_fixed_lens, kwargs_fixed_source=kwargs_fixed_source,
                        kwargs_fixed_lens_light=kwargs_fixed_lens_light, kwargs_fixed_ps=kwargs_fixed_ps, kwargs_fixed_special=None,
                        kwargs_fixed_extinction=None, 
                        kwargs_lower_lens=kwargs_lower_lens, kwargs_lower_source=kwargs_lower_source, 
                        kwargs_lower_lens_light=kwargs_lower_lens_light, kwargs_lower_ps=kwargs_lower_ps,
                        kwargs_lower_special=None, kwargs_lower_extinction=None,
                        kwargs_upper_lens=kwargs_upper_lens, kwargs_upper_source=kwargs_upper_source, 
                        kwargs_upper_lens_light=kwargs_upper_lens_light, kwargs_upper_ps=kwargs_upper_ps,
                        kwargs_upper_special=None, kwargs_upper_extinction=None,
                        kwargs_lens_init=None, **kwargs_constraints)

    return param_class

def get_Param(setting,save=True):
    try:
        with open(get_savefigpath(setting)+"/Prm_class.pkl","rb") as f:
            param_class = pickle.load(f)
    except FileNotFoundError:
        param_class = _get_Param(setting)
        if save:
            with open(get_savefigpath(setting)+"/Prm_class.pkl","wb") as f:
                pickle.dump(param_class,f)
    return param_class

def get_prm_list(setting,backup_path="./backup_path"):
    param_class = get_Param(setting)
    list_prm    = param_class.num_param()[1]
    # validity check:
    try:
        list_prm_mcmc=get_mcmc_prm(setting,backup_path=backup_path)
        if list_prm!=list_prm_mcmc:
            raise RuntimeError("The parameter have changed since the MCMC run!")
    except FileNotFoundError:
        print("warning: I couldn't double check that the parameter didn't change since the MCMC run")
    return list_prm

def conv_mcmc_i_to_kwargs(setting,mcmc_i):
    param_class   = get_Param(setting)
    kwargs_result = param_class.args2kwargs(mcmc_i, bijective=True)
    return kwargs_result
