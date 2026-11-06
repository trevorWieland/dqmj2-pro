typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
typedef struct {
    s32 feedback;
    s32 first;
    s32 second;
    u8 table[256];
} State;

void native_ov004_021d89e4(State *state, const u8 *key, u32 length) {
    u8 first_value;
    u8 second_value;
    s32 position;
    u8 accumulator;
    u32 key_position;
    u32 *destination;
    u32 *limit;
    u32 pattern;
    u32 increment;
    key_position = 0;
    accumulator = 0;
    state->feedback = 0xAA;
    state->first = 0;
    state->second = 0;
    destination = (u32 *)state->table;
    limit = (u32 *)(state->table + 256);
    pattern = 0x03020100;
    increment = 0x04040404;
    do {
        *destination++ = pattern;
        pattern += increment;
    } while (destination < limit);
    for (position = 255; position >= 0; position--) {
        first_value = state->table[position];
        accumulator = accumulator + key[key_position] + first_value;
        second_value = state->table[accumulator];
        state->table[accumulator] = first_value;
        state->table[position] = second_value;
        key_position++;
        if (key_position >= length) {
            key_position = 0;
        }
    }
}
