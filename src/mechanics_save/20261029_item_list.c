typedef signed short s16;
typedef signed int s32;
typedef unsigned char u8;
typedef unsigned short u16;
extern void native_fn_02008c58(s32, void *, s32);
extern s32 native_fn_02063144(s32);
extern u8 *native_fn_02065d88(s32);
extern s32 native_fn_02065db0(s32);
extern void native_fn_02076508(s16);
extern s32 native_fn_ov000_022178cc(s32);
__declspec(align(4)) extern u8 native_data_021c5a24[];
__declspec(align(4)) extern s32 native_data_021c5df8[];

void native_main_02076530(s32 mode)
{
    s16 item;
    s16 group;
    native_fn_02008c58(0, native_data_021c5df8, 1024);
    group = 0;
    native_data_021c5a24[0x7D4] = 0;
    switch (mode) {
    case 0: {
        do {
            item = 0;
            do {
                if (group == native_fn_02065db0(item)
                    && native_fn_ov000_022178cc(item) != 0
                    && native_fn_02063144(item) != 0) {
                    native_fn_02076508(item);
                }
                item++;
            } while (item < 255);
            group++;
        } while (group < 255);
        break;
    }
    case 1: {
        s32 sorted[256] = {0};
        {
            s16 candidate;
            candidate = 0;
            do {
                u8 category = native_fn_02065d88(candidate)[0x24];
                if ((category == 0 || category == 1)
                    && native_fn_ov000_022178cc(candidate) != 0
                    && native_fn_02063144(candidate) != 0) {
                    sorted[*(u16 *)(native_fn_02065d88(candidate) + 12)] = candidate;
                }
                candidate++;
            } while (candidate < 255);
        }
        {
            s16 rank;
            rank = 0;
            do {
                if (sorted[rank] != 0) {
                    native_fn_02076508((s16)sorted[rank]);
                }
                rank++;
            } while (rank < 255);
        }
        break;
    }
    }
}
