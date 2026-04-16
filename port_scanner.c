#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <sys/time.h>
 
#define TARGET_IP    "127.0.0.1"
#define TIMEOUT_SEC  1
 
/* ── scan_port() ─────────────────────────────────────────────────
 * Attempts a TCP connection to TARGET_IP on the given port.
 * Returns 1 if OPEN, 0 if CLOSED.
 * ─────────────────────────────────────────────────────────────── */
int scan_port(int port) {
    int sockfd;
    struct sockaddr_in target;
    struct timeval timeout;
 
    /* Create TCP socket */
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        return 0;
    }
 
    /* Set connection timeout */
    timeout.tv_sec  = TIMEOUT_SEC;
    timeout.tv_usec = 0;
    setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout));
    setsockopt(sockfd, SOL_SOCKET, SO_SNDTIMEO, &timeout, sizeof(timeout));
 
    /* Build target address */
    memset(&target, 0, sizeof(target));
    target.sin_family      = AF_INET;
    target.sin_port        = htons((unsigned short)port);
    target.sin_addr.s_addr = inet_addr(TARGET_IP);
 
    /* Try to connect */
    int result = connect(sockfd, (struct sockaddr *)&target, sizeof(target));
    close(sockfd);
 
    return (result == 0) ? 1 : 0;
}
 
/* ── main() ──────────────────────────────────────────────────── */
int main(void) {
 
    int ports[] = { 22, 80, 443, 3306 };
    int num_ports = sizeof(ports) / sizeof(ports[0]);
 
    printf("Scanning %s ...\n\n", TARGET_IP);
 
    for (int i = 0; i < num_ports; i++) {
        if (scan_port(ports[i])) {
            printf("Port %d: OPEN\n", ports[i]);
        } else {
            printf("Port %d: CLOSED\n", ports[i]);
        }
    }
 
    printf("\nScan complete.\n");
    return 0;
}
