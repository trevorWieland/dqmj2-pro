typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
typedef struct {
    s32 feedback;
    s32 first;
    s32 second;
    u8 table[256];
} State;
extern u32 func_ov004_021d7de8(u32 instruction);
extern u8 func_ov004_021d8a70(State *state);
extern u32 func_ov004_021d8ac8(u8 *table);
static inline void encrypt_byte(State *state, u8 *input, u8 *output) {
    s32 encoded;
    encoded = func_ov004_021d8a70(state) ^ *input;
    state->feedback = encoded;
    *output = encoded;
}
static inline void decrypt_byte(State *state, u8 *input, u8 *output) {
    s32 encoded;
    s32 decoded;
    decoded = func_ov004_021d8a70(state) ^ *input;
    state->feedback = *input;
    *output = decoded;
}
u32 native_ov004_021d8b00(State *state, void *input, void *output, u32 length) {
    u8 mapping[256];
    u32 offset;
    u32 instruction;
    u32 source;
    u8 *destination;
    u32 current;
    if (length & 3) {
        return -1;
    }
    source = (u32)input;
    destination = (u8 *)output;
    func_ov004_021d8ac8(mapping);
    for (offset = 0; offset < length; offset += 4) {
        current = (u32)(source + offset);
        instruction = *(u32 *)current;
        switch (func_ov004_021d7de8(instruction)) {
        case 1:
        case 2: {
            u32 high;
            u32 low;
            u32 *from = (u32 *)((u8 *)current);
            u32 *to = (u32 *)(destination + offset);
            *to = *from;
            high = (*to & 0xFF000000) ^ 0x01000000;
            low = ((*to & 0x00FFFFFF) + 0x402) & 0x00FFFFFF;
            state->feedback += high >> 24;
            *to = high | low;
            break;
        }
        case 3:
            *(u32 *)((u8 *)current) ^= 0x01000000;
        default:
            encrypt_byte(state, (u8 *)current, destination + offset);
            encrypt_byte(state, (u8 *)current + 1, destination + offset + 1);
            destination[offset + 2] = mapping[((u8 *)current)[2]];
            destination[offset + 3] = ((u8 *)current)[3];
            state->feedback = state->feedback * destination[offset + 2] - destination[offset + 3];
            break;
        }
    }
    return 0;
}
