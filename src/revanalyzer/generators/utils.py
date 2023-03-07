import numpy as np
import os


def make_cuts(datadir, image, outputdir, L, l, total=True):
    cut_names = []
    A = _read_array(os.path.join(datadir, image), L, 'uint8')
    A0 = A[int((L-l)/2):int((L+l)/2), int((L-l)/2)
               :int((L+l)/2), int((L-l)/2):int((L+l)/2)]
    cut_name0 = "cut0_" + str(l) + "_" + image
    cut_names.append(cut_name0)
    fout0 = os.path.join(outputdir, cut_name0)
    A0.astype('uint8').tofile(fout0)
    if (total):
        A1 = A[:l, :l, :l]
        A2 = A[:l, :l, L-l:]
        A3 = A[:l, L-l:, :l]
        A4 = A[L-l:, :l, :l]
        A5 = A[L-l:, L-l:, L-l:]
        A6 = A[:l, L-l:, L-l:]
        A7 = A[L-l:, :l, L-l:]
        A8 = A[L-l:, L-l:, :l]
        A = [A1, A2, A3, A4, A5, A6, A7, A8]
        for i in range(1, 9):
            cut_name = "cut" + str(i) + "_" + str(l) + "_" + image
            cut_names.append(cut_name)
            fout = os.path.join(outputdir, cut_name)
            A[i-1].astype('uint8').tofile(fout)
        return cut_names
    else:
        return cut_name0


def _read_array(image, dim, dtype):
    v = np.fromfile(image, dtype=dtype, sep="")
    return v.reshape([dim, dim, dim])
