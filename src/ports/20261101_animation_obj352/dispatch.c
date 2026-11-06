typedef unsigned int u32;
struct NNSG3dResTexPatAnm_;
struct NNSG3dResTexPatAnmFV_;
struct NNSG3dResDictTexPatAnmData_;
extern u32 native_main_0202bf2c(signed int resource, u32 index);
extern const struct NNSG3dResTexPatAnmFV_ *native_main_0202bfe0(const struct NNSG3dResTexPatAnm_ *resource, u32 index, u32 frame);
extern const struct NNSG3dResDictTexPatAnmData_ *native_fn_0202c054(const struct NNSG3dResTexPatAnm_ *resource, u32 index);
extern int native_main_020364dc(int width, int height);
__declspec(dllexport) u32 j2p_run(u32 entry, u32 a, u32 b, u32 c) {
    switch (entry) {
    case 0x0202BF2C:
        return native_main_0202bf2c((signed int)a, b);
    case 0x0202BFE0:
        return (u32)native_main_0202bfe0((const struct NNSG3dResTexPatAnm_ *)a, b, c);
    case 0x0202C054:
        return (u32)native_fn_0202c054((const struct NNSG3dResTexPatAnm_ *)a, b);
    case 0x020364DC:
        return native_main_020364dc((signed int)a, (signed int)b);
    }
    return 0xFFFFFFFFU;
}
