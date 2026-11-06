typedef unsigned int u32;
typedef signed int s32;

extern s32 data_ov007_021da0f4[];
extern s32 func_ov007_021d864c(u32);
extern s32 func_ov007_021d8634(u32);
extern u32 func_ov007_021d873c(u32);
extern s32 func_ov007_021d7e1c(u32);

s32 native_ov007_021d7e1c(u32 direction) {
    s32 best = 0x7FFFFFFF;
    s32 selected = -1;
    s32 sum = data_ov007_021da0f4[1] + data_ov007_021da0f4[0];
    s32 difference = data_ov007_021da0f4[1] - data_ov007_021da0f4[0];
    s32 firstSign;
    s32 secondSign;
    s32 index;
    s32 value;
    s32 vertical;
    s32 horizontal;
    switch (direction) {
        case 1:
            firstSign = -1;
            secondSign = firstSign;
            break;
        case 2:
            firstSign = 1;
            secondSign = firstSign;
            break;
        case 3:
            firstSign = -1;
            secondSign = 1;
            break;
        case 4:
            secondSign = -1;
            firstSign = 1;
            break;
    }
    for (index = 0; index < 16; index++) {
        value = func_ov007_021d864c(index);
        if ((value + func_ov007_021d8634(index) - sum) * firstSign >= 0) {
            value = func_ov007_021d864c(index);
            if ((value - func_ov007_021d8634(index) - difference) * secondSign >= 0) {
                if (func_ov007_021d873c(index)) {
                    if (func_ov007_021d864c(index) - data_ov007_021da0f4[1] >= 0) {
                        vertical = func_ov007_021d864c(index) - data_ov007_021da0f4[1];
                    } else {
                        vertical = -(func_ov007_021d864c(index) - data_ov007_021da0f4[1]);
                    }
                    if (func_ov007_021d8634(index) - data_ov007_021da0f4[0] >= 0) {
                        horizontal = func_ov007_021d8634(index) - data_ov007_021da0f4[0];
                    } else {
                        horizontal = -(func_ov007_021d8634(index) - data_ov007_021da0f4[0]);
                    }
                    value = horizontal + vertical;
                    if (value < best && index != data_ov007_021da0f4[2]) {
                        best = value;
                        selected = index;
                    }
                }
            }
        }
    }
    if (selected == -1 && data_ov007_021da0f4[1] >= 0 && data_ov007_021da0f4[1] < 192 && data_ov007_021da0f4[0] >= 0 && data_ov007_021da0f4[0] < 256) {
        best = data_ov007_021da0f4[2];
        data_ov007_021da0f4[2] = -1;
        switch (direction) {
            case 1:
                data_ov007_021da0f4[1] += 192;
                selected = func_ov007_021d7e1c(1);
                data_ov007_021da0f4[1] -= 192;
                break;
            case 2:
                data_ov007_021da0f4[1] -= 192;
                selected = func_ov007_021d7e1c(2);
                data_ov007_021da0f4[1] += 192;
                break;
            case 3:
                data_ov007_021da0f4[0] += 256;
                selected = func_ov007_021d7e1c(3);
                data_ov007_021da0f4[0] -= 256;
                break;
            case 4:
                data_ov007_021da0f4[0] -= 256;
                selected = func_ov007_021d7e1c(4);
                data_ov007_021da0f4[0] += 256;
                break;
        }
        data_ov007_021da0f4[2] = best;
    }
    return selected;
}
