#include "context.h"
int native_main_0207d74c(int mode,int threshold,int *output){
    const Info *info=native_fn_0207d2c8(mode);
    if(mode==0)return 0;
    if(info->kind==4){switch(info->subtype){case 3:if(native_fn_0203d294(1600)<threshold){*output=-1;return 2;}break;}}
    if(info->kind==6){switch(info->subtype){case 3:if(native_fn_0203d294(1600)<threshold){*output=1;return 42;}break;}}
    if(info->kind==8){switch(info->subtype){case 3:if(native_fn_0203d294(1600)<threshold){*output=1;return 53;}break;}}
    if(info->kind==7){
        switch(info->subtype){
        case 3:if(native_fn_0203d294(1600)<threshold){*output=-1;return 8;}break;
        case 4:if(native_fn_0203d294(800)<threshold){*output=-1;return 8;}break;
        }
    }
    return 0;
}
