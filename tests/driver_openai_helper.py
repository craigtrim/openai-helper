from pprint import pprint

from openai_helper.bp import OpenAICompletion

import os
os.environ['OPENAI_KEY'] = 'gAAAAABiH-eZKbScaS9reXABcCVeRA-VK7rbh-ZBzH72tfzRjTHIH6y5DmcFPxs1Hbf5suJufyD6Z_WhL4h1N1s_BBGpV5JqGZpVCPoB-dAPIFz6gE3uEgUMv_le5RYej5jnZawccsOSKA1RWWpC-CVTcn80S4LehA=='
os.environ['OPENAI_ORG'] = 'gAAAAABiH-0FMWAwMybowrACJ6GPkC91E4DgaV2lJoextMR7U4O5DjB_pw9jBUusuCdH9KEUXp-3Iq-Fni1X-eE6ulSg8JEKtZs-bClX_D-2DyvYpv65iPs='


def manually_test_bp():

    bp = OpenAICompletion()
    assert bp

    bp.run(input_prompt="Generate a one random number between 1 and 5000")

    d_output = bp.run(
        engine="text-davinci-002",
        temperature=1.0,
        max_tokens=256,
        input_prompt="Rewrite the input in grammatical English:\n\nInput: You believe I can help you understand what trust yourself? don't you?\nOutput:\n\n")

    pprint(d_output)


def main():
    manually_test_bp()


if __name__ == "__main__":
    main()
