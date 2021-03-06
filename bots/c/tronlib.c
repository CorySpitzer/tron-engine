/*******
 * tronlib.c
 * See ./tronlib.h and testbot.c for the interface and usage.
 * Jim Mahoney | cs.marlboro.edu | Feb 9 2014 | MIT License
 *****/

#include "tronlib.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int stderror_to_logfile = 0;

void _warn_no_newline(const char* message){
  /* output message to stderr */
  fprintf(stderr, "%s", message);
}

void warn(const char* message){
  _warn_no_newline(message);
  _warn_no_newline("\n");
}

void init_error_log(const char* filename){
  time_t timedata;
  struct tm *timeinfo;
  //char buffer[128];
  timedata = time(NULL);                /* get current time */
  timeinfo = localtime(&timedata);      /* convert to local time format */
  freopen(filename, "a", stderr);
  _warn_no_newline("=== starting C bot at ");
  _warn_no_newline(asctime(timeinfo));
  stderror_to_logfile = 1;
}

void _fatal_error(const char* error_message){
  /* send message + \n to stdout (and stderr if its to a log), and quit. */
  printf("FATAL ERROR: %s \n", error_message);
  if (stderror_to_logfile){
    _warn_no_newline("FATAL ERROR: ");
    warn(error_message);
  }
  exit(1);
}

void read_line(char* buffer, char* error_message){
  /* copy a line from stdin to buffer */
  char* status;
  size_t length;
  buffer[0] = 0;  /* initialize to length 0 */
  status = fgets(buffer, MAX_BOARD_WIDTH+1, stdin);
  length = strlen(buffer);
  if (status == NULL || length == 0 || length > MAX_BOARD_WIDTH){
    _fatal_error(error_message);
  }
}

boardp new_board(){
  boardp b = malloc(sizeof(struct _board));
  b->width = b->height = b->_me.row = b->_them.row = -1;
  return b;
}

void read_map(boardp b){
  /* The bot reads the map from stdin on each turn,
     with the width and height on the first line,
     and the map on the following height x width lines, like this :
        5 4               // 5 columns by 4 rows
        #####             // row 0, column 0 to 4
        #1 2#             // 1 is "me", 2 is "them"
        #   #             // # is wall
        #####
   */
  char buffer[MAX_BOARD_WIDTH+2];
  int width, height, status, i;
  read_line(buffer, " 'width height' input line could not be read");
  status = sscanf(buffer, "%d %d", &width, &height);
  if (status != 2){
    _fatal_error(" 'width height' not found as expected");
  }
  if (b->width == -1){             /* 1st time: initialize board map */
    b->map = malloc(width * height + 1);
    b->width = width;
    b->height = height;
    b->map[0] = 0;                /* set to zero length string */
  }
  if (width != b->width || height != b->height){
    _fatal_error("inconsistent width or height");
  }
  for (i=0; i<height; i++){
    read_line(buffer, "could not read board row");
    memcpy(b->map + i*width, buffer, width);
  }
  b->map[width * height] = 0;     /* make map null terminated */
  b->_me.row = b->_them.row = -1;  /* clear cached values */
}

void init_map(boardp b, int width, int height){
  if (width < 0 || height < 0){
    _fatal_error("illegal width or height in init_map()");
  }
  if (b->width != -1){  /* map allocated ? */
    free(b->map);
  }
  b->map = malloc(width * height + 1);
  b->width = width;
  b->height = height;
  b->map[0] = 0;                /* map initilized to zero length string */
}

void free_board(boardp b){
  if (b->width != -1){  /* map allocated ? */
    free(b->map);
  }
  free(b);
}

char tile(boardp b, cell c){
  if (c.row > b->height || c.col > b->width){
    return '?';   /* out of bounds error */
  }
  else {
    // b->map is a 1D array of a 2D board,
    // stored row by row, i.e. width*height chars in this order (row,col) order:
    // (0,0) (0,1) ... (0,width-1) (1,0) (1,1) ... (height-1,width-1)
    return b->map[(c.row * b->width) + c.col];
  }
}

cell find(boardp b, char what){
  int i;
  cell c;
  if (b->width < 0){
    _fatal_error("find() called on board without map");
  }
  for (i=0; i< b->width * b->height; i++){
    if (b->map[i] == what){
      c.row = i / b->width;
      c.col = i % b->width;
      return c;
    }
  }
  _fatal_error("find() failed");
}

cell me(boardp b){
  if (b->_me.row < 0){
    b->_me = find(b, ME);
  }
  return b->_me;
}

cell them(boardp b){
  if (b->_them.row < 0){
    b->_them = find(b, THEM);
  }
  return b->_them;
}

void commit_move(int direction){
  printf("%i\n", direction);
  fflush(stdout);
}

