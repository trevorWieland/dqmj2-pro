typedef unsigned short int u16;
typedef unsigned int u32;
typedef struct NNSG2dUserExCellAttr {
    u32 * pAttr;
} NNSG2dUserExCellAttr;
typedef struct NNSG2dUserExCellAttrBank {
    u16 numCells;
    u16 numAttribute;
    NNSG2dUserExCellAttr * pCellAttrArray;
} NNSG2dUserExCellAttrBank;
void native_main_020344c8(signed int rawObject);
void native_main_020344c8 (signed int rawObject)
{
    NNSG2dUserExCellAttrBank *pCellAttrBank = (NNSG2dUserExCellAttrBank *)rawObject;
    u16 i;
    pCellAttrBank->pCellAttrArray = (void *)((u32)(pCellAttrBank->pCellAttrArray) + (u32) pCellAttrBank)
                                    ;
    for (i = 0; i < pCellAttrBank->numCells; i++) {
        pCellAttrBank->pCellAttrArray[i].pAttr = (void *)((u32)(pCellAttrBank->pCellAttrArray[i].pAttr) + (u32) pCellAttrBank)
                                        ;
    }
}
