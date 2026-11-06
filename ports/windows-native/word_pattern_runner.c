typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
_Static_assert(sizeof(void *) == 4, "The original record layout requires four-byte pointers");
_Static_assert(sizeof(u32) == 4, "Word width differs");

typedef struct {
    s32 count;
    u32 mode;
    u32 use_default;
    u32 result;
    u8 before[512];
    u8 after[512];
    u8 flag_before[16];
    u8 flag_after[16];
} PatternCase;

#include "word_pattern_vectors.h"

__declspec(dllimport) void __stdcall ExitProcess(u32 code);
__declspec(dllimport) void *__stdcall GetStdHandle(u32 handle);
__declspec(dllimport) s32 __stdcall WriteFile(void *handle, const void *data, u32 bytes,
                                           u32 *written, void *overlapped);
extern u32 native_main_0203c5b8(u8 *record);

_Alignas(4) u8 native_data_020f5bf0[16];
_Alignas(4) u8 native_data_020f5c00[12];
static _Alignas(4) u8 explicit_record[12];
static _Alignas(4) u8 saved_explicit[12];
static _Alignas(4) u8 saved_default[12];
static u32 guarded_buffer[130];
static u32 helper_calls;
static u32 helper_bad;
static const PatternCase *current;

u32 native_fn_02008c58(u32 value, s32 *destination, u32 bytes) {
    u32 index;
    u8 *buffer = (u8 *)&guarded_buffer[1];
    ++helper_calls;
    if (current->count <= 0 || value != (current->mode ? 2u : 1u) ||
        destination != (s32 *)buffer + (current->mode ? 1 : 0) ||
        bytes != (u32)(current->count - 1) * 4u) {
        helper_bad = 1;
    }
    if ((u8 *)destination < buffer || (u8 *)destination + bytes > buffer + 512 || bytes % 4u) {
        helper_bad = 1;
        return value;
    }
    for (index = 0; index < bytes / 4u; ++index) {
        destination[index] = (s32)value;
    }
    return value;
}

static u32 copy_equal(u8 *destination, const u8 *source, u32 bytes, u32 copy) {
    u32 index;
    u32 equal = 1;
    for (index = 0; index < bytes; ++index) {
        if (copy) {
            destination[index] = source[index];
        } else if (destination[index] != source[index]) {
            equal = 0;
        }
    }
    return equal;
}

void j2p_entry(void) {
    u32 index;
    u32 word;
    u32 returned;
    u32 actual_returns = 0;
    u32 total_helpers = 0;
    u32 failed = 0;
    u32 digest = 2166136261u;
    u32 written = 0;
    u32 receipt[8];
    u8 *buffer = (u8 *)&guarded_buffer[1];
    u8 *selected;
    for (index = 0; index < PATTERN_CASE_COUNT; ++index) {
        current = &pattern_cases[index];
        helper_calls = helper_bad = 0;
        guarded_buffer[0] = 0x13579bdfu;
        guarded_buffer[129] = 0x2468ace0u;
        for (word = 0; word < 12; ++word) {
            explicit_record[word] = native_data_020f5c00[word] = 0x57;
        }
        selected = current->use_default ? native_data_020f5c00 : explicit_record;
        *(u32 *)selected = (u32)buffer;
        *(s32 *)(selected + 4) = current->count;
        selected[8] = (u8)current->mode;
        copy_equal(saved_explicit, explicit_record, 12, 1);
        copy_equal(saved_default, native_data_020f5c00, 12, 1);
        copy_equal(buffer, current->before, 512, 1);
        copy_equal(native_data_020f5bf0, current->flag_before, 16, 1);
        returned = native_main_0203c5b8(current->use_default ? (u8 *)0 : explicit_record);
        ++actual_returns;
        total_helpers += helper_calls;
        digest = (digest ^ returned) * 16777619u;
        if (returned != current->result || helper_bad ||
            helper_calls != (u32)(current->count > 0) ||
            !copy_equal(buffer, current->after, 512, 0) ||
            !copy_equal(native_data_020f5bf0, current->flag_after, 16, 0) ||
            !copy_equal(explicit_record, saved_explicit, 12, 0) ||
            !copy_equal(native_data_020f5c00, saved_default, 12, 0) ||
            guarded_buffer[0] != 0x13579bdfu || guarded_buffer[129] != 0x2468ace0u) {
            failed = index + 1;
            break;
        }
    }
    receipt[0] = 0x4a325057u;
    receipt[1] = sizeof(void *);
    receipt[2] = PATTERN_CASE_COUNT;
    receipt[3] = actual_returns;
    receipt[4] = total_helpers;
    receipt[5] = failed;
    receipt[6] = digest;
    receipt[7] = 0x16403210u;
    if (!WriteFile(GetStdHandle((u32)-11), receipt, sizeof(receipt), &written, (void *)0) ||
        written != sizeof(receipt)) {
        ExitProcess(90);
    }
    ExitProcess(failed ? 41 : 0);
}
