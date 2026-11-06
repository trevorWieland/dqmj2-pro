typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
_Static_assert(sizeof(void *) == 4, "Four-byte pointer ABI required");
_Static_assert(sizeof(u32) == 4, "Four-byte words required");
__declspec(dllimport) void __stdcall ExitProcess(u32 code);
__declspec(dllimport) void *__stdcall GetStdHandle(u32 handle);
__declspec(dllimport) s32 __stdcall ReadFile(void *handle, void *data, u32 bytes, u32 *read, void *overlapped);
__declspec(dllimport) s32 __stdcall WriteFile(void *handle, const void *data, u32 bytes, u32 *written, void *overlapped);
__declspec(dllimport) void *__stdcall VirtualAlloc(void *address, u32 bytes, u32 kind, u32 protection);
extern u32 native_main_0203b660(void *, s32, s32, u32, u32, u32, s32, s32);

typedef struct {
    u32 kind;
    u32 count;
    u32 transient;
    u32 arguments[10];
} Service;

static Service expected_services[16];
static u32 arguments[8];
static u32 expected_helpers[6];
static u32 helpers[6];
static u32 service_count;
static u32 services_seen;
static u32 irq_mask;
static u32 helper_bad;
static u8 scratch[256];
static void *input;
static u32 receipt[8] = {0x4A324E44u, 4, 0, 0, 0, 0, 0, 2166136261u};

static void finish(u32 code) {
    u32 written;
    WriteFile(GetStdHandle((u32)-11), receipt, sizeof(receipt), &written, (void *)0);
    ExitProcess(code);
}

static void read_exact(void *destination, u32 bytes) {
    u8 *target = destination;
    u32 received;
    while (bytes) {
        if (!ReadFile(input, target, bytes, &received, (void *)0) || !received || received > bytes) {
            finish(43);
        }
        target += received;
        bytes -= received;
    }
}

static u32 check_page(const u8 *actual, u32 bytes) {
    u32 offset = 0;
    u32 equal = 1;
    u32 count;
    u32 i;
    while (offset < bytes) {
        count = bytes - offset;
        if (count > sizeof(scratch)) {
            count = sizeof(scratch);
        }
        read_exact(scratch, count);
        for (i = 0; i < count; ++i) {
            equal &= scratch[i] == actual[offset + i];
            receipt[7] = (receipt[7] ^ actual[offset + i]) * 16777619u;
        }
        offset += count;
    }
    return equal;
}

static void observe(u32 kind, const u32 *values, u32 count, u32 transient) {
    u32 i;
    Service *expected;
    ++receipt[5];
    if (services_seen >= service_count) {
        helper_bad = 1;
        return;
    }
    expected = &expected_services[services_seen++];
    helper_bad |= expected->kind != kind || expected->count != count || expected->transient != transient;
    for (i = 0; i < count; ++i) {
        helper_bad |= values[i] != expected->arguments[i];
    }
}

u32 native_fn_02026350(u32 first, u32 second) {
    ++helpers[0];
    return second ? first / second : first;
}

u32 native_fn_02038970(void) {
    u32 *pool = (u32 *)0x020F4C3Cu;
    u32 bit;
    ++helpers[1];
    for (bit = 0; bit < 8; ++bit) {
        if (!(*pool & (1u << bit))) {
            *pool |= 1u << bit;
            return bit;
        }
    }
    return 0xFFFFFFFFu;
}

static void empty_list(u8 *view, u8 *node) {
    u32 offset = *(u16 *)(view + 10);
    ++helpers[3];
    *(u32 *)(node + offset + 4) = 0;
    *(u32 *)(node + offset) = 0;
    *(u32 *)view = (u32)node;
    *(u32 *)(view + 4) = (u32)node;
    *(u16 *)(view + 8) += 1;
}

void native_fn_0202ba20(u8 *view, void *value) {
    u8 *node = value;
    u32 offset = *(u16 *)(view + 10);
    u8 *tail = (u8 *)*(u32 *)(view + 4);
    ++helpers[2];
    if (!*(u32 *)view) {
        empty_list(view, node);
        return;
    }
    *(u32 *)(node + offset) = (u32)tail;
    *(u32 *)(node + offset + 4) = 0;
    *(u32 *)(tail + offset + 4) = (u32)node;
    *(u32 *)(view + 4) = (u32)node;
    *(u16 *)(view + 8) += 1;
}

u32 native_fn_02007ff4(void) {
    u32 previous = irq_mask;
    ++helpers[4];
    irq_mask = 128;
    return previous;
}

void native_fn_02008008(u32 mask) {
    ++helpers[5];
    irq_mask = mask;
}

void native_fn_0203b854(void *context, s32 flag) {
    u32 values[2] = {(u32)context, (u32)flag};
    observe(0, values, 2, 0xFFFFFFFFu);
}

void native_fn_0200932c(u32 channel, u32 mode, u32 address, u32 repeat, u32 offset,
                       u32 words, u32 volume, u32 zero, u32 scale, u32 pan) {
    u32 values[10] = {channel, mode, address, repeat, offset, words, volume, zero, scale, pan};
    observe(1, values, 10, 0xFFFFFFFFu);
}

void native_fn_02009264(u32 slot, u32 first, u32 second, void (*callback)(void *), void *context) {
    u32 values[5] = {slot, first, second, (u32)callback, (u32)context};
    observe(2, values, 5, 0xFFFFFFFFu);
}

void native_fn_0203b9c0(void *context, u32 zero) {
    u32 values[2] = {(u32)context, zero};
    helper_bad |= irq_mask != 128;
    observe(3, values, 2, *(u32 *)((u8 *)context + 0x2C));
}

void j2p_entry(void) {
    u32 header[2];
    u32 index;
    u32 i;
    u32 expected_result;
    u32 initial_irq;
    u32 result;
    u32 equal;
    input = GetStdHandle((u32)-10);
    read_exact(header, sizeof(header));
    if (header[0] != 0x4A324E56u || !header[1] || header[1] > 1024) {
        finish(44);
    }
    receipt[2] = header[1];
    if (VirtualAlloc((void *)0x02380000u, 4096, 0x3000, 4) != (void *)0x02380000u ||
        VirtualAlloc((void *)0x020F0000u, 65536, 0x3000, 4) != (void *)0x020F0000u) {
        finish(45);
    }
    for (index = 0; index < header[1]; ++index) {
        read_exact(arguments, sizeof(arguments));
        read_exact(&initial_irq, 4);
        read_exact(&expected_result, 4);
        read_exact(expected_helpers, 6 * 4);
        read_exact(&service_count, 4);
        if (service_count > 16 || arguments[0] != 0x02380000u) {
            finish(46);
        }
        read_exact(expected_services, service_count * sizeof(Service));
        read_exact((void *)0x02380000u, 4096);
        read_exact((void *)0x020F4000u, 8192);
        services_seen = helper_bad = 0;
        irq_mask = initial_irq;
        for (i = 0; i < 6; ++i) {
            helpers[i] = 0;
        }
        result = native_main_0203b660((void *)arguments[0], (s32)arguments[1], (s32)arguments[2],
                                     arguments[3], arguments[4], arguments[5], (s32)arguments[6], (s32)arguments[7]);
        ++receipt[3];
        equal = result == expected_result && irq_mask == initial_irq && !helper_bad && services_seen == service_count;
        for (i = 0; i < 6; ++i) {
            receipt[4] += helpers[i];
            equal &= helpers[i] == expected_helpers[i];
        }
        equal &= check_page((const u8 *)0x02380000u, 4096);
        equal &= check_page((const u8 *)0x020F4000u, 8192);
        for (i = 0; i < 4; ++i) {
            receipt[7] = (receipt[7] ^ (result >> (i * 8) & 255)) * 16777619u;
        }
        if (!equal) {
            receipt[6] = index + 1;
            finish(42);
        }
    }
    finish(0);
}
