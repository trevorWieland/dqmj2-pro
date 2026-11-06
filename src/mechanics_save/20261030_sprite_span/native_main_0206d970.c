#include "../20261030_sprite_constructor/sprite_constructor_context_types_20261030.h"
void native_main_0206d970(s32 sprite, s32 *begin, s32 *end) {
    *begin = native_data_021c4af4.slots[sprite].first;
    *end = native_data_021c4af4.slots[sprite].first + native_data_021c4af4.slots[sprite].children;
    if (*begin >= 12) {
        *begin -= 3;
        *end -= 3;
    }
}
