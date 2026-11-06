#include "context.h"
GT2Byte * native_main_020b3a58
(
	GT2Byte * buffer,
	const GT2Byte * challenge
)
{
	int i;
	int valid;
	char cchar;
	int keylen = (int)strlen(GT2ChallengeKey);
	int chalrand;
	valid = gti2VerifyChallenge(challenge); 
	
	for (i = 0 ; i < GTI2_RESPONSE_LEN ; i++)
	{
		
		if (!valid || i == 0 || i == 13)
			buffer[i] = (GT2Byte)(33 + rand() % 93); 
		else
		{ 
			if (i == 1 || i == 14)
				cchar = (char)challenge[i];
			else
				cchar = (char)challenge[i-1];
			chalrand = abs((challenge[((i * challenge[i]) + GT2ChallengeKey[(i + challenge[i]) % keylen]) % GTI2_CHALLENGE_LEN] ^ GT2ChallengeKey[(i * 17991 * cchar) % keylen]));
			buffer[i] = (GT2Byte)(33 + chalrand % 93);
		}
	}
	return buffer;
}
