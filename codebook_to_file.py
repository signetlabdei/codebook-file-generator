# AUTHOR(S):
# Mattia Lecci <mattia.lecci@dei.unipd.it>
# 
# University of Padova (UNIPD), Italy
# Information Engineering Department (DEI) 
# SIGNET Research Group @ http://signet.dei.unipd.it/
# 
# Date: February 2021

import os
from typing import Sequence, Dict


def codebook_to_file(codebook: Sequence[Sequence[complex]], file: str, array_info: Dict) -> None:
    # Create folder if it does not exist
    folder = os.path.dirname(file)
    if folder != '':
        os.makedirs(folder, exist_ok=True)

    if array_info.get("ns3_class") == "ns3::UniformPlanarArray":
        n_codewords, n_elements = _check_codebook(codebook)

        assert n_elements == array_info.get("NumRows") * array_info.get("NumColumns"), \
            f"n_elements={n_elements}, NumRows={array_info.get('NumRows')}, NumColumns={array_info.get('NumColumns')}"

        with open(file, "wt") as f:
            # Write the PhasedArray ns-3 class used
            f.write(f"{array_info.get('ns3_class')}\n")
            # Write the fields of the class
            for field in ["AntennaElement", "AntennaVerticalSpacing", "AntennaHorizontalSpacing", "NumRows",
                          "NumColumns"]:
                f.write(f"{field},{array_info.get(field)}\n")
            # Write the number of codewords (csv rows)
            f.write(f"{n_codewords}\n")
            # Write the number of antenna elements (csv columns)
            f.write(f"{n_elements}\n")
            # Write the codebook
            for codeword in codebook:
                line = ""
                for weight in codeword:
                    # Complex number format read by C++
                    line += f"({weight.real},{weight.imag});"
                # Remove last ';'
                f.write(f"{line[:-1]}\n")

    else:
        raise ValueError(f"array_info['ns3_class']='{array_info.get('ns3_class')}' currently not supported")


def _check_codebook(codebook: Sequence[Sequence[complex]]) -> (int, int):
    n_codewords = len(codebook)
    # At least 1 codeword
    assert n_codewords > 0

    n_elements = len(codebook[0])
    # At least 1 antenna element
    assert n_codewords > 0

    for codeword in codebook:
        # All codewords should have the same length
        assert len(codeword) == n_elements

    return n_codewords, n_elements


if __name__ == "__main__":
    antenna_array = {"ns3_class": "ns3::UniformPlanarArray",
                     "AntennaElement": "ns3::IsotropicAntennaModel",
                     "AntennaVerticalSpacing": 0.5,
                     "AntennaHorizontalSpacing": 0.5,
                     "NumRows": 2,
                     "NumColumns": 2}

    cb = [[0.5, 0.5, 0.5, 0.5],
          [complex(0.027194, 0.499260), complex(0.027194, -0.499260), complex(0.027194, 0.499260),
           complex(0.027194, -0.499260)],
          [complex(0.027194, 0.499260), complex(0.027194, 0.499260), complex(0.027194, -0.499260),
           complex(0.027194, -0.499260)]]

    filename = f"codebooks/{antenna_array.get('NumRows')}x{antenna_array.get('NumColumns')}.txt"

    codebook_to_file(codebook=cb,
                     file=filename,
                     array_info=antenna_array)
