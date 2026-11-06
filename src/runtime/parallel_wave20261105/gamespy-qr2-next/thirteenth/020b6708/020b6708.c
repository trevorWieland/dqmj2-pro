#include "context.h"
void native_main_020b6708(NATNegotiator neg)
{
	NatNegPacket p;
	native_fn_0201b19c(p.magic, native_data_020e1738, NATNEG_MAGIC_LEN);
	p.version = NN_PROTVER;
	p.packettype = NN_REPORT;
	p.cookie = (int)htonl(neg->cookie);
	p.Packet.Report.clientindex = (unsigned char)neg->clientindex;
	p.Packet.Report.negResult = (unsigned char)(neg->result==nr_success?gsi_true:gsi_false);
	native_fn_0201b19c(p.Packet.Report.natType,&native_data_020e172c,4);
	native_fn_0201b19c(p.Packet.Report.natMappingScheme,&native_data_021d2bcc,4);
	if(native_fn_0201d69c(native_data_021d23f0) > 0)
		native_fn_0201b19c(&p.Packet.Report.gamename, native_data_021d23f0, sizeof(p.Packet.Report.gamename));
	gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
		"Sending REPORT to %s:%d (result: %d)\n", inet_ntoa(*(struct in_addr *)&matchup1ip), MATCHUP_PORT1, p.Packet.Report.negResult);
	native_fn_020b6670(neg->negotiateSock, matchup1ip, MATCHUP_PORT1, &p, REPORTPACKET_SIZE);
}
