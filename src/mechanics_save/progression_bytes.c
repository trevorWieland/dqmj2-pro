typedef unsigned char u8;
typedef struct { u8 bytes[100]; } NativeKind;
extern struct { void *file; NativeKind *records; } native_kind_state;
extern int native_level_bucket(int);
u8 saved_progression_byte47(int species, int previous, int level) {
    int bucket = native_level_bucket(level);
    int value;
    bucket--;
    value = (native_kind_state.records[species].bytes + bucket)[0x47];
    value += previous;
    value -= previous;
    return value;
}
u8 saved_progression_byte4b(int species, int previous, int level) {
    int bucket = native_level_bucket(level);
    int value;
    bucket--;
    value = (native_kind_state.records[species].bytes + bucket)[0x4b];
    value += previous;
    value -= previous;
    return value;
}
u8 saved_progression_byte4f(int species, int previous, int level) {
    int bucket = native_level_bucket(level);
    int value;
    bucket--;
    value = (native_kind_state.records[species].bytes + bucket)[0x4f];
    value += previous;
    value -= previous;
    return value;
}
u8 saved_progression_byte53(int species, int previous, int level) {
    int bucket = native_level_bucket(level);
    int value;
    bucket--;
    value = (native_kind_state.records[species].bytes + bucket)[0x53];
    value += previous;
    value -= previous;
    return value;
}
u8 saved_progression_byte57(int species, int previous, int level) {
    int bucket = native_level_bucket(level);
    int value;
    bucket--;
    value = (native_kind_state.records[species].bytes + bucket)[0x57];
    value += previous;
    value -= previous;
    return value;
}
u8 saved_progression_byte5b(int species, int previous, int level) {
    int bucket = native_level_bucket(level);
    int value;
    bucket--;
    value = (native_kind_state.records[species].bytes + bucket)[0x5b];
    value += previous;
    value -= previous;
    return value;
}
