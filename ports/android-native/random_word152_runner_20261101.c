#include <stdint.h>
#include <stdio.h>
#include <stdalign.h>
#include "random_word152_record_20261101.h"

uint32_t native_rng_state;
J2pRandomWordRecord native_data_020f6028;
extern uint32_t native_main_0203d158(uint32_t);
extern uint32_t native_main_0203d1f0(void);
extern uint32_t saved_runtime_random(int);
_Static_assert(sizeof(uint32_t) == 4 && sizeof(void *) == 8, "ARM64 word and pointer ABI");
_Static_assert(__BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__, "Little-endian vector protocol");

uint32_t native_fn_0203d294(uint32_t limit) {
    if (limit != 256 && limit != 65535) return 0;
    return saved_runtime_random((int)limit);
}

uint32_t native_fn_0203d1f0(void) {
    return native_main_0203d1f0();
}

int main(void) {
    uint32_t count;
    uint32_t index;
    uint32_t arguments[2];
    uint32_t results[3];
    if (fread(&count, sizeof(count), 1, stdin) != 1 || count > 4096) return 91;
    for (index = 0; index < count; index++) {
        if (fread(arguments, sizeof(arguments), 1, stdin) != 1) return 92;
        if (fread(&native_data_020f6028, sizeof(native_data_020f6028), 1, stdin) != 1) return 93;
        native_rng_state = arguments[0];
        results[0] = native_main_0203d158(arguments[1]);
        results[1] = native_rng_state;
        results[2] = native_main_0203d1f0();
        if (fwrite(results, sizeof(results), 1, stdout) != 1) return 94;
        if (fwrite(&native_data_020f6028, sizeof(native_data_020f6028), 1, stdout) != 1) return 95;
    }
    if (fgetc(stdin) != EOF) return 96;
    return fflush(stdout) == 0 ? 0 : 97;
}
