typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u8 prefix[0x4c]; u16 first; u16 second; u16 third; } NativeCounters;
typedef struct { u8 prefix[0x1c]; int gold; } NativeMoney;
typedef struct { u32 marker; u32 total_length; u32 payload_length; u8 prefix[0x1c]; u32 header_word_28; u8 rest[0x5c]; u32 payload_sum; u32 header_sum; } NativeSaveBank;
typedef struct { u8 status; signed char heap; u16 reserved; int (*validator)(NativeSaveBank *); u8 *buffer; } NativeSaveIo;
extern u8 native_main[];
extern u8 native_numeric[];
extern u32 native_event[];
extern u32 native_secondary[];
extern NativeCounters native_counters;
extern u8 native_section2[];
extern u8 native_section3[];
extern u8 native_section4[];
extern u8 native_record_array[];
extern u32 native_minimums[];
extern NativeMoney native_money;
extern signed char native_inventory[];
extern u32 save_payload_checksum(const void *bank);
extern u32 save_header_checksum(const void *bank);
extern void native_copy(const void *source, void *destination, u32 bytes);
extern NativeSaveIo native_save_io;
extern void *native_allocate(int heap, u32 bytes, int alignment);
extern int native_save_read(u32 index, void *destination, u32 bytes);
extern int native_save_async_read(u32 index, void *destination, u32 bytes, int first, int second);
extern int native_save_poll(u8 *error);
extern void native_free(int heap, void *buffer);
u8 *save_main_pointer(void) { return native_main; }
u8 *save_record_pointer(int index) { return native_record_array + index * 0x24; }
u32 save_numeric_get(int index) { return native_numeric[index]; }
u32 save_numeric_set(int index, u32 value) {
    u32 previous = native_numeric[index];
    native_numeric[index] = value;
    return previous;
}
u32 save_event_get(int index) { return (native_event[index >> 5] >> (index & 31)) & 1; }
u32 save_event_set(int index, int value) {
    u32 previous = save_event_get(index);
    if (value) native_event[index >> 5] |= 1 << (index & 31);
    else native_event[index >> 5] &= ~(1 << (index & 31));
    return previous;
}
u32 save_secondary_get(int index) { return (native_secondary[index >> 5] >> (index & 31)) & 1; }
u32 save_secondary_history_get(int index) { return (native_secondary[(index + 64) >> 5] >> (index & 31)) & 1; }
u32 save_secondary_history_set(int index, int value) {
    u32 previous = save_secondary_history_get(index);
    if (value) native_secondary[(index + 64) >> 5] |= 1 << (index & 31);
    else native_secondary[(index + 64) >> 5] &= ~(1 << (index & 31));
    return previous;
}
u32 save_secondary_set(int index, int value) {
    u32 previous = save_secondary_get(index);
    if (value) native_secondary[index >> 5] |= 1 << (index & 31);
    else native_secondary[index >> 5] &= ~(1 << (index & 31));
    if (value && !previous) {
        save_secondary_history_set(index, value);
        if (value) save_event_set(76, 1);
    }
    return previous;
}
u32 save_counter_first_get(void) { return native_counters.first; }
void save_counter_first_increment(void) {
    native_counters.first++;
    if (native_counters.first > 9999) native_counters.first = 9999;
}
u32 save_counter_second_get(void) { return native_counters.second; }
void save_counter_second_increment(void) {
    native_counters.second++;
    if (native_counters.second > 9999) native_counters.second = 9999;
}
u32 save_counter_third_get(void) { return native_counters.third; }
void save_counter_third_increment(void) {
    native_counters.third++;
    if (native_counters.third > 9999) native_counters.third = 9999;
}
u8 *save_section2_pointer(void) { return native_section2; }
u8 *save_section3_pointer(void) { return native_section3; }
u8 *save_section4_pointer(void) { return native_section4; }
void save_minimum_set(int index, u32 value) {
    u32 previous = native_minimums[index];
    if (!previous) native_minimums[index] = value;
    else if (value < previous) native_minimums[index] = value;
}
int save_gold_get(void) { return native_money.gold; }
int save_gold_replace(int value) {
    int previous = native_money.gold;
    native_money.gold = value;
    return previous;
}
int save_gold_adjust(int delta) {
    int value = native_money.gold + delta;
    if (value < 0) value = 0;
    else if (value > 999999) value = 999999;
    native_money.gold = value;
    return value;
}
int save_gold_halve(void) {
    int value = native_money.gold >> 1;
    if (value < 0) value = 0;
    else if (value > 999999) value = 999999;
    native_money.gold = value;
    return value;
}
int save_inventory_get(int index) {
    if (index >= 255) return 0;
    return native_inventory[index];
}
int save_payload_valid(NativeSaveBank *bank) { return bank->payload_sum == save_payload_checksum(bank); }
int save_payload_header28_valid(NativeSaveBank *bank) {
    if (bank->header_word_28 < 0x8ca0) return bank->payload_sum == save_payload_checksum(bank);
    return 0;
}
void save_deserialize(u8 *bank) {
    u8 *main_state = save_main_pointer();
    u8 *section2 = save_section2_pointer();
    u8 *section3 = save_section3_pointer();
    u8 *section4 = save_section4_pointer();
    native_copy(bank + 0x90, main_state, 0x39d8);
    native_copy(bank + 0x3a68, section2, 0x34);
    native_copy(bank + 0x3a9c, section3, 0x22a4);
    native_copy(bank + 0x5d40, section4, 0x1390);
}
int save_bank_validate(NativeSaveBank *bank) {
    int valid = 0;
    if (bank->marker == 0x5a4953) {
        if (bank->total_length == 0x10000) {
            if (bank->payload_length == 0x70d0) {
                if (native_save_io.validator(bank)) {
                    int header_valid = bank->header_sum == save_header_checksum(bank);
                    if (header_valid) {
                        native_save_io.status = 0;
                        valid = 1;
                    } else native_save_io.status = 5;
                } else native_save_io.status = 6;
            } else native_save_io.status = 7;
        } else native_save_io.status = 4;
    } else native_save_io.status = 3;
    return valid;
}
int save_load_primary(int heap) {
    int valid = 0;
    u8 *bank = native_allocate(heap, 0x70d0, 4);
    if (bank) {
        if (native_save_read(0, bank, 0)) {
            if (save_bank_validate((NativeSaveBank *)bank)) {
                save_deserialize(bank);
                native_save_io.status = 0;
                valid = 1;
            }
        } else native_save_io.status = 2;
        native_free(heap, bank);
    }
    return valid;
}
int save_load_async(int index, int heap) {
    int valid = 0;
    u8 *bank = native_allocate(heap, 0x70d0, 4);
    native_save_io.buffer = bank;
    if (bank) {
        native_save_io.heap = heap;
        if (native_save_async_read(index, bank, 0, 0, 0)) {
            native_save_io.status = 0;
            valid = 1;
        } else {
            native_free(heap, native_save_io.buffer);
            native_save_io.buffer = 0;
            native_save_io.status = 2;
        }
    } else native_save_io.status = 8;
    return valid;
}
int save_load_primary_async(int heap) { return save_load_async(0, heap); }
int save_load_backup_async(int heap) { return save_load_async(1, heap); }
int save_load_async_poll(void) {
    int done = 0;
    u8 error;
    native_save_io.status = 0;
    if (native_save_poll(&error)) {
        if (!error) {
            if (native_save_io.buffer) {
                if (save_bank_validate((NativeSaveBank *)native_save_io.buffer)) {
                    save_deserialize(native_save_io.buffer);
                    native_save_io.status = 0;
                }
                native_free(native_save_io.heap, native_save_io.buffer);
                native_save_io.buffer = 0;
            } else if (!native_save_io.status) native_save_io.status = 8;
        } else native_save_io.status = 2;
        done = 1;
    }
    return done;
}
