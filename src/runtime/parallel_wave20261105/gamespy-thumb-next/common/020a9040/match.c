#include "context.h"
void native_main_020a9040(const char *input, char *output, int inlen, int * outlen, int encodingType)
{
	const char *encoding = NULL;
	const char *holdin = input;
	int readpos = 0;
	int writepos = 0;
	char block[4];
	
	
	

	
	
	
	switch(encodingType)
	{	
		case 1: 
			encoding = native_data_020dc550;
			break;
		case 2:
			encoding = native_data_020dc554;
			break;
		default: encoding = native_data_020dc558;
	}

	GS_ASSERT(inlen >= 0);
	if (inlen <= 0)
	{
		if (outlen)
			*outlen = 0;
		output[0] = '\0';
		return;
	}

	
	while (readpos < inlen && input[readpos] != encoding[2])
	{
		
		
		
		
		
		if (input[readpos] >= '0' && input[readpos] <= '9')
			block[readpos%4] = (char)(input[readpos] - 48 + 52);
		else if (input[readpos] >= 'a' && input[readpos] <= 'z')
			block[readpos%4] = (char)(input[readpos] - 71);
		else if (input[readpos] >= 'A' && input[readpos] <= 'Z')
			block[readpos%4] = (char)(input[readpos] - 65);
		else if (input[readpos] == encoding[0])
			block[readpos%4] = 62;
		else if (input[readpos] == encoding[1])
			block[readpos%4] = 63;

		
		else if (input[readpos] == encoding[2])
			break;
		else if (input[readpos] == '\0')
			break;
		else 
		{
			
			if (outlen)
				*outlen = 0;
			output[0] = '\0';
			return; 
		}

		
		if (readpos%4==3) 
		{
			native_fn_020a8f9c(block, &output[writepos], 4);
			writepos += 3;
		}
		readpos++;
	}

	
	if ((readpos != 0) && (readpos%4 != 0))
	{
		
		native_fn_0201b208(&block[readpos%4], encoding[2], (unsigned int)4-(readpos%4)); 
		native_fn_020a8f9c(block, &output[writepos], readpos%4);

		
		if (readpos%4 == 3)
			writepos += 2;
		else 
			writepos += 1;
	}

	if (outlen)
		*outlen = writepos;

	GSI_UNUSED(holdin);
}
