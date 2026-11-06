#include "context_00.h"
void native_main_020168a4 (u32 ggid, u16 tgid, u8 attribute)
{
	u32 lastAddr = (u32)native_data_main_020e68c0.field_0018.nowGameInfop + sizeof(MBGameInfoFixed);
	if ((u32)native_data_main_020e68c0.field_0018.srcp + ((112 - 8) - 6) <= lastAddr) {
		native_data_main_020e68c0.field_0040.data.fixed.size = ((112 - 8) - 6) ;
	} else {
		native_data_main_020e68c0.field_0040.data.fixed.size = (u8)(lastAddr - (u32)native_data_main_020e68c0.field_0018.srcp);
		MI_CpuClear16((void *)((u8 *)native_data_main_020e68c0.field_0040.data.fixed.data + native_data_main_020e68c0.field_0040.data.fixed.size),
		              (u32)(((112 - 8) - 6) - native_data_main_020e68c0.field_0040.data.fixed.size));
	}
	((void)0) ;
	MI_CpuCopy16(native_data_main_020e68c0.field_0018.srcp, native_data_main_020e68c0.field_0040.data.fixed.data, native_data_main_020e68c0.field_0040.data.fixed.size);
	native_data_main_020e68c0.field_0040.data.fixed.flagmentNo = native_data_main_020e68c0.field_0018.flagmentNo;
	native_data_main_020e68c0.field_0040.data.fixed.flagmentMaxNum = native_data_main_020e68c0.field_0018.flagmentMaxNum;
	native_data_main_020e68c0.field_0040.dataAttr = native_data_main_020e68c0.field_0018.nowGameInfop->dataAttr;
	native_data_main_020e68c0.field_0040.seqNoFixed = native_data_main_020e68c0.field_0018.nowGameInfop->seqNoFixed;
	native_data_main_020e68c0.field_0040.seqNoVolat = native_data_main_020e68c0.field_0018.seqNoVolat;
	native_data_main_020e68c0.field_0040.ggid = native_data_main_020e68c0.field_0018.nowGameInfop->ggid;
	native_data_main_020e68c0.field_0040.fileNo = native_data_main_020e68c0.field_0018.nowGameInfop->fileNo;
	native_data_main_020e68c0.field_0040.beaconNo = native_data_main_020e68c0.field_0018.beaconNo++;
	native_data_main_020e68c0.field_0040.data.fixed.sum = 0;
	native_data_main_020e68c0.field_0040.data.fixed.sum = native_fn_0201641c((u16 *)&native_data_main_020e68c0.field_0040.data, (112 - 8) );
	native_data_main_020e68c0.field_0018.flagmentNo++;
	if (native_data_main_020e68c0.field_0018.flagmentNo < native_data_main_020e68c0.field_0018.flagmentMaxNum) {
		native_data_main_020e68c0.field_0018.srcp += ((112 - 8) - 6) ;
	} else {
		native_data_main_020e68c0.field_0018.state = MB_BEACON_STATE_VOLAT_START;
	}
	(void)native_fn_020140f8(((void *)0) , (u16 *)&native_data_main_020e68c0.field_0040, 112 , ggid, tgid,
	                     (u8)(attribute | (1 << 1) | (1 << 0) ));
}
