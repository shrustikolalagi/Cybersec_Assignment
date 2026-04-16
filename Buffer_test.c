#include <stdio.h>
#include <string.h>
 
int main(void) {
 
    /* ── Vulnerable buffer (16 bytes) ── */
    char input_buffer[16];
 
    /*
     * Canary variable: placed right after the buffer so we can
     * visually observe when an overflow corrupts it.
     */
    int canary = 0xDEADBEEF;
 
    printf("=== Buffer Overflow Demo (EDUCATIONAL) ===\n");
    printf("Buffer size     : %zu bytes\n", sizeof(input_buffer));
    printf("Canary value    : 0x%X (should stay 0xDEADBEEF)\n\n", canary);
 
    printf("Enter a string (try more than 15 characters): ");
    fflush(stdout);
 
    /*
     * VULNERABLE: strcpy() does NOT check bounds.
     * Safe programs would use: fgets(input_buffer, sizeof(input_buffer), stdin)
     */
    char raw_input[256];
    if (fgets(raw_input, sizeof(raw_input), stdin) == NULL) {
        printf("[!] Input error.\n");
        return 1;
    }
 
    /* Remove trailing newline from fgets */
    raw_input[strcspn(raw_input, "\n")] = '\0';
 
    printf("\n[DEBUG] Input length: %zu characters\n", strlen(raw_input));
 
    /* ── INTENTIONALLY UNSAFE copy ── */
    strcpy(input_buffer, raw_input);   /* <-- BUFFER OVERFLOW HAPPENS HERE */
 
    printf("Copied string   : %s\n", input_buffer);
 
    /* Check if the canary was overwritten by the overflow /*/
    if (canary != (int)0xDEADBEEF) {
        printf("\n[!!! OVERFLOW DETECTED !!!]\n");
        printf("    Canary corrupted: was 0xDEADBEEF, now 0x%X\n", canary);
        printf("    Memory beyond the buffer has been overwritten!\n");
    } else {
        printf("Canary value    : 0x%X (intact – no overflow)\n", canary);
    }
 
    printf("\n=== End of Demo ===\n");
    return 0;
}
/*  ANSWER 1 – What happens with long input (30+ characters)?
 
  The buffer 'input_buffer' is only 16 bytes in size.
  strcpy() copies the entire user-supplied string into it WITHOUT
  checking the length.
 
  When more than 15 characters are entered (16th byte = '\0'), the
  extra bytes overflow PAST the end of the buffer and begin
  overwriting adjacent stack memory. This includes:
 *   - Local variables declared after the buffer
 *   - The saved frame pointer (SFP / RBP)
 *   - The return address (RIP / EIP)
 *   - Function arguments above the stack frame
 
 * Observed effects:
    • The 'canary' variable next to the buffer is overwritten (shown
      in this demo).
    • With stack-protector disabled and enough input, the saved
      return address is corrupted → program jumps to an invalid
      address → Segmentation Fault (SIGSEGV) or undefined behaviour.
    • With GCC's stack-smashing protector enabled (default), the
      canary value is checked on return and the program prints:
        "*** stack smashing detected ***" then aborts.
 

 * ANSWER 2 – Why is this dangerous?
  Buffer overflows are dangerous because an attacker who controls
  the input can:
    1. Overwrite the return address to redirect execution to
       attacker-supplied shellcode (classic code injection).
    2. Use Return-Oriented Programming (ROP) to chain existing
       code gadgets and execute arbitrary commands.
    3. Overwrite adjacent variables to escalate privileges, bypass
       authentication checks, or corrupt program logic.
    4. Crash the program, causing a Denial of Service (DoS).
 
  Real-world examples: Morris Worm (1988), MS Blaster (2003),
  Heartbleed-adjacent overreads, countless CVEs to this day.
 

 * ANSWER 3 – How would you fix this?
  Safe alternatives to strcpy():
    a) strncpy(dest, src, sizeof(dest) - 1);
       dest[sizeof(dest) - 1] = '\0';        // ensure null-termination
 
    b) strlcpy(dest, src, sizeof(dest));      // BSD / POSIX extension
 
    c) snprintf(dest, sizeof(dest), "%s", src);
 
    d) Use fgets() instead of gets()/scanf for user input:
         fgets(input_buffer, sizeof(input_buffer), stdin);
*/
