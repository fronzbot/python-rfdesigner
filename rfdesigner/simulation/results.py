"""Results handler."""


def csv_cascade(system, sim_result):
    """Generate a csv results structure."""
    csv_lines = []
    csv_lines.append("Total Results")
    for key, value in sorted(sim_result.items()):
        csv_lines.append(f"{key},{value}")
    csv_lines.append("")
    header_props = [
        "Block Name",
        "Gain (dB)",
        "NF (dB)",
        "IIP3 (dBm)",
        "P1dB (dBm)",
        "Total Gain (dB)",
        "Total NF (dB)",
        "Total IIP3 (dB)",
        "Total P1dB (dB)",
    ]

    csv_lines.append(",".join(header_props))

    for block in system:
        props = [
            block.gain,
            block.nf,
            block.iip3,
            block.p1db,
            block.total_gain,
            block.total_nf,
            block.total_iip3,
            block.total_p1db,
        ]
        value_props = ",".join(str(round(x, 2)) for x in props)
        prop_string = f"{block.name},{value_props}"
        csv_lines.append(prop_string)

    return csv_lines


def print_cascade(system, sim_result, return_lines=False):
    """
    Print the results of cascade analysis.

    :param system: system to ge results from (list of block elements)
    :param sim_result: results from cascade analysis
    :param return_lines: set to TRUE to supress printing and return lines to be printed instead
    """
    lines = csv_cascade(system, sim_result)
    print_lines = []
    for line in lines:
        print_lines.append(line.split(","))
    if return_lines:
        return print_lines

    for line in print_lines:
        print_string = ""
        for element in line:
            print_string += f"{element:<16}"
        print(print_string)
    return []


def save_csv(save_file, results):
    """Save results as csv."""
    new_results = []
    for line in results:
        new_results.append(line + "\n")
    with open(save_file, "w") as csvfile:
        csvfile.writelines(new_results)
    return save_file
