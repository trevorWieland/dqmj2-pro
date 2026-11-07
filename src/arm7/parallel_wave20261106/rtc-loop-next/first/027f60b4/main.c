#include "context000.h"

void native_host_arm7_main_027f60b4(void *arg)
{
    OSMessage msg;
    RTCRawData *prd = (RTCRawData *)(((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->real_time_clock);
    while (1 ) {
        native_host_arm7_arm_037fc760(&(native_host_arm7_data_027f8e34.work).msgQueue, &msg, 1 );
        switch ((native_host_arm7_data_027f8e34.work).command) {
        case 0x00 :
            native_host_arm7_arm_027f6638();
            (native_host_arm7_data_027f8e34.work).busy = 0 ;
            native_host_arm7_arm_027f6074(0x00 , RTC_PXI_RESULT_SUCCESS);
            break;
        case 0x01 :
            native_host_arm7_arm_027f667c(prd->a.status1.format);
            (native_host_arm7_data_027f8e34.work).busy = 0 ;
            native_host_arm7_arm_027f6074(0x01 , RTC_PXI_RESULT_SUCCESS);
            break;
        case 0x10 :
            native_host_arm7_arm_027f67a0(prd);
            (native_host_arm7_data_027f8e34.work).busy = 0 ;
            native_host_arm7_arm_027f6074(0x10 , RTC_PXI_RESULT_SUCCESS);
            break;
        case 0x11 :
            native_host_arm7_arm_027f6804(&prd->t.date);
            (native_host_arm7_data_027f8e34.work).busy = 0 ;
            native_host_arm7_arm_027f6074(0x11 , RTC_PXI_RESULT_SUCCESS);
            break;
        case 0x12 :
            native_host_arm7_arm_027f6830(&prd->t.time);
            (native_host_arm7_data_027f8e34.work).busy = 0 ;
            native_host_arm7_arm_027f6074(0x12 , RTC_PXI_RESULT_SUCCESS);
            break;
        case 0x13 :
            if (!native_host_arm7_arm_027f6894(&prd->a.pulse)) {
                (native_host_arm7_data_027f8e34.work).busy = 0 ;
                native_host_arm7_arm_027f6074(0x13 , RTC_PXI_RESULT_ILLEGAL_STATUS);
            } else {
                (native_host_arm7_data_027f8e34.work).busy = 0 ;
                native_host_arm7_arm_027f6074(0x13 , RTC_PXI_RESULT_SUCCESS);
            }
            break;
        case 0x14 :
            if (!native_host_arm7_arm_027f6970(&prd->a.alarm)) {
                (native_host_arm7_data_027f8e34.work).busy = 0 ;
                native_host_arm7_arm_027f6074(0x14 , RTC_PXI_RESULT_ILLEGAL_STATUS);
            } else {
                (native_host_arm7_data_027f8e34.work).busy = 0 ;
                native_host_arm7_arm_027f6074(0x14 , RTC_PXI_RESULT_SUCCESS);
            }
            break;
        case 0x15 :
            if (!native_host_arm7_arm_027f6a44(&prd->a.alarm)) {
                (native_host_arm7_data_027f8e34.work).busy = 0 ;
                native_host_arm7_arm_027f6074(0x15 , RTC_PXI_RESULT_ILLEGAL_STATUS);
            } else {
                (native_host_arm7_data_027f8e34.work).busy = 0 ;
                native_host_arm7_arm_027f6074(0x15 , RTC_PXI_RESULT_SUCCESS);
            }
            break;
        case 0x16 :
            native_host_arm7_arm_027f6b10(&prd->a.status1);
            (native_host_arm7_data_027f8e34.work).busy = 0 ;
            native_host_arm7_arm_027f6074(0x16 , RTC_PXI_RESULT_SUCCESS);
            break;
        case 0x17 :
            native_host_arm7_arm_027f6b74(&prd->a.status2);
            (native_host_arm7_data_027f8e34.work).busy = 0 ;
            native_host_arm7_arm_027f6074(0x17 , RTC_PXI_RESULT_SUCCESS);
            break;
        case 0x18 :
            native_host_arm7_arm_027f6bd8(&prd->a.adjust);
            (native_host_arm7_data_027f8e34.work).busy = 0 ;
            native_host_arm7_arm_027f6074(0x18 , RTC_PXI_RESULT_SUCCESS);
            break;
        case 0x19 :
            native_host_arm7_arm_027f6c3c(&prd->a.free);
            (native_host_arm7_data_027f8e34.work).busy = 0 ;
            native_host_arm7_arm_027f6074(0x19 , RTC_PXI_RESULT_SUCCESS);
            break;
        case 0x20 :
            native_host_arm7_arm_027f67cc(prd);
            (native_host_arm7_data_027f8e34.work).busy = 0 ;
            native_host_arm7_arm_027f6074(0x20 , RTC_PXI_RESULT_SUCCESS);
            break;
        case 0x21 :
            native_host_arm7_arm_027f6830(&prd->t.time);
            native_host_arm7_arm_027f67cc(prd);
            (native_host_arm7_data_027f8e34.work).busy = 0 ;
            native_host_arm7_arm_027f6074(0x21 , RTC_PXI_RESULT_SUCCESS);
            break;
        case 0x22 :
            native_host_arm7_arm_027f685c(&prd->t.time);
            (native_host_arm7_data_027f8e34.work).busy = 0 ;
            native_host_arm7_arm_027f6074(0x22 , RTC_PXI_RESULT_SUCCESS);
            break;
        case 0x23 :
            if (!native_host_arm7_arm_027f68fc(&prd->a.pulse)) {
                (native_host_arm7_data_027f8e34.work).busy = 0 ;
                native_host_arm7_arm_027f6074(0x23 , RTC_PXI_RESULT_ILLEGAL_STATUS);
            } else {
                (native_host_arm7_data_027f8e34.work).busy = 0 ;
                native_host_arm7_arm_027f6074(0x23 , RTC_PXI_RESULT_SUCCESS);
            }
            break;
        case 0x24 :
            if (!native_host_arm7_arm_027f69d4(&prd->a.alarm)) {
                (native_host_arm7_data_027f8e34.work).busy = 0 ;
                native_host_arm7_arm_027f6074(0x24 , RTC_PXI_RESULT_ILLEGAL_STATUS);
            } else {
                (native_host_arm7_data_027f8e34.work).busy = 0 ;
                native_host_arm7_arm_027f6074(0x24 , RTC_PXI_RESULT_SUCCESS);
            }
            break;
        case 0x25 :
            if (!native_host_arm7_arm_027f6aa4(&prd->a.alarm)) {
                (native_host_arm7_data_027f8e34.work).busy = 0 ;
                native_host_arm7_arm_027f6074(0x25 , RTC_PXI_RESULT_ILLEGAL_STATUS);
            } else {
                (native_host_arm7_data_027f8e34.work).busy = 0 ;
                native_host_arm7_arm_027f6074(0x25 , RTC_PXI_RESULT_SUCCESS);
            }
            break;
        case 0x26 :
            native_host_arm7_arm_027f6b3c(&prd->a.status1);
            (native_host_arm7_data_027f8e34.work).busy = 0 ;
            native_host_arm7_arm_027f6074(0x26 , RTC_PXI_RESULT_SUCCESS);
            break;
        case 0x27 :
            native_host_arm7_arm_027f6ba0(&prd->a.status2);
            (native_host_arm7_data_027f8e34.work).busy = 0 ;
            native_host_arm7_arm_027f6074(0x27 , RTC_PXI_RESULT_SUCCESS);
            break;
        case 0x28 :
            native_host_arm7_arm_027f6c04(&prd->a.adjust);
            (native_host_arm7_data_027f8e34.work).busy = 0 ;
            native_host_arm7_arm_027f6074(0x28 , RTC_PXI_RESULT_SUCCESS);
            break;
        case 0x29 :
            native_host_arm7_arm_027f6c68(&prd->a.free);
            (native_host_arm7_data_027f8e34.work).busy = 0 ;
            native_host_arm7_arm_027f6074(0x29 , RTC_PXI_RESULT_SUCCESS);
            break;
        default: {
            u16 comm = (native_host_arm7_data_027f8e34.work).command;
            (native_host_arm7_data_027f8e34.work).busy = 0 ;
            native_host_arm7_arm_027f6074(comm, RTC_PXI_RESULT_INVALID_COMMAND);
        } break;
        }
    }
}
