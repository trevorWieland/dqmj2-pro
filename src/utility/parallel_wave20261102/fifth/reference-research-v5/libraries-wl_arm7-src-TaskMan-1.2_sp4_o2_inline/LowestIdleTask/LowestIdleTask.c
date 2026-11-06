#include "context000.h"

#include "context001.h"

#include "context002.h"

void LowestIdleTask(void)
{
    OSMessage msg;
    OS_ReceiveMessage(((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->pRecvMsgQueue, &msg, 1 );
    ExecuteMessage(&msg);
    AddTask(3 , 12 );
}

#include "context003.h"
