inline void NNS_G3dGeRestoreMtx (int num)
{
    ((void) 0) ;
    native_fn_main_0202e434(0x14 , (u32 *)&num, 1 );
}
inline void NNS_G3dGeTranslateVec (const VecFx32 * vec)
{
    ((void) 0) ;
    native_fn_main_0202e434(0x1c , (u32 *)vec, 3 );
}
inline void NNS_G3dGeTexCoord (fx32 s, fx32 t)
{
    u32 tmp;
    ((void) 0) ;
    ((void) 0) ;
    tmp = (((GXSt)((u16)((s16)(((s)) >> 8)) | ((u16)((s16)(( ( t)) >> 8)) << 16)))) ;
    native_fn_main_0202e434(0x22 , (u32 *)&tmp, 1 );
}
inline void NNS_G3dGeLoadMtx44 (const MtxFx44 * m)
{
    ((void) 0) ;
    native_fn_main_0202e434(0x16 ,
                        (u32 *) m,
                        16 );
}
inline void NNS_G3dGeMultMtx44 (const MtxFx44 * m)
{
    ((void) 0) ;
    native_fn_main_0202e434(0x18 ,
                        (u32 *) m,
                        16 );
}
inline void NNS_G3dGeMultMtx43 (const MtxFx43 * m)
{
    ((void) 0) ;
    native_fn_main_0202e434(0x19 ,
                        (u32 *) m,
                        12 );
}
inline void NNS_G3dGeMultMtx33 (const MtxFx33 * m)
{
    ((void) 0) ;
    native_fn_main_0202e434(0x1a ,
                        (u32 *) m,
                        9 );
}
inline void * NNS_G3dGetResDataByIdx (const NNSG3dResDict * dict, u32 idx)
{
    NNSG3dResDictEntryHeader * hdr;
    ((void) 0) ;
    if (dict != ((void *)0) && idx < dict->numEntry) {
        ((void) 0) ;
        hdr = (NNSG3dResDictEntryHeader *)((u8 *)dict + dict->ofsEntry);
        return (void *)(&hdr->data[0] + hdr->sizeUnit * idx);
    } else {
        return ((void *)0) ;
    }
}
inline NNSG3dResMatData * NNS_G3dGetMatDataByIdx (const NNSG3dResMat * mat, u32 idx)
{
    NNSG3dResDictMatData * data;
    ((void) 0) ;
    if (mat) {
        data = (NNSG3dResDictMatData *)NNS_G3dGetResDataByIdx(&mat->dict, idx);
        if (data) {
            ((void) 0) ;
            return (NNSG3dResMatData *)((u8 *)mat + data->offset);
        }
    }
    return ((void *)0) ;
}
