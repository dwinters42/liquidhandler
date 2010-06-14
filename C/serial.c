#include <stdio.h>
#include <stdlib.h> 
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h> 
#include <errno.h>
#include <termios.h>

int serial_open(const char*, int);
int serial_writebyte(int, uint8_t);
int serial_write(int, const char*);
int serial_readline(int, char*, char);

int main(int argc, char *argv[]) {
  int fd = 0;
  //  char buf[256];
  //  int rc,n;
  
  fd = serial_open("/dev/ttyUSB0",9600);
  if (fd == -1) {
    perror("could not open serial port!");
    exit(-1);
  }
  
  return 0;
} 

int serial_open(const char* serial, int baud) {
  struct termios toptions;
  int fd;
  
  fd = open(serial, O_RDWR | O_NOCTTY | O_NDELAY);
  if (fd == -1)  {
    perror("serial_open: Unable to open port ");
    return -1;
  }
    
  if (tcgetattr(fd, &toptions) < 0) {
    perror("serial_open: Couldn't get term attributes");
    return -1;
  }

  speed_t brate = baud;

  switch(baud) {
  case 4800:   brate=B4800;   break;
  case 9600:   brate=B9600;   break;
  case 19200:  brate=B19200;  break;
  case 38400:  brate=B38400;  break;
  case 57600:  brate=B57600;  break;
  case 115200: brate=B115200; break;
  }
  cfsetispeed(&toptions, brate);
  cfsetospeed(&toptions, brate);
  
  // 8N1
  toptions.c_cflag &= ~PARENB;
  toptions.c_cflag &= ~CSTOPB;
  toptions.c_cflag &= ~CSIZE;
  toptions.c_cflag |= CS8;

  // no flow control
  toptions.c_cflag &= ~CRTSCTS;
  
  // turn on READ & ignore ctrl lines
  toptions.c_cflag |= CREAD | CLOCAL;  
  // turn off s/w flow ctrl
  toptions.c_iflag &= ~(IXON | IXOFF | IXANY); 
  
  // make raw
  toptions.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG); 
  toptions.c_oflag &= ~OPOST;
  
  // see: http://unixwiz.net/techtips/termios-vmin-vtime.html
  toptions.c_cc[VMIN]  = 0;
  toptions.c_cc[VTIME] = 20;
  
  if(tcsetattr(fd, TCSANOW, &toptions) < 0) {
    perror("serial_open: Couldn't set term attributes");
    return -1;
  }
  
  return fd;
}

int serial_writebyte( int fd, uint8_t b) {
  int n = write(fd,&b,1);
  if( n!=1)
    return -1;
  return 0;
}

int serial_write(int fd, const char* str) {
  int len = strlen(str);
  int n = write(fd, str, len);
  if( n!=len ) 
    return -1;
  return 0;
}

int serial_readline(int fd, char* buf, char until) {
  char b;
  int n,i=0;

  do { 
    n = read(fd, b, 1);

    if (n==-1)
      return -1;
    if (n==0) {
      usleep(10 * 1000);
      continue;
    }
    buf[i] = b[0]; 
    i++;
  } while (b[0] != until);
  
  buf[i] = 0;
  return 0;
}
