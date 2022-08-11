from openai_helper.dmo import OpenAIConnector


import os
os.environ['OPENAI_KEY'] = 'gAAAAABiH-eZKbScaS9reXABcCVeRA-VK7rbh-ZBzH72tfzRjTHIH6y5DmcFPxs1Hbf5suJufyD6Z_WhL4h1N1s_BBGpV5JqGZpVCPoB-dAPIFz6gE3uEgUMv_le5RYej5jnZawccsOSKA1RWWpC-CVTcn80S4LehA=='
os.environ['OPENAI_ORG'] = 'gAAAAABiH-0FMWAwMybowrACJ6GPkC91E4DgaV2lJoextMR7U4O5DjB_pw9jBUusuCdH9KEUXp-3Iq-Fni1X-eE6ulSg8JEKtZs-bClX_D-2DyvYpv65iPs='


def manually_test_component_with_creds():

    dmo = OpenAIConnector()
    assert dmo

    conn = dmo.process()
    assert conn


def main():
    manually_test_component_with_creds()


if __name__ == "__main__":
    main()
