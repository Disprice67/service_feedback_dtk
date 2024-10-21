from onelogin.saml2.settings import OneLogin_Saml2_Settings
from feedback.settings import SAML_DIR


def load_saml_config():
    saml_settings = OneLogin_Saml2_Settings(
        settings=None,
        custom_base_path=SAML_DIR
    )
    return saml_settings
