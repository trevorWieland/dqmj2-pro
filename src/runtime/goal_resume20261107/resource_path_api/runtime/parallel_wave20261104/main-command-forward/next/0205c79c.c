#include "../../../../resource_path_api.h"
#include "context.h"
int native_main_0205c79c(int id)
{
    int result=0;
    if(native_fn_0205c404()==0) {
        ResourceSlot *slot=native_fn_0205c448();
        if(slot) {
            char name[16];
            u32 size;
            void *data;
            native_fn_0201d444(name,(const char*)0x20ddbd8,id);
            size=native_fn_0202a8e0(name);
            if(size) {
                data=native_fn_0202a428(size,4);
                if(data && native_fn_0202a954(0,name,data,size,0)) {
                    slot->data=data;slot->id=id;result=1;
                }
            }
        }
    }
    return result;
}
