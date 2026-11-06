#include <stdio.h>
extern unsigned int j2p_async_run_all(void);
extern unsigned int j2p_async_cases_done(void);
extern unsigned int j2p_async_provider_calls(void);

int main(void) {
    unsigned int failed = j2p_async_run_all();
    printf("{\"cases\":%u,\"providedCalls\":%u,\"firstFailure\":%u}\n",
        j2p_async_cases_done(), j2p_async_provider_calls(), failed);
    return failed ? 1 : 0;
}
