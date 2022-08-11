from baseblock import Enforcer

from openai_helper.bp import OpenAICustomModel

import os

os.environ['USE_OPENAI'] = str(True)
os.environ['OPENAI_KEY'] = 'gAAAAABiH-eZKbScaS9reXABcCVeRA-VK7rbh-ZBzH72tfzRjTHIH6y5DmcFPxs1Hbf5suJufyD6Z_WhL4h1N1s_BBGpV5JqGZpVCPoB-dAPIFz6gE3uEgUMv_le5RYej5jnZawccsOSKA1RWWpC-CVTcn80S4LehA=='
os.environ['OPENAI_ORG'] = 'gAAAAABiH-0FMWAwMybowrACJ6GPkC91E4DgaV2lJoextMR7U4O5DjB_pw9jBUusuCdH9KEUXp-3Iq-Fni1X-eE6ulSg8JEKtZs-bClX_D-2DyvYpv65iPs='


def manually_test_component_with_creds():

    johnkao_model_name = "file-N2QMp92F0kkETGSdknISails"

    bp = OpenAICustomModel(johnkao_model_name)
    assert bp

    output_text, event = bp.process("How can I be successful in business?")

    Enforcer.is_str(output_text)
    Enforcer.is_dict(event)


def main():
    manually_test_component_with_creds()


if __name__ == "__main__":
    main()
