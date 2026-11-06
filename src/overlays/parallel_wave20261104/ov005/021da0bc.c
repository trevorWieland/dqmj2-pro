typedef unsigned int u32;
typedef unsigned short u16;
typedef struct Inner {
    u32 first;
    unsigned char pad[0x41c];
    u32 count;
    u32 chunks;
    void *buffer;
    unsigned char scratch[0x158];
} Inner;
typedef struct Methods {
    unsigned char pad[0x24];
    Inner *inner;
} Methods;
typedef struct Interface {
    unsigned char pad[12];
    Methods *methods;
} Interface;
typedef struct Object {
    void *buffer;
    u32 count;
    u32 reserved;
    u16 checksum;
    u16 pad;
    void *other;
    u32 otherSize;
    u32 length;
    u32 reserved2;
    Interface *interface;
} Object;
extern void native_fn_ov005_021d9910(Inner *);
extern u16 native_fn_02019bd4(const void *, u32);
extern void native_fn_02008c14(u32, void *, u32);
int native_ov005_021da0bc(Object *object, void *buffer, u32 count, void *other, u32 length)
{
    Inner *inner = object->interface->methods->inner;
    native_fn_ov005_021d9910(inner);
    object->buffer = buffer;
    object->count = (u16)count;
    object->checksum = native_fn_02019bd4(buffer, count);
    object->other = other;
    object->length = (u16)length;
    native_fn_02008c14(0, inner->scratch, sizeof(inner->scratch));
    inner->chunks = length / 508 + (length % 508 != 0);
    inner->count = count;
    inner->buffer = buffer;
    inner->first = (u32)other;
    return 1;
}
