"""
The previous code generated ABF1 files which display properly in ClampFit but
not in MiniAnalysis. To assess why, the ABF converter was used to convert this 
"unknown binary" format to an ABF with a header MiniAnalysis is comfortable 
with. By inspecting that header we can see what needs to be changed to support
MiniAnalysis.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf

if __name__ == "__main__":

    # load both files
    print("loading original ABF...")
    abfOrig = pyabf.ABF(PATH_HERE+"/2018-11-25 abf1 de novo.abf")
    print("loading MiniAnalysis Converted ABF...")
    abfMini = pyabf.ABF(PATH_HERE+"/2018-11-26 mini analysis converted.abf")

    # load the string headers of each file
    abfOrigHeader = abfOrig.getInfoPage().getText().split("\n")
    abfMiniHeader = abfMini.getInfoPage().getText().split("\n")
    assert len(abfOrigHeader)==len(abfMiniHeader)

    # compare the headers line by line, showing differences
    text = "# ABF1 Header Differences\n\n"
    text += f"comparing `{abfOrig.abfID}` and `{abfMini.abfID}` \n\n"
    headerStarted = False
    for i in range(len(abfOrigHeader)):
        origLine = abfOrigHeader[i]
        miniLine = abfMiniHeader[i]
        if "ABF1 Header" in origLine:
            headerStarted=True
        if not headerStarted:
            continue
        if "\\" in origLine or "Protocol" in origLine or "protocol" in origLine:
            continue
        if origLine!=miniLine:
            text += f"```\n{origLine}\n{miniLine}\n```\n\n"
    with open(PATH_HERE+"/2018-11-26 abf file comparison.md",'w') as f:
        f.write(text)
    print("DONE")
