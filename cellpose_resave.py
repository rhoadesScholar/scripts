# %%
import numpy as np
from PIL import Image
from glob import glob
import os
import shutil
from pathlib import Path


dataset = "jrc_mus-liver-zon-2"
base_folder = "/prfs/cellmap/cellmap/annotations/amira/{dataset}/whole_cell_single_slices/".format(dataset=dataset)
output_folder = "/nrs/cellmap/rhoadesj/tmp_data/whole_cell_single_slices/{dataset}".format(dataset=dataset)
os.makedirs(output_folder, exist_ok=True)
seg_input_prefix = "slice_"
raw_input_prefix = "raw_"
folders = ["yz", "xy", "xz"]
for folder in folders:
    input_folder = os.path.join(base_folder, folder)
    if not os.path.exists(input_folder):
        input_folder = os.path.join(base_folder, folder.upper())
    print(f"Processing {input_folder} ...")
    for seg_file in glob(os.path.join(input_folder, f"{seg_input_prefix}*.tif")):
        print(f"\tLoading {seg_file} ...")
        seg = np.array(Image.open(seg_file))
        raw_file = os.path.join(input_folder, seg_file.removeprefix(input_folder + os.sep).replace(seg_input_prefix, raw_input_prefix))
        slice_num = Path(seg_file).stem.removeprefix(seg_input_prefix)
        try:
            out_raw = os.path.join(output_folder, f"{dataset}_{folder}_{slice_num}.tif")
            print(f"\tResaving {raw_file} to {out_raw} ...")
            shutil.copy(raw_file, out_raw)
        except Exception as e:
            print(f"\t\tFailed to resave {raw_file} to {out_raw}\n\t{e}")
            continue
        out_seg = os.path.join(output_folder, f"{dataset}_{folder}_{slice_num}_seg.npy")
        print(f"\tSaving {out_seg}...")
        np.save(out_seg, np.array({"masks": seg, "outlines": []}))

# %%
