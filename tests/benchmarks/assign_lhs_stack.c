#include "runtime.h"





int
main(void)
{
    int count;
    int x;
    int pygen_0_compF_temp;
    int y;
    int z;
    int w;
    int a;
    int b;
    int c;
    int d;
    int e;
    int pygen_0_addF_temp;
    int pygen_1_addF_temp;
    int pygen_2_addF_temp;
    int pygen_3_addF_temp;
    int pygen_4_addF_temp;
    int pygen_5_addF_temp;
    int pygen_6_addF_temp;
    int f;
    int pygen_0_usubF_temp;
    int pygen_0_injF_temp;
    count = 1000000;
    x = 1;
    pygen_0_compF_temp = (0 != count);
    while (pygen_0_compF_temp) {
        x = (x + 1);
        y = (x + x);
        z = (y + y);
        w = (z + z);
        a = (w + w);
        b = (a + a);
        c = (b + b);
        d = (c + c);
        e = (d + d);
        pygen_0_addF_temp = (x + y);
        pygen_1_addF_temp = (pygen_0_addF_temp + z);
        pygen_2_addF_temp = (pygen_1_addF_temp + w);
        pygen_3_addF_temp = (pygen_2_addF_temp + a);
        pygen_4_addF_temp = (pygen_3_addF_temp + b);
        pygen_5_addF_temp = (pygen_4_addF_temp + c);
        pygen_6_addF_temp = (pygen_5_addF_temp + d);
        f = (pygen_6_addF_temp + e);
        pygen_0_usubF_temp = -(1);
        count = (count + pygen_0_usubF_temp);
        pygen_0_compF_temp = (0 != count);
    }
    pygen_0_injF_temp = inject_int(f);
    print_any(pygen_0_injF_temp);
}
