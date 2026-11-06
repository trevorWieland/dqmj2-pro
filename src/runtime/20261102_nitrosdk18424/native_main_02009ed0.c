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
void native_main_02009ed0(struct SNDBankData * bank, int index, struct SNDWaveArc * waveArc);
void native_fn_020072ec(const void * startAddr, u32 nBytes);
void native_fn_020094ec(void);
void native_fn_02009500(void);
void native_main_02009ed0 (SNDBankData * bank, int index, SNDWaveArc * waveArc)
{
    SNDWaveArcLink * next;
    SNDWaveArcLink * prev;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    native_fn_020094ec();
    if (bank->waveArcLink[index].waveArc != ((void *)0) ) {
        if (waveArc == bank->waveArcLink[index].waveArc) {
            native_fn_02009500();
            return;
        }
        if (&bank->waveArcLink[index] == bank->waveArcLink[index].waveArc->topLink) {
            bank->waveArcLink[index].waveArc->topLink = bank->waveArcLink[index].next;
            native_fn_020072ec(bank->waveArcLink[index].waveArc, sizeof(SNDWaveArc));
        } else {
            prev = bank->waveArcLink[index].waveArc->topLink;
            while (prev != ((void *)0) ) {
                if (&bank->waveArcLink[index] == prev->next)
                    break;
                prev = prev->next;
            }
            ((void) 0) ;
            prev->next = bank->waveArcLink[index].next;
            native_fn_020072ec(prev, sizeof(SNDWaveArcLink));
        }
    }
    next = waveArc->topLink;
    waveArc->topLink = &bank->waveArcLink[index];
    bank->waveArcLink[index].next = next;
    bank->waveArcLink[index].waveArc = waveArc;
    native_fn_02009500();
    native_fn_020072ec(bank, sizeof(SNDBankData));
    native_fn_020072ec(waveArc, sizeof(SNDWaveArc));
}
