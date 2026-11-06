#include "context.h"
int native_main_0209063c(const SocConfigInput *config){
native_data_021d15b4.configuration40.dhcp0=(config->flagC==1)?1:0;native_data_021d15b4.configuration40.address4=SWAP32(config->address10);native_data_021d15b4.configuration40.net8=SWAP32(config->net14);native_data_021d15b4.configuration40.routerC=SWAP32(config->router18);native_data_021d15b4.configuration40.dns10=SWAP32(config->dns1C);native_data_021d15b4.configuration40.dns14=SWAP32(config->dns20);native_data_021d15b4.configuration40.allocate18=native_fn_02090608;native_data_021d15b4.configuration40.release1C=native_fn_02090624;
native_data_021d15b4.allocateC=config->allocate4;native_data_021d15b4.release4=config->release8;
native_data_021d15b4.configuration40.commandMax20=64;native_data_021d15b4.configuration40.mtu30=config->mtu2C;native_data_021d15b4.configuration40.window34=config->window30;
return native_fn_0208e990(&native_data_021d15f4);
}
