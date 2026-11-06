typedef unsigned int u32;
typedef unsigned char u8;

u32 native_ov004_021d8340(u8 *input, int length) {
    u32 crc = ~0U;
    if (length--) {
        do {
            u32 value = crc ^ *input++;
            if (value & 1) {
                crc = value >> 1;
            } else {
                crc = 0xEDB88320U ^ (value >> 1);
            }
            if (crc & 1) {
                crc >>= 1;
            } else {
                crc = 0xEDB88320U ^ (crc >> 1);
            }
            if (crc & 1) {
                crc >>= 1;
            } else {
                crc = 0xEDB88320U ^ (crc >> 1);
            }
            if (crc & 1) {
                crc >>= 1;
            } else {
                crc = 0xEDB88320U ^ (crc >> 1);
            }
            if (crc & 1) {
                crc >>= 1;
            } else {
                crc = 0xEDB88320U ^ (crc >> 1);
            }
            if (crc & 1) {
                crc >>= 1;
            } else {
                crc = 0xEDB88320U ^ (crc >> 1);
            }
            if (crc & 1) {
                crc >>= 1;
            } else {
                crc = 0xEDB88320U ^ (crc >> 1);
            }
            if (crc & 1) {
                crc >>= 1;
            } else {
                crc = 0xEDB88320U ^ (crc >> 1);
            }
        } while (length--);
    }
    return ~crc;
}
