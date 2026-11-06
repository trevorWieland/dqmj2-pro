import wave20261104_main_front_eighth_fs_fixture as F
import wave20261104_main_front_eighth_geometry_fixture as G


def execute(address,native,source,bindings):
    if address==0x020451c4:return F.execute(address,native,source,bindings)
    assert address==0x020446f8
    return G.execute(address,native,source,bindings)
