#include "context.h"
void native_main_020a91a0(const char *input, char *output, int inlen, int encodingType)
{
	const char *encoding;
	char *holdout = output;
	char *lastchar;
	int todo = inlen;
	
	
	
	
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
	

	while (todo > 0)
	{
		native_fn_020a8fe0(input, output, min(todo, 3));
		output += 4;
		input += 3;
		todo -= 3;
	}
	lastchar = output;
	if (inlen % 3 == 1)
		lastchar -= 2;
	else if (inlen % 3 == 2)
		lastchar -= 1;
	*output = 0; 
	while (output > holdout)
	{
		output--;
		if (output >= lastchar) 
			*output = encoding[2];
		else if (*output <= 25)
			*output = (char)(*output + 65);
		else if (*output <= 51)
			*output = (char)(*output + 71);
		else if (*output <= 61)
			*output = (char)(*output + 48 - 52);
		else if (*output == 62)
			*output = encoding[0];
		else if (*output == 63)
			*output = encoding[1];
	} 
}
