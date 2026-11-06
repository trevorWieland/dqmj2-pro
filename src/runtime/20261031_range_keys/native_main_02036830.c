#include "native_range_types.h"
u32 native_main_02036830(const Node *node, u32 key) {
    u32 result = 65535;
    switch (node->format) {
    case 0:
        result = (u16)((key - node->first) + node->words[0]);
        break;
    case 1:
        result = node->words[key - node->first];
        break;
    case 2: {
        const u8 *low = (const u8 *)node + 14;
        const u8 *high = low + ((s32)node->words[0] - 1) * 4;
        while (low <= high) {
            s32 offset = (high - low) / 4;
            const u8 *middle = low + (offset / 2) * 4;
            u16 value = *(const u16 *)middle;
            if (value < key) low = middle + 4;
            else if (key < value) high = middle - 4;
            else {
                result = *(const u16 *)(middle + 2);
                break;
            }
        }
        break;
    }
    }
    return result;
}
