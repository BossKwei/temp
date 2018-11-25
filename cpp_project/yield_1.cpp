//
// Created by bosskwei on 18-9-29.
//

#include "utils.hpp"


int range(int a, int b)
{
    static int i;
    static int state = 0;
    switch (state)
    {
        default:
            fprintf(stderr, "unhandled state %d\n", state);
            break;
        case 0: /* start of function */
            state = 1;
            for (i = a; i < b; i++)
            {
                return i;

                /* Returns control */
                case 1:; /* resume control straight
                    after the return */
            }
    }
    state = 0;
    return 0;
}

#define crBegin static int state=0; switch(state) { case 0:
#define crReturn(i,x) do { state=i; return x; case i:; } while (0)
#define crFinish }
int range2(int a, int b) {
    static int i = 0;
    crBegin;
            for (i = a; i < b; i++)
                crReturn(1, i);
    crFinish;
}

// Driver code
int main()
{
    int i; //For really large numbers

    for (; (i=range2(1, 5));)
        printf("control at main :%d\n", i);

    return 0;
}
