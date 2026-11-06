#include "context.h"
void
native_main_020b2c98(
  const char * unencodedString,
  char * encodedString
)
{
	size_t i;
	const int useAlternateEncoding = 1;
	char passwordxor[GP_PASSWORD_LEN];
	size_t passwordlen = strlen(unencodedString);
	Util_RandSeed((unsigned long)GP_XOR_SEED);
	for (i=0; i < passwordlen; i++)
	{
		char aRand = (char)Util_RandInt(0, 0xFF);
		passwordxor[i] = (char)(unencodedString[i] ^ aRand);
	}
	passwordxor[i] = '\0';
	B64Encode(passwordxor, encodedString, (int)passwordlen, useAlternateEncoding);
}
