#include "context.h"
void native_main_020b7334(qr2_t qrec)
{
	if (qrec == NULL)
		qrec = native_data_020e179c;
	if (qrec->ispublic)
		native_fn_020b73c0(qrec);
	native_fn_020b7360(qrec);
	native_fn_020b8068(qrec);
}
