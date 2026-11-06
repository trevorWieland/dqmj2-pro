typedef unsigned short int u16;
typedef unsigned long u32;
typedef struct SNDBinaryFileHeader {
	char signature[4];
	u16 byteOrder;
	u16 version;
	u32 fileSize;
	u16 headerSize;
	u16 dataBlocks;
} SNDBinaryFileHeader;
typedef struct SNDBinaryBlockHeader {
	u32 kind;
	u32 size;
} SNDBinaryBlockHeader;
struct SNDWaveArc;
typedef struct SNDWaveArcLink {
	struct SNDWaveArc * waveArc;
	struct SNDWaveArcLink * next;
} SNDWaveArcLink;
typedef struct SNDWaveArc {
	struct SNDBinaryFileHeader fileHeader;
	struct SNDBinaryBlockHeader blockHeader;
	struct SNDWaveArcLink * topLink;
	u32 reserved[7];
	u32 waveCount;
	u32 waveOffset[0];
} SNDWaveArc;
typedef struct SNDBankData {
	struct SNDBinaryFileHeader fileHeader;
	struct SNDBinaryBlockHeader blockHeader;
	struct SNDWaveArcLink waveArcLink[4 ];
	u32 instCount;
	u32 instOffset[0];
} SNDBankData;
void native_main_02009f9c(struct SNDBankData * bank);
void native_fn_020072ec(const void * startAddr, u32 nBytes);
void native_fn_020094ec(void);
void native_fn_02009500(void);
void native_main_02009f9c (SNDBankData * bank)
{
    SNDWaveArc * waveArc;
    SNDWaveArcLink * prev;
    int i;
    ((void) 0) ;
    ((void) 0) ;
    native_fn_020094ec();
    for (i = 0; i < 4 ; i++) {
        waveArc = bank->waveArcLink[i].waveArc;
        if (waveArc == ((void *)0) )
            continue;
        if (&bank->waveArcLink[i] == waveArc->topLink) {
            waveArc->topLink = bank->waveArcLink[i].next;
            native_fn_020072ec(waveArc, sizeof(SNDWaveArc));
        } else {
            prev = waveArc->topLink;
            while (prev != ((void *)0) ) {
                if (&bank->waveArcLink[i] == prev->next)
                    break;
                prev = prev->next;
            }
            ((void) 0) ;
            prev->next = bank->waveArcLink[i].next;
            native_fn_020072ec(prev, sizeof(SNDWaveArcLink));
        }
    }
    native_fn_02009500();
}
