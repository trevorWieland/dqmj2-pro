#include "context.h"
void native_main_020a6300(SBServer server, char *data, int len)
{
	int dlen;
	char *k;
	char *v;
	unsigned int packetNum = 0;
	gsi_bool isFinal = gsi_false;

	
	if (*data == '\0')
		return;
	
	
	dlen = native_fn_020a6fa8(data, len);
	if (dlen < 0)
		return;
	k = data;
	data += dlen;
	len -= dlen;
	
	if (native_fn_02023f60(QR2_SPLITPACKET_NUMSTRING,k,native_fn_0201d69c(QR2_SPLITPACKET_NUMSTRING))!=0)
		return;
	if (len < 1)
		return;

	packetNum = (unsigned int)((unsigned char)*data);
	data++;
	len--;

	
	if ((packetNum & QR2_SPLITPACKET_FINAL) == QR2_SPLITPACKET_FINAL)
	{
		isFinal = gsi_true;
		packetNum ^= QR2_SPLITPACKET_FINAL;
	}

	
	if (packetNum > QR2_SPLITPACKET_MAX)
		return;

	
	if (isFinal == SBTrue)
		
		server->bitmap |= (char)(0xFF<<packetNum); 
	else
		
		server->bitmap |= (1<<packetNum);

	
	if (len < 1)
		return;

	
	while(len > 0)
	{
		int keyType = 0;
		int nindex = 0;

		
		keyType = *data;
		data++;
		len--;

		if (keyType < 0 || keyType > 2)
		{
			gsDebugFormat(GSIDebugCat_SB, GSIDebugType_Network, GSIDebugLevel_WarmError,
					"Split packet parse error, invalid key type! (%d)\r\n", keyType);
			return; 
		}

		
		while(*data)
		{
			
			dlen = native_fn_020a6fa8(data, len);
			if (dlen < 0)
				return;
			k = data;
			data += dlen;
			len -= dlen;
				
			if (keyType == 0)
			{
				
				dlen = native_fn_020a6fa8(data, len);
				if (dlen < 0)
					return;
				v = data;
				data += dlen;
				len -= dlen;

				
				if (!native_fn_020b85a8(k))
				{
					native_fn_020a5f98(server, k, v);
				}	
			}
			else
			{
				char tempkey[128];

				
				if (len < 1)
					return;

				nindex = *data;
				data++;
				len--;

				
				while(*data)
				{
					
					dlen = native_fn_020a6fa8(data, len);
					if (dlen < 0)
						return;
					v = data;
					data += dlen;
					len -= dlen;
					
					native_fn_0200616c(tempkey, native_data_020e0324, k, nindex);
					native_fn_020a5f98(server, tempkey, v);
					nindex++; 
				}

				
				if (len > 0)
				{
					data++;
					len--;
				}
			}
		} 

		
		if (len > 0)
		{
			if (*data != '\0')
			{
				gsDebugFormat(GSIDebugCat_SB, GSIDebugType_Network, GSIDebugLevel_WarmError,
					"Split packet parse error, NULL byte expected!\r\n");
				return; 
			}
			data++;
			len--;
		}
	}
}
