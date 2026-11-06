typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
typedef struct {
    u32 enabled;
    u32 unknown4;
    u32 unknown8;
    u32 allocations;
    u32 heap;
} HeapSlot;

s8 native_data_020dd580[1];
HeapSlot native_data_020edd64[16];
u8 native_data_020edd54[3];
u32 allocation_contract_result;
u32 allocation_contract_calls;
u32 allocation_contract_address;
u32 allocation_contract_words[3];

static u32 supplied(u32 address, u32 heap, u32 bytes, s32 alignment) {
    allocation_contract_calls++;
    allocation_contract_address = address;
    allocation_contract_words[0] = heap;
    allocation_contract_words[1] = bytes;
    allocation_contract_words[2] = (u32)alignment;
    return allocation_contract_result;
}

u32 native_fn_0202b044(u32 heap, u32 bytes, s32 alignment) {
    return supplied(0x0202b044, heap, bytes, alignment);
}

u32 native_fn_0202b0f8(u32 heap, u32 bytes, s32 alignment) {
    return supplied(0x0202b0f8, heap, bytes, alignment);
}
