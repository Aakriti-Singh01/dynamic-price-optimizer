import shap


def get_shap_values(model, X_sample, X_background):
    """
    Generate SHAP values using KernelExplainer
    """

    def predict_fn(data):
        return model.predict(data)

    explainer = shap.KernelExplainer(predict_fn, X_background)
    shap_values = explainer.shap_values(X_sample)

    return shap_values