#include "context_00.h"
BOOL native_main_02019214 (void)
{
	BOOL retval = 1 ;
	CTRDGLockByProc lockInfo;
	CTRDGHeader *chp = ((CTRDGHeader *)0x08000000) ;
	CTRDGModuleInfo *cip = ((CTRDGModuleInfo *)(0x02000000 + 0x007ffc30)) ;
	if (cip->moduleID.raw == 0xffff) {
		return 0 ;
	}
	if (cip->detectPullOut == 1 ) {
		return 0 ;
	}
	native_fn_0201939c(native_data_main_020ec3b8.field_0004.lockID, &lockInfo);
	{
		CTRDGRomCycle rc;
		u8 isRomCode;
		native_fn_02019320(&rc);
		isRomCode = chp->isRomCode;
		if ((isRomCode == 0x96 && cip->moduleID.raw != chp->moduleID)
		    || (isRomCode != 0x96 && cip->moduleID.raw != *((u16 *)(0x08000000 + 0x0001fffe)) )
		    || ((cip->gameCode != chp->gameCode) && cip->isAgbCartridge)) {
			cip->detectPullOut = 1 ;
			retval = 0 ;
		}
		native_fn_02019368(&rc);
	}
	native_fn_020193f8(native_data_main_020ec3b8.field_0004.lockID, &lockInfo);
	return retval;
}
