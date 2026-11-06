typedef unsigned char u8;
typedef unsigned int u32;
extern struct { u32 *descriptor; } native_backup_backend;
extern void native_backend_fill(void *, u32, u32);
void save_backend_descriptor_select(u32 type) {
    u32 *descriptor = native_backup_backend.descriptor;
    u32 capacity;
    u32 category;
    u32 subtype;
    native_backend_fill((u8 *)descriptor + 0x18, 0, 0x48);
    descriptor[1] = type;
    descriptor[0x58 / 4] = 0x203f;
    if (!type) return;
    capacity = 1U << (((int)type >> 8) & 0xff);
    category = type & 0xff;
    subtype = ((int)type >> 16) & 0xff;
    descriptor[0x18 / 4] = capacity;
    ((u8 *)descriptor)[0x54] = 0xff;
    if (category == 1) {
        switch (capacity) {
        case 0x200:
            descriptor[0x24 / 4] = 0x10;
            descriptor[0x28 / 4] = 1;
            descriptor[0x2c / 4] = 5;
            ((u8 *)descriptor)[0x54] = 0xf0;
            break;
        case 0x2000:
            descriptor[0x24 / 4] = 0x20;
            descriptor[0x28 / 4] = 2;
            descriptor[0x2c / 4] = 5;
            ((u8 *)descriptor)[0x54] = 0;
            break;
        case 0x10000:
            descriptor[0x24 / 4] = 0x80;
            descriptor[0x28 / 4] = 2;
            descriptor[0x2c / 4] = 10;
            ((u8 *)descriptor)[0x54] = 0;
            break;
        case 0x20000:
            descriptor[0x24 / 4] = 0x100;
            descriptor[0x28 / 4] = 3;
            descriptor[0x2c / 4] = 5;
            ((u8 *)descriptor)[0x54] = 0;
            break;
        default:
            goto invalid;
        }
        descriptor[0x1c / 4] = descriptor[0x24 / 4];
        descriptor[0x58 / 4] |= 0x40;
        descriptor[0x58 / 4] |= 0x4300;
    } else if (category == 2) {
        switch (capacity) {
        case 0x40000:
        case 0x80000:
        case 0x100000:
            descriptor[0x30 / 4] = 25;
            descriptor[0x34 / 4] = 300;
            descriptor[0x50 / 4] = 300;
            descriptor[0x40 / 4] = 5000;
            descriptor[0x58 / 4] |= 0x480;
            break;
        case 0x200000:
            descriptor[0x30 / 4] = 23;
            descriptor[0x34 / 4] = 300;
            descriptor[0x40 / 4] = 500;
            descriptor[0x44 / 4] = 5000;
            descriptor[0x38 / 4] = 10000;
            descriptor[0x3c / 4] = 60000;
            ((u8 *)descriptor)[0x54] = 0;
            descriptor[0x58 / 4] |= 0x80;
            descriptor[0x58 / 4] |= 0x5400;
            break;
        case 0x400000:
            descriptor[0x40 / 4] = 600;
            descriptor[0x44 / 4] = descriptor[0x40 / 4] + 2400;
            descriptor[0x48 / 4] = 70;
            descriptor[0x4c / 4] = 150;
            descriptor[0x38 / 4] = 23000;
            descriptor[0x3c / 4] = 800000;
            ((u8 *)descriptor)[0x54] = 0;
            descriptor[0x20 / 4] = 0x1000;
            descriptor[0x58 / 4] |= 0xd000;
            break;
        case 0x800000:
            if (subtype == 0) {
                descriptor[0x40 / 4] = 1000;
                descriptor[0x44 / 4] = descriptor[0x40 / 4] + 2000;
                descriptor[0x38 / 4] = 68000;
                descriptor[0x3c / 4] = 160000;
                ((u8 *)descriptor)[0x54] = 0;
                descriptor[0x58 / 4] |= 0x5000;
            } else if (subtype == 1) {
                descriptor[0x40 / 4] = 1000;
                descriptor[0x44 / 4] = descriptor[0x40 / 4] + 2000;
                descriptor[0x38 / 4] = 68000;
                descriptor[0x3c / 4] = 160000;
                ((u8 *)descriptor)[0x54] = 0x84;
                descriptor[0x58 / 4] |= 0x5000;
            }
            break;
        default:
            goto invalid;
        }
        descriptor[0x1c / 4] = 0x10000;
        descriptor[0x24 / 4] = 0x100;
        descriptor[0x28 / 4] = 3;
        descriptor[0x2c / 4] = 5;
        descriptor[0x58 / 4] |= 0xb40;
    } else if (category == 3) {
        if (capacity != 0x2000 && capacity != 0x8000) goto invalid;
        descriptor[0x24 / 4] = capacity;
        descriptor[0x1c / 4] = capacity;
        descriptor[0x28 / 4] = 2;
        ((u8 *)descriptor)[0x54] = 0;
        descriptor[0x58 / 4] |= 0x40;
        descriptor[0x58 / 4] |= 0x4300;
    } else {
invalid:
        descriptor[1] = 0;
        descriptor[0x18 / 4] = descriptor[1];
        native_backup_backend.descriptor[0] = 3;
    }
}
