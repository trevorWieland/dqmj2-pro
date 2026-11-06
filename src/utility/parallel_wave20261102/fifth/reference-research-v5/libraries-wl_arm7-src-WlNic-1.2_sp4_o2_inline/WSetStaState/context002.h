void WStop(void);

void SetupPeriodicTimeOut(u32 ms, void (*pFunc)(void *));

void WIntervalTimer(void *arg);

void ClearTimeOut(void);
