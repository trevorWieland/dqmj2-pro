typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
void saved_crc8_table(u8 *table, u32 polynomial) {
    u32 value;
    u32 index = 0;
    u32 bit;
    do {
        value = index;
        bit = 0;
        do {
            if (value & 128) value = (value << 1) ^ polynomial;
            else value <<= 1;
            bit++;
        } while (bit < 8);
        table[index] = (u8)value;
        index++;
    } while (index < 256);
}
void saved_crc8_update(const u8 *table, u8 *state, const u8 *input, u32 length) {
    u32 value = *state;
    u32 index = 0;
    if (index < length) do { value = table[((value ^ *input++) << 24) >> 24]; index++; } while (index < length);
    *state = (u8)value;
}
void saved_crc16_table(u16 *table, u32 polynomial) {
    u32 value;
    u32 index = 0;
    u32 bit;
    do {
        value = index;
        bit = 0;
        do {
            if (value & 1) value = (value >> 1) ^ polynomial;
            else value >>= 1;
            bit++;
        } while (bit < 8);
        table[index] = (u16)value;
        index++;
    } while (index < 256);
}
void saved_crc16_update(const u16 *table, u16 *state, const u8 *input, u32 length) {
    u32 value = *state;
    u32 index = 0;
    if (index < length) do { value = (value >> 8) ^ table[((value ^ *input++) << 24) >> 24]; index++; } while (index < length);
    *state = (u16)value;
}
void saved_crc32_table(u32 *table, u32 polynomial) {
    u32 value;
    u32 index = 0;
    u32 bit;
    do {
        value = index;
        bit = 0;
        do {
            if (value & 1) value = (value >> 1) ^ polynomial;
            else value >>= 1;
            bit++;
        } while (bit < 8);
        table[index] = value;
        index++;
    } while (index < 256);
}
void saved_crc32_update(const u32 *table, u32 *state, const u8 *input, u32 length) {
    u32 value = *state;
    u32 index = 0;
    if (index < length) do { value = (value >> 8) ^ table[((value ^ *input++) << 24) >> 24]; index++; } while (index < length);
    *state = value;
}
