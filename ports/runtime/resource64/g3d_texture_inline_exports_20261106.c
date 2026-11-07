#if !defined(_MSC_VER)
#include "g3d_texture_types_20261106.h"

extern u32 NNS_GfdGetTexKeyAddr(NNSGfdTexKey);
extern void *native_fn_0202bbb4(const NNSG3dResDict *, const NNSG3dResName *);

NNSG3dResDictTexData *NNS_G3dGetTexDataByName(const NNSG3dResTex *texture, const NNSG3dResName *name) {
    if (texture) return (NNSG3dResDictTexData *)native_fn_0202bbb4(&texture->dict, name);
    return 0;
}

NNSG3dResDictPlttData *NNS_G3dGetPlttDataByName(const NNSG3dResTex *texture, const NNSG3dResName *name) {
    const NNSG3dResDict *dictionary;
    if (!texture || !texture->plttInfo.ofsDict) return 0;
    dictionary = (const NNSG3dResDict *)((const u8 *)texture + texture->plttInfo.ofsDict);
    return (NNSG3dResDictPlttData *)native_fn_0202bbb4(dictionary, name);
}
#endif
