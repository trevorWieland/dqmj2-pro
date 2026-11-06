#include "context000.h"

void native_main_0207a168(const Input *input){
    void *context=native_fn_ov000_02215698();
    Point point;point.x=16;point.y=40;
    point.y+=(input->a-input->b)*16;
    native_fn_0204b53c((char *)context+16,&point);
}
