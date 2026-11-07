#include "context000.h"

void native_host_arm7_main_027f5188(SPIEntry *entry)
{
    OSIntrMode e = native_host_arm7_arm_037fdd00();
    if (!native_host_arm7_arm_03803b0c(SPI_DEVICE_TYPE_NVRAM)) {
        native_host_arm7_arm_037fdd14(e);
        native_host_arm7_arm_03803a48(entry->process, 0x0004 );
        return;
    }
    native_host_arm7_arm_03803b28(SPI_DEVICE_TYPE_NVRAM);
    native_host_arm7_arm_037fdd14(e);
    switch (entry->process) {
    case 0x0020 :
        native_host_arm7_arm_027f54b0();
        break;
    case 0x0021 :
        native_host_arm7_arm_027f5514();
        break;
    case 0x0022 :
        native_host_arm7_arm_027f5554((u8 *)(entry->arg[2]));
        break;
    case 0x0023 :
        if (!native_host_arm7_arm_027f545c()) {
            native_host_arm7_arm_03803a48(entry->process, 0x0003 );
            native_host_arm7_arm_03803b40(SPI_DEVICE_TYPE_NVRAM);
            return;
        }
        native_host_arm7_arm_027f55c4(entry->arg[0], entry->arg[1], (u8 *)(entry->arg[2]));
        break;
    case 0x0024 :
        if (!native_host_arm7_arm_027f545c()) {
            native_host_arm7_arm_03803a48(entry->process, 0x0003 );
            native_host_arm7_arm_03803b40(SPI_DEVICE_TYPE_NVRAM);
            return;
        }
        native_host_arm7_arm_027f56ec(entry->arg[0], entry->arg[1], (u8 *)(entry->arg[2]));
        break;
    case 0x0025 :
        if (!native_host_arm7_arm_027f5480()) {
            native_host_arm7_arm_03803a48(entry->process, 0x0003 );
            native_host_arm7_arm_03803b40(SPI_DEVICE_TYPE_NVRAM);
            return;
        }
        native_host_arm7_arm_027f580c(entry->arg[0], entry->arg[1], (const u8 *)(entry->arg[2]));
        break;
    case 0x0026 :
        if (!native_host_arm7_arm_027f5480()) {
            native_host_arm7_arm_03803a48(entry->process, 0x0003 );
            native_host_arm7_arm_03803b40(SPI_DEVICE_TYPE_NVRAM);
            return;
        }
        native_host_arm7_arm_027f5918(entry->arg[0], entry->arg[1], (const u8 *)(entry->arg[2]));
        break;
    case 0x0027 :
        if (!native_host_arm7_arm_027f5480()) {
            native_host_arm7_arm_03803a48(entry->process, 0x0003 );
            native_host_arm7_arm_03803b40(SPI_DEVICE_TYPE_NVRAM);
            return;
        }
        native_host_arm7_arm_027f5a24(entry->arg[0]);
        break;
    case 0x0028 :
        if (!native_host_arm7_arm_027f5480()) {
            native_host_arm7_arm_03803a48(entry->process, 0x0003 );
            native_host_arm7_arm_03803b40(SPI_DEVICE_TYPE_NVRAM);
            return;
        }
        native_host_arm7_arm_027f5aac(entry->arg[0]);
        break;
    case 0x0029 :
        native_host_arm7_arm_027f5b34();
        break;
    case 0x002a :
        native_host_arm7_arm_027f5b74();
        break;
    case 0x002b :
        if (!native_host_arm7_arm_027f5480()) {
            native_host_arm7_arm_03803a48(entry->process, 0x0003 );
            native_host_arm7_arm_03803b40(SPI_DEVICE_TYPE_NVRAM);
            return;
        }
        native_host_arm7_arm_027f5bb4();
        break;
    case 0x002c :
        native_host_arm7_arm_027f5bf4((u8 *)(entry->arg[2]));
        break;
    case 0x002d :
        native_host_arm7_arm_027f5c90();
        break;
    default:
        native_host_arm7_arm_03803b40(SPI_DEVICE_TYPE_NVRAM);
        native_host_arm7_arm_03803a48(entry->process, 0x0001 );
        return;
    }
    native_host_arm7_arm_03803a48(entry->process, 0x0000 );
    native_host_arm7_arm_03803b40(SPI_DEVICE_TYPE_NVRAM);
}

#include "context001.h"
