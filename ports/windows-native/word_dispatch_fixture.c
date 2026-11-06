typedef unsigned char u8;
typedef unsigned int u32;

_Alignas(4) u8 native_data_020e335c[96];
_Alignas(4) u8 native_data_027e0000[88];

void j2p_word_setup(const u8 *shared, const u8 *table) {
    u32 index;
    for (index = 0; index < 88; ++index) {
        native_data_027e0000[index] = shared[index];
    }
    for (index = 0; index < 96; ++index) {
        native_data_020e335c[index] = table[index];
    }
}

u32 j2p_word_unchanged(const u8 *shared, const u8 *table) {
    u32 index;
    for (index = 0; index < 88; ++index) {
        if (native_data_027e0000[index] != shared[index]) {
            return 0;
        }
    }
    for (index = 0; index < 96; ++index) {
        if (native_data_020e335c[index] != table[index]) {
            return 0;
        }
    }
    return 1;
}
