#include "context.h"
void native_main_020aa068(GPConnection*connection){GPIConnection*iconnection;if(connection==NULL||*connection==NULL)return;iconnection=(GPIConnection*)*connection;if(iconnection->simulation)return;gpiDisconnect(connection,GPITrue);gpiReset(connection);}
