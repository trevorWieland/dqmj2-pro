typedef unsigned char byte;typedef unsigned int uint;
typedef void*(*ACAlloc)(unsigned long,signed long);typedef void(*ACFree)(unsigned long,void*,signed long);
typedef struct{ACAlloc alloc;ACFree free;byte allocState,phase,phaseError,findAP;int error,errorTest;byte endState,endType,endSequence,type;char apSpotInfo[10];byte overrideType;}tagACHOLD;
int native_main_02095324(tagACHOLD*);
