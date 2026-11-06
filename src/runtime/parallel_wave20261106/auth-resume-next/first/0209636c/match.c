#include "context.h"
long native_main_0209636c(u8 c)
{
	if( (c >= (u8)'A') && (c <= (u8)'Z') ) {
		return (long)(c - (u8)'A');
	}
	else if( (c >= (u8)'a') && (c <= (u8)'z') ) {
		return ((long)(c - (u8)'a') +26);
	}
	else if( (c >= (u8)'0') && (c <= (u8)'9') ) {
		return ((long)(c - (u8)'0') +52);
	}
	else if( (u8)'+' == c ) {
		return (long)62;
	}
	else if( (u8)'/' == c ) {
		return (long)63;
	}
	else if( (u8)'=' == c ) {
		return (long)0;
	}
	else {
		return -1;
	}
}
