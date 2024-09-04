from pymol import cmd
from pymol import stored

def listResidues(selName, output=False):
    """
    list the model name, chain name, residual name and residual index of a selection.

    PARAMS
        selName
            The selection name to list information.

        output
            If False the information will print on the screen,
            else True the information will also be saved in csv file in present working directory.
            Default filename is {selName}_info.csv

    RETURN
        A list of tuple contains the aforemetioned information.

    AUTHOR
        xhp 2024.09.04
    """

    # get model chain resn resi
    stored.r, rVals = [], []
    cmd.iterate(f"{selName}", "stored.r.append((model, chain, resn, resi))")

    # transfer data from stored.r to rVals
    for (model, chain, resn, resi) in stored.r:
        rVals.append((model, chain, resn, resi))
    rVals = sorted(set(rVals), key=lambda x: (x[0], x[1], int(x[-1]))) # remove duplicated residues

    # print information
    models = {} # a dictionary to organize residues information by model
    print("-" * 51)
    print(f"{'Model name':<15}|{'Chain':<6}|{'Residue name':<13}|{'Residue index':<14}")
    print("-" * 51)
    for (model, chain, resn, resi) in rVals:
        print(f"{model:>15} {chain:>6} {resn:>13} {resi:>14}")
        if model in models:
            models[model].append(f"{resn}{resi}({chain})")
        else:
            models[model] = []
            models[model].append(f"{resn}{resi}({chain})")
    print("-" * 51)
    print()
    for model in models:
        print(f"Residues in {model}: {', '.join(models[model])}.\n")

    # save information to csv file
    if output:
        f = open(f"{selName}_info.csv", "w+")
        f.write("Model name, Chain, Residue name, Residue index\n")
        for (model, chain, resn, resi) in rVals:
            f.write(f"{model}, {chain}, {resn}, {resi}\n")
        f.close()
        print(f"All data has been saved.")
    else:
        pass

    return rVals

cmd.extend("listResidues", listResidues)