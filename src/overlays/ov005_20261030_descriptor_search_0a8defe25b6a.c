typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;

typedef struct Request Request;
typedef struct Context Context;
typedef struct Entry Entry;

typedef struct {
    u8 unknown_0[8];
    u32 (*select)(Context *, Request *);
} Methods;

struct Entry {
    u32 unknown_0;
    u32 key;
    u32 unknown_8;
    Methods *methods;
    u8 unknown_10[0x20];
};

struct Context {
    u8 unknown_0[0x20];
    Entry *selected;
    Entry entries[16];
    u32 key;
};

struct Request {
    u8 unknown_0[0x44];
    u32 key;
};

u32 native_ov005_021d7480(Context *context, Request *request) {
    u32 key;
    Entry *selected;
    s32 index;
    Entry *entry;
    u32 high;
    u32 value;
    u32 generic;
    u32 result;

    key = request->key;
    result = 0;
    if (key == 0) {
        return result;
    }
    selected = 0;
    entry = context->entries;
    high = key & 0x80000000U;
    index = 0;
    do {
        value = entry->key;
        if (value == key) {
            selected = entry;
            break;
        }
        if (high != 0 && (value & 0x80000000U) != 0) {
            generic = value == 0x80000000U;
            if (key == 0x80400120U) {
                if (generic == 0) {
                    key = value;
                    selected = entry;
                    break;
                }
            } else if (generic != 0) {
                selected = entry;
                break;
            }
        }
        index++;
        entry++;
    } while (index < 16);
    if (selected != 0) {
        result = selected->methods->select(context, request);
        if (result != 0) {
            context->selected = selected;
            context->key = key;
        }
    }
    return result;
}
