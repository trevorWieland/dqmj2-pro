#include "context.h"
int native_main_02047ac0(u32 position)
{
    u8 *text = (u8 *)&native_data_020fb264;
    if (position < 128) {
        do {
            int skip = 0;
            u8 *command = text + position;
            if (*command == 0xe3 && command[1] == 0x1b) break;
            if (*command == 0xe3) {
                skip = 1;
                switch (command[1]) {
                case 0x1c:
                    position = (u8)(position + (native_fn_02047018(command[2]) - 1));
                    break;
                case 0x15:
                    position = (u8)(position + (native_fn_02046fc8() - 1));
                    break;
                default:
                    skip = 0;
                    break;
                }
            }
            if (!skip) {
                if (!*command) break;
                position = (u8)(position + (native_fn_02046e68(command) - 1));
            }
            position = (u8)(position + 1);
        } while (position < 128);
    }
    return 0;
}
