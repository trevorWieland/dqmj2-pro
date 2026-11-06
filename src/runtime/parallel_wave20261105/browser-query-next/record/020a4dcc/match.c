#include "context.h"
u16 native_main_020a4dcc(u32 ignored,u32 value,u32 error){native_data_021d230c.status=(u8)value;native_data_021d230c.ready=1;if(error)native_data_021d230c.status=255;return native_data_021d230c.status;}
