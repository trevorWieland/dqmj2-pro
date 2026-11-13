#include "context.h"
u32 native_ov001_0220984c(void) {
    u32 temp_r0;
    s32 var_r2;
    u32 temp_r4_2;
    u8 *temp_r4;
    u32 var_r5;

    Descriptor356 descriptor;
    u32 resource[2];
    u16 coordinates[2];

    var_r5 = 1;
    switch (native_data_ov001_0223def8.field_14) {
    case 0:
        temp_r4 = native_fn_02062a10(native_data_ov001_0223def8.field_1c);
        descriptor.kind = 1;
        descriptor.species = M2C_FIELD(temp_r4, s16 *, 0x18);
        descriptor.variant = M2C_FIELD(temp_r4, u8 *, 0x1A);
        descriptor.raw = M2C_FIELD(temp_r4, u8 *, 0x1B);
        descriptor.name = native_fn_ov001_021fbe70() + 0x6D;
        descriptor.length = 0x10;
        descriptor.last = 0;
        native_fn_0207e720(&descriptor);
        native_fn_0206dcd0(temp_r4);
        native_fn_02041538(0U, 2U, 0x10U);
        break;
    case 1:
        native_fn_02045680(0);
        native_fn_02045680(1);
        native_fn_02045680(2);
        native_fn_02045680(3);
        var_r2 = 0;
        do {
            M2C_FIELD(native_data_ov001_0223df1c, u32 *, var_r2 * 4) = 0x20;
            var_r2 += 1;
        } while (var_r2 < 4);
        native_fn_02068ae8();
        temp_r0 = native_fn_0203cc2c((u32) native_data_ov001_0222f0b0, 2U);
        native_fn_0204518c(resource, temp_r0, 1U);
        native_fn_02045490(3, resource[0], 0, resource[1]);
        native_data_ov001_0223def8.field_30 = resource[1];
        native_fn_0204518c(resource, temp_r0, 8U);
        native_fn_02045994(3U, resource[0], 0, 0x800U);
        native_fn_0202a498(2, temp_r0);
        native_fn_ov001_0220aaa0();
        native_fn_ov001_0220aab8(native_data_ov001_0223df1c);
        native_fn_ov001_0220a5e0();
        native_fn_ov001_0220ad70(ov001_table_f0_entry_02202360(6));
        native_fn_ov001_0220af00(ov001_table_f0_entry_02202360(6), 0);
        native_fn_ov001_0220af68(ov001_table_f0_entry_02202360(6));
        native_fn_ov001_0220a6cc(native_data_ov001_0223def8.field_1c);
        temp_r4_2 = native_fn_02062aa0();
        native_fn_02068eb8(2U, 0, 0, (s8) (temp_r4_2 + native_fn_02062ad0()));
        native_fn_0206be08(0U, 0U);
        native_data_ov001_0223def8.field_6 = 1;
        native_fn_0206de44(1);
        native_fn_02041538(0U, 2U, 0x10U);
        break;
    case 3:
        coordinates[1] = native_data_ov001_0222e0e4.field_2;
        coordinates[0] = native_data_ov001_0222e0e4.field_0;
        native_fn_ov001_0220af00(ov001_table_f0_entry_02202360(6), 0);
        native_fn_ov001_0220af68(ov001_table_f0_entry_02202360(6));
        native_fn_ov001_0220afe4(ov001_table_f0_entry_02202360(6), native_data_ov001_0223def8.field_18);
        native_fn_ov001_0220b0f0(ov001_table_f0_entry_02202360(6), 2, coordinates, 2, 9, 0xE);
        var_r5 = 4;
        break;
    }
    return var_r5;
}
