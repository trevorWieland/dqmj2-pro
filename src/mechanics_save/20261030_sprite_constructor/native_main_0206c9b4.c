#include "sprite_constructor_context_types_20261030.h"
s32 native_main_0206c9b4(s32 species, u32 form, u32 kind, u32 resource, s8 mode) {
    s32 firstChild;
    s32 index = native_data_021c4af4.counters.slots;
    native_data_021c4af4.slots[index].children = 1;
    native_data_021c4af4.slots[index].resource = resource + native_data_021c4af4.counters.tiles * 32;
    native_data_021c4af4.slots[index].kind = kind;
    firstChild = native_data_021c4af4.counters.children;
    native_data_021c4af4.slots[index].first = firstChild;
    native_data_021c4af4.slots[index].marker = -1;
    native_data_021c4af4.slots[index].species = species;
    native_data_021c4af4.slots[index].form = form;
    native_fn_0206d2e0(index, species, kind, native_data_021c4af4.slots[index].resource,
        firstChild * 32, mode, 1);
    native_data_021c4af4.counters.tiles = (s16)(native_data_021c4af4.counters.tiles + 25);
    native_data_021c4af4.counters.slots = (s8)(native_data_021c4af4.counters.slots + 1);
    native_data_021c4af4.counters.children = (s8)(native_data_021c4af4.counters.children + 1);
    return (s8)(native_data_021c4af4.counters.slots - 1);
}
