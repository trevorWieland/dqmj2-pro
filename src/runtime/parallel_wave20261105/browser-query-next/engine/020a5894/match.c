#include "context.h"
SBBool native_main_020a5894(SBServerFIFO *fifo, SBServer server)
{
	SBServer hold, prev;
	prev = NULL;
	hold = fifo->first;
	while (hold != NULL)
	{
		if (hold == server) 
		{
			if (prev != NULL) 
				prev->next = hold->next;
			if (fifo->first == hold)
				fifo->first = hold->next;
			if (fifo->last == hold)
				fifo->last = prev;
			fifo->count--;
		
			return SBTrue;
		}
		prev = hold;
		hold = hold->next;
	}

	FIFODebugCheck(fifo);
	return SBFalse;
}