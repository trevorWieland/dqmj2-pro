#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027eab68(u32 us, void (*pFunc)(void *arg))
{
    native_host_arm7_arm_037fd5c0(&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Alarm);
    native_host_arm7_arm_037fd4dc(&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Alarm, ((OSTick)(((33514000 / 1000) * (u64)(us)) / 64 / 1000)) , pFunc, 0 );
}
