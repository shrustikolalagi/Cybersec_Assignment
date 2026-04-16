/*
 *Assignment
 * pointer_basic
 */

#include <stdio.h>

int main(void) {

    
    int port = 80;
    int *ptr = &port;   
    printf("=== Pointer Basics Demo ===\n\n");
    printf("[1] Port value using variable  : %d\n", port);
    printf("[2] Port value using pointer   : %d\n", *ptr);
    printf("    Address stored in pointer  : %p\n", (void *)ptr);
    printf("    Address of port variable   : %p\n\n", (void *)&port);
    *ptr = 443;
    printf("[3] Port changed via pointer.\n");
    printf("    New port value (variable)  : %d\n", port);
    printf("    New port value (pointer)   : %d\n\n", *ptr);

    printf("=== End of Demo ===\n");
    return 0;
}
