#include "context_00.h"
void native_main_02016a38 (u32 ggid, u16 tgid, u8 attribute)
{
	int i;
	int setPlayerNum;
	u16 remainPlayerFlag;
	if (native_data_main_020e68c0.field_0018.seqNoVolat != native_data_main_020e68c0.field_0018.nowGameInfop->seqNoVolat) {
		native_fn_02016a08();
	}
	native_data_main_020e68c0.field_0040.dataAttr = MB_BEACON_DATA_ATTR_VOLAT;
	native_data_main_020e68c0.field_0040.seqNoFixed = native_data_main_020e68c0.field_0018.nowGameInfop->seqNoFixed;
	native_data_main_020e68c0.field_0040.seqNoVolat = native_data_main_020e68c0.field_0018.seqNoVolat;
	native_data_main_020e68c0.field_0040.ggid = native_data_main_020e68c0.field_0018.nowGameInfop->ggid;
	native_data_main_020e68c0.field_0040.fileNo = native_data_main_020e68c0.field_0018.nowGameInfop->fileNo;
	native_data_main_020e68c0.field_0040.beaconNo = native_data_main_020e68c0.field_0018.beaconNo++;
	native_data_main_020e68c0.field_0040.data.volat.nowPlayerNum = native_data_main_020e68c0.field_0018.nowGameInfop->volat.nowPlayerNum;
	native_data_main_020e68c0.field_0040.data.volat.nowPlayerFlag = native_data_main_020e68c0.field_0018.nowGameInfop->volat.nowPlayerFlag;
	native_data_main_020e68c0.field_0040.data.volat.changePlayerFlag = native_data_main_020e68c0.field_0018.nowGameInfop->volat.changePlayerFlag;
	if (native_data_main_020e68c0.field_0010 == MB_SEND_VOLAT_CALLBACK_TIMMING_BEFORE
	    && native_data_main_020e68c0.field_0014 != ((void *)0) ) {
		native_data_main_020e68c0.field_0014(native_data_main_020e68c0.field_0018.nowGameInfop->ggid);
	}
	for (i = 0; i < 8 ; i++) {
		native_data_main_020e68c0.field_0040.data.volat.userVolatData[i] = native_data_main_020e68c0.field_0018.nowGameInfop->volat.userVolatData[i];
	}
	((void)0) ;
	MI_CpuClear16(&native_data_main_020e68c0.field_0040.data.volat.member[0], sizeof(MBUserInfo) * (((112 - 8) - 8) / sizeof(MBUserInfo)) );
	setPlayerNum = 0;
	remainPlayerFlag = (u16)(native_data_main_020e68c0.field_0018.nowGameInfop->broadcastedPlayerFlag ^ native_data_main_020e68c0.field_0018.nowGameInfop->volat.nowPlayerFlag);
	for (i = 0; i < 15 ; i++) {
		if ((remainPlayerFlag & (0x0002 << i)) == 0) {
			continue;
		}
		((void)0) ;
		MI_CpuCopy16(&native_data_main_020e68c0.field_0018.nowGameInfop->volat.member[i], &native_data_main_020e68c0.field_0040.data.volat.member[setPlayerNum], sizeof(MBUserInfo));
		native_data_main_020e68c0.field_0018.nowGameInfop->broadcastedPlayerFlag |= 0x0002 << i;
		if (++setPlayerNum == (((112 - 8) - 8) / sizeof(MBUserInfo)) ) {
			break;
		}
	}
	if (setPlayerNum < (((112 - 8) - 8) / sizeof(MBUserInfo)) ) {
		native_data_main_020e68c0.field_0040.data.volat.member[setPlayerNum].playerNo = 0;
	}
	native_data_main_020e68c0.field_0040.data.volat.sum = 0;
	native_data_main_020e68c0.field_0040.data.volat.sum = native_fn_0201641c((u16 *)&native_data_main_020e68c0.field_0040.data, (112 - 8) );
	if (native_data_main_020e68c0.field_0018.nowGameInfop->broadcastedPlayerFlag == native_data_main_020e68c0.field_0018.nowGameInfop->volat.nowPlayerFlag) {
		native_data_main_020e68c0.field_0018.state = MB_BEACON_STATE_READY;
	}
	(void)native_fn_020140f8(((void *)0) , (u16 *)&native_data_main_020e68c0.field_0040, 112 , ggid, tgid,
	                     (u8)(attribute | (1 << 1) | (1 << 0) ));
	if (native_data_main_020e68c0.field_0010 == MB_SEND_VOLAT_CALLBACK_TIMMING_AFTER
	    && native_data_main_020e68c0.field_0014 != ((void *)0) ) {
		native_data_main_020e68c0.field_0014(native_data_main_020e68c0.field_0018.nowGameInfop->ggid);
	}
}
